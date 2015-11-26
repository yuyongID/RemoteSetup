#!/usr/bin/env python
# coding=UTF-8
import wx
import sys
import threading
import time
from wx.lib.pubsub import Publisher
import basewin
import commands


class LoginWindow(basewin.BaseLoginDialog):

    def show_and_get_keys(self):
        result = self.ShowModal()
        if result == wx.ID_OK:
            # can not return a unicode, change it to be string.
            return str(self.text_ip_addr.GetValue()),\
                int(self.text_port.GetValue()),\
                self.text_user_name.GetValue(),\
                self.text_password.GetValue(),
        elif result == wx.ID_CANCEL:
            sys.exit()
        else:
            sys.exit()


class NetworkWindow(basewin.BaseNetworkWindow):

    def init_network_window(self, server_connection):
        self.server = server_connection
        self.__get_netwrok_info()
        self.listbox_dev.AppendItems(self.dev_list)
        self.listbox_dev.SetSelection(1)
        self.__show_dev_info()

    def __show_dev_info(self):
        selection_dev = self.listbox_dev.GetStringSelection()
        try:
            mac, mtu, speed, status = self.__get_dev_info(selection_dev)
        except UnboundLocalError:
            mac, mtu, speed, status = 'None'
        ip_list = self.__get_ip_list(selection_dev)
        ip_list = '\n'.join(ip_list)
        self.text_dev_name.Clear()
        self.text_ip_addr.Clear()
        self.text_mac.Clear()
        self.text_mtu.Clear()
        self.text_speed.Clear()
        self.text_dev_name.AppendText(selection_dev)
        self.text_ip_addr.AppendText(ip_list)
        self.text_mac.AppendText(mac)
        self.text_mtu.AppendText(str(mtu))
        self.text_speed.AppendText(str(speed) + ' Mbps')

    def __get_netwrok_info(self):
        self.network_info = self.server.get_network()
        self.dev_list = self.network_info.keys()

    def __get_dev_info(self, dev_name):
        try:
            # pick up information in dict
            mac = self.network_info.get(dev_name, 'None').get('mac', 'None')
            mtu = self.network_info.get(dev_name, 'None').get('mtu', 'None')
            speed = self.network_info.get(dev_name, 'None').get('speed', 'None')
            status = self.network_info.get(dev_name, 'None').get('status', 'None')
        except AttributeError:
            return 'None', 'None', 'None', 'None'
        return mac, mtu, speed, status

    def __get_ip_info(self):
        selection_dev = self.listbox_dev.GetStringSelection()
        try:
            ip_info = self.network_info.get(
                selection_dev, 'None').get('ip', 'None')
        except AttributeError:
            return None
        return (selection_dev, ip_info)

    def __get_ip_list(self, dev_name):
        ip_list = []
        try:
            base_info = self.network_info.get(dev_name, None).get('ip', None)
            for ip_info in base_info:
                ip_list.append(ip_info[1])
        except AttributeError:
            return "None"
        return ip_list

    def click_listbox_dev(self, event):
        self.__show_dev_info()

    def click_modify(self, event):
        # nobody can change 'lo' port's information.
        if self.listbox_dev.GetStringSelection() == 'lo':
            wx.MessageBox('嘿，小伙子！别想打网口lo的注意\n她是我的╭(╯^╰)╮', '别闹了，好不好')
            return 1
        # initial a dialog window for changing.
        dev_modify_win = DevModifyDialog(self)
        dev_modify_win.init_dev_ip_info(self.server, self.__get_ip_info())
        dev_modify_win.show_and_get_ip_restul()
        self.listbox_dev.Clear()
        self.init_network_window(self.server)

    def click_button_monitor(self, event):
        dev_name = self.listbox_dev.GetStringSelection()
        monitor_win = DevMonitor(self)
        monitor_win.init_monitor_window(
            dev_name,
            self.server
        )
        monitor_win.Show()


