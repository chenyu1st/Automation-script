#!/usr/bin/env python
# -*-coding:utf-8-*-
import yagmail 
import os
import sys
import time
import sys
from dingtalkchatbot.chatbot import DingtalkChatbot



_node_top = os.popen('/opt/top/pods_top.sh')
_node_status_ = _node_top.read()
#print(_node_status_)

mail = yagmail.SMTP("xxx@qq.com","passwd","smtp.qq.com",465)
word = "_node_status_"
mail.send(["xxx@qq.com","xxx@qq.com"],"K8S资源使用情况",word)

webhook = ''
xiaoding = DingtalkChatbot(webhook)

xiaoding.send_text(msg=_node_status_)
