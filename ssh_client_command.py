#!/usr/bin/env python
#coding=UTF-8

import commands 
import pprint

#log formating
def format_log(title, log_message):
    print '##############################'
    print title
    print(log_message)

if __name__=='__main__':
    cmd = 'ip addr show'
    ip = '127.0.0.1'
    port = 2222
    username = 'lenovo'
    password = 'lenovopassword'
    print '程序开始执行.......'
    test = "获取远端操作系统版本信息"
    server = commands.RemoteSystem(ip, username, password, port)
    
#    format_log("端操作系统版本信息", server.system_release)
#
#    format_log('远端服务列表', server.system_server_list)
#
#    format_log('selinux状态', server.system_selinux_status)
#
#    format_log('ip转发状态', server.system_ip_forward_status)
#
#    format_log('防火墙状态', server.system_iptables_status)
#
#    print "主机名"
#    print server.system_hostname
#    print "处理ip地址"
#    pprint.pprint(server.get_network_status())
    pprint.pprint(server.get_network_status())
