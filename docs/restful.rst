基础协定
====

支持的http方法
---------

- GET 获取数据

- POST 创建数据

- PUT 全量更新数据，需要传数据全部属性，如重填用户表更新全部信息。

- PATCH 定量更新，仅需要传指定数据项，如仅更新用户头像。

- DELETE 删除数据，指定id删除数据。

可接收数据格式
-------

- json

- html表单

- multipart/form-data

- 文件

- 可扩展支持 XML, YAML。如有需要，请指出。


返回数据
----

- json

- 可扩展支持 xml, yaml, jsonp。如有需要，请指出。

**HTTP更新操作说明**
--------------

除用户信息等特殊接口, 所有接口都支持CRUD操作, 其中更新支持 PUT 和 PATCH 两种操作。

PUT 操作和 POST传参一样, 故不会重复说明;

PATCH 操作 只需要传其中部分参数操作, 也不再额外说明;

如遇到接口不一致, 会在文档中额外给出说明.

.. image:: _static/url_desc.png

所有接口的url路径格式如上图所示:

其中 prefix 为资源名称, 如profile, 对它进行 GET 获取列表数据, post 创建新数据;

methodname 指特定的列表过滤方法, 一般只有内部指定才会有;

lookup 指查询到具体单一资源的查询方式, 一般是数据库的 id. 对单一次源, get获取详情, put 全量更新, patch 定量更新, delete 删除数据项;

特别说明
----

关于跨域请求，服务器支持指定IP和域名跨域，如果有调试测试需求，请联系我配置IP或域名。

默认情况下，不建议使用jsonp封装建数据。


用户认证协议
------

系统目前仅支持微信登录，建立虚似用户与微信openid绑定。

登录支持 **TokenAuthentication** 和 **SessionAuthentication** 两种机制。

客户端和Web前端目前与服务端分离，主要使用 TokenAuthentication 验证用户身份。

访问方式，在http header中指定 Authorization 值，格式如下所示：

> curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

