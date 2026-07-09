import re, json, urllib.request, argparse

parser = argparse.ArgumentParser(description="生成黄历页面")
parser.add_argument("--rq", type=str, default='', help="日期 YYYY-MM-DD，默认取今天")
args = parser.parse_args()

if args.rq:
    rq = args.rq
    URL = f'https://www.qmrl888.com/{rq}.html'
    # out_file = rf'G:\temp\my-site\content\static\huangl_{rq}.html'
else:
    rq = ''
    URL = 'https://www.qmrl888.com/'
out_file = r'G:\temp\my-site\content\static\huangl.html'

req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='replace')

pattern = r"self\.__next_f\.push\(\[1,(.*?)\]\)"
matches = re.findall(pattern, html, re.DOTALL)
if not matches:
    raise RuntimeError("data not found")

content = matches[-1].strip()
if content.startswith('"') and content.endswith(')'):
    content = content[1:-2]
elif content.startswith('"'):
    content = content[1:-1]
decoded = content.replace('\\"', '"').replace('\\n', '\n')

idx = decoded.find('"lunarData"')
start = decoded.index('{', idx)
depth = 0
end = start
for pos in range(start, len(decoded)):
    if decoded[pos] == '{':
        depth += 1
    elif decoded[pos] == '}':
        depth -= 1
        if depth == 0:
            end = pos + 1
            break

ld = json.loads(decoded[start:end])

# ── extract fields ──
yi_list = ld['yiji']['yi']
ji_list = ld['yiji']['ji']
week_name = ld['weekIndex']
solar = ld['solarYmd']
lunar = ld['lunarYmd']
ganzhi = ld['ganzhi']
shengxiao = ld['shengxiao']
jishen = ld['jishen']
jishenxiongsha = ld['jishenxiongsha']
chongsha = ld['chongsha']
tianshen = ld['tianshen']
nayin = ld['nayin']
zhixing = ld['zhixing']
time_list = ld['timeList']
xiu = ld['xiu']
lu_val = ld.get('lu', '')
gong = ld.get('gong', '')
yue = ld.get('yue', '')
nine_star = ld.get('nine', {})
zmt = ld.get('zmt', {})
taishen = ld.get('taishen', '')
pengzu = ld.get('pengzu', {})

solar_date = f"{solar['year']}年{solar['month']}月{solar['day']}日"
lunar_date = f"{lunar['year']}年 {lunar['month']}月{lunar['day']}日"
year_ganzhi = ganzhi.get('yearInGanZhiByLiChun', '')
month_ganzhi = ganzhi['monthInGanZhi']
day_ganzhi = ganzhi['dayInGanZhi']
year_sx = shengxiao.get('yearShengXiaoByLiChun', '')
month_sx = shengxiao['monthShengXiao']
day_sx = shengxiao['dayShengXiao']
year_nayin = nayin['yearNaYin']
month_nayin = nayin['monthNaYin']
day_nayin = nayin['dayNaYin']

is_good = tianshen['dayTianShenLuck'] == '吉'

sheng_xiao_color = {
    '鼠':'#6b7280','牛':'#8b5cf6','虎':'#f97316','兔':'#ec4899',
    '龙':'#eab308','蛇':'#22c55e','马':'#ef4444','羊':'#a855f7',
    '猴':'#f59e0b','鸡':'#06b6d4','狗':'#6366f1','猪':'#f472b6'
}

def sx_circle(sx, size=40):
    c = sheng_xiao_color.get(sx, '#6b7280')
    return f'<span class="sx-circle" style="background:{c}20;color:{c};border-color:{c};width:{size}px;height:{size}px;font-size:{size*0.45}px">{sx}</span>'

ji_shen_html = ''.join(f'<span class="tag ji-shen">{x}</span>' for x in jishenxiongsha.get('dayJiShen', []))
xiong_sha_html = ''.join(f'<span class="tag xiong-sha">{x}</span>' for x in jishenxiongsha.get('dayXiongSha', []))
yi_html = ''.join(f'<span class="tag yi">{x}</span>' for x in yi_list)
ji_html = ''.join(f'<span class="tag ji">{x}</span>' for x in ji_list if x != '无')

time_rows_html = ''
for t in time_list:
    cl = 'ji' if t['tianshenLuck'] == '吉' else 'xiong'
    ts_type = t['tianshenType']
    time_rows_html += f'''          <tr class="{cl}">
            <td class="time-label">{t['startTime']}-{t['endTime']}</td>
            <td class="time-ganzhi">{t['ganzhi']}</td>
            <td class="time-sx">{t['shengxiao']}</td>
            <td class="time-ts">{t['tianshen']}<span class="ts-tag {ts_type}">{ts_type}</span></td>
            <td class="time-luck">{t['tianshenLuck']}</td>
            <td class="time-yi">{' '.join(t['yi'])}</td>
            <td class="time-ji">{' '.join(t['ji'])}</td>
            <td class="time-chong">{t['chongDesc']}</td>
          </tr>'''