class DevMonitor(basewin.BaseDevMonitor):

    def init_monitor_window(self, dev_name, server_connection):
        self.dev_shower = GetServerDevThreading(server_connection, dev_name)
        Publisher().subscribe(self.__show_dev, "update_dev")
        # initial, for calculate the speed
        self.receive_bytes_old = 0
        self.transmit_bytes_old = 0

    def __show_dev(self, message):
        receive_bytes, transmit_bytes = message.data
        self.label_receive_bytes.SetLabel(receive_bytes + ' bytes')
        self.label_transmit_bytes.SetLabel(receive_bytes + ' bytes')
        speed = str(int(receive_bytes) - self.receive_bytes_old)
        self.label_receive_speed.SetLabel(speed + ' byte/s')
        speed = str(int(transmit_bytes) - self.transmit_bytes_old)
        self.label_transmit_speed.SetLabel(speed + ' byte/s')
        self.receive_bytes_old = int(receive_bytes)
        self.transmit_bytes_old = int(transmit_bytes)

    def __del__(self):
        self.dev_shower.stop()


class RouteWindow(basewin.BaseRouteWindow):

    def init_route_window(self, server_connection):
        self.server = server_connection
        route_info = self.server.get_route()
        self.edit_route = []
        self.listbox_kernel.Clear()
        self.listbox_route.Clear()
        self.__show_route_info(route_info)

    def __show_route_info(self, route_info):
        ketnel_route = route_info.get('kernel', None)
        static_route = route_info.get('static', None)
        show_info = []
        # show kernel route in list box
        for info in ketnel_route:
            info = info[0] .center(20, ' ') +\
                info[1].center(20, ' ') +\
                info[2].rjust(10, ' ')
            show_info.append(info)
        self.listbox_kernel.AppendItems(show_info)
        # show static route in list box
        for info in static_route:
            self.__show_static_route(info[0],  info[2], info[1])

    def __show_static_route(self, net_netmask, gateway, port_ip="unknow"):
        show_info = []
        info = net_netmask.center(20, ' ') + \
            port_ip.center(20, ' ') + \
            gateway.rjust(10, ' ')
        show_info.append(info)
        self.listbox_route.AppendItems(show_info)
        self.listbox_route.SetSelection(0)

    def __enforce_edit_route(self, control, net_netmask, gateway):
        if control == 'add':
            result = self.server.add_static_route(net_netmask, gateway)
            control = '路由"添加"操作：\n'
        elif control == 'del':
            result = self.server.delete_static_route(net_netmask, gateway)
            control = '路由"删除"操作：\n'
        elif control == 'modify':
            result = self.server.add_static_route(net_netmask, gateway)
            control = '路由"修改"操作：\n'
        else:
            return 1
        # if remote control has any erro, show a message.and go on.
        if result:
            wx.MessageBox(
                control +
                '网络：' + net_netmask +
                '\n网关：' + gateway +
                '\n乱填的是什么鬼？\n' +
                '远程系统返回结果：\n' +
                ''.join(result), '路由填错了')

    def click_add(self, event):
        route_modify = GetRoutedialog(self)
        result = route_modify.show_and_get_route_restul()
        # if result is None, that means user click cancel button.
        if result:
            # if user input nothing, than pass it.
            if result[0] == '/' or result[1] == '':
                return 0
            self.__show_static_route(result[0], result[1])
            self.edit_route.append(('add', result))

    def click_del(self, event):
        route_info = self.listbox_route.GetStringSelection().split()
        # if route_info has something, go on. delete it
        if route_info:
            net_netmask = route_info[0].encode('utf-8')
            gateway = route_info[2].encode('utf-8')
            self.edit_route.append(('del', (net_netmask, gateway)))
            # remove route info from list box, user seleted.
            self.listbox_route.Delete(self.listbox_route.GetSelection())
            # select the last one, after user remove some one.
            self.listbox_route.SetSelection(self.listbox_route.GetCount() - 1)

    def click_modify(self, event):
        route_info = self.listbox_route.GetStringSelection().split()
        # if route_info has nothing, it means user select nothing.return
        if not route_info:
            wx.MessageBox('忘记选了？好歹选择一个吧？', '忘记选了？')
            return 1
        # and then, go on. enforce user selection.get the selection strings.
        net_netmask = route_info[0].encode('utf-8')
        gateway = route_info[2].encode('utf-8')
        # init a route modify dialog, and show route info just got.
        route_modify = GetRoutedialog(self)
        result = route_modify.show_and_get_route_restul(net_netmask, gateway)
        # if result is None, that means user click cancel button on dialog.
        if result:
            # if user input nothing, than pass it.
            if result[0] == '/' or result[1] == '':
                return 0
            self.click_del(event)
            self.__show_static_route(
                result[0].encode('utf-8'),
                result[1].encode('utf-8')
            )
            self.edit_route.append(('modify', result))

    def click_apply(self, event):
        for info in self.edit_route:
            self.__enforce_edit_route(info[0], info[1][0], info[1][1])
        # initial the window , after enforce the list
        self.init_route_window(self.server)

    def double_click_route_list(self, event):
        self.click_modify(event)

    def click_cancel(self, event):
        self.Destroy()


