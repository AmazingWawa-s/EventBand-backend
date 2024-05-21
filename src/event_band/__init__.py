import pymysql
pymysql.install_as_MySQLdb()
# your_app/__init__.py
 
default_app_config = 'event.apps.YourAppConfig'
#conn=pymysql.connect(host="192.168.43.246",user="sa",password="",db="eventband",port=3306,charset="utf8")