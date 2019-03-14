# 公共信息 API

此章节是关于公共信息 API 的描述。

## `Public` objects

[`Public`](public.md#public-objects) 对象提供了一系列公共信息 API。

**Constructor**:

_class_ hdu\_api.**Public**(*session*)

| 参数 | type | required | default | 备注 |
| :---: | :---: | :---: | :---: | :---: |
| session | objects `PublicSession` | true | 无 | 一个已初始化的 `PublicSession` 对象

**Class methods**:

- _classmethod_ Public.**classroom_free**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;空闲教室。

- _classmethod_ Public.**classroom_in_use**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;在使用的教室。

- _classmethod_ Public.**schooltime**(*location=0, raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;上课时间表。

参数说明：

- raw - 是否输出为原始格式
- dictionary - raw 为 true 时，使用该字典替换返回数据的 key
- location - 校区，0 表示下沙, 1 表示青山湖

**Class attributes**:

- Public.**session**
    
    &ensp;&ensp;`PublicSession` 对象。