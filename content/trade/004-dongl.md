---
Title: 截面动量 vs 时序动量
Date: 2026-06-30
Category: 量化
Tags: python, 量化
Series: 动量策略入门
Series_index: 4
Author: 悠游
Summary: 理解截面动量（CSM）和时序动量（TSM）的核心区别、适用场景和实现方式
---

# 截面动量 vs 时序动量——策略选择的关键区别

Lesson 0004策略进阶~20 min



**本课目标：**理解截面动量（CSM）和时序动量（TSM）的核心区别、适用场景和实现方式。

## 截面动量（CSM）

在横截面上比较所有资产，做多相对强势的，做空（或避开）相对弱势的。

CSM: signal_i = rank(ret_i) - mean(rank(ret))

```
def csm_signal(returns):
    """截面动量：在股票之间排序"""
    rank = returns.rank(ascending=True)
    return (rank - rank.mean()) / rank.std()
```

## 时序动量（TSM）

每只资产独立看：如果自己过去涨了，就买入；跌了就卖出/空仓。

TSM: signal_i = sign(ret_i - 0) 或使用连续值

```
def tsm_signal(returns):
    """时序动量：只看资产自身"""
    return returns / returns.abs().mean()  # 标准化信号强度
```

## 关键区别

| 维度     | 截面动量             | 时序动量         |
| :------- | :------------------- | :--------------- |
| 信号来源 | 相对强弱             | 绝对涨跌         |
| 多空     | 多+空                | 仅多头（或空仓） |
| 适用市场 | 股票（多资产）       | 期货、ETF、指数  |
| 牛市表现 | 好                   | 好               |
| 熊市表现 | 差（强制做多最差的） | 好（可空仓）     |
| 容量     | 大                   | 中               |

## 实际应用建议

- **A股多头策略**：CSM更适合，选top-k做多
- **期货CTA**：TSM更适合，单品种趋势跟踪
- **ETF轮动**：两者结合效果更好

熊市中，哪种动量策略表现更好？

1. 截面动量
2. 时序动量（可空仓）
3. 两者一样

显示答案

## 📚 延伸资料

- [Moskowitz (2012) TSM 原文](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2292849)
- [SciPy 统计库（rank 相关计算）](https://scipy.org/)
- [QuantConnect: CSM vs TSM](https://www.quantconnect.com/docs/key-concepts/time-series-vs-cross-section)
- [Wikipedia: Momentum (Finance)](https://en.wikipedia.org/wiki/Momentum_(finance))

**提示：**有任何不清楚的地方，随时问我。

------

