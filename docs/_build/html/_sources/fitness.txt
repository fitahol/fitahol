
健身接口
====

健身动作类别
------
.. http:get:: /fitness/category/

    获取健身房信息

    **请求参数**:

    Token 认证通过, 可以获得私有类别

    **请求示例**

    .. sourcecode:: http

        GET /fitness/category/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        [
            {
            "id": 1,
            "name": "肩部",
            "en_name": "Shoulders",
            "icon": "http://0.0.0.0:9999/media/gym/icons/shoulders_iconiphone2x.png",
            },
            {
            "id": 2,
            "name": "胸部",
            "en_name": "Chest",
            "icon": "http://0.0.0.0:9999/media/gym/icons/chest_iconiphone2x.png",
            },
        ]

添加健身动作类别
--------
.. http:post:: /fitness/category/

    添加健身动作类别

    **请求参数**:

    需要 Token 认证通过

    :param name: 名称
    :type name: string
    :param desc: 描述
    :type desc: string
    :param icon: 图标, 文件上传需要 multipart/form-data 请求
    :type icon: file

    **请求示例**

    .. sourcecode:: http

        GET /fitness/category/ HTTP/1.1
        Host: api.fitahol.com
        Accept: multipart/form-data

        **因为需要上传文件,所以请求只能是form-data,不能传json**

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "id": 1,
        "name": "有氧运动",
        "en_name": "cardio",
        "icon": "http://0.0.0.0:9999/media/gym/icons/fuhe.png",
        }

删除健身动作类别
--------
.. http:delete:: /fitness/category/<category_id>/

    删除健身动作类别, 只能删除自己创建的私有类别

    **请求参数**:

    需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        DELETE /fitness/category/1/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:
    :statuscode 204: 删除成功, 无内容


肌肉群分类
-----
.. http:get:: /fitness/muscle/

    获取健身房信息

    **请求参数**:

    Token 认证通过, 可以获得私有类别

    **请求示例**

    .. sourcecode:: http

        GET /fitness/category/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        [
            {
            "name": "斜方肌",
            "en_name": "Trapezius",
            "image": "http://0.0.0.0:9999/media/gym/muscle/Trapezius_PMiphone.png",
            "id": 1
            },
            {
            "name": "肱三头肌",
            "en_name": "Triceps Brachii",
            "image": "http://0.0.0.0:9999/media/gym/muscle/Triceps_Brachii_PMiphone.png",
            "id": 2
            },
            {
            "name": "胸大肌",
            "en_name": "Pectoralis Major",
            "image": "http://0.0.0.0:9999/media/gym/muscle/Pectoralis_Major_PMiphone.png",
            "id": 3
            },

        ]

查看动作列表
------
.. http:get:: /fitness/exercise/

    获取动作列表, 可以通过参数过滤列表; 如无参数分页返回所有.

    **请求参数**:

    Token 认证通过, 可以获得私有动作

    数据分页;
    可以通过两种试过滤健身动作, 之后会添加通过设备过滤;
    不过滤则显示全部.

    category_id 健身类型Id
    muscle_id 肌肉群分类Id

    **请求示例**

    .. sourcecode:: http

        GET /fitness/exercise/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "count": 39,
        "next": "http://0.0.0.0:9999/fitness/exercise/?category_id=6&page=2",
        "previous": null,
        "results":[
            {
            "id": 93,
            "name": "引体向上",
            "en_name": "Chin-UpsN",
            "icon": "http://0.0.0.0:9999/media/gym/exercise_icon/Chin-Upsiphone.png",
            "is_public": true
            },
        ]
        }

    **返回参数**

    :param id: 健身动作id
    :type id: int
    :param name: 名称
    :type name: string
    :param en_name: 英文名
    :type en_name: string
    :param icon: 图标url
    :type icon: string
    :param is_public: 是否公开
    :type is_public: bool


