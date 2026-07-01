---
Title: 数据获取与处理
Date: 2026-06-29
Category: 量化
Tags: python, 量化
Series: 动量策略入门
Series_index: 2
Author: 悠游
Summary: 学会使用 AKShare 库获取 A 股历史行情数据，并做基础的数据清洗和预处理。
---

# 数据获取与处理——用Python拉取A股行情数据

Lesson 0002基础数据~20 min



**本课目标：**学会使用 AKShare 库获取 A 股历史行情数据，并做基础的数据清洗和预处理。

## 安装 AKShare

```
pip install akshare
```

AKShare 是一个免费、开源的 Python 财经数据接口库，覆盖 A 股、期货、基金、债券等。

## 获取单只股票的历史数据

```
import akshare as ak

# 获取贵州茅台日线数据（前复权）
df = ak.stock_zh_a_hist(
    symbol="600519",
    period="daily",
    start_date="20100101",
    end_date="20241231",
    adjust="qfq"  # 前复权
)
print(df.head())
```

## 数据清洗要点

```
# 1. 日期列转为 datetime 并设为索引
df['日期'] = pd.to_datetime(df['日期'])
df = df.set_index('日期')

# 2. 排序（AKShare 默认降序，需要变为升序）
df = df.sort_index()

# 3. 检查缺失值
print(df.isnull().sum())

# 4. 统一列名（英文方便后续处理）
df.columns = ['开盘', '收盘', '最高', '最低', '成交量', '成交额',
              '振幅', '涨跌幅', '涨跌额', '换手率']
```

## 批量获取多只股票

```
import pandas as pd

stock_list = ["600519", "000858", "000568", "600809", "000596"]
data = {}

for symbol in stock_list:
    df = ak.stock_zh_a_hist(symbol, adjust="qfq")
    df = df.set_index('日期')
    df.index = pd.to_datetime(df.index)
    data[symbol] = df['收盘']

# 合并为一个 DataFrame
price_df = pd.DataFrame(data)
price_df = price_df.sort_index()
print(price_df.head())
```

**注意：**AKShare 有频率限制，不要短时间内大量请求。建议单次请求间隔 0.5-1 秒。

## 保存数据

```
# 保存为 CSV
price_df.to_csv('stock_prices.csv')

# 下次读取
price_df = pd.read_csv('stock_prices.csv', index_col=0, parse_dates=True)
```

AKShare 中获取前复权数据的参数是？

1. adjust='qfq'
2. adjust='hfq'
3. adjust='none'

显示答案

## 📚 延伸资料

- [AKShare 官方文档](https://akshare.akfamily.xyz/)
- [pandas read_csv 文档](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [Tushare 数据接口（备选数据源）](https://www.tushare.pro/)
- [聚宽数据API文档](https://www.joinquant.com/help/api/help#name:api)

**提示：**有任何不清楚的地方，随时问我。

