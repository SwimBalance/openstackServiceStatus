#!/usr/bin/python
#-*- coding: UTF-8 -*- 
#coding=utf-8
import MySQLdb;
import os, sys,string;
import cgi,cgitb;
import ConfigParser


print "Content-Type: text/html; charset=utf-8"

print ""
print('<html>')  
print('<head>')  
print('<meta http-equiv="refresh" content="10">')  
print('<title>chinac openstack service check</title>')
print("<style type='text/css'>* {margin: 0px;padding: 0px;} .top{  width: 90%;background-color: #B2D3F5;  height: 80px;  margin: 0px auto;  margin-bottom:10px;  border:1px solid #96C2F1;  background-color: #EFF7FF } .top h5{margin: 1px;background-color: #B2D3F5;  height: 38;font-size: 25px;padding-top:10px;padding-bottom:10px;} .top h3{margin: 1px;background-color: #B2D3F5;  height: 30px;font-size: px;padding-left: 150px;padding-top:1px;} .content {  width: 90%;  margin: 0px auto;  margin-bottom:10px;  border:1px solid #92B0DD;  background-color: #FFFFFf}  .content h5{  margin: 1px;  background-color: #E2EAF8;  height: 25px;} </style>")

print ("<style type='text/css'> table.t1 {border:1px solid #cad9ea;color:#666;} table.t1 th {background-image: url (th_bg1.gif);background-repeat::repeat-x;height:30px;} table.t1 td,table.t1 th{border:1px solid #cad9ea;padding:0 1em 0;} table.t1 tr.a1{background-color:#f5fafe;} </style>")


print('</head>')  
#print "<style type='text/css'> p {color:black;background:#CCFFFF;} </style>"
print('<body>')
#----------------------------------------------
cf = ConfigParser.ConfigParser()
cf.read('/var/www/cgi-bin/database.ini')

conn= MySQLdb.connect(
        host=cf.get("mysqlConfig", "host"),
        port = int(cf.get("mysqlConfig", "port")),
        user=cf.get("mysqlConfig", "user"),
        passwd=cf.get("mysqlConfig", "passwd"),
        db =cf.get("mysqlConfig", "dbname"),
        charset=cf.get("mysqlConfig", "charset")
        )
'''
conn= MySQLdb.connect(
        host='192.168.35.66',
        port = 3306,
        user='hiiservice',
        passwd='hiiservice',
        db ='openstackService',
        charset='utf8'
        )
'''
#-------------------------------------------------------
cur = conn.cursor()
#----------------------------------------------
print '<div class="top">'
print   ' <h5>Chinac: CU Service Status</h5>'
print "</div>"
print ' <div class="content">'
print "    <h5>集群信息：</h5>"
print '    <div id="contentfoot" >'
#--------------------------------------------------------------
#clusterinfo
print "<table id=mytab  border=1 class='t1' width='100%' >"
print   "<tr>"
print           " <th bgcolor=#E2EAF8>集群名称</th>"
print           " <th bgcolor=#E2EAF8>HA集群</th>"
print           " <th bgcolor=#E2EAF8>底层版本</th>"
print		" <th bgcolor=#E2EAF8>CU版本</th>"
print           " <th bgcolor=#E2EAF8>项目时间</th>"
print		"<th bgcolor=#E2EAF8>更新状态</th>"
print           " <th bgcolor=#E2EAF8>NeoCU地址</th>"
print   "</tr>"
#------------------------------------------
result = cur.execute("select id,name,haType,openstackVersion,cuVersion,updateTime,groupURL from clusterinfo")
records = cur.fetchmany(result)
for record in records:
	print "<tr>"
	print "<td>%s</td>" % (record[1])
	print "<td>"+ record[2] +"</td>"
	print "<td>"+ record[3] +"</td>"
	print "<td>"+ record[4] +"</td>"
	print "<td>"+ record[5] +"</td>"
	print "<td><a href='http://10.0.20.1/cgi-bin/plan.py' target='_blank' >更新状态</a></td>"
	print '<td><a target="_blank" href="'+ record[6] +'">Open</a></td>"'
	print "</tr>"

print "</table>"
print "<h5>角色架构信息</h5>"
#==================================================================
# host roles
print "<table id=mytab  border=1 class='t1' width='100%' >"
print   "<tr>"
print           " <th bgcolor=#E2EAF8>主机名</th>"
print           " <th bgcolor=#E2EAF8>管理IP</th>"
print           " <th bgcolor=#E2EAF8>安装角色</th>"
print           " <th bgcolor=#E2EAF8>状态</th>"
print           " <th bgcolor=#E2EAF8>OS版本</th>"
print           " <th bgcolor=#E2EAF8>运行时间</th>"
#print           " <th bgcolor=#E2EAF8>打开平台</th>"
print   "</tr>"
#--------------------------------------------------------------
result = cur.execute("select DISTINCT hostIP,hostname,allRoles,status,os,weburl,uptime  from hostSchema ORDER BY hostIP ")
records = cur.fetchmany(result)
for record in records:
	print "<tr>"
	print "<td>"+ record[1] +"</td>"
	print "<td>"+ record[0] +"</td>"
	print "<td>"+ record[2] +"</td>"
	if  ( record[3] == "Running" ):
                print "<td  bgcolor=#3cb371 >"+ record[3] +"</td>"
        else :
                print "<td  bgcolor=#FF6666 >"+ record[3] +"</td>"
	print "<td>"+ record[4] +"</td>"
	print "<td>"+ record[6] +"</td>"
