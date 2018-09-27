# Mxonline3

[![Build Status](https://travis-ci.org/jiangming1/Mxonline3.svg?branch=master)](https://travis-ci.org/jiangming1/Mxonline3.svg?branch=master)


使用Python3.x与Django2.0.1开发的在线教育平台网站: http://mxonline.mtianyan.cn

## Quick Start

```
$ git clone https://github.com/mtianyan/Mxonline3.git
$ cd Mxonline3
$ pip install -r requirements.txt
$ python manage.py runserver
```
#运行应用容器和mysql
docker run --name mysql57-db -p 3306:3306 -v /my/own/datadir:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-1pw -d mysql:5.7
docker run -d -p 8080:8080 --name k8s aontimer/mxonline3 -e "host=mysql57-db"
#生成数据库
docker exec -it k8s python3 manage.py makemigrations
docker exec -it k8s python3 manage.py migrate
#创建超级管理员
docker exec -it k8s python3 manage.py createsuperuser

#
use the address: http://127.0.0.1:8000/

## Contents：

对应教程已开通简书连载文集: https://www.jianshu.com/nb/21010157

**欢迎大家关注订阅，点赞！！！**

## Background:

- 最近重装了系统，所以从环境配置开始,我都做到尽可能从零开始，对初学者友好。
- 自己已经学习Python一年了，最近对于Python相关开始进行一个较全面复习。
- 希望可以帮到那些对于Python，对Django有兴趣的同学少走弯路。

[项目线上演示地址](http://mxonline.mtianyan.cn)
[原版视频课程地址:](https://coding.imooc.com/learn/list/78.html)

>一次性的一个完整项目代码很难被学习，所以我采用commit记录源码快照 + 阶段性教程结合的形式。类似关卡式学习概念。

- 每节教程前面会写明对应的上节commit：开始某一节教程的前置条件。
- 每节教程后面会写明对应的已结束commit: 方便本节出错参考。

希望可以对Django初学者，Python爱好者有所帮助。

## About me
[简书](https://www.jianshu.com/u/db9a7a0daa1f) && [mtianyan's blog](http://blog.mtianyan.cn/)

有趣的Python群：619417153

欢迎关注简书，star项目！谢谢！

你的关注支持是我继续分享前进的动力。

## 求打赏鼓励

很高兴我写的文章（或我的项目代码）对你有帮助，请我吃包辣条吧！

微信打赏:

![mark](http://myphoto.mtianyan.cn/blog/180302/i52eHgilfD.png?imageslim)

支付宝打赏:

![mark](http://myphoto.mtianyan.cn/blog/180302/gDlBGemI60.jpg?imageslim)
