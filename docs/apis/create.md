# hdu_api

此章节是关于如何创建一个 client 的描述。

## `HDU` Objects

[`HDU`](#hdu-objects) 对象是使用 `hdu-api` 的起点，它提供了创建 `HduClient` 对象的方法。

**Constructor**:

*class* hdu_api.**HDU**(username, password, **kwargs)

| 参数 | type |required | default | 备注 |
|:---:|:---:|:---:|:---:|:---:|
| username | str | true | 无 | 学号 |
| password | str | true | 无 | 密码 |
| kwargs | dict | false | 无 | |

**Class methods**:

*classmethod* HDU.**create**(*args)

返回一个 `HduClient` 对象。

**Class attributes**:

HDU.username

&ensp;&ensp;学号，字符串类型。
    
HDU.password

&ensp;&ensp;密码，数字杭电的密码，字符串类型。

