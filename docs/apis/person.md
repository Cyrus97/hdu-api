# 个人信息 API

此章节是关于个人信息 API 的描述。

## `Person` objects

[`Person`](person.md#person-objects) 对象提供了一系列个人信息 API。

**Constructor**:

_class_ hdu\_api.**Person**(*session*)

| 参数 | type | required | default | 备注 |
| :---: | :---: | :---: | :---: | :---: |
| session | objects `PersonSession` | true | 无 | 一个已初始化的 `PersonSession` 对象

**Class methods**:

- _classmethod_ Person.**profile**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;基本个人信息。

- _classmethod_ Person.**instructor**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;辅导员信息。

- _classmethod_ Person.**status**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;学籍信息。

- _classmethod_ Person.**accommodation**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;住宿信息。

- _classmethod_ Person.**award**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;奖项信息。

- _classmethod_ Person.**profile_all**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;全部个人信息，即以上信息的集合。

参数说明：

- raw - 是否输出为原始格式
- dictionary - raw 为 true 时，使用该字典替换返回数据的 key

**Class attributes**:

- Person.**session**
    
    &ensp;&ensp;`PersonSession` 对象。