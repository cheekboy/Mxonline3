# Mxonline3

[![Build Status](https://travis-ci.org/jiangming1/Mxonline3.svg?branch=master)](https://travis-ci.org/jiangming1/Mxonline3.svg?branch=master)
[![Build status](https://aontimer.visualstudio.com/python/_apis/build/status/python-Docker%20container-CI)](https://aontimer.visualstudio.com/python/_build/latest?definitionId=2)


使用Python3.x与Django2.0.1开发的在线教育平台网站: http://h1.caiwuhao.com:8000

## 已经完成的功能

```
管理平台
ecs创建
dns 创建和更新
k8s 创建和更新


```
## Roadmap
```
diskbackup
mysql create


```

# 使用地址
use the address: http://h1.caiwuhao.com:8000/

## Contents：
docker run --name some-mysql33061 -v /33061:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d -p 33061:3306 mysql:5.7
创建mysql服务器
修改Mxonline3/setting.py 修改数据库地址
docker run -p 8000:8000 -it aontimer/p8h-ops:ops5 python manage.py makemigration
docker run -p 8000:8000 -it aontimer/p8h-ops:ops5 python manage.py migrate
docker run -p 8000:8000 -it aontimer/p8h-ops:ops5 python manage.py createsuperuser
创建默认管理员账号
这几个步骤做完后就可以运行
docker run -p 8000:8000 -d aontimer/p8h-ops:ops5 python manage.py runserver 0.0.0.0:8000


## Background:

## About me
(http://github.com/jiangming1)

有趣的Python群：141708431

欢迎关注简书，star项目！谢谢！

你的关注支持是我继续分享前进的动力。

## 求打赏鼓励

很高兴我写的文章（或我的项目代码）对你有帮助，请我吃包辣条吧！

微信打赏:
