#!/usr/bin/env python
#coding=UTF-8

import paramiko

class BasicRemoteCommand():

    #initial the ssh connection
    def __init__(self, ip_addr, username, password, ssh_port=22):
        self.ssh_connection = paramiko.SSHClient()
        self.ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            #initial connection
            self.ssh_connection.connect(ip_addr, ssh_port, username, password, timeout=5)
        except:
            print '尝试与目标ip地址连接时发生错误：(╯‵□′)╯︵┻━┻'
            raise
    #close ssh connection when calss delete
    def __del__(self):
        self.ssh_connection.close()

    def send_remote_cmd(self, command): 
        try:
            #put the result into three variable, that rescive from ssh server.
            stdin, stdout, stderr = self.ssh_connection.exec_command(command)
        except:
            print '远程执行命令列表时出现错误不知道为啥，╮(╯▽╰)╭'
            raise
        result = stdout.readlines()
        #Check the result from stdout,if stdout is null,
        #then put the stderr into result list.
        if result:
            return result
        else:
            return stderr.readlines()

#get the system information of remote server.    
class RemoteSystem():

    #initial the connection that use for getting system information.
    def __init__(self, ip_addr, username, password, ssh_port=22):
        self.connection = BasicRemoteCommand(ip_addr, username, password, ssh_port)
        #init all the system information, easy to call
        self.system_release = self.get_release()
        self.system_server_list = self.get_chkconfig()
        self.system_selinux_status = self.get_selinux()
        self.system_ip_forward_status = self.get_ip_forward_status()
        self.system_iptables_status = self.get_iptables_status()
        #self.system_ip_addrs = self.get_ip_list()
        self.system_hostname = self.get_hostname()

    #get remote server system release
    def get_release(self):
        cmd = 'cat /etc/issue'
        system_release = self.connection.send_remote_cmd(cmd)
        system_release = system_release[0].split('\\')[0].strip()
        return system_release

    #get network status
    def get_network_status(self):
        #init a emty list to put the dev name and ip addrs
        network_status = {}

        #get the dev name, first.
        cmd = 'ip -o link | cut -d " " -f 2 | sed "s/://g"'
        dev_list = self.connection.send_remote_cmd(cmd)
        #remove '\n'
        dev_list = [dev.strip('\n') for dev in dev_list]

        #get the dev's network information.
        for dev_name in dev_list:
            dev_status = self.enforce_dev(dev_name)
            network_status[dev_name] = dev_status

        return network_status

    #return a dev's information about ip addr, hardward addr, adapter type...
    def enforce_dev(self, dev_name):
        dev_info = {}
        ip_list = []
        mac_addr = None
        adapter_type = None
        status = None #mark up or down?
        mtu = None
        speed = None
        
        #get information from remote server
        cmd = 'ip addr show ' + dev_name + '| grep -v inet6 | grep -v valid_lft'
        original_info = self.connection.send_remote_cmd(cmd)
        
        #remove all the '\n' and space in list
        original_info = [tmp_info.strip('\n').strip() for tmp_info in original_info]
        #want to pop the list, so list has reversaled.
        original_info.reverse()

        #split the first line, that de base information about dev.
        base_info = original_info.pop().split()

        #if 5th string is a number, then it is the value of mtu.
        try:
            mtu = int(base_info[4])
        except ValueError:
            pass
        dev_info['mtu'] = mtu

        #if 9th string is not UP or DOWN or UNKNOWN, then not the true value.
        if base_info[8].upper() in ['UP', 'DOWN', 'UNKNOWN']:
            status = base_info[8]
        dev_info['status'] = status

        #if 13th string is a number, it is the value of speed.
        try:
            speed = int(base_info[12])
        except (ValueError, IndexError):
            pass
        dev_info['speed'] = speed

        #the hardware addr in 2nd line of original_info, get it.
        mac_addr = original_info.pop().split()[1]
        dev_info['mac'] = mac_addr

        #pop the last thing in the list,get the ip addrs now
        while len(original_info) != 0:
            ip_addr = original_info.pop().split()[1]
            ip_list.append(ip_addr)
        dev_info['ip'] = ip_list

        return dev_info


    #get system chkconfig list
    def get_chkconfig(self):
        cmd = 'chkconfig --list'
        list = self.connection.send_remote_cmd(cmd)
        return list

    #get selinux status
    def get_selinux(self):
        cmd = '/usr/sbin/sestatus -v'
        status = self.connection.send_remote_cmd(cmd)
        return status

    #get ip forward status
    def get_ip_forward_status(self):
        cmd = 'cat /proc/sys/net/ipv4/ip_forward'
        status = self.connection.send_remote_cmd(cmd)
        status = status[0].strip()
        return status

    #get hostname status
    def get_hostname(self):
        cmd = 'uname -n'
        hostname = self.connection.send_remote_cmd(cmd)
        hostname = hostname[0].strip()
        return hostname

    #get iptables status
    def get_iptables_status(self):
        cmd = 'service iptables status'
        status = self.connection.send_remote_cmd(cmd)
        status = status[0].strip()
        return status
