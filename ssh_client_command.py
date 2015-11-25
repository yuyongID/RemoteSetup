#!/usr/bin/env python
# coding=UTF-8

import commands
import pprint

# log formating


def format_log(title, log_message):
    print '##############################'
    print title
    pprint.pprint(log_message)

if __name__ == '__main__':
    cmd = 'ip addr show'
    ip = '127.0.0.1'
    port = 2222
    username = 'lenovo'
    password = 'lenovopassword'
    print '程序开始执行.......'
    test = "获取远端操作系统版本信息"

    server = commands.RemoteSystem(ip, username, password, port)
    print server.get_dev_bytes('eth0')
#    print server.get_memory_used()
#    format_log("端操作系统版本信息", server.system_release)
#    format_log('selinux状态', server.system_selinux)
#    format_log('ip转发状态', server.system_ip_forward)
#    format_log('防火墙状态', server.system_iptables)
#    print "主机名"
#    print server.get_hostname()
#    print "处理ip地址"
#    pprint.pprint(server.get_network())
#    print '服务列表'
 #   pprint.pprint(server.get_chkconfig())
#    print '路由表'
#    pprint.pprint(server.get_route())
#    server.change_ip_addr('eth1:9', '9.9.9.9/255.0.0.0')
#    server = commands.BasicRemoteCommand(ip, username, password)
#    server.download_file('/tmp/123.txt')
#    server.change_selinux_status('disabled')
#    server.change_chkconfig('ip6tables', 'off')
#    server.change_ip_forward('1')
#    server.save_new_network('eth1:1', '192.168.1.124/255.255.255.0', '08:00:27:EC:39:C1')
#    server.save_new_network('eth1:1', '192.168.1.124/16' )
#    server.change_ip_addr('eth1:9', '192.168.9.124/24')
#    result = server.add_static_route('170.5.2.0/24', '192.168.0.123')
#    pprint.pprint(server.get_route())
#    result = server.delete_static_route('170.5.2.0/255.255.255.0', '192.168.0.123')
#    pprint.pprint(server.get_route())
#    server.delete_static_route('170.5.1.0', '255.255.255.0', '192.168.1.123')
#    pprint.pprint(server.get_route())
#    server.delete_netwok_config('eth3')
#    print server.netmask_to_CIDR('255.255.0.0')
#    print server.CIDR_to_netmask('24')
#    print ''.join(server.get_hosts())
 #   server.change_hosts('')
 #   print server.get_time()
#    pprint.pprint(server.get_hard_disk_used())
#    print '路由表'
#    pprint.pprint(server.get_route())
#    server.change_ip_addr('eth1:9', '9.9.9.9/255.0.0.0')
    #server = commands.BasicRemoteCommand(ip, username, password)
    # server.download_file('/tmp/123.txt')
#    server.change_selinu_status('disabled')
    #server.change_chkconfig('ip6tables', 'off')
#    server.change_ip_forward('1')
    #server.save_new_network('eth1:1', '192.168.1.124/255.255.255.0', '08:00:27:EC:39:C1')
#    server.save_new_network('eth1:1', '192.168.1.124/16' )
    # server.change_ip_addr('eth1:9', '192.168.9.124/24')
    #result = server.add_static_route('170.5.2.0/24', '192.168.0.123')
    #pprint.pprint(server.get_route())
    #result = server.delete_static_route('170.5.2.0/255.255.255.0', '192.168.0.123')
    #pprint.pprint(server.get_route())
#    server.delete_static_route('170.5.1.0', '255.255.255.0', '192.168.1.123')
#    pprint.pprint(server.get_route())
#    server.delete_netwok_config('eth3')
    # print server.netmask_to_CIDR('255.255.0.0')
    # print server.CIDR_to_netmask('24')
