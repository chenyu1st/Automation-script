# 环境
使用python2.7 即linux自带python版本

不知道pip的自行百度安装

安装python SDK

pip install DingtalkChatbot 

pip install yagmail

# 添加钉钉告警机器人
在钉钉群里添加一个自定义机器人Webhook

将 Webhook 地址添加到monitor.py中

```
webhook = ''
```

# 定时任务
将脚本到一个文件夹,将monitor.py加入到定时任务


```
[root@localhost ~]#crontab -e

0 10 * * *  $HOME/.bash_profile;/usr/bin/python /opt/top/monitor.py
```

# 参考文档

[获取自定义机器人webhook](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)

[python自动发邮件库yagmail](https://www.cnblogs.com/fnng/p/7967213.html)

