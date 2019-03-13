# 一卡通 API

此章节是关于一卡通 API 的描述。

## `Card` objects

[`Card`](card.md#card-objects) 对象提供了一系列一卡通信息 API。

**Constructor**:

_class_ hdu\_api.**Card**(*session*)

| 参数 | type | required | default | 备注 |
| :---: | :---: | :---: | :---: | :---: |
| session | objects `CardSession` | true | 无 | 一个已初始化的 `CardSession` 对象

**Class methods**:

- _classmethod_ Card.**account**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;一卡通账户信息。

- _classmethod_ Card.**balance**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;一卡通余额。

- _classmethod_ Card.**consume**(*year, month, raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;某年某月一卡通流水。

- _classmethod_ Card.**consume_today**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;今日一卡通流水。

- _classmethod_ Card.**statistics**(*year, month, raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;月交易统计。
    
参数说明：

- raw - 是否输出为原始格式
- dictionary - raw 为 true 时，使用该字典替换返回数据的 key
- year - 年份，如 2019
- month - 月份，如 1, 3, 4, 12

**Class attributes**:

- Card.session
    
    &ensp;&ensp;`CardSession` 对象。