xiu_name = f"{xiu['xiu']}木{xiu['animal']}" if xiu.get('zheng') else xiu['xiu']

zmt_html = ''
if zmt:
    zmt_labels = {
        'touLiang':'几鼠偷粮','caoZi':'草子几分','gengTian':'几牛耕田','huaShou':'花收几分',
        'zhiShui':'几龙治水','tuoGu':'几马驮谷','qiangMi':'几鸡抢米','kanCan':'几姑看蚕',
        'jiaTian':'甲田几分','fenBing':'几人分饼','deJin':'几日得金'
    }
    for k, label in zmt_labels.items():
        if k in zmt:
            zmt_html += f'<span class="tag" style="background:var(--card2);color:var(--gold)">{label}: {zmt[k]}</span> '

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta content="了解今日吉凶，趋利避害，招财进宝，逢凶化吉" name="description"/>
<meta content="命理,运势，吉凶" name="keywords"/>
<title>今日黄历 - {solar_date} · {lunar_date} 黄道吉日查询</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #f7f3eb;
  --card: #ffffff;
  --card2: #f0ebe1;
  --border: #e2dbcf;
  --gold: #b8860b;
  --red: #c41e3a;
  --green: #2e7d32;
  --text: #2c2c2c;
  --text2: #6b6b7b;
  --ji-color: #c41e3a;
  --yi-color: #2e7d32;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:'Noto Serif SC','SimSun','STSong',serif;min-height:100vh;padding:20px}}
.wrap{{max-width:780px;margin:0 auto;background:var(--card);border-radius:16px;box-shadow:0 2px 20px rgba(0,0,0,0.08);padding:24px}}
.header{{text-align:center;padding:30px 0 20px;position:relative}}
.header::after{{content:'';position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:120px;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent)}}
.header h1{{font-size:1rem;color:var(--text2);font-weight:400;letter-spacing:4px;margin-bottom:6px}}
.header .solar-date{{font-size:2.2rem;font-weight:900;letter-spacing:2px;margin-bottom:4px}}
.header .week{{font-size:1rem;color:var(--text2);margin-bottom:4px}}
.header .lunar-date{{font-size:1.3rem;color:var(--gold);letter-spacing:3px}}

.verdict{{text-align:center;padding:24px;margin:20px 0;background:linear-gradient(135deg,{'#fff5f5' if is_good else '#f5fff5'} 0%,var(--card) 100%);border-radius:16px;border:1px solid {'rgba(196,30,58,0.2)' if is_good else 'rgba(46,125,50,0.2)'}}}
.verdict .badge{{display:inline-block;padding:6px 20px;border-radius:20px;font-size:1.1rem;font-weight:700;margin-bottom:12px;background:{'rgba(196,30,58,0.1)' if is_good else 'rgba(46,125,50,0.1)'};color:{'#c41e3a' if is_good else '#2e7d32'}}}
.verdict .tian-shen{{font-size:1.5rem;font-weight:700;margin-bottom:4px}}
.verdict .sub{{font-size:0.9rem;color:var(--text2);margin-top:4px}}
.verdict .sub span{{margin:0 8px;color:var(--gold)}}

.row-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0}}
.card{{background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center}}
.card .label{{font-size:0.72rem;color:var(--text2);margin-bottom:6px;letter-spacing:2px}}
.card .value{{font-size:1.1rem;font-weight:700}}

.sx-row{{display:flex;justify-content:center;gap:20px;margin:8px 0}}
.sx-item{{text-align:center}}
.sx-item .sx-label{{font-size:0.68rem;color:var(--text2);margin-top:4px}}
.sx-circle{{display:inline-flex;align-items:center;justify-content:center;border-radius:50%;border:2px solid;font-weight:700;line-height:1}}

.row-2{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}}
.section-title{{font-size:0.82rem;color:var(--gold);letter-spacing:2px;margin:20px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--gold);display:flex;align-items:center;gap:8px}}
.section-title::before{{content:'◆';font-size:0.6rem}}