查看动作详情
------
.. http:get:: /fitness/exercise/<exercise_id>/

    获取动作详情

    **请求参数**:

    Token 认证通过, 可以获得私有动作

    **请求示例**

    .. sourcecode:: http

        GET /fitness/exercise/94/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "id": 94,
        "equipment":[],
        "pictures":[
            {
            "id": 183,
            "picture": "http://0.0.0.0:9999/media/gym/pictures/Dead-Lifts-1iphone.png"
            },
            {
            "id": 184,
            "picture": "http://0.0.0.0:9999/media/gym/pictures/Dead-Lifts-2iphone.png"
            }
        ],
        "videos":[],
        "muscles":[
            {
            "name": "Latissimus Dorsi",
            "image": null,
            "id": 16,
            "level": "primary"
            },
            {
            "name": "Biceps Femoris",
            "image": null,
            "id": 17,
            "level": "secondary"
            }
        ],
        "name": "哑铃硬拉",
        "en_name": "Dead-LiftsN",
        "desc": "该动作练习下背部和腿部肌肉。\n\n步骤：双脚分开，与肩同宽。"
        "icon": "http://0.0.0.0:9999/media/gym/exercise_icon/Dead-Liftsiphone.png",
        "unit": "KG",
        "strength": "",
        "is_public": true
        }

    **返回参数**

    :param id: 健身动作id
    :type id: int
    :param name: 名称
    :type name: string
    :param en_name: 英文名
    :type en_name: string
    :param icon: 图标url
    :type icon: string
    :param is_public: 是否公开
    :type is_public: bool
    :param pictures: 配图, 核心字段picture: 图片地址
    :type pictures: list
    :param desc: 详细描述
    :type desc: string
    :param muscles: 肌肉群,包括字段 name, image, level(包括primary和secondary两种肌肉锻炼)
    :type muscles: list
    :params videos: 视频
    :type videos: list
    :params videos: 使用到的设备
    :type videos: list
    :param unit: 计量单位
    :type unit: string
    :param strength: 强度单位, 如分钟或次数
    :type strength: string

创建新动作
-----
.. http:get:: /fitness/exercise/

    本部分待确认!!

    **请求参数**:

    Token 认证通过, 可以获得私有动作

    **请求示例**

    .. sourcecode:: http



查看健身设备
------
.. http:get:: /fitness/equipment/

    获取健身房信息

    **请求参数**:

    Token 认证通过, 可以获得私有动作

    **请求示例**

    .. sourcecode:: http

        GET /fitness/equipment/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "count": 1,
        "next": null,
        "previous": null,
        "results":[
        {
        "id": 1,
        "pictures":[
            {
            "id": 1,
            "picture": "http://0.0.0.0:9999/media/gym/pictures/ba5e30cbb8ffcf4a61ee9683e36743e0.jpg"
            }
        ],
        "name": "哑铃",
        "cover": "http://.....",
        "desc": "哑铃"
        }
        ]
        }

添加健身设备
------
.. http:post:: /fitness/equipment/

    添加健身动作类别

    **请求参数**:

    需要 Token 认证通过

    :param name: 名称
    :type name: string
    :param desc: 描述
    :type desc: string
    :param cover: 封面图, 文件上传需要 multipart/form-data 请求
    :type cover: file

    **请求示例**

    .. sourcecode:: http

        GET /fitness/equipment/ HTTP/1.1
        Host: api.fitahol.com
        Accept: multipart/form-data

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "id": 2,
        "name": "哑铃",
        "cover": "http://.....",
        "desc": "哑铃"
        }



