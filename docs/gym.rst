健身房信息
=====

获取省份
----
.. http:get:: /central/province/

    获取健身房信息

    **请求参数**:
    如果已登录需要 添加auth认证, 如果无可以不传

    **请求示例**

    .. sourcecode:: http

        GET /central/province/ HTTP/1.1
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
            "code": "11",
            "name": "北京",
            "fullname": "北京市",
            "pinyin": "beijing",
            "suffix": "市"
            },
            {
            "code": "12",
            "name": "天津",
            "fullname": "天津市",
            "pinyin": "tianjin",
            "suffix": "市"
            },
            {
            "code": "13",
            "name": "河北",
            "fullname": "河北省",
            "pinyin": "hebei",
            "suffix": "省"
            }
        ]

    **返回参数**

    :param code: 省代号
    :type code: int
    :param name: 名称
    :type name: string
    :param fullname: 全称
    :type fullname: string
    :param suffix: 行政单位
    :type suffix: string
    :param pinyin: 名称拼音
    :type pinyin: string


获取城市
----
.. http:get:: /central/city/<province_code>/

    获取健身房信息

    **请求参数**:
    如果已登录需要 添加auth认证, 如果无可以不传

    **请求示例**

    .. sourcecode:: http

        GET /central/city/13/ HTTP/1.1
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
            "code": "1301",
            "name": "石家庄",
            "fullname": "石家庄市",
            "pinyin": "shijiazhuang",
            "suffix": "市"
            },
            {
            "code": "1302",
            "name": "唐山",
            "fullname": "唐山市",
            "pinyin": "tangshan",
            "suffix": "市"
            },
            {
            "code": "1303",
            "name": "秦皇岛",
            "fullname": "秦皇岛市",
            "pinyin": "qinhuangdao",
            "suffix": "市"
            }
        ]

    **返回参数**

    :param code: 城市代号
    :type code: int
    :param name: 名称
    :type name: string
    :param fullname: 全称
    :type fullname: string
    :param suffix: 行政单位
    :type suffix: string
    :param pinyin: 名称拼音
    :type pinyin: string

获取县/区
-----
.. http:get:: /central/district/<city_code>/

    获取健身房信息

    **请求参数**:
    如果已登录需要 添加auth认证, 如果无可以不传

    **请求示例**

    .. sourcecode:: http

        GET /central/district/1301/ HTTP/1.1
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
            "code": "130101",
            "name": "",
            "fullname": "市辖区",
            "pinyin": "",
            "suffix": "市辖区"
            },
            {
            "code": "130102",
            "name": "长安",
            "fullname": "长安区",
            "pinyin": "changan",
            "suffix": "区"
            },
            {
            "code": "130104",
            "name": "桥西",
            "fullname": "桥西区",
            "pinyin": "qiaoxi",
            "suffix": "区"
            }
        ]

    **返回参数**

    :param code: 县/区代号
    :type code: int
    :param name: 名称
    :type name: string
    :param fullname: 全称
    :type fullname: string
    :param suffix: 行政单位
    :type suffix: string
    :param pinyin: 名称拼音
    :type pinyin: string


获取健身房
-----
.. http:get:: /central/gym/

    获取健身房信息

    **请求参数**:

    需要 Token 认证通过

    以下三个过滤均可，请使用其中之一。

    :param name: 健身房名称
    :type name: string
    :param city_code: 城市码
    :type city_code: string
    :param district_code: 城区码
    :type district_code: string

    **请求示例**

    .. sourcecode:: http

        GET /central/gym/?name=麦加 HTTP/1.1
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
            "name": "麦加健身美黑工作室",
            "address": "青年路国美第一城3号院10号楼3单元",
            "telephone": "010-85583632",
            "lat": 0,
            "lng": 0,
            "city_info":
                {
                    "province":{"name":"北京","code":"11","fullname":"北京市"},
                    "city":{"name":"市辖区","code":"1101","fullname":"市辖区"},
                    "district":{"name":"朝阳","code":"110105","fullname":"朝阳区"}
                }
            }
        ]

添加健身房
-----
.. http:post:: /central/gym/

    添加健身记录

    **请求参数**:

    需要 Token 认证通过

    :param name: 名称
    :type name: string
    :param address: 地址
    :type address: string
    :param telephone: 电话，允许写多个以,号间隔
    :type telephone: string
    :param lat: 地理位置,纬度; 可无
    :type lat: float
    :param lng: 地理位置, 经度; 可无
    :type lng: float
    :param district_code: 县/区code
    :type district_code: int
    :param city_code: 城市code, 如果县区上传, 城市可不传
    :type city_code: int

    **请求示例**

    .. sourcecode:: http

        POST /account/goal_record/ HTTP/1.1
        Host: api.fitahol.com
        Accept: application/json, application/x-www-form-urlencoded

        {
            "name": "麦加健身",
            "address": "青年路国美第一城3号院10号楼3单元",
            "telephone": "010-85583632",
            "lat": "124.049720",
            "lng": "41.820831",
            "city_code": 1101,
            "district_code": 110105
        }
