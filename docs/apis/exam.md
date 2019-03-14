# 考试 API

此章节是关于考试 API 的描述。

## `Exam` objects

[`Exam`](exam.md#exam-objects) 对象提供了一系列考试信息 API。

**Constructor**:

_class_ hdu\_api.**Exam**(*session*)

| 参数 | type | required | default | 备注 |
| :---: | :---: | :---: | :---: | :---: |
| session | objects `ExamSession` | true | 无 | 一个已初始化的 `ExamSession` 对象

**Class methods**:

- _classmethod_ Exam.**grade**(*year, term, raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;学期成绩。

- _classmethod_ Exam.**grade_current**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;本学期成绩。

- _classmethod_ Exam.**level_grade**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;等级考试成绩，如 CET-4 成绩。

- _classmethod_ Exam.**schedule**(*year, term, raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;考试安排。

- _classmethod_ Exam.**schedule_current**(*raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;本学期考试安排。

- _classmethod_ Exam.**schedule_make_up**(*term, raw=False, dictionary=DEFAULT_DICTIONARY*)

    &ensp;&ensp;补考安排。

参数说明：

- raw - 是否输出为原始格式
- dictionary - raw 为 true 时，使用该字典替换返回数据的 key
- year - 学年，格式如 '2018-2019'
- term - 学期，1 表示第一个学期，2 表示第二个学期

**Class attributes**:

- Exam.**session**
    
    &ensp;&ensp;`ExamSession` 对象。
