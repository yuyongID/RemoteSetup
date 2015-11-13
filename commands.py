#!/usr/bin/env python
#coding=UTF-8

import paramiko
import os

class BasicRemoteCommand():

    #initial the ssh connection
    def __init__(self, ip_addr, username, password, ssh_port=22):
        self.ip_addr = ip_addr
        self.username = username
        self.password = password
        self.ssh_port =ssh_port
        self.ssh_connection = paramiko.SSHClient()
        self.ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            #initial ssh connection
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

    #initial a sftp connection.
    def init_sftp_connection(self):
        self.sftp_base = paramiko.Transport((self.ip_addr, self.ssh_port))
        try:
            self.sftp_base.connect(username=self.username, password=self.password)
        except:
            print '创建sftp链接的时候失败了，为啥捏?(⊙o⊙)…'
            raise
        sftp_connection = paramiko.SFTPClient.from_transport(self.sftp_base)
        return sftp_connection

    #stop a sftp connection.
    def stop_sftp_connection(self):
        try:
            self.sftp_base.close()
        except:
            print '关闭sftp链接失败，+_+'
            raise

    #download file to server by sftp.
    def download_file(self, file):
        sftp = self.init_sftp_connection()
        try:
            sftp.get(file, os.path.basename(file))
        except:
            print '尝试下载文件的时候失败了，为啥捏？'
            raise
        self.stop_sftp_connection()

     #upload file to server by sftp.
    def upload_file(self, file):
        sftp = self.init_sftp_connection()
        try:
            sftp.put(os.path.basename(file), file)
        except:
            print '尝试上传文件的时候失败了，为啥捏？'
            raise
        self.stop_sftp_connection()