获取学员健身目标及7日记录
-------------
.. http:get:: /fitness/fit_goal/

    获取学员选用的健身目标及7日记录
    !!!数据不分页!!!

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /fitness/fit_goal/?user_id=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        [
            {
                "id": 19,
                "name": "wer",
                "measure": "Kg",
                "user_id": 9,
                "goal": 33,
                "initial": 50,
                "schedule": 30,
                "is_public": false,
                "goal_record":[{"current": 30, "cdate": "2016-07-01", "id: 1, "figure": ""}, ]
            },
            {
                "id": 11,
                "user_id": 9,
                "name": "手臂增肌",
                "measure": "CM",
                "initial": 50,
                "schedule": 30,
                "goal": 50,
                "is_public": false,
                "goal_record":[{"current": 30, "cdate": "2016-07-01", "id: 1, "figure": ""}, ]
            }
        ]

    **返回参数**:

    :param name: 目标名称
    :type name: string
    :param measure: 计量单位
    :type measure: string
    :param initial: 初始值
    :type initial: int
    :param schecule: 计划周期，按天数计
    :type schecule: int
    :param goal: 目标值
    :type goal: int
    :param is_public: 是否系统默认, False则为个人私有
    :type is_public: boolean
    :param goal_record: 目标数据记录，默认最近一周，无则为空列表
    :type goal_record: list


获取学员健身目标最近状态
------------
.. http:get:: /fitness/fit_goal/last/

    获取学员最近健身目标变更状态

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /fitness/fit_goal/?user_id=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
            "id": 19,
            user":{
                "nickname": "马德岭",
                "portrait": "http://www.fitahol.com/media/account/portrait/shiwantuan2.png",
                "user_id": 9
            },
            "name": "身体复健",
            "measure": "Kg",
            "goal": 33,
            "initial": 33,
            "schedule": 33,
            "is_public": false,
            "goal_record":{
                "id": 11,
                "current_desc": "20 Kg",
                "current": 20,
                "cdate": "2016-10-18",
                "figure": "晒图地址",
                "user": 9
            }
        }

    **返回参数**:

    :param name: 目标名称
    :type name: string
    :param measure: 计量单位
    :type measure: string
    :param initial: 初始值
    :type initial: int
    :param schecule: 计划周期，按天数计
    :type schecule: int
    :param goal: 目标值
    :type goal: int
    :param is_public: 是否系统默认, False则为个人私有
    :type is_public: boolean
    :param goal_record: 目标数据记录，默认最近一周，无则为空列表
    :type goal_record: list


创建学员健身目标
--------
.. http:post:: /fitness/fit_goal/

    创建健身目标, 可选用公用健身目标, 也可以创建新的健身目标;
    1. 选用公用健身目标创建个人目标时,只需要传公用目标id;
    2. 创建新健身目标, 需要传完整的目标数据+用户ID

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int
    :param name: 目标名称
    :type name: string
    :param measure: 计量单位
    :type measure: string
    :param inital: 初始值
    :type initial: int
    :param goal: 目标值
    :type goal: int
    :param schedule: 计划周期，按天数计
    :type schedule: int
    :param is_public: 是否作为公开标签
    :type is_public: boolean

    **请求示例**

    .. sourcecode:: http

        POST /fitness/fit_goal/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded
        1. 选用 公用健身目标
        {"fit_goal": 123, "user_id": 6}

        2. 创建 新的健身目标
        {"name":"手臂增肌", "desc": "健身增肌肉", "is_public": true,
        "measure": "CM", "goal": "50", "user_id": 6, "initial": 80, "schedule": 30}

    **返回状态码**:

    :statuscode 201: 创建成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "detail": "创建成功"
        }


删除学员健身目标
--------
.. http:delete:: /fitness/fit_goal/<fit_goal_id>/

    删除健身目标

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        DELETE /fitness/fit_goal/9/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 204: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:
    :statuscode 204: 删除成功, 无内容

    **请求出错情况**
    :statuscode 400: 没有上传user_id参数
    :statuscode 400: user_id 不是您的学员


获取学员健身目标变化记录
------------
.. http:get:: /fitness/goal_record/

    获取学员选用的健身目标,
    !!!数据不分页!!!

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int
    :param fit_goal_id: 健身目标id
    :type fit_goal_id: int
    :param interval: 间隔时间，如值为7表示最近7天内，30表示最近30天内; 默认7
    :type interval: int

    **请求示例**

    .. sourcecode:: http

        GET /fitness/goal_record/?user_id=6&fit_goal_id=11 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        [
            {
            "id": 1,
            "current_desc": "30 Kg",
            "current": 30,
            "cdate": "2016-07-01"
            }
        ]

    **返回参数**:

    :param name: 目标名称
    :type name: string
    :param measure: 计量单位
    :type measure: string
    :param goal: 目标值
    :type goal: int
    :param is_public: 是否系统默认, False则为个人私有
    :type is_public: boolean
    :param goal_record: 目标数据记录，默认最近一周，无则为空列表
    :type goal_record: list


添加学员健身目标变化记录
------------
.. http:post:: /fitness/goal_record/

    添加学员健身目标对应的记录。

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int
    :param fit_goal_id: 目标ID
    :type fit_goal_id: int
    :param current: 当前记录值
    :param figure: 晒图
    :type figure: file
    :type current: int
    :param cdate: 记录日期
    :type cdate: string

    **请求示例**

    .. sourcecode:: http

        POST /fitness/goal_record/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {"current": 30, "cdate": "2016-07-01", "id: 1}

    **返回状态码**:

    :statuscode 201: 创建成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "detail": "创建成功"
        }


删除学员健身目标变化记录
------------
.. http:delete:: /fitness/goal_record/<goal_record_id>/

    添加学员健身目标对应的记录。

    **请求参数**:

    需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        DELETE /fitness/goal_record/1/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {"user_id": 3, "fit_goal_id": 1, "current": 30, "cdate": "2016-07-01"}

    **返回状态码**:

    :statuscode 202: 删除成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "detail": "删除成功"
        }


