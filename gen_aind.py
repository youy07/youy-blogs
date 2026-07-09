import csv, json, re, sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="gen aind html")
parser.add_argument("--ktype", type=int, default=15, choices=[1, 3, 5, 15, 60],
                    help="Kline type in minutes")
args = parser.parse_args()
ktype = args.ktype

CSV_PATH = f'880009_{ktype}min.csv'
MD_PATH  = r'K线分析.md'
OUT_PATH = r'G:\temp\my-site\content\static\aind.html'

HIGHER = [p for p in [3, 5, 15, 60] if p > ktype]
PERIODS = [ktype] + HIGHER + ['daily']

rows = []
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        rows.append({
            't': r['datetime'],
            'o': float(r['open']),
            'h': float(r['high']),
            'l': float(r['low']),
            'c': float(r['close']),
            'v': float(r['vol'])
        })

def agg_to(data, base_mins, target):
    if target == 'daily':
        by_day = defaultdict(list)
        for d in data:
            by_day[d['t'][:10]].append(d)
        out = []
        for day in sorted(by_day):
            chunk = by_day[day]
            out.append({'t': day, 'o': chunk[0]['o'],
                'h': max(d['h'] for d in chunk),
                'l': min(d['l'] for d in chunk),
                'c': chunk[-1]['c'], 'v': sum(d['v'] for d in chunk)})
        return out
    target_mins = int(target)
    if base_mins == target_mins:
        return data
    group_size = target_mins // base_mins
    out = []
    for i in range(0, len(data), group_size):
        chunk = data[i:i+group_size]
        out.append({'t': chunk[0]['t'], 'o': chunk[0]['o'],
            'h': max(d['h'] for d in chunk),
            'l': min(d['l'] for d in chunk),
            'c': chunk[-1]['c'], 'v': sum(d['v'] for d in chunk)})
    return out

def make_ma(data, n):
    c = [d['c'] for d in data]
    r = []
    for i in range(len(c)):
        if i < n-1: r.append(None)
        else: r.append(round(sum(c[i-n+1:i+1])/n, 2))
    return r

def make_boll(data, n, k):
    c = [d['c'] for d in data]
    mid = make_ma(data, n)
    up, lo = [], []
    for i in range(len(c)):
        if i < n-1:
            up.append(None); lo.append(None)
        else:
            avg = mid[i]
            sq = sum((c[j]-avg)**2 for j in range(i-n+1, i+1))
            sd = (sq/n)**0.5
            up.append(round(avg+k*sd, 2))
            lo.append(round(avg-k*sd, 2))
    return up, mid, lo

def ema_series(data, n):
    r = []
    k = 2 / (n + 1)
    for i in range(len(data)):
        if i == 0:
            r.append(data[i])
        else:
            r.append(data[i]*k + r[-1]*(1-k))
    return r

def make_macd(data, fast=12, slow=26, signal=9):
    c = [d['c'] for d in data]
    ema_f = ema_series(c, fast)
    ema_s = ema_series(c, slow)
    dif = [round(ema_f[i]-ema_s[i], 4) for i in range(len(c))]
    dea = ema_series(dif, signal)
    macd_bar = [round(2*(dif[i]-dea[i]), 4) for i in range(len(c))]
    return dif, dea, macd_bar

def build_series(data, period):
    is_day = period == 'daily'
    dates = [d['t'] if is_day else d['t'][5:16].replace('T',' ') for d in data]
    ohlc = [[d['o'],d['c'],d['l'],d['h']] for d in data]
    vols = [d['v'] for d in data]
    cl = [d['c'] for d in data]
    vc = ['#ef5350' if i==0 or cl[i]>=cl[i-1] else '#26a69a' for i in range(len(cl))]
    mas = {f'ma{p}': make_ma(data,p) for p in [5,13,34,55,144,233]}
    bup, bmid, blo = make_boll(data,233,2)
    macd_dif, macd_dea, macd_bar = make_macd(data)
    return {'dates':dates,'ohlc':ohlc,'vols':vols,'vc':vc,'mas':mas,
            'boll':[bup,bmid,blo],'macd':[macd_dif,macd_dea,macd_bar],'raw':data}

agg_map = {}
for p in PERIODS:
    if p == ktype:
        agg_map[p] = rows
    elif p == 'daily':
        agg_map[p] = agg_to(rows, ktype, 'daily')
    else:
        agg_map[p] = agg_to(rows, ktype, p)

DATA = {}
for p in PERIODS:
    key = f'{p}min' if p != 'daily' else 'daily'
    DATA[key] = build_series(agg_map[p], p)

data_json = json.dumps(DATA)

PERIOD_KEYS = [f'{p}min' if p != 'daily' else 'daily' for p in PERIODS]
tab_labels = {('daily' if p == 'daily' else f'{p}min'): ('日线' if p == 'daily' else f'{p}分钟') for p in PERIODS}

with open(MD_PATH, 'r', encoding='utf-8') as f:
    md_text = f.read()