#get the system information of remote server.    
class RemoteSystem():

    #initial the connection that use for getting system information.
    def __init__(self, ip_addr, username, password, ssh_port=22):
        self.connection = BasicRemoteCommand(ip_addr, username, password, ssh_port)
        #init all the system information, easy to call
        self.system_release = self.get_release()
        self.system_selinux = self.get_selinux()
        self.system_ip_forward = self.get_ip_forward()
        self.system_iptables = self.get_iptables()
        self.system_hostname = self.get_hostname()

    #get remote server system release
    def get_release(self):
        cmd = 'cat /etc/issue'
        system_release = self.connection.send_remote_cmd(cmd)
        system_release = system_release[0].split('\\')[0].strip()
        return system_release

    #get network status
    def get_network(self):
        #init a emty list to put the imformation of networking.
        network_status = {}

        #get the dev name, first.
        cmd = 'ip -o link | cut -d " " -f 2 | sed "s/://g"'
        dev_list = self.connection.send_remote_cmd(cmd)
        #remove '\n'
        dev_list = [dev.strip('\n') for dev in dev_list]

        #get all the dev's network information, that in dev_list.
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
        status = None #mark dev up or down?
        mtu = None
        speed = None
        
        #get information from remote server
        cmd = 'ip addr show ' + dev_name + '| grep -v inet6 | grep -v valid_lft'
        original_info = self.connection.send_remote_cmd(cmd)
        
        #remove all the '\n' and space in list
        original_info = [tmp_info.strip('\n').strip() for tmp_info in original_info]

        for base_info in original_info:

            if 'mtu' in base_info:
                #if 5th string is a number, then it is the value of mtu.
                try:
                    mtu = int(base_info.split()[4])
                except ValueError:
                    pass
                dev_info['mtu'] = mtu

                #if 9th string is not UP or DOWN or UNKNOWN, then not the true value.
                if base_info.split()[8].upper() in ['UP', 'DOWN', 'UNKNOWN']:
                    status = base_info.split()[8]
                dev_info['status'] = status

                #if 11th string is a number, it is the value of speed.
                try:
                    speed = int(base_info.split()[10])
                except (ValueError, IndexError):
                    pass
                dev_info['speed'] = speed

            #the hardware addr in line of base_info, get it.
            if "link/ether" in base_info or "link/loopback" in base_info:
                mac_addr = base_info.split()[1]
                dev_info['mac'] = mac_addr

            #if 'inet' in the line,get the ip addrs now
            if 'inet' in base_info:
                ip_addr = base_info.split()[1]
                try:
                    name = base_info.split()[6]
                except IndexError:
                    name = None
                ip_list.append((name, ip_addr))
            dev_info['ip'] = ip_list

        return dev_info

    #get system chkconfig list
    def get_chkconfig(self):
        chkconfig_list = {}
        #get system yun level first.
        cmd = 'runlevel | cut -d " " -f 2'
        run_level = int(self.connection.send_remote_cmd(cmd)[0])
        #get server list
        cmd = 'chkconfig --list | sed "s/\t/ /g"'
        original_list = self.connection.send_remote_cmd(cmd)
        original_list = [tmp_line.strip('\n') for tmp_line in original_list]
        
        #pick up service name and status in chkconfig list, in this running level.
        while len(original_list) != 0:
            tmp_line = original_list.pop().split()
            name = tmp_line[0]
            status = tmp_line[run_level+1].split(':')[1]
            chkconfig_list[name] = status
        return chkconfig_list

    #get selinux status
    def get_selinux(self):
        cmd = 'getenforce'
        status = self.connection.send_remote_cmd(cmd)
        status = status[0].strip('\n')
        return status

    #get ip forward status
    def get_ip_forward(self):
        cmd = 'cat /proc/sys/net/ipv4/ip_forward'
        status = self.connection.send_remote_cmd(cmd)
        status = status[0].strip()
        return status

    #get hostname 
    def get_hostname(self):
        cmd = 'uname -n'
        hostname = self.connection.send_remote_cmd(cmd)
        hostname = hostname[0].strip()
        return hostname

    #get iptables status
    def get_iptables(self):
        cmd = 'service iptables status'
        status = self.connection.send_remote_cmd(cmd)
        status = status[0].strip()
        if 'not running' in status:
            return 'not running'
        return 'running'

    #get route tables
    def get_route(self):
        route_tables = {}
        kernel_route = []
        statick_route = []
        cmd = 'ip route show | grep -v "metric" '
        original_tables = self.connection.send_remote_cmd(cmd)
        original_tables = [line.strip('\n').strip() for line in original_tables]

        for route_info in original_tables:

            if 'proto kernel' in route_info:
                route_info = route_info.split()
                route, dev, src = route_info[0], route_info[2], route_info[8]
                kernel_route.append((route, dev, src))

            if 'via' in route_info:
                route_info = route_info.split()
                route, dev, via = route_info[0], route_info[4], route_info[2]
                statick_route.append((route, dev, via))

        route_tables['kernel'] = kernel_route
        route_tables['static'] = statick_route
        return route_tables

    #change selinux status
    def change_selinu(self, status):
        #check status
        if status.lower() not in ['enforcing', 'permissive', 'disabled']:
            return 1

        cmd = 'sed -i "s/^SELINUX=.*/SELINUX='\
                + status.lower()\
                + '/" /etc/selinux/config'
        result = self.connection.send_remote_cmd(cmd)
        if result:
            #format the result, in case result has more than one line.
            result = [tmp.strip('\n') for tmp in result]
            print '设置selinux失败'
            for tmp in result:
                print tmp
            return 1
        return 0
        
    #change chkconfig
    def change_chkconfig(self, name, status):
        #check status
        if status.lower() not in ['off', 'on']:
            return 1

        cmd = 'chkconfig ' + name + ' ' + status.lower()
        result = self.connection.send_remote_cmd(cmd)
        #if result has some text, it means that cmd return fail.
        if result:
            print name + '设置失败'
            return 1
        return 0

    #control the system service
    def change_system_service(self, name, control):
        #check control
        if control.lower() not in ['start', 'stop']:
            return 1

        cmd = 'service ' + name + ' ' + control.lower()
        result = self.connection.send_remote_cmd(cmd)
        #if result has this text, it means that cmd return fail.
        if 'unrecognized service' in result[0]:
            print name + ' 设置失败:未被识别的服务'
            print result
            return 1
        return 0

    #change the system ip forward
    def change_ip_forward(self, control):
        #check control
        if control not in ['1', '0']:
            return 1

        cmd = 'echo "' + control + '" > /proc/sys/net/ipv4/ip_forward'
        result = self.connection.send_remote_cmd(cmd)
        #if result has some text, it means that cmd return fail.
        if result:
            print 'ip转发设置失败:未被识别的服务'
            print result
            return 1

        cmd = 'sed -i "s/ip_forward = ./ip_forward = '\
            + control\
            + '/" /etc/sysctl.conf'
        result = self.connection.send_remote_cmd(cmd)
        #if result has some text, it means that cmd return fail.
        if result:
            print 'ip转发设置失败:未被识别的服务'
            print result
            return 1
        return 0

    #change network confige
    def save_new_network(self, dev_name, ip_addr, netmask, mac_addr):
        config_part1 = 'DEVICE="' + dev_name + '"\n'
        config_part2 = 'BOOTPROTO="static"\n'
        config_part3 = 'IPADDR="' + ip_addr + '"\n'
        config_part4 = 'NETMASK="' + netmask + '"\n'
        config_part5 = 'HWADDR="' + mac_addr + '"\n'
        config_part6 = 'ONBOOT="yes"\nTYPE="Ethernet"'
        config = config_part1 + config_part2 + config_part3\
                + config_part4 + config_part5 + config_part6
        cmd = 'echo -e \'' + config\
                + '\'>/etc/sysconfig/network-scripts/ifcfg-' \
                + dev_name 
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '保存网络配置失败'
            return 1
        return 0

    #change a ip address provisional.
    def change_ip_addr(self, dev_name, ip_addr, netmask):
        cmd = 'ifconfig ' + dev_name + ' ' + ip_addr\
                + ' netmask ' + netmask
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '修改ip地址失败'
            return 1
        return 0

    #delete a ip address provisional.
    def delete_ip_addr(self, dev_name, ip_addr, netmask):
        cmd = 'ip addr delete ' + ip_addr + '/'\
                + netmask + ' dev ' + dev_name
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '删除ip地址失败'
            return 1
        return 0

    #add a static route provisional.
    def add_static_route(self, net, netmask, gatewate):
        cmd = 'ip route add ' + net + '/'\
                + netmask + ' via ' + gatewate
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '添加路由失败'
            return 1
        return 0

    #delete a static route provisional.
    def delete_static_route(self, net, netmask, gatewate):
        cmd = 'ip route delete ' + net + '/'\
                + netmask + ' via ' + gatewate
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '删除路由失败'
            return 1
        return 0