.tags{{display:flex;flex-wrap:wrap;gap:6px}}
.tag{{display:inline-block;padding:3px 10px;border-radius:6px;font-size:0.82rem;font-weight:500}}
.tag.yi{{background:rgba(46,125,50,0.1);color:var(--yi-color)}}
.tag.ji{{background:rgba(196,30,58,0.1);color:var(--ji-color)}}
.tag.ji-shen{{background:rgba(46,125,50,0.1);color:#2e7d32}}
.tag.xiong-sha{{background:rgba(196,30,58,0.1);color:#c41e3a}}

.dir-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0}}
.dir-item{{background:var(--card2);border:1px solid var(--border);border-radius:8px;padding:12px 8px;text-align:center}}
.dir-item .dir-label{{font-size:0.65rem;color:var(--text2);margin-bottom:3px}}
.dir-item .dir-value{{font-size:1rem;font-weight:700;color:var(--gold)}}

.pengzu{{background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:14px;margin:10px 0}}
.pengzu p{{font-size:0.85rem;line-height:1.7;color:var(--text)}}
.pengzu p strong{{color:var(--red)}}

.time-table{{width:100%;border-collapse:collapse;font-size:0.78rem;margin:10px 0}}
.time-table th{{background:var(--gold);padding:8px 6px;text-align:center;color:#fff;font-weight:600;border-bottom:2px solid var(--gold);font-size:0.72rem;letter-spacing:1px}}
.time-table td{{padding:8px 6px;text-align:center;border-bottom:1px solid var(--border);vertical-align:middle}}
.time-table tr:nth-child(even) td{{background:var(--card2)}}
.time-table tr.ji td{{background:rgba(46,125,50,0.05)}}
.time-table tr.xiong td{{background:rgba(196,30,58,0.05)}}
.time-label{{font-weight:600;white-space:nowrap}}
.time-ganzhi{{font-weight:700;color:var(--gold)}}
.time-sx{{color:var(--text2)}}
.time-ts{{font-weight:500}}
.ts-tag{{display:inline-block;font-size:0.6rem;padding:1px 5px;border-radius:3px;margin-left:4px;vertical-align:middle}}
.ts-tag.黄道{{background:rgba(46,125,50,0.15);color:#2e7d32}}
.ts-tag.黑道{{background:rgba(196,30,58,0.15);color:#c41e3a}}
.time-luck{{font-weight:700}}
.time-yi{{color:var(--yi-color);font-size:0.72rem}}
.time-ji{{color:var(--ji-color);font-size:0.72rem}}
.time-chong{{color:var(--text2);font-size:0.72rem}}

.xiu-card{{display:flex;align-items:center;gap:14px;background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:14px}}
.xiu-card .xiu-name{{font-size:1.3rem;font-weight:700;color:var(--gold)}}
.xiu-card .xiu-detail{{flex:1}}
.xiu-card .xiu-detail .xiu-animal{{font-size:0.9rem;color:var(--text)}}
.xiu-card .xiu-detail .xiu-luck{{font-size:0.78rem;color:var(--text2)}}
.xiu-card .xiu-song{{font-size:0.72rem;color:var(--text2);line-height:1.6;margin-top:4px}}

.zmt-wrap{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}}

.footer-meta{{text-align:center;padding:20px 0 10px;font-size:0.7rem;color:var(--text2);border-top:1px solid var(--border);margin-top:20px}}
</style>
</head>
<body>
<div class="wrap">

<div class="header">
  <h1>✦ 今 日 黄 历 ✦</h1>
  <div class="solar-date">{solar_date}</div>
  <div class="week">{week_name}</div>
  <div class="lunar-date">{lunar_date}</div>
</div>

<div class="verdict">
  <div class="badge">{'↥ 吉日 · 诸事可行' if is_good else '↧ 凶日 · 宜静不宜动'}</div>
  <div class="tian-shen">{tianshen['dayTianShen']}</div>
  <div class="sub"><span>{tianshen['dayTianShenType']}</span> · 今日{tianshen['dayTianShenLuck']}神值日</div>
</div>

<div class="row-3">
  <div class="card"><div class="label">年干支</div><div class="value">{year_ganzhi}</div><div style="font-size:0.7rem;color:var(--text2)">{year_nayin} · {year_sx}年</div></div>
  <div class="card"><div class="label">月干支</div><div class="value">{month_ganzhi}</div><div style="font-size:0.7rem;color:var(--text2)">{month_nayin} · {month_sx}月</div></div>
  <div class="card"><div class="label">日干支</div><div class="value">{day_ganzhi}</div><div style="font-size:0.7rem;color:var(--text2)">{day_nayin} · {day_sx}日</div></div>
</div>

<div class="row-2">
  <div class="card">
    <div class="label">生肖 · 三合六合</div>
    <div class="sx-row" style="gap:10px">
      <div class="sx-item">{sx_circle(year_sx,50)}<div class="sx-label">值年</div></div>
      <div class="sx-item">{sx_circle(month_sx,50)}<div class="sx-label">值月</div></div>
      <div class="sx-item">{sx_circle(day_sx,50)}<div class="sx-label">值日</div></div>
    </div>
  </div>
  <div class="card">
    <div class="label">冲煞</div>
    <div style="font-size:1.3rem;font-weight:700;color:var(--red);margin:6px 0">{chongsha['dayChongShengXiao'] if 'dayChongShengXiao' in chongsha else ''}</div>
    <div style="font-size:0.85rem;color:var(--text2)">{chongsha['dayChongDesc']} · 煞{chongsha['daySha']}</div>
  </div>
</div>

<div class="section-title">宜 / 忌</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:8px">
  <div class="card" style="text-align:left">
    <div style="color:var(--yi-color);font-size:0.85rem;font-weight:600;margin-bottom:8px">宜</div>
    <div class="tags">{yi_html}</div>
  </div>
  <div class="card" style="text-align:left">
    <div style="color:var(--ji-color);font-size:0.85rem;font-weight:600;margin-bottom:8px">忌</div>
    <div class="tags">{ji_html if ji_list[0] != '无' else '<span style="color:var(--text2);font-size:0.82rem">百无禁忌</span>'}</div>
  </div>
</div>

<div class="section-title">吉神 / 凶煞</div>
<div style="margin-bottom:16px">
  <div style="margin-bottom:8px"><span style="font-size:0.75rem;color:var(--text2)">吉神</span><br>{ji_shen_html if ji_shen_html else '<span style="color:var(--text2);font-size:0.82rem">无</span>'}</div>
  <div><span style="font-size:0.75rem;color:var(--text2)">凶煞</span><br>{xiong_sha_html if xiong_sha_html else '<span style="color:var(--text2);font-size:0.82rem">无</span>'}</div>
</div>

<div class="section-title">二十八宿</div>
<div class="xiu-card" style="margin-bottom:16px">
  <div class="xiu-name">{xiu['xiu']}</div>
  <div class="xiu-detail">
    <div class="xiu-animal">{xiu_name}</div>
    <div class="xiu-luck">吉凶: <span style="color:{'#dc3545' if xiu['xiuLuck']=='凶' else '#28a745'};font-weight:700">{xiu['xiuLuck']}</span></div>
    <div class="xiu-song">{xiu.get('xiuSong','')}</div>
  </div>
</div>

<div class="row-3">
  <div class="card"><div class="label">建除十二神</div><div class="value" style="color:var(--gold);font-size:1.3rem">{zhixing}</div><div style="font-size:0.7rem;color:var(--text2)">值日神煞</div></div>
  <div class="card"><div class="label">九星</div><div class="value" style="font-size:0.85rem">{nine_star.get('dayNineStar','')}</div><div style="font-size:0.7rem;color:var(--text2)">日九星</div></div>
  <div class="card"><div class="label">日禄</div><div class="value" style="color:var(--gold);font-size:0.85rem">{lu_val}</div><div style="font-size:0.7rem;color:var(--text2)">日禄</div></div>
</div>

<div class="section-title">财神 · 喜神 · 福神 · 贵神</div>
<div class="dir-grid">
  <div class="dir-item"><div class="dir-label">财神</div><div class="dir-value">{jishen['dayCai']}</div></div>
  <div class="dir-item"><div class="dir-label">喜神</div><div class="dir-value">{jishen['dayXi']}</div></div>
  <div class="dir-item"><div class="dir-label">福神</div><div class="dir-value">{jishen['dayFu']}</div></div>
  <div class="dir-item"><div class="dir-label">阳贵神</div><div class="dir-value" style="font-size:0.85rem">{jishen['dayYangGui']}</div></div>
  <div class="dir-item"><div class="dir-label">阴贵神</div><div class="dir-value" style="font-size:0.85rem">{jishen['dayYinGui']}</div></div>
  <div class="dir-item"><div class="dir-label">胎神</div><div class="dir-value" style="font-size:0.75rem">{taishen}</div></div>
  <div class="dir-item"><div class="dir-label">月相</div><div class="dir-value">{yue}</div></div>
  <div class="dir-item"><div class="dir-label">月厌</div><div class="dir-value" style="font-size:0.75rem">{ld.get('shou','')}</div></div>
</div>

<div class="section-title">彭祖百忌</div>
<div class="pengzu">
  <p><strong>{pengzu.get('tiangan','')}</strong></p>
  <p><strong>{pengzu.get('dizhi','')}</strong></p>
</div>

<div class="section-title">灶马头</div>
<div class="zmt-wrap">{zmt_html}</div>

<div class="section-title">时辰吉凶</div>
<div style="overflow-x:auto;margin-bottom:20px">
<table class="time-table">
  <thead><tr>
    <th>时辰</th><th>干支</th><th>生肖</th><th>星神</th><th>吉凶</th><th>宜</th><th>忌</th><th>冲煞</th>
  </tr></thead>
  <tbody>{time_rows_html}</tbody>
</table>
</div>

<div class="footer-meta">
  <p>数据来源: 全民万年历 · 吉凶仅供参考</p>
</div>

</div>
</body>
</html>'''

with open(out_file, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f'Done: {out_file}')
print(f'{solar_date}  {lunar_date}')
