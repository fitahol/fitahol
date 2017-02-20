接口协定
====

接口地址
----

- 服务器地址： http://api.fitahol.com


HTTP STATUS协议
-------------

所有接口均按restful协议：

1. 请求成功 Successful - 2xx

最常用的三个：
	
	- HTTP_200_OK  get和put/patch请求成功
	- HTTP_201_CREATED  post 创建成功
	- HTTP_202_ACCEPTED delete 删除接受

2. 客户端请求有误 Client Error - 4xx

最常遇到的：

	- HTTP_400_BAD_REQUEST 前端参数格式或类型有误
	- HTTP_401_UNAUTHORIZED 用户未登录，需要先登录
	- HTTP_403_FORBIDDEN  用户身份权限不足
	- HTTP_404_NOT_FOUND  请求或访问的数据不存在
	- HTTP_405_METHOD_NOT_ALLOWED  http请求方法不被允许
	- HTTP_406_NOT_ACCEPTABLE  数据内容有问题，不接受处理

3. 服务器异常 Server Error - 5xx

常见的包括：

	- HTTP_500_INTERNAL_SERVER_ERROR 服务器代码程序有bug，崩溃
	- HTTP_502_BAD_GATEWAY  nginx网关出错误
	- HTTP_503_SERVICE_UNAVAILABLE  nginx网关连接不到应用服务器
	- HTTP_504_GATEWAY_TIMEOUT  达到nginx设置的超时限制

4. 特殊处理：

需要特殊处理的状态包括:

    - 200-300 正常加载数据，

    - 400 客户端参数错误，

    - 401 用户未登陆跳转登录，

    - 403 用户权限不足或被禁用，

    - 410 资源丢失>>刷新处理 ，

    - 404 访问资源被删除或不存在，报错弹窗msg

    - 500 服务端异常

    - 其他的全部都直接 {"detail": "弹窗内容", "opcode:": 245}

    - 避免出现 opcode 操作码。

返回数据格式说明
--------

详情数据
****

json 数据项：

.. code:: json

	{
	    "total": 10,
	    "balance": 0,
	    "ad_count": 4,
	    "ad_money": 0,
	    "invite_money": 0
	}
	
哈希对象包括了相关的属性值。

列表数据
****

默认服务端都会 **分页** ，如果不需要分页会在接口中特别说明！

默认每页数据10项，数据格式如下所示：

.. code:: json

	{
	    "count": 1,
	    "next": null,
	    "previous": null,
	    "results": [
	        {
	            "id": 1,
	            "withdraw_good": 1,
	            "pay": 3000,
	            "pay_status": 1,
	            "ptype": 1,
	            "remark": ""
	        }
	    ]
	}
	
next和previous值如:

> http://api.example.org/accounts/?page=5

服务端支持客户端指定 每页数据大小，参数值为 page_size，上限为100。（超过100，全部按上限处理）

说明：如果接口未分页，返回数据为列表数据

.. code:: json

    [
        {"key": "value"}, {"key": "value"}
    ]

返回所有数据列表。

5. user-agent定制

User Agent定制, 格式为 app_version=1.0.0&device_id=53244890

具体参数如下, 请按下面的参数顺序排序

    - "device_id": "863151020303571",
    - "user":"3456345"
    - "os_type": "android",
    - "os_version": "4.2.1",
    - "package_name": "com.happy.lock.wifi",
    - "app_version": "1.0.0",
    - "imsi": "460025012436898",
    - "channel": "wall",
    - "device_name": "M355",
    - "net": "WIFI",
    - "language": "zh"
