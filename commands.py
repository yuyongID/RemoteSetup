#!/usr/bin/env python
# coding=UTF-8

import paramiko
import os


class BasicRemoteCommand():

    # initial the ssh connection
    def __init__(self, ip_addr, username, password, ssh_port=22):
        self.ip_addr = ip_addr
        self.username = username
        self.password = password
        self.ssh_port = ssh_port
        self.ssh_connection = paramiko.SSHClient()
        self.ssh_connection.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        try:
            # initial ssh connection
            self.ssh_connection.connect(
                ip_addr, ssh_port, username, password, timeout=5)
        except:
            print '尝试与目标ip地址连接时发生错误：(╯‵□′)╯︵┻━┻'
            raise

    # close ssh connection when calss delete
    def __del__(self):
        self.ssh_connection.close()

    def send_remote_cmd(self, command):
        try:
            # put the result into three variable, that rescive from ssh server.
            stdin, stdout, stderr = self.ssh_connection.exec_command(command)
        except:
            print '远程执行命令列表时出现错误不知道为啥，╮(╯▽╰)╭'
            raise
        result = stdout.readlines()
        # Check the result from stdout,if stdout is null,
        # then put the stderr into result list.
        if result:
            return result
        else:
            return stderr.readlines()

    # initial a sftp connection.
    def init_sftp_connection(self):
        self.sftp_base = paramiko.Transport((self.ip_addr, self.ssh_port))
        try:
            self.sftp_base.connect(
                username=self.username, password=self.password)
        except:
            print '创建sftp链接的时候失败了，为啥捏?(⊙o⊙)…'
            raise
        sftp_connection = paramiko.SFTPClient.from_transport(self.sftp_base)
        return sftp_connection

    # stop a sftp connection.
    def stop_sftp_connection(self):
        try:
            self.sftp_base.close()
        except:
            print '关闭sftp链接失败，+_+'
            raise

    # download file to server by sftp.
    def download_file(self, file):
        sftp = self.init_sftp_connection()
        try:
            sftp.get(file, os.path.basename(file))
        except:
            print '尝试下载文件的时候失败了，为啥捏？'
            raise
        self.stop_sftp_connection()

     #  upload file to server by sftp.
    def upload_file(self, file):
        sftp = self.init_sftp_connection()
        try:
            sftp.put(os.path.basename(file), file)
        except:
            print '尝试上传文件的时候失败了，为啥捏？'
            raise
        self.stop_sftp_connection()

# get the system information of remote server.


