# django_blog
用django搭建的个人博客

# Docker depoly
首先你得有docker 而且安装了docker-compose，进入项目目录运行下面指令

```
docker-compose up -d
```
等待完成即可在浏览器，分别有postgresql、redis、ubuntu三个镜像需要下载

```
docker-compose down -v
```
删掉容器停止部署
```
docker-compose down -v --rmi all
```
删掉容器停止部署 并删除镜像

# 在blog的settings.py
```
DEBUG = True
```
测试完成后记得DEBUG设置False，默认先是True

```
DEPOLY_HOST = '192.168.56.xx'
ALLOWED_HOSTS = ['*']
```
修改成你要部署的IP或者域名```DEPOLY_HOST```这个参数决定WebSocket 连接的服务器地址（私信的聊天功能）

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xx@163.com'
EMAIL_HOST_PASSWORD = 'xxxx'
EMAIL_SUBJECT_PREFIX = '[zzr的博客]'
EMAIL_USE_TLS = True
```
修改成你自己的邮箱服务器的配置，如果设置不成功，会导致注册时发送邮箱失败，触发异常

# 在django_nginx.conf

```
listen 808;
server_name 192.168.56.135;
```
nginx的配置，修改成你自己的