class GetRoutedialog(basewin.BaseGetRoutedialog):

    def __init_get_route_dialog(self, net_netmask, gateway):
        route, net_mask = net_netmask.split('/')
        self.text_net.AppendText(route)
        self.text_mask.AppendText(net_mask)
        self.text_gateway.AppendText(gateway)

    def show_and_get_route_restul(self, net_netmask=None, gateway=None):
        # if it net_netmask is not None, it means user click modify button.
        # so, we show the route info on get route dialog
        if net_netmask:
            self.__init_get_route_dialog(net_netmask, gateway)
        result = self.ShowModal()
        if result == wx.ID_OK:
            net_netmask = self.text_net.GetValue().encode('utf-8') + \
                '/' + self.text_mask.GetValue().encode('utf-8')
            gateway = self.text_gateway.GetValue().encode('utf-8')
            return net_netmask, gateway
        elif result == wx.ID_CANCEL:
            return None


class DevModifyDialog(basewin.BaseDevModifyDialog):

    def init_dev_ip_info(self, connection, (dev_name, ip_info)):
        # init the server connection, be use for add or del ip addr.
        self.server = connection
        self.default_dev_name = dev_name
        self.__ip_info_to_str_list(ip_info)
        self.listbox_ip_list.SetSelection(0)
        self.edit_ip_list = []

    def __ip_info_to_str_list(self, ip_info):
        ip_list = []
        for info in ip_info:
            if info[0] is None:
                text = ' ' * 18 + info[1].ljust(17, ' ')
            else:
                text = info[0].center(10, ' ') + info[1].center(17, ' ')
            ip_list.append(text)
        self.listbox_ip_list.AppendItems(ip_list)

    def show_and_get_ip_restul(self):
        result = self.ShowModal()
        if result == wx.ID_OK:
            self.__enforce_edit_ip_list()
        elif result == wx.ID_CANCEL:
            self.Destroy()

    def __enforce_edit_ip_list(self):
        process_len = len(self.edit_ip_list)
        # if edit_ip_list have nothing, then nothing will change.
        if process_len == 0:
            return 0
        # Now go on, to process the edit_list
        enforce_pro_dlg = wx.ProgressDialog('处理中..', '开始处理', process_len)
        process_index = 0
        wx.Sleep(1)
        for edit_step in self.edit_ip_list:
            process_index += 1
            enforce_pro_dlg.Update(
                process_index,
                str(process_index) + '/' + str(process_len)
            )
            if edit_step[0] is 'add':
                self.__enforce_change_ip(edit_step[1])
            elif edit_step[0] is 'del':
                self.__enforce_delete_ip(edit_step[1])
        enforce_pro_dlg.Destroy()

    def __enforce_change_ip(self, (dev_name, ip_and_mask)):
        result = self.server.change_ip_addr(dev_name, ip_and_mask)
        # if result is empty, it means ip address add fail.
        if not result:
            result = self.server.save_new_network(dev_name, ip_and_mask)
            if result:
                wx.MessageBox(''.join(result), '保存自启动失败')
        else:
            wx.MessageBox(
                dev_name + '操作失败\n' + ''.join(result),
                '操作ip失败'
            )

    def __enforce_delete_ip(self, (dev_name, ip_and_mask)):
        result = self.server.delete_ip_addr(dev_name, ip_and_mask)
        # if result is empty, it means ip address add fail.
        if not result:
            result = self.server.delete_netwok_config(dev_name)
            if result:
                wx.MessageBox(''.join(result), '保存自启动失败')
        else:
            wx.MessageBox(
                dev_name + '操作失败\n' + ''.join(result),
                '操作ip失败'
            )

    def click_add(self, event):
        add_ip_win = GetIPAddrdialog(self)
        result = add_ip_win.show_and_get_new_ip()
        # if user click 'cancel(取消)', then pass
        if not result:
            return 0
        # if user input nothing, and pass.
        if result[0] == '' and result[1] == '/':
            pass
        else:
            self.__ip_info_to_str_list([result])
            self.edit_ip_list.append(('add', result))

    def click_del(self, event):
        if self.listbox_ip_list.GetSelection() == 0:
            wx.MessageBox(
                '你连这个地址都敢删除，\n弄坏了别来找我。\n反正不关我的事！\n(ー`´ー)',
                '你作死！！'
            )
            wx.MessageBox(
                '怕了吧?后悔还来得及，\n还不赶紧点【取消】?\no(￣ヘ￣o＃)',
                '还作死？'
            )
        # get the info, that will bean deleted.
        # if it did not have a dev name, use default dev name
        ip_info = self.listbox_ip_list.GetStringSelection().split()
        if len(ip_info) == 1:
            dev_name = self.default_dev_name.encode('utf-8')
            ip_and_mask = ip_info[0].encode('utf-8')
        else:
            dev_name = ip_info[0].encode('utf-8')
            ip_and_mask = ip_info[1].encode('utf-8')
        self.listbox_ip_list.Delete(self.listbox_ip_list.GetSelection())
        self.edit_ip_list.append(('del', (dev_name, ip_and_mask)))

    def click_modify(self, event):
        # get the ip info from listbox choose
        ip_info = self.listbox_ip_list.GetStringSelection().split()
        if len(ip_info) == 1:
            dev_name = self.default_dev_name.encode('utf-8')
            ip_and_mask = ip_info[0].encode('utf-8')
        else:
            dev_name = ip_info[0].encode('utf-8')
            ip_and_mask = ip_info[1].encode('utf-8')

        # then init a dialog window, and show the ip info.
        add_ip_win = GetIPAddrdialog(self)
        result = add_ip_win.show_and_get_new_ip(dev_name, ip_and_mask)

        # if user click 'cancel(取消)', then pass
        if not result:
            return 0
        # if user input nothing, and pass.
        if result[0] == '' and result[1] == '/':
            pass
        else:
            self.listbox_ip_list.Delete(self.listbox_ip_list.GetSelection())
            self.__ip_info_to_str_list([result])
            self.edit_ip_list.append(('add', result))

    def click_list_box(self, event):
        text = self.listbox_ip_list.GetStringSelection()
        if len(text.split()) == 1:
            self.button_modify.Disable()
        else:
            self.button_modify.Enable()

    def double_click_list_box(self, event):
        text = self.listbox_ip_list.GetStringSelection()
        if len(text.split()) == 1:
            self.button_modify.Disable()
        else:
            self.button_modify.Enable()
            self.click_modify(event)


