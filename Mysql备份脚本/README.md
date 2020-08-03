mysqldump备份脚本(保留7天)

# 环境
安装部署模式按照
[离线安装Mysql5.7.28及调优](https://rugod.cn/2020/05/01/mysql/mysql-install/)

# 配置参数
根据实际修改账号密码以及Mysql的一些基础文件目录
```
db_user="root"
db_passwd="123456"
db_host="localhost"

DICPATH=/data/backup/$HOSTNAME
......
```



# 步骤
进入mysql安装的服务器里

加权限
```
[root@test-data-01 scripts]# pwd
/data/backup/scripts
[root@test-data-01 scripts]# chmod +x mysqldump_172.31.24.21_3306.sh
[root@test-data-01 scripts]# ll
-rwxr-xr-x 1 root root 1823 Jul 30 19:00 mysqldump_172.31.24.21_3306.sh
```

添加到定时任务，每天凌晨1点10分备份
```
10 1 * * *  /data/backup/scripts/mysqldump_172.31.24.21_3306.sh  > /dev/null 2>&1
```

# 结果展示
```
[root@test-data-01 test-data-01]# pwd
/data/backup/test-data-01
[root@test-data-01 test-data-01]# ll
drwxr-xr-x. 2 root root 12288 Aug  3 01:14 backup.1
drwxr-xr-x. 2 root root 12288 Aug  2 01:14 backup.2
drwxr-xr-x. 2 root root 12288 Aug  1 01:14 backup.3
drwxr-xr-x. 2 root root 12288 Jul 31 01:14 backup.4
drwxr-xr-x. 2 root root 12288 Jul 30 19:06 backup.5
drwxr-xr-x. 2 root root  4096 Dec  5  2019 backup.6
drwxr-xr-x. 2 root root  4096 Dec  5  2019 data
drwxr-xr-x. 2 root root  4096 Dec  5  2019 log
[root@test-data-01 test-data-01]# du -sh ./*
89M	./backup.1
89M	./backup.2
89M	./backup.3
89M	./backup.4
89M	./backup.5
491M	./backup.6
4.0K	./data
4.0K	./log
```


