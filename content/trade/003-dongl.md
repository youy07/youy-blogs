---
Title: 第一个回测
Date: 2026-06-29
Category: 量化
Tags: python, 量化
Series: 动量策略入门
Series_index: 3
Author: 悠游
Summary: 用 Python 实现第一个动量策略回测——买入过去 N 日涨幅最大的股票，持有 M 日。
---

# 第一个回测——实现最简单的动量策略

Lesson 0003回测基础~20 min



**本课目标：**用 Python 实现第一个动量策略回测——买入过去 N 日涨幅最大的股票，持有 M 日。

## 策略逻辑

最简单的截面动量策略：

1. 每 N 个交易日，计算每只股票过去 N 日的收益率
2. 选收益率最高的 K 只股票买入（等权）
3. 持有 M 个交易日
4. 重复

## 实现代码

```
import numpy as np
import pandas as pd

def simple_momentum_backtest(price_df, lookback=20, hold=10, topk=5):
    """
    price_df: DataFrame, 每列是一只股票的收盘价
    lookback: 回顾期（计算过去 N 日收益）
    hold: 持有期
    topk: 选几只股票
    """
    returns = price_df.pct_change(lookback)  # N 日收益
    positions = pd.DataFrame(0, index=price_df.index, columns=price_df.columns)

    for i in range(lookback, len(price_df) - hold, hold):
        rank = returns.iloc[i].rank(ascending=False)
        selected = rank <= topk  # 选 top-k
        for j in range(i, i + hold):
            if j < len(positions):
                positions.iloc[j] = selected.astype(int)

    # 计算策略收益
    daily_ret = price_df.pct_change()
    strategy_ret = (positions.shift(1) * daily_ret).sum(axis=1) / topk
    nav = (1 + strategy_ret).cumprod()

    return nav
```

## 运行回测

```
nav = simple_momentum_backtest(price_df, lookback=20, hold=10, topk=5)

# 计算关键指标
total_ret = nav.iloc[-1] - 1
annual_ret = (nav.iloc[-1]) ** (252 / len(nav)) - 1
sharpe = strategy_ret.mean() / strategy_ret.std() * np.sqrt(252)
max_dd = (nav / nav.cummax() - 1).min()

print(f"总收益率: {total_ret:.2%}")
print(f"年化收益率: {annual_ret:.2%}")
print(f"夏普比率: {sharpe:.2f}")
print(f"最大回撤: {max_dd:.2%}")
```

## 可视化

```
import matplotlib.pyplot as plt

nav.plot(figsize=(12, 6), title='动量策略净值曲线')
plt.ylabel('净值')
plt.grid(True)
plt.show()
```

简单动量策略的核心步骤是什么？

1. 随机选股买入持有
2. 回顾期→选top-k→持有期→重复
3. 每天买卖所有股票

显示答案

## 📚 延伸资料

- [pandas 基础计算与滚动窗口](https://pandas.pydata.org/docs/user_guide/computation.html)
- [matplotlib pyplot 教程](https://matplotlib.org/stable/tutorials/introductory/pyplot.html)
- [Investopedia: 夏普比率详解](https://www.investopedia.com/terms/s/sharperatio.asp)
- [Investopedia: 最大回撤详解](https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp)

**提示：**有任何不清楚的地方，随时问我。

