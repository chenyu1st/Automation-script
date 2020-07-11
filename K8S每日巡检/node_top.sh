#!/bin/bash

G_Mem=`kubectl top nodes |  awk '{print $5}'`

Top_Sum=`kubectl top nodes | grep -v MEM | sed  's/%//g' |  awk '{print $5}' |  awk '{sum+=$1}END{print sum}'`
Cput_Sum=`kubectl top nodes | grep -v MEM | sed  's/%//g' |  awk '{print $3}' |  awk '{cpusum+=$1}END{print cpusum}'`
B_Sum=`kubectl top nodes | grep -v MEM | wc -l`


Cfb=`expr $Cput_Sum / $B_Sum`
Bfb=`expr $Top_Sum / $B_Sum`



echo -e "数据统计时间 `date "+%Y-%m-%d %H:%M:%S"` \n" 
kubectl top nodes
echo -e " \n"
echo -e "K8S Node节点数量为 $B_Sum台 "
echo -e "内存平均负载为$Top_Sum/$B_Sum=$Bfb% "
echo -e "cpu平均负载为$Cput_Sum/$B_Sum=$Cfb% "