class GetIPAddrdialog(basewin.BaseGetIPAddrdialog):

    def show_and_get_new_ip(self, dev_name=None, ip_and_mask=None):
        # if it has any arguments, that means dialog be use for ip addr modify
        if dev_name:
            self.__init_modify_text(dev_name, ip_and_mask)
        # then show the dialog window.
        result = self.ShowModal()
        if result == wx.ID_OK:
            dev_name = str(self.text_dev_name.GetValue())
            ip_addr = str(self.text_ip_addr.GetValue())
            mask = str(self.text_mask.GetValue())
            return (dev_name, ip_addr + '/' + mask)
        elif result == wx.ID_CANCEL:
            self.Destroy()

    def __init_modify_text(self, dev_name, ip_and_mask):
        ip, mask = ip_and_mask.split('/')
        self.text_dev_name.AppendText(dev_name)
        self.text_ip_addr.AppendText(ip)
        self.text_mask.AppendText(mask)
        self.text_dev_name.Disable()


class SysServiceWindow(basewin.BaseSysServiceWindow):

    def init_ntsysv_window(self, server_connection):
        self.server = server_connection
        self.__enforce_service_info()
        self.__show_ntsysv_info()

    def __show_ntsysv_info(self):
        # init all the server's service into list
        self.checklistbox_service.Clear()
        self.checklistbox_service.AppendItems(self.ntsysv_name_list)
        self.checklistbox_service.SetCheckedStrings(self.ntsysv_on_old)
        # if server did not has the xinetd service, hide the listbox and return
        try:
            type(self.xinetd_name_list)
        except (NameError, AttributeError):
            self.label_xinetd.Hide()
            self.checklistbox_winetd.Hide()
            self.SetSize((215, 398))
            return 0
        # init all the xinetd service into listbox.
        self.SetSize((215, 520))
        self.checklistbox_winetd.Clear()
        self.checklistbox_winetd.AppendItems(self.xinetd_name_list)
        self.checklistbox_winetd.SetCheckedStrings(self.xinetd_on_old)

    # enforce any information from remote service
    def __enforce_service_info(self):
        ntsysv_info, xinetd_info = self.server.get_chkconfig()
        self.ntsysv_name_list = []
        self.ntsysv_on_old = []
        # init service list from remote server data
        for serv_info in ntsysv_info:
            self.ntsysv_name_list.append(serv_info[0])
            if serv_info[1] == 'on':
                self.ntsysv_on_old.append(serv_info[0])
        # init xinetd list fron data
        # if server did not has the xinetd service, return
        if not xinetd_info:
            return 0
        # if server has any xinetd service, then go on.
        self.xinetd_name_list = []
        self.xinetd_on_old = []
        for serv_info in xinetd_info:
            self.xinetd_name_list.append(serv_info[0])
            if serv_info[1] == 'on':
                self.xinetd_on_old.append(serv_info[0])

    def __enforce_edit_service(self):
        ntsysv_on_new = []
        for name in self.checklistbox_service.GetCheckedStrings():
            ntsysv_on_new.append(name.encode('utf-8'))
        # pick up the service that been set 'on'
        set_on_service = [
            name for name in ntsysv_on_new if name not in self.ntsysv_on_old]
        # pick up the service that been set 'off'
        set_off_service = [
            name for name in self.ntsysv_on_old if name not in ntsysv_on_new]
        if set_on_service:
            self.__enforce_service_chkconfig(set_on_service, 'on')
        if set_off_service:
            self.__enforce_service_chkconfig(set_off_service, 'off')

    def __enforce_service_chkconfig(self, service_list, status):
        for service in service_list:
            result = self.server.change_chkconfig(service, status)
            if result:
                wx.MessageBox(''.join(result), '悲剧了！~~~~(>_<)~~~~ ')

    def click_ok(self, event):
        self.__enforce_edit_service()
        self.Destroy()

    def click_cancel(self, event):
        self.Destroy()

    def double_click_service(self, event):
        service_name = self.checklistbox_service.GetStringSelection()
        service_name = service_name.encode('utf-8')
        control_win = ServiceControl(self)
        control_win.init_and_show_info(service_name, self.server)


