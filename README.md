# Fitahol Server
在线文档地址: [http://www.fitahol.com/docs/index.html](http://www.fitahol.com/docs/index.html)

使用 sphinx-docs 生成。

## 部署准备:

系统使用python3 + django开发，环境依赖在 requirements.txt 中列出；

方便部署环境隔离，需要先安装 virtualenv >>  pip install virtualenv

创建python环境 >> virtualenv fitaholEnv

进入目录 >> cd fitaholEnv

拉取线上代码 >> git clone git@git.oschina.net:lingnck/fitahol.git

启动virtualenv进入python虚拟环境，在不同系统下的不同启动方式
- linux/mac启动方式：在fitaholEnv目录中执行 >> source bin/activate
- windows启动方式：执行fitaholEnv\Scripts\activate.bat

在python虚拟环境中安装依赖模块，执行 >> pip install -r fitahol/requirements.txt ;


## 操作例子：
> pip install virtualenv
>
> virtualenv /data/fitaholEnv
>
> cd /data/fitaholEnv
> 
> git clone git@git.oschina.net:lingnck/fitahol.git
> 
> source ./bin/activate
>
> pip install -r fitahol/requirements.txt


## 部署文件：

在目录 /etc 中有两个文件：

> supervisord.conf 是项目的supervisor 启动配置；
>
> gunicorn.py 是多线程并发配置，最大并发10000
>
> 启动supervisor: supervisord -c /etc/supervisord.d/supervisord.conf
>
> 重启服务 supervisorctl start/status/stop/restart fitahol