#	print '<td><a target="_blank" href="'+ record[5] +'">open</a></td>'
	print "</tr>"


print "</table>"
print "<h5>异常服务信息</h5>"
#--------------------------------------------------------------
#===================================================================
# 异常服务
print "<table id=mytab  border=1 class='t1' width='100%' >"
print 	"<tr>"
print           " <th bgcolor=#E2EAF8>主机名</th>"
print           " <th bgcolor=#E2EAF8>管理IP</th>"
print           " <th bgcolor=#E2EAF8>服务名</th>"
print           " <th bgcolor=#E2EAF8>所属角色</th>"
print           " <th bgcolor=#E2EAF8>高可用</th>"
#print           " <th bgcolor=#E2EAF8>进程ID</th>"
print           " <th bgcolor=#E2EAF8>状态</th>"
print           " <th bgcolor=#E2EAF8>检测时间</th>"
print           " <th bgcolor=#E2EAF8>异常建议</th>"
print   "</tr>"
#--------------------------------------------------------------
#strcmd="select * from serviceStatus where status='Error' or status='Stopped' or status='Unknown' ORDER BY hostName"
result = cur.execute("select * from serviceStatus where status != 'Running' ORDER BY hostIP ")
records = cur.fetchmany(result)
for record in records:
        print "<tr>"
        print "<td>"+ record[0] +"</td>"
        print "<td>"+ record[1] +"</td>"
        print "<td>"+ record[2] +"</td>"
        print "<td>"+ record[3] +"</td>"
	print "<td>"+ record[4] +"</td>"
#        print "<td>"+ record[7] +"</td>"
	if  ( record[5] == "Error" ):
		print "<td  bgcolor=#FF6666 >"+ record[5] +"</td>"
	else :
		print "<td  bgcolor=#Ff9900 >"+ record[5] +"</td>"
	print "<td>"+ record[6] +"</td>"
	print "<td>"
	print	record[8] 
	print	"</td>"
        print "</tr>"

print "</table>"
print "<h5>所有服务信息</h5>"
#--------------------------------------------------------------
#所有服务状态
#===================================================================
print "<table id=mytab  border=1 class='t1' width='100%' >"
print   "<tr>"
print           " <th bgcolor=#E2EAF8>主机名</th>"
print           " <th bgcolor=#E2EAF8>管理IP</th>"
print           " <th bgcolor=#E2EAF8>服务名</th>"
print           " <th bgcolor=#E2EAF8>所属角色</th>"
print           " <th bgcolor=#E2EAF8>高可用</th>"
print           " <th bgcolor=#E2EAF8>进程ID</th>"
print           " <th bgcolor=#E2EAF8>状态</th>"
print           " <th bgcolor=#E2EAF8>检测时间</th>"
print           " <th bgcolor=#E2EAF8>软件包版本</th>"
#print           " <th bgcolor=#E2EAF8>异常建议</th>"
print   "</tr>"
#--------------------------------------------------------------
result = cur.execute("select * from serviceStatus  ORDER BY hostIP ")
records = cur.fetchmany(result)
hostname = "controller01"
for record in records:
	if ( hostname != record[0] ):
                print "<tr><td height='20px'  bgcolor=#B9D3EE colspan='8'></td></tr>"
                hostname = record[0]
        print "<tr>"
        print "<td>"+ record[0] +"</td>"
        print "<td>"+ record[1] +"</td>"
        print "<td>"+ record[2] +"</td>"
        print "<td>"+ record[3] +"</td>"
        print "<td>"+ record[4] +"</td>"
        print "<td>"+ record[7] +"</td>"
	if    ( record[5] == "Running"):
		print "<td  bgcolor=#3cb371 >"+ record[5] +"</td>"
        elif  ( record[5] == "Error" ):
                print "<td  bgcolor=#FF6666 >"+ record[5] +"</td>"
        else :
                print "<td  bgcolor=#Ff9900 >"+ record[5] +"</td>"
        print "<td>"+ record[6] +"</td>"
	print "<td>"+ record[11] +"</td>"
        #print "<td>"
        #print   record[7] 
        #print   "</td>"
        print "</tr>"

print "</table>"
print "<h5></h5>"
#--------------------------------------------------------------
print "    </div>"
print "</div>"
#-----------------------------------------------
cur.close()
print "</body></html>"