课堂训练动作列表
--------
.. http:get:: /fitness/exercise_record/

    获取用户健身课程对应的健身动作列表
    数据不分页。

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int
    :param event_id: 课程事件id
    :type event_id: int

    **请求示例**

    .. sourcecode:: http

        GET /fitness/goal_record/?user=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        [
            {
            "id": 2,
            "exercise":
                {"id": 1,
                "name": "健身动作名称",
                "en_name": "英文名称",
                "icon": "图标地址",
                "is_public": true,
                "unit": "计量单位KG"
                },
            "value": 30,
            "number": 12,
            }
        ]

    **返回参数**:

    :param exercise: 动作说明
    :type current: json
    :param value: 训练体量，如80KG杠铃
    :type value: int
    :param number: 训量次数，如举10次
    :type number: int


添加课堂训练动作
--------
.. http:post:: /fitness/exercise_record/

    添加健身记录

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int
    :param exercise_id: 健身动作id
    :type exercise_id: int
    :param event_id: 课程事件id
    :type event_id: int
    :params value: 训练体量，如80KG杠铃
    :type value: int
    :params number: 训量次数，如举10次
    :type number: int

    **请求示例**

    .. sourcecode:: http

        POST /fitness/exercise_record/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "id": 2,
            "exercise_id": 1,
            "event_id"; 1,
            "value": 30,
            "number": 12,
        }

    **返回状态码**:

    :statuscode 201: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "detail": "创建成功"
        }


删除课堂训练动作
--------
.. http:delete:: /fitness/exercise_record/<exercise_record_id>/

    创建健身目标

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        DELETE /fitness/exercise_record/1/?user=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:
    :statuscode 204: 删除成功, 无内容


公用教练擅长领域
--------
.. http:get:: /fitness/expert_tag/public/

    获取教练擅长领域, 公开的标签型 教练擅长领域;
    !!! 数据分页 !!!

    **请求参数**:

    需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /fitness/expert_tag/public/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        [
            {
            "id": 1,
            "name": "减脂",
            "desc": "减脂圣经",
            "is_public": false
            },
        ]

    **返回参数**:

    :param name: 名称
    :type name: string
    :param desc: 描述
    :type desc: string
    :param is_public: 是否系统默认, False则为个人私有
    :type is_public: boolean


教练擅长领域
------
.. http:get:: /fitness/expert_tag/

    获取学员选用的健身目标,
    !!!数据不分页!!!

    **请求参数**:

    需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        GET /fitness/expert_tag/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        [
            {
            "id": 1,
            "name": "减脂",
            "desc": "减脂圣经",
            "is_public": false
            },
            {
            "id": 2,
            "name": "增肌",
            "desc": "肌肉维度",
            "is_public": false
            }
        ]

    **返回参数**:

    :param name: 名称
    :type name: string
    :param desc: 描述
    :type desc: string
    :param is_public: 是否系统默认, False则为个人私有
    :type is_public: boolean


创建教练擅长领域
--------
.. http:post:: /fitness/expert_tag/

    创建教练擅长领域, 可选用公用擅长领域, 也可以创建新的擅长领域;
    1. 选用公用擅长领域 创建个人擅长领域时, 只需要传公用领域id;
    2. 创建新教练擅长领域, 需要传完整的 领域数据

    **请求参数**:

    需要 Token 认证通过

    :param name: 目标名称
    :type name: string
    :param desc: 描述
    :type desc: string
    :param is_public: 是否作为公开标签
    :type is_public: boolean

    **请求示例**

    .. sourcecode:: http

        POST /fitness/expert_tag/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded
        1. 选用 公用健身目标
        {"expert_tag": 123}

        2. 创建 新的健身目标
        {"name":"手臂增肌", "desc": "健身增肌肉", "is_public": true}

    **返回状态码**:

    :statuscode 201: 创建成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "detail": "创建成功"
        }