class RemoteSystem():

    # initial the connection that use for getting system information.
    def __init__(self, ip_addr, username, password, ssh_port=22):
        self.connection = BasicRemoteCommand(
            ip_addr, username, password, ssh_port)
        # init all the system information, easy to call
        self.system_release = self.get_release()
        self.system_selinux = self.get_selinux()
        self.system_ip_forward = self.get_ip_forward()
        self.system_iptables = self.get_iptables()
        self.system_hostname = self.get_hostname()

    # get remote server system release
    def get_release(self):
        cmd = 'cat /etc/issue'
        system_release = self.connection.send_remote_cmd(cmd)
        system_release = system_release[0].split('\\')[0].strip()
        return system_release

    # get network status
    def get_network(self):
        # init a emty list to put the imformation of networking.
        network_status = {}
        # get the dev name, first.
        cmd = 'ip -o link | cut -d " " -f 2 | sed "s/://g"'
        dev_list = self.connection.send_remote_cmd(cmd)
        # remove '\n'
        dev_list = [dev.strip('\n') for dev in dev_list]
        # get all the dev's network information, that in dev_list.
        for dev_name in dev_list:
            dev_status = self.enforce_dev(dev_name)
            network_status[dev_name] = dev_status
        return network_status

    # return a dev's information about ip addr, hardward addr, adapter type...
    def enforce_dev(self, dev_name):
        dev_info = {}
        ip_list = []
        mac_addr = None
        status = None  # mark dev up or down?
        mtu = None
        speed = None
        # get information from remote server
        cmd = 'ip addr show ' + \
            dev_name + \
            '| grep -v inet6 | grep -v valid_lft'
        original_info = self.connection.send_remote_cmd(cmd)
        # remove all the '\n' and space in list
        original_info = [
            tmp_info.strip('\n').strip() for tmp_info in original_info
        ]

        for base_info in original_info:

            if 'mtu' in base_info:
                # if 5th string is a number, then it is the value of mtu.
                try:
                    mtu = int(base_info.split()[4])
                except ValueError:
                    pass
                dev_info['mtu'] = mtu

                # if 9th string is not UP or DOWN or UNKNOWN, then not the true
                # value.
                if base_info.split()[8].upper() in ['UP', 'DOWN', 'UNKNOWN']:
                    status = base_info.split()[8]
                dev_info['status'] = status

                # if 11th string is a number, it is the value of speed.
                try:
                    speed = int(base_info.split()[10])
                except (ValueError, IndexError):
                    pass
                dev_info['speed'] = speed

            # the hardware addr in line of base_info, get it.
            if "link/ether" in base_info or "link/loopback" in base_info:
                mac_addr = base_info.split()[1]
                dev_info['mac'] = mac_addr

            # if 'inet' in the line,get the ip addrs now
            if 'inet' in base_info:
                ip_addr = base_info.split()[1]
                try:
                    name = base_info.split()[6]
                except IndexError:
                    name = None
                ip_list.append((name, ip_addr))
            dev_info['ip'] = ip_list

        return dev_info

    # get dev Receive and Transmit bytes
    def get_dev_bytes(self, dev_name):
        cmd = "cat /proc/net/dev | grep " + dev_name + " | awk '{print $2, $10}' "
        result = self.connection.send_remote_cmd(cmd)[0].strip('\n')
        receive_bytes, transmit_bytes = result.split()
        return receive_bytes, transmit_bytes

    # get system chkconfig list
    def get_chkconfig(self):
        chkconfig_list = []
        xinetd_list = []
        # get system yun level first.
        cmd = 'runlevel | cut -d " " -f 2'
        run_level = int(self.connection.send_remote_cmd(cmd)[0])
        # get server list
        cmd = 'chkconfig --list | sed "s/\t/ /g"'
        original_list = self.connection.send_remote_cmd(cmd)
        original_list = [tmp_line.strip('\n') for tmp_line in original_list]
        # pick up service name and status in chkconfig list, in this running
        # level.
        for tmp_line in original_list:
            tmp_line = tmp_line.split()
            # if it has 8 parts, it means this is a service line
            if len(tmp_line) == 8:
                # the 1st part must be a service name
                name = tmp_line[0]
                status = tmp_line[run_level + 1].split(':')[1]
                chkconfig_list.append((name, status))
            # if it has 2 parts, i put them into xinetd list.
            elif len(tmp_line) == 2:
                # the 1st part must be a service name
                name = tmp_line[0]
                status = tmp_line[1]
                xinetd_list.append((name, status))
            else:
                continue
        return chkconfig_list, xinetd_list

    # get selinux status
    def get_selinux(self):
        cmd = 'grep "^SELINUX=" /etc/selinux/config | cut -d "=" -f2'
        status = self.connection.send_remote_cmd(cmd)
        status = status[0].strip('\n')
        return status

    # get ip forward status
    def get_ip_forward(self):
        cmd = 'cat /proc/sys/net/ipv4/ip_forward'
        status = self.connection.send_remote_cmd(cmd)
        status = status[0].strip()
        return status

    # get hostname
    def get_hostname(self):
        cmd = 'uname -n'
        hostname = self.connection.send_remote_cmd(cmd)
        hostname = hostname[0].strip()
        return hostname

    # get iptables status
    def get_iptables(self):
        cmd = 'service iptables status'
        status = self.connection.send_remote_cmd(cmd)
        status = status[0].strip()
        if 'not running' in status:
            return 'not running'
        return 'running'

    # get route tables
    def get_route(self):
        route_tables = {}
        kernel_route = []
        statick_route = []
        cmd = 'ip route show | grep -v "metric" '
        original_tables = self.connection.send_remote_cmd(cmd)
        original_tables = [line.strip('\n').strip()
                           for line in original_tables]

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

    # get the host file file string.
    def get_hosts(self):
        cmd = 'cat /etc/hosts'
        result = self.connection.send_remote_cmd(cmd)
        return result

    # get server time, return a string.
    def get_time(self):
        cmd = 'date "+%Y-%m-%d %H:%M:%S"'
        result = self.connection.send_remote_cmd(cmd)
        return result[0].strip('\n')

    # get all the disk used info
    def get_hard_disk_used(self):
        hd_used = {}
        cmd = 'df | cut -d " " -f1 | sed "/^$/d" | sed "1d" | grep -v "none" '
        result = self.connection.send_remote_cmd(cmd)
        hd_list = [info .strip('\n') for info in result]
        for hd_name in hd_list:
            singel_used_info = self.__get_singel_dh_used(hd_name)
            hd_used[hd_name] = singel_used_info
        return hd_used

    # get a singel disk used info
    def __get_singel_dh_used(self, disk_name):
        if disk_name == 'tmpfs':
            cmd = 'df -h | grep tmpfs'
        else:
            cmd = 'df -h ' + disk_name + ' | sed  "1d" '
        result = self.connection.send_remote_cmd(cmd)
        singel_info = [info.strip('\n').strip() for info in result]
        # join info as a singel string, cut dowm the disk_name
        # split it as a result
        singel_info = ''.join(singel_info).lstrip(disk_name).split()
        # singel_info will retrun information like next line showing.
        # ['Size',  'Used', 'Avail',  'Use%',   'Mounted']
        return singel_info

    # get CUP use persent information.
    def get_cup_used(self):
        cmd = "vmstat 1 2 | tail -1 | awk '{print $13,$14,$15}'"
        result = self.connection.send_remote_cmd(cmd)
        cpu_info = result[0].rstrip('\n').split()
        return cpu_info

    # get memory used.
    def get_memory_used(self):
        cmd = "head -2 /proc/meminfo | awk '{print $2}'  "
        result = self.connection.send_remote_cmd(cmd)
        mem_info = [info.strip('\n') for info in result]
        return mem_info

    # change the hosts file.
    def change_hosts(self, hosts_string):
        cmd = 'echo "' + hosts_string + '" > /etc/hosts'
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '修改hosts失败'
            return result
        return 0

    # change selinux status
    def change_selinu(self, status):
        # check status
        if status.lower() not in ['enforcing', 'permissive', 'disabled']:
            return 1

        cmd = 'sed -i "s/^SELINUX=.*/SELINUX='\
            + status.lower()\
            + '/" /etc/selinux/config'
        result = self.connection.send_remote_cmd(cmd)
        if result:
            # format the result, in case result has more than one line.
            result = [tmp.strip('\n') for tmp in result]
            print '设置selinux失败'
            for tmp in result:
                print tmp
            return result
        return 0

    # change chkconfig
    def change_chkconfig(self, name, status):
        # check status
        if status.lower() not in ['off', 'on']:
            return 1

        cmd = 'chkconfig ' + name + ' ' + status.lower()
        result = self.connection.send_remote_cmd(cmd)
        # if result has some text, it means that cmd return fail.
        if result:
            print name + '设置失败'
            print ''.join(result)
            return result
        return 0

    # control the system service
    def change_system_service(self, name, control):
        # check control
        if control.lower() not in ['start', 'stop', 'status']:
            return 1

        cmd = 'service ' + name + ' ' + control.lower()
        result = self.connection.send_remote_cmd(cmd)
        return result

    # change the system ip forward
    def change_ip_forward(self, control):
        control = str(control)
        # check control
        if control not in ['1', '0']:
            return control + '不在选择范围内'

        cmd = 'echo "' + control + '" > /proc/sys/net/ipv4/ip_forward'
        result = self.connection.send_remote_cmd(cmd)
        # if result has some text, it means that cmd return fail.
        if result:
            print 'ip转发设置失败'
            print result
            return result

        cmd = 'sed -i "s/ip_forward = ./ip_forward = '\
            + control\
            + '/" /etc/sysctl.conf'
        result = self.connection.send_remote_cmd(cmd)
        # if result has some text, it means that cmd return fail.
        if result:
            print 'ip转发设置失败'
            print result
            return result
        return 0

    # netmask translate into CIDR(255.255.255.0 ==> 24)
    def netmask_to_CIDR(self, mask):
        if '.' in mask:
            bin = lambda n: (n > 0) and (bin(n / 2) + str(n % 2)) or ''
            count_bit = lambda bin_str: len([i for i in bin_str if i == '1'])
            mask_splited = mask.split('.')
            mask_count = [count_bit(bin((int(i)))) for i in mask_splited]
            return str(sum(mask_count))
        return mask

    def CIDR_to_netmask(self, cidr_mask):
        if '.' not in cidr_mask:
            bin_arr = ['0' for i in range(32)]
            for i in range(int(cidr_mask)):
                bin_arr[i] = '1'
            tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
            tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
            return '.'.join(tmpmask)
        return cidr_mask

    # change network confige
    def save_new_network(self, dev_name, ip_and_mask, mac_addr=None):
        ip_addr, netmask = ip_and_mask.split('/')
        netmask = self.CIDR_to_netmask(netmask)
        config_part1 = 'DEVICE="' + dev_name + '"\n'
        config_part2 = 'BOOTPROTO="static"\n'
        config_part3 = 'IPADDR="' + ip_addr + '"\n'
        config_part4 = 'NETMASK="' + netmask + '"\n'
        if mac_addr:
            config_part5 = 'HWADDR="' + mac_addr + '"\n'
        else:
            config_part5 = ''
        config_part6 = 'ONBOOT="yes"\nTYPE="Ethernet"'
        config = config_part1 + config_part2 + config_part3\
            + config_part4 + config_part5 + config_part6
        cmd = 'echo -e \'' + config\
            + '\'>/etc/sysconfig/network-scripts/ifcfg-' \
            + dev_name
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '保存网络配置失败'
            return result
        return 0

    def delete_netwok_config(self, dev_name):
        cmd = 'rm -fr /etc/sysconfig/network-scripts/ifcfg-' + dev_name
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '删除网络配置文件失败'
            return result
        return 0

    # change a ip address provisional.
    def change_ip_addr(self, dev_name, ip_and_mask):
        ip_addr, netmask = ip_and_mask.split('/')
        netmask = self.netmask_to_CIDR(netmask)
        cmd = 'ifconfig ' + dev_name + ' ' + ip_addr +\
            '/' + netmask
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '修改ip地址失败'
            return result
        return 0

    # delete a ip address provisional.
    def delete_ip_addr(self, dev_name, ip_and_mask):
        ip_addr, netmask = ip_and_mask.split('/')
        netmask = self.netmask_to_CIDR(netmask)
        cmd = 'ip addr delete ' + ip_addr + '/' + netmask + ' dev ' + dev_name
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '删除ip地址失败'
            return result
        return 0

    # add a static route provisional.
    def add_static_route(self, net_netmask, gatewate):
        cmd = 'ip route add ' + net_netmask + ' via ' + gatewate
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '添加路由失败'
            return result
        return 0

    # delete a static route provisional.
    def delete_static_route(self, net_netmask, gatewate):
        cmd = 'ip route delete ' + net_netmask + ' via ' + gatewate
        result = self.connection.send_remote_cmd(cmd)
        if result:
            print '删除路由失败'
            return result
        return 0
