# fisher
鱼书项目  
示例站点: https://fisher.yase.me

请支持正版: https://coding.imooc.com/class/194.html
***
#### 1 部署时遇到问题
(1)、nginx无法启动,报无法打开err.log
```shell
cd /var/log/
mkdir nginx
nginx -t
systemctl start nginx
systemctl enable nginx
```
(2)、OSError: mysql_config not found
```shell
apt-get install default-libmysqlclient-dev python3-dev
```
(3)、安装gunicorn
```shell
pip install gunicorn
```
(4)、nginx报错,报相同配置
```shell
nginx: [emerg] a duplicate default server for 0.0.0.0:80 in /etc/nginx/sites-enabled/default:22
nginx: configuration file /etc/nginx/nginx.conf test failed

# 解决方法
注释默认配置
/etc/nginx/sites-enabled/*;
```
#### 2 20230520问题
(1)、 由于flask等包版本升级造成的一些方法无法使用
(2)、 orm的使用
```shell
export FLASK_APP=fisher.py
flask db init
flask db migrate
flask db upgrade
```