# a simple window for service controling.
class ServiceControl(basewin.BaseServiceControl):

    def init_and_show_info(self, service_name, server_connection):
        self.server = server_connection
        self.service_name = service_name
        self.SetTitle(service_name + '服务控制')
        self.__service_control('status')
        self.Show()

    def __service_control(self, control):
        result = self.server.change_system_service(self.service_name, control)
        self.text_status.Clear()
        self.text_status.AppendText(''.join(result))

    def click_start(self, event):
        self.text_status.Clear()
        self.text_status.AppendText('正在启动服务：' + self.service_name)
        self.__service_control('start')

    def click_stop(self, event):
        self.text_status.Clear()
        self.text_status.AppendText('正在停止服务：' + self.service_name)
        self.__service_control('stop')

    def click_status(self, event):
        self.text_status.Clear()
        self.text_status.AppendText('正在查询服务：' + self.service_name)
        self.__service_control('status')


class HostsEditor(basewin.BaseHostsEditor):

    def init_and_show_hosts_info(self, server_connection):
        self.server = server_connection
        old_hosts = self.server.get_hosts()
        self.text_hosts.SetValue(''.join(old_hosts))

    def click_ok(self, event):
        new_hosts = self.text_hosts.GetValue().encode('utf-8')
        result = self.server.change_hosts(new_hosts)
        if result:
            wx.MessageBox('提交编辑失败了，客官。+_+\n' + ''.join(result), '悲剧了')
            return 1
        wx.MessageBox(
            '提交成功了，开森。\nO(∩_∩)O~',
            '成功了'
        )
        self.Destroy()
        return 0

    def click_cancel(self, event):
        self.Destroy()