def md_to_html(t):
    t = re.sub(r'^### (.+)$', r'<h3>\1</h3>', t, flags=re.M)
    t = re.sub(r'^## (.+)$', r'<h2>\1</h2>', t, flags=re.M)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    blocks = []
    for line in t.split('\n'):
        s = line.strip()
        if not s or s.startswith('<h'):
            if s: blocks.append(s)
            continue
        blocks.append(f'<p>{s}</p>')
    return '\n'.join(blocks)

md_html = md_to_html(md_text)

tabs_html = '\n'.join(
    f'    <div class="tab{" active" if i == 0 else ""}" data-per="{k}">{tab_labels[k]}</div>'
    for i, k in enumerate(PERIOD_KEYS)
)

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全A指数 K线图</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;font-family:-apple-system,BlinkMacSystemFont,sans-serif;padding:16px;color:#e6edf3}}
.wrap{{max-width:1400px;margin:0 auto}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:8px}}
.header h1{{font-size:1.2rem;font-weight:600}}
.header .info{{font-size:0.78rem;color:#8b949e}}
.tabs{{display:flex;gap:6px;flex-wrap:wrap}}
.tab{{padding:4px 16px;border-radius:6px;font-size:0.8rem;cursor:pointer;border:1px solid #30363d;background:transparent;color:#8b949e;transition:all .15s}}
.tab:hover{{border-color:#58a6ff;color:#e6edf3}}
.tab.active{{background:#1f6feb;border-color:#1f6feb;color:#fff}}
.malegend{{display:flex;gap:8px;flex-wrap:wrap;font-size:0.72rem;margin-bottom:10px}}
.malegend span{{cursor:pointer;padding:2px 6px;border-radius:4px;border:1px solid transparent;user-select:none}}
.malegend span.hide{{opacity:.3;text-decoration:line-through}}
#chart{{width:100%;height:75vh;border-radius:10px;background:#161b22;border:1px solid #30363d}}
.analysis{{margin-top:20px;background:#161b22;border:1px solid #30363d;border-radius:10px;padding:24px 28px;color:#e6edf3}}
.analysis h2{{font-size:1.1rem;font-weight:600;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #30363d}}
.analysis h3{{font-size:0.95rem;color:#58a6ff;margin:14px 0 6px}}
.analysis p{{font-size:0.85rem;line-height:1.7;color:#c9d1d9;margin:4px 0}}
.analysis code{{background:#1c2128;padding:1px 5px;border-radius:3px;font-size:0.82rem;color:#f0c674}}
.analysis strong{{color:#e6edf3}}
</style>
</head>
<body>
<div class="wrap">
<div class="header">
  <h1>全A指数</h1>
  <div class="tabs">
{tabs_html}
  </div>
  <span class="info" id="rangeInfo">-</span>
</div>
<div class="malegend" id="malegend"></div>
<div id="chart"></div>
<div class="analysis">
{md_html}
</div>
</div>
<script>
const DATA = {data_json};

const MA_PERIODS = [5,13,34,55,144,233];
const MA_COLORS = ['#fbbf24','#a78bfa','#60a5fa','#34d399','#f472b6','#fb923c'];
const MA_NAMES = MA_PERIODS.map(p => 'MA' + p);
const BOLL_SERIES = ['BOLL_UPPER','BOLL_MID','BOLL_LOWER'];
const BOLL_COLORS = ['rgba(255,183,77,0.7)','rgba(255,183,77,0.9)','rgba(255,183,77,0.7)'];
const PERIOD_KEYS = {json.dumps(PERIOD_KEYS)};

let cur = PERIOD_KEYS[0];
let hideMA = new Set();
let showBoll = true;

function buildOpt(data) {{
  const dates = data.dates, ohlc = data.ohlc, vols = data.vols;
  const vc = data.vc, mas = data.mas, boll = data.boll, raw = data.raw;
  const macd = data.macd;
  const isDay = cur === 'daily';

  const allNames = [...MA_NAMES, ...BOLL_SERIES];
  const sel = {{}};
  allNames.forEach(n => sel[n] = n.startsWith('BOLL') ? showBoll : !hideMA.has(n));

  const macdColors = macd[2].map((v,i) => {{
    if (i === 0) return '#ef5350';
    return macd[2][i] >= macd[2][i-1] ? '#ef5350' : '#4caf50';
  }});

  const list = [
    {{type:'candlestick',data:ohlc,xAxisIndex:0,yAxisIndex:0,name:'K线',
      itemStyle:{{color:'#ef5350',color0:'#26a69a',borderColor:'#ef5350',borderColor0:'#26a69a'}}}},
    ...MA_PERIODS.map((p,i)=>({{name:'MA'+p,type:'line',data:mas['ma'+p],
      xAxisIndex:0,yAxisIndex:0,symbol:'none',color:MA_COLORS[i],
      lineStyle:{{width:1,color:MA_COLORS[i]}}}})),
    ...(boll[0].some(v=>v!==null)?[0,1,2].map(i=>({{name:BOLL_SERIES[i],type:'line',
      data:boll[i],xAxisIndex:0,yAxisIndex:0,symbol:'none',color:BOLL_COLORS[i],
      lineStyle:{{width:i===1?1.5:1,color:BOLL_COLORS[i],type:i===1?'solid':'dashed'}}}})):[]),
    {{type:'bar',data:vols,xAxisIndex:1,yAxisIndex:1,z:2,
      itemStyle:{{color:p=>vc[p.dataIndex]}}}},
    {{name:'MACD_DIF',type:'line',data:macd[0],xAxisIndex:2,yAxisIndex:2,
      symbol:'none',lineStyle:{{width:1,color:'#60a5fa'}}}},
    {{name:'MACD_DEA',type:'line',data:macd[1],xAxisIndex:2,yAxisIndex:2,
      symbol:'none',lineStyle:{{width:1,color:'#fbbf24'}}}},
    {{name:'MACD',type:'bar',data:macd[2],xAxisIndex:2,yAxisIndex:2,z:1,
      itemStyle:{{color:p=>macdColors[p.dataIndex]}}}}
  ];

  return {{
    animation:false,backgroundColor:'transparent',
    tooltip:{{trigger:'axis',axisPointer:{{type:'cross'}},
      backgroundColor:'#1c2128',borderColor:'#30363d',borderWidth:1,
      textStyle:{{color:'#e6edf3',fontSize:11}},
      formatter:function(p){{const d=raw[p[0].dataIndex]; var s='<b>'+d.t+'</b><br/>'; for(var j=0;j<p.length;j++){{s+=p[j].marker+' '+p[j].seriesName+': '+p[j].value+'<br/>'}}; return s;}}}},
    grid:[
      {{left:'5%',right:'3%',top:'5%',height:'50%'}},
      {{left:'5%',right:'3%',top:'59%',height:'12%'}},
      {{left:'5%',right:'3%',top:'75%',height:'17%'}}
    ],
    xAxis:[
      {{type:'category',data:dates,gridIndex:0,axisLine:{{show:false}},axisLabel:{{show:false}},splitLine:{{show:false}}}},
      {{type:'category',data:dates,gridIndex:1,axisLine:{{show:false}},axisLabel:{{show:false}},splitLine:{{show:false}}}},
      {{type:'category',data:dates,gridIndex:2,axisLine:{{lineStyle:{{color:'#30363d'}}}},axisLabel:{{color:'#8b949e',fontSize:10,interval:isDay?5:80}},splitLine:{{show:false}}}}
    ],
    yAxis:[
      {{scale:true,gridIndex:0,splitLine:{{lineStyle:{{color:'#21262d',type:'dashed'}}}},axisLabel:{{color:'#8b949e',fontSize:10}}}},
      {{scale:true,gridIndex:1,splitNumber:2,splitLine:{{show:false}},axisLabel:{{color:'#8b949e',fontSize:10,formatter:v=>(v/1e8).toFixed(0)+'亿'}}}},
      {{scale:true,gridIndex:2,splitNumber:3,splitLine:{{lineStyle:{{color:'#21262d',type:'dashed'}}}},axisLabel:{{color:'#8b949e',fontSize:10}}}}
    ],
    dataZoom:[
      {{type:'inside',xAxisIndex:[0,1,2],start:0,end:100}},
      {{type:'slider',xAxisIndex:[0,1,2],start:0,end:100,
        borderColor:'#30363d',backgroundColor:'#0d1117',
        fillerColor:'rgba(56,139,253,0.15)',handleStyle:{{color:'#58a6ff'}},textStyle:{{color:'#8b949e'}}}}
    ],
    series:list,
    legend:{{data:allNames,top:'1%',right:'5%',textStyle:{{color:'#8b949e',fontSize:10}},icon:'roundRect',selected:sel}}
  }};
}}

function render() {{
  const d = DATA[cur];
  chart.setOption(buildOpt(d), true);
  const r = d.raw;
  document.getElementById('rangeInfo').textContent = r[0].t+' ~ '+r[r.length-1].t+' | '+r.length+' bars';
}}

const chart = echarts.init(document.getElementById('chart'), 'dark');

document.querySelectorAll('.tab').forEach(t=>{{
  t.addEventListener('click',function(){{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    this.classList.add('active'); cur=this.dataset.per; render();
  }});
}});

const leg = document.getElementById('malegend');
MA_NAMES.forEach((n,i)=>{{
  const s=document.createElement('span'); s.textContent=n; s.style.color=MA_COLORS[i];
  s.addEventListener('click',function(){{
    if(hideMA.has(n)){{hideMA.delete(n);this.classList.remove('hide');}}
    else{{hideMA.add(n);this.classList.add('hide');}}
    render();
  }}); leg.appendChild(s);
}});
const bs=document.createElement('span'); bs.textContent='BOLL(233,2)'; bs.style.color='#ffb74d';
bs.addEventListener('click',function(){{showBoll=!showBoll;this.classList.toggle('hide');render();}});
leg.appendChild(bs);

render();
window.addEventListener('resize',()=>chart.resize());
</script>
</body>
</html>'''

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(HTML)

counts = '  '.join(f'{k}: {len(agg_map[p])}' for k, p in zip(PERIOD_KEYS, PERIODS))
print(f'Done: {OUT_PATH}')
print(counts)
