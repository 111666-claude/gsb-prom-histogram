# prom-histogram

合并直方图的累计桶并计算分位：桶按边界数值排序、同边界累加、总量取最大边界的累计值。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m promhist --sample=order
python3 -m promhist --sample=merge
python3 -m promhist --sample=normalize
python3 -m promhist --sample=total
python3 -m promhist --sample=work
```

## 口径

- **边界**：桶按 `le` 的数值升序排列，同一个数值的边界只占一个桶。
- **合并**：多次投入同一个边界时累加，不是覆盖。
- **总量**：总量取最大边界上的累计值。
- **分位**：名次为 `q * 总量`；找第一个累计不小于名次的桶，在该桶边界与前一个桶边界之间线性插值，第一个桶的前边界记 0。

## 不变量

- 桶序列按边界数值严格递增，累计值非降。
- 同一个 `q` 在同样输入上得到同样的结果。
- `scanned` 不随桶数乘查询次数放大：八百个桶查八百次的 `scanned` 不超过 6000。

## 输出契约

场景打印一行 JSON，键随场景而定。`--sample=work` 打印 `{"buckets": N, "scanned": N}`。