# get server time by threading class.
class GetServerMemoryCPUThreading(threading.Thread):

    def __init__(self, ip, username, password, port):
        threading.Thread.__init__(self)
        self.server = commands.RemoteSystem(
            ip, username,
            password, port
        )
        self.stop_flag = 0
        self.start()

    def run(self):
        while True:
            if self.stop_flag != 1:
                # get memory info and return to window
                server_memory = self.server.get_memory_used()
                wx.CallAfter(
                    Publisher().sendMessage,
                    "update_memory", server_memory
                )
                # get CPU info and return to window,
                # it will keep 1s sleep at remote server
                server_cpu = self.server.get_cup_used()
                wx.CallAfter(
                    Publisher().sendMessage,
                    "update_cpu", server_cpu
                )
            else:
                return 1
            # time.sleep(2.2)

    def stop(self):
        self.stop_flag = 1


# get server time by threading class.
class GetServerTimeThreading(threading.Thread):

    def __init__(self, ip, username, password, port):
        threading.Thread.__init__(self)
        self.server = commands.RemoteSystem(
            ip, username,
            password, port
        )
        self.stop_flag = 0
        self.start()

    def run(self):
        while True:
            if self.stop_flag != 1:
                server_time = self.server.get_time()
                wx.CallAfter(
                    Publisher().sendMessage,
                    "update_time", server_time
                )
            else:
                return 1
            time.sleep(1)

    def stop(self):
        self.stop_flag = 1


# get server dev bytes speed by threading calss.
class GetServerDevThreading(threading.Thread):

    def __init__(self, server_connection, dev_name):
        threading.Thread.__init__(self)
        self.server = server_connection
        self.dev_name = dev_name
        self.stop_flag = 0
        self.start()

    def set_dev(self, dev_name):
        self.dev_name = dev_name

    def run(self):
        while True:
            if self.stop_flag != 1:
                server_dev = self.server.get_dev_bytes(self.dev_name)
                wx.CallAfter(
                    Publisher().sendMessage,
                    "update_dev", server_dev
                )
            else:
                return 1
            time.sleep(1.3)

    def stop(self):
        self.stop_flag = 1