删除教练擅长领域
--------
.. http:delete:: /fitness/expert_tag/<expert_tag_id>/

    创建擅长领域

    **请求参数**:

    需要 Token 认证通过

    **请求示例**

    .. sourcecode:: http

        DELETE /fitness/expert_tag/9/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 204: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:
    :statuscode 204: 删除成功, 无内容

    **请求出错情况**
    :statuscode 404: 数据不存在


Inbody体测
--------
.. http:get:: /fitness/inbody/

    获取健身目标, 包括系统

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        GET /fitness/inbody/?user=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
        "count": 1,
        "next": null,
        "previous": null,
        "results":[
            {
            "id": 1,
            "cdate": "2016-01-30",
            "weight": 0,
            "metabolism": 0,
            "body_fat": 0,
            "fat_weight": 0,
            "skeletal_muscle": 0,
            "chest": 0,
            "arm": 0,
            "upper_arm": 0,
            "waistline": 0,
            "thigh": 0,
            "crus": 0,
            "user": 6
            }
        ]
        }


    **返回参数**:

    :param cdate: 日期
    :type cdate: string
    :param weight: 体重
    :type weight: int
    :param metabolism: 基础代谢
    :type metabolism: int
    :param body_fat: 体脂率
    :type body_fat: int
    :param fat_weight: 脂肪重量
    :type fat_weight: int
    :param skeletal_muscle: 骨骼肌
    :type skeletal_muscle: int
    :param chest: 胸围
    :type chest: int
    :param arm: 臂围
    :type arm: int
    :param upper_arm: 上臂围
    :type upper_arm: int
    :param waistline: 腰围
    :type waistline: int
    :param thigh: 大腿围
    :type thigh: int
    :param crus: 小腿围
    :type crus: int


添加inbody记录
----------
.. http:post:: /fitness/inbody/

    添加健身记录

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int
    :param cdate: 日期
    :type cdate: string
    :param weight: 体重
    :type weight: int
    :param metabolism: 基础代谢
    :type metabolism: int
    :param body_fat: 体脂率
    :type body_fat: int
    :param fat_weight: 脂肪重量
    :type fat_weight: int
    :param skeletal_muscle: 骨骼肌
    :type skeletal_muscle: int
    :param chest: 胸围
    :type chest: int
    :param arm: 臂围
    :type arm: int
    :param upper_arm: 上臂围
    :type upper_arm: int
    :param waistline: 腰围
    :type waistline: int
    :param thigh: 大腿围
    :type thigh: int
    :param crus: 小腿围
    :type crus: int

    **请求示例**

    .. sourcecode:: http

        POST /fitness/inbody/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "cdate": "2016-01-30",
            "weight": 0,
            "metabolism": 0,
            "body_fat": 0,
            "fat_weight": 0,
            "skeletal_muscle": 0,
            "chest": 0,
            "arm": 0,
            "upper_arm": 0,
            "waistline": 0,
            "thigh": 0,
            "crus": 0,
            "user": 6
        }

    **返回状态码**:

    :statuscode 201: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:

    .. sourcecode:: http

        {
        "id": 9,
        "name": "手臂增肌",
        "measure": "CM",
        "goal": 50,
        "is_default": false
        }


删除inbody记录
----------
.. http:delete:: /fitness/inbody/<inbody_id>/

    创建健身目标

    **请求参数**:

    需要 Token 认证通过

    :param user_id: 学员用户id
    :type user_id: int

    **请求示例**

    .. sourcecode:: http

        DELETE /fitness/inbody/1/?user=6 HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

    **返回状态码**:

    :statuscode 200: 请求成功
    :statuscode 401: 用户未登陆
    :statuscode 403: 用户权限不足

    **请求成功返回**:
    :statuscode 204: 删除成功, 无内容

