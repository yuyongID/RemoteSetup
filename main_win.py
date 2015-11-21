#!/usr/bin/env python
# coding=UTF-8
import wx
import sys
import basewin
import commands


class LoginWindow(basewin.BaseLoginDialog):

    def ShowAndGetKeys(self):
        result = self.ShowModal()
        if result == wx.ID_OK:
            # can not return a unicode, change it to be string.
            return str(self.text_ip_addr.GetValue()),\
                int(self.text_port.GetValue()),\
                str(self.text_user_name.GetValue()),\
                str(self.text_password.GetValue()),
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
            pass
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
            mac = self.network_info.get(dev_name, None).get('mac', None)
            mtu = self.network_info.get(dev_name, None).get('mtu', None)
            speed = self.network_info.get(dev_name, None).get('speed', None)
            status = self.network_info.get(dev_name, None).get('status', None)
        except AttributeError:
            return 'None', 'None', 'None', 'None'
        return mac, mtu, speed, status

    def __get_ip_info(self):
        selection_dev = self.listbox_dev.GetStringSelection()
        try:
            ip_info = self.network_info.get(
                selection_dev, None).get('ip', None)
        except AttributeError:
            return 'None'
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
        if self.listbox_dev.GetStringSelection() == 'lo':
            wx.MessageBox('嘿，小伙子！别想打网口lo的注意\n她是我的╭(╯^╰)╮', '别闹了，好不好')
            return 1
        dev_modify_win = DevModifyDialog(self)
        dev_modify_win.init_dev_ip_info(self.server, self.__get_ip_info())
        dev_modify_win.show_and_get_ip_restul()
        self.listbox_dev.Clear()
        self.init_network_window(self.server)


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
        except NameError:
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
        control_win.Show()


class ServiceControl(basewin.BaseServiceControl):

    def init_and_show_info(self, service_name, server_connection):
        self.server = server_connection
        self.service_name = service_name
        self.SetTitle(service_name + '服务控制')
        self.__service_control('status')

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
        self.text_ip_addr.AppendText(self.server_ip)
        self.text_sys_reslease.AppendText(self.server.system_release)
        self.text_hostname.AppendText(self.server.system_hostname)
        self.text_iptables.AppendText(self.server.system_iptables)
        self.text_ip_forward.AppendText(self.server.system_ip_forward)
        self.text_selinux.AppendText(self.server.system_selinux)

    def call_login_window(self):
        login_win = LoginWindow(self)
        try:
            self.server_ip, self.server_port, self.username, self.password =\
                login_win.ShowAndGetKeys()
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

if __name__ == '__main__':
    app = wx.App()
    main_win = MainWindow(None)
    main_win.call_login_window()
    main_win.connect_and_get_info()
    main_win.Show()
    app.MainLoop()