class SystemInfoWindow(basewin.BaseSystemInfoWindow):

    def init_and_show_system_info(self, server_connection):
        self.server = server_connection
        init_pro_dlg = wx.ProgressDialog('正在...', '开门', 100)
        wx.Sleep(1)
        init_pro_dlg.Update(10, '放置家具')
        self.hard_disk_used_info = self.server.get_hard_disk_used()
        # initial threading, refresh system time per 1 second.
        init_pro_dlg.Update(30, '安排time跟班')
        self.time_shower = GetServerTimeThreading(
            self.server_ip, self.server_user,
            self.server_password, self.server_port
        )
        Publisher().subscribe(self.__show_time, "update_time")
        # initial threading, refresh system cpu per 2 second.
        init_pro_dlg.Update(40, '安排cpu跟班')
        self.memory_cpu_shower = GetServerMemoryCPUThreading(
            self.server_ip, self.server_user,
            self.server_password, self.server_port
        )
        Publisher().subscribe(self.__show_cpu, "update_cpu")
        init_pro_dlg.Update(50, '安排memory跟班')
        Publisher().subscribe(self.__show_memory, "update_memory")
        init_pro_dlg.Update(80, '打扫中...')
        self.__show_hard_disk_info()
        init_pro_dlg.Update(100, '主人请进')
        init_pro_dlg.Destroy()

    # set all of the server login information, for threading
    # build new connection to server.
    def set_login_info(self, ip, username, password, port):
        self.server_ip = ip
        self.server_user = username
        self.server_password = password
        self.server_port = port

    def __show_time(self, message):
        text = message.data
        self.text_time_value.SetValue(text)

    # show server cpu information from threading.
    def __show_cpu(self, message):
        cpu_info = message.data
        # refresh cpu information.
        try:
            cpu_info = self.server.get_cup_used()
        except wx._core.PyDeadObjectError:
            return 1
        self.text_usr_cpu.SetValue(cpu_info[0] + '%')
        self.text_sys_cpu.SetValue(cpu_info[1] + '%')
        self.text_free_cpu.SetValue(cpu_info[2] + '%')
        self.gauge_cpu_persent.SetValue(100 - int(cpu_info[2]))

    # show server memory information from threading.
    def __show_memory(self, message):
        memory_info = message.data
        self.text_memory_size.SetValue(memory_info[0] + ' kB')
        self.text_memory_free.SetValue(memory_info[1] + ' kB')
        # self.gauge_memory_persent.SetValue

    # show all the hard disk information on the window.
    def __show_hard_disk_info(self):
        # show disk device used.
        hard_disk_list = self.hard_disk_used_info.keys()
        self.listbox_hard_disk.AppendItems(hard_disk_list)
        self.listbox_hard_disk.SetSelection(0)
        self.show_singel_hard_disk_info(1)  # this argument '1' is useless.

    # show hard disk information on TextCtrl, when user select some device
    def show_singel_hard_disk_info(self, event):
        hard_disk_name = self.listbox_hard_disk.GetStringSelection()
        singel_info = self.hard_disk_used_info.get(hard_disk_name)
        try:
            self.text_size.SetValue(singel_info[0])
            self.text_used.SetValue(singel_info[1])
            self.text_avail.SetValue(singel_info[2])
            self.text_use_persent.SetValue(singel_info[3])
            self.text_mounted.SetValue(singel_info[4])
            # when window close, will happen TypeError.
            # I don't know why. @_@
        except TypeError:
            pass
        try:
            self.gauge_used_persent.SetValue(
                int(singel_info[3].strip('%'))
            )
        # I don't know what happend...., too.╮(╯▽╰)╭
        except (wx._core.PyDeadObjectError, TypeError):
            return 1

    def __del__(self):
        self.time_shower.stop()
        self.memory_cpu_shower.stop()


class MainWindow(basewin.BaseMainWindow):

    def connect_and_get_info(self):
        print '开始尝试链接服务器:', self.server_ip
        init_pro_dlg = wx.ProgressDialog('载入进度', '开始', 100)
        wx.Sleep(1)
        init_pro_dlg.Update(10, '正在登陆服务器...')
        try:
            self.server = commands.RemoteSystem(
                self.server_ip, self.username,
                self.password, self.server_port
            )
        except:
            wx.MessageBox('不能成功连接到服务器！+_+', '错误')
            raise
        init_pro_dlg.Update(50, '成功登陆...')
        print '链接成功！O(∩_∩)O~~'
        init_pro_dlg.Update(90, '准备接客！')
        print '正在给主窗口装修，准备接客！'
        self.__show_server_info()
        init_pro_dlg.Update(100, '客官请进！')
        init_pro_dlg.Destroy()

    def __show_server_info(self):
        self.SetTitle(self.server_ip)
        self.text_ip_addr.SetValue(self.server_ip)
        self.text_sys_reslease.SetValue(self.server.system_release)
        self.text_hostname.SetValue(self.server.system_hostname)
        self.text_iptables.SetValue(self.server.system_iptables)
        self.text_ip_forward.SetValue(self.server.system_ip_forward)
        self.choice_ip_forward.SetSelection(int(self.server.system_ip_forward))
        self.text_selinux.SetValue(self.server.system_selinux)
        self.choice_selinux.SetStringSelection(self.server.system_selinux)

    def call_login_window(self):
        login_win = LoginWindow(self)
        try:
            self.server_ip, self.server_port, self.username, self.password =\
                login_win.show_and_get_keys()
        except TypeError:
            pass
        login_win.Destroy()

    def click_network(self, event):
        network_win = NetworkWindow(self)
        network_win.Show()
        network_win.init_network_window(self.server)
        network_win.Destroy

    def click_route(self, event):
        route_win = RouteWindow(self)
        route_win.init_route_window(self.server)
        route_win.Show()

    def click_ntsysv(self, event):
        ntsysv_win = SysServiceWindow(self)
        ntsysv_win.init_ntsysv_window(self.server)
        ntsysv_win.Show()

    def click_hosts(self, event):
        host_editor = HostsEditor(self)
        host_editor.init_and_show_hosts_info(self.server)
        host_editor.Show()

    def click_system_info(self, event):
        sys_info_win = SystemInfoWindow(None)
        sys_info_win.set_login_info(
            self.server_ip,
            self.username,
            self.password,
            self.server_port
        )
        sys_info_win.Show()
        sys_info_win.init_and_show_system_info(self.server)

    def double_click_iptables(self, event):
        iptables_control = ServiceControl(self)
        iptables_control.init_and_show_info('iptables', self.server)

    def click_iptable_control(self, event):
        iptables_control = ServiceControl(self)
        iptables_control.init_and_show_info('iptables', self.server)

    # enforce user try to change ip forward status
    def choise_ip_forward_control(self, event):
        control = self.choice_ip_forward.GetSelection()
        result = self.server.change_ip_forward(control)
        if result:
            wx.MessageBox(
                '失败鸟～你权限不够？\n' + ''.join(result),
                '天呐～'
            )
            return 1
        wx.MessageBox('客官，你的ip转发处理完了\nO(∩_∩)O~~', '妥了')
        self.text_ip_forward.SetValue(self.server.get_ip_forward())

    # enforce user try to change selinux status
    def choice_selinux_control(self, event):
        control = self.choice_selinux.GetStringSelection().encode('utf-8')
        result = self.server.change_selinux(control)
        if result:
            wx.MessageBox(
                '失败鸟～你权限不够？\n' + ''.join(result),
                '天呐～'
            )
            return 1
        wx.MessageBox('客官，你的selinux处理完了\nO(∩_∩)O~~', '妥了')
        self.text_selinux.SetValue(self.server.get_selinux())

if __name__ == '__main__':
    app = wx.App()
    main_win = MainWindow(None)
    main_win.call_login_window()
    main_win.connect_and_get_info()
    main_win.Show()
    app.MainLoop()
