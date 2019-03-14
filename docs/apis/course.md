# 课程 API

此章节是关于课程 API 的描述。

## `Course` objects

[`Course`](course.md#course-objects) 对象提供了一系列课程信息 API。

**Constructor**:

_class_ hdu\_api.**Course**(*session*)

| 参数 | type | required | default | 备注 |
| :---: | :---: | :---: | :---: | :---: |
| session | objects `CourseSession` | true | 无 | 一个已初始化的 `CourseSession` 对象

**Class methods**:

- _classmethod_ Course.**selected**(_year, term, raw=False, dictionary=DEFAULT\_DICTIONARY_)

    &ensp;&ensp;已选课程。

- _classmethod_ Course.**selected_current**(_raw=False, dictionary=DEFAULT\_DICTIONARY_)

    &ensp;&ensp;本学期已选课程。

- _classmethod_ Course.**schedule**(_year, term, raw=False, dictionary=DEFAULT\_DICTIONARY_)

    &ensp;&ensp;课表。

- _classmethod_ Course.**schedule_current**(_raw=False, dictionary=DEFAULT\_DICTIONARY_)

    &ensp;&ensp;本学期课表。

参数说明：

- raw - 是否输出为原始格式
- dictionary - raw 为 true 时，使用该字典替换返回数据的 key
- year - 学年，格式如 '2018-2019'
- term - 学期，1 表示第一个学期，2 表示第二个学期

**Class attributes**:

- Course.**session**
    
    &ensp;&ensp;`CourseSession` 对象。