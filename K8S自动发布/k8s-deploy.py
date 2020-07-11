#!/usr/bin/env python
#coding:utf-8
# @Author  : chenyu
# @Time    : 2020/5/18 10:21
# @Blog    : rugod.cn
import  os
import  sys
from datetime import datetime
import time
from collections import Counter 


def pods_upgrade_success(project):
     global kubectl_get_pods
     kubectl_images=[]
     #查看所有pods-id
     kubectl_get_pods=os.popen("kubectl get pods |grep %s|awk '{print $1}'"%project).read().split()
     for a in kubectl_get_pods:
           #查看每个容器的镜像号
           kubectl_describe_cmd=os.popen("kubectl describe pods %s |sed -n '/Image:/p' |awk '{print $2}'|cut -d ':' -f2"%a).read().split()
           if kubectl_describe_cmd:                  
                    kubectl_images.append(kubectl_describe_cmd[0])
     print Counter(kubectl_images)
     time.sleep(10) 
     return len(set(kubectl_images))
#查看滚动更新完成时间内日志
def pods_health(time_process,id):
     kubectl_log_cmd=os.popen("kubectl logs --since=%s   %s"%(time_process,id)).read()
     if "JVM running" in kubectl_log_cmd:
         print("%s 容器启动正常"%(id))
         return "yes"
     else:
         print("%s 容器启动异常"%(id))
         return "no"

def deploy(project):
    while True:
       if pods_upgrade_success(project)==1:
         #查看项目滚动更新是否完成
          kubectl_rollout_status=os.popen("kubectl rollout status deployment %s --watch=false | grep -ic waiting1"%project).read()
          if kubectl_rollout_status.strip()=="0":
              time_end=datetime.now()# 获得当前时间戳
              time_process=str((time_end-time_begin).seconds)+"s"   #将时间戳转换成秒
              num_error=0
              print("发布时间为%s,开始分析日志"%(time_process))
              for i in kubectl_get_pods:
                   if  pods_health(time_process, i)=="no":
                       num_error=num_error+1
          if num_error==0:
                  print("%s更新成功"%(project))
                  return 1
          else:
                  time_max_end=datetime.now()
                  time_max_begin_end=(time_max_end-time_begin).seconds
                  if time_max_begin_end<=600:
                          print("%s更新异常,一共有%s个容器更新异常,开始重试------"%(project,num_error))
                  else:
                          print("都10分钟了，还没发完，咋回事啊")
                          break


def upgrade(project):
     os.system('kubectl apply -f /opt/service/%s/prod-deploy.yaml' %project)
     print "开始滚动发布"+project+"项目"

if __name__ == "__main__":
     if len(sys.argv)==1:
         sys.exit(0)
     print("主函数开始执行")
     print("当前时间为"+time.strftime('%Y-%m-%d %H:%M:%S'))
     succ=[]
     for i in sys.argv:
         if i !='k8s-deploy.py' :
              time_begin = datetime.now() #获得当前时间戳
              upgrade(i) 
              time.sleep(5)
              if deploy(i)==1:
                    print "稍等片刻，休息一下" 
                    time.sleep(5) 
                    succ.append(i)
              else:
                    print ("%s项目发布失败，终止整个发布"%(i))
                    break
     if len(succ)+1==len(sys.argv):
            print "已经全部发布完成"       
     else:
            print "未完全发布,已经发布成功的项目为:"
            print succ
