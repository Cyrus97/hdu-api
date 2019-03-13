# hdu\_api

此章节是关于如何创建一个 client 的描述。

## `HDU` Objects

[`HDU`](create.md#hdu-objects) 对象是使用 `hdu-api` 的起点，它提供了创建 `HduClient` 对象的方法。

**Constructor**:

_class_  hdu\_api.**HDU**\(*username, password, \*\*kwargs*)

| 参数 | type | required | default | 备注 |
| :---: | :---: | :---: | :---: | :---: |
| username | str | true | 无 | 学号 |
| password | str | true | 无 | 密码 |
| kwargs | dict | false | 无 |  |

**Class methods**:

- _classmethod_ HDU.**create**\(*\*args*)

    &ensp;&ensp;返回一个 `HduClient` 对象。

**Class attributes**:

- HDU.**username**

    &ensp;&ensp;学号，字符串类型。

- HDU.**password**

    &ensp;&ensp;密码，数字杭电的密码，字符串类型。

## `HduClient` Objects

[`HduClient`](create.md#hduclient-objects) 对象提供了对 API 访问的通道。

**Constructor**:

_class_ hdu_api.**HduClient**(*sess_mgr, \*\*kwargs*)

| 参数 | type | required | default | 备注 |
| :---: | :---: | :---: | :---: | :---: |
| sess_mgr | objects `SessionManager` | true | 无 | |
| kwargs | dict | false | 无 |  |

**Class methods**:


**Class attributes**:

- HduClient.**sess_mgr**

    &ensp;&ensp;`SessionManager` 对象，提供了 session 管理。

- HduClient.**username**

    &ensp;&ensp;学号，字符串类型。
    
- HduClient.**card**

    &ensp;&ensp;`Card` 对象，提供了对一卡通 API 的访问，详情请查看[这里](card.md)。

- HduClient.**exam**

    &ensp;&ensp;`Exam` 对象，提供了对考试 API 的访问，详情请查看[这里](exam.md)。

- HduClient.**person**

    &ensp;&ensp;`Person` 对象，提供了对个人信息 API 的访问，详情请查看[这里](person.md)。

- HduClient.**course**

    &ensp;&ensp;`Course` 对象，提供了对课程 API 的访问，详情请查看[这里](course.md)。

- HduClient.**public**

    &ensp;&ensp;`Public` 对象，提供了对公共信息 API 的访问，详情请查看[这里](public.md)。
