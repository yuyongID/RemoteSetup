#!/usr/bin/env python
#coding=UTF-8
import wx
import sys
import basewin
import commands
import pprint

class LoginWindow(basewin.BaseLoginDialog):

    def ShowAndGetKeys(self):
        result = self.ShowModal()
        if result == wx.ID_OK:
            print '点击了确定'
            #can not return a unicode, change it to be string.
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
        self.text_speed.AppendText(str(speed)+' Mbps')

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
            ip_info = self.network_info.get(selection_dev, None).get('ip', None)
        except AttributeError:
            print 'AttributeError'
            return 'None'
        return (selection_dev, ip_info)
        
    def __get_ip_list(self, dev_name):
        ip_list = []
        try:
            for ip_info in self.network_info.get(dev_name, None).get('ip', None):
                ip_list.append(ip_info[1])
        except AttributeError:
            return "None"
        return ip_list

    def click_listbox_dev(self, event):
        self.__show_dev_info()

    def click_modify(self, event):
        print '点击了修改网络'
        if self.listbox_dev.GetStringSelection() == 'lo':
            wx.MessageBox('嘿，小伙子！别想打网口lo的注意\n她是我的╭(╯^╰)╮', '别闹了，好不好')
            return 1
        dev_modify_win = DevModifyDialog(self)
        dev_modify_win.init_dev_ip_info(self.server, self.__get_ip_info())
        dev_modify_win.show_and_get_ip_restul()
        self.listbox_dev.Clear()
        self.init_network_window(self.server)
        
class RouteWindow(basewin.BaseRouteWindow):

    def click_add(self, event):
        print '点击了增加'
        route_modify = GetRoutedialog(self)
        route_modify.show_and_get_route_restul()

    def click_del(self, event):
        print '点击了删除'

    def click_modify(self, event):
        print '点击了修改'
        route_modify = GetRoutedialog(self)
        route_modify.show_and_get_route_restul()

    def click_apply(self, event):
        print '点击了应用'

    def click_cancel(self, event):
        print '点击了取消'
        self.Destroy()

class GetRoutedialog(basewin.BaseGetRoutedialog):

    def show_and_get_route_restul(self):
        result = self.ShowModal()
        if result == wx.ID_OK:
            print '点击了确定'
        elif result == wx.ID_CANCEL:
            print '点击了取消'

class DevModifyDialog(basewin.BaseDevModifyDialog):

    def init_dev_ip_info(self, connection, (dev_name, ip_info)):
        #init the server connection, be use for add or del ip addr.
        self.server = connection
        self.default_dev_name = dev_name
        self.__ip_info_to_str_list(ip_info)
        self.listbox_ip_list.SetSelection(0)
        self.edit_ip_list = []

    def __ip_info_to_str_list(self, ip_info):
        ip_list = []
        for info in ip_info:
            if info[0] is None:
                text = ' '*18 + info[1].ljust(17, ' ')
            else:
                text = info[0].center(10, ' ') + info[1].center(17, ' ')
            ip_list.append(text)
        self.listbox_ip_list.AppendItems(ip_list)

    def show_and_get_ip_restul(self):
        result = self.ShowModal() 
        if result == wx.ID_OK:
            print '点击了确定'
            print self.edit_ip_list
            self.__enforce_edit_ip_list()
        elif result == wx.ID_CANCEL:
            print '点击了取消'
        
    def __enforce_edit_ip_list(self):
        process_len = len(self.edit_ip_list)
        #if edit_ip_list have nothing, then nothing will change.
        if process_len == 0:
            return 0
        #Now go on, to process the edit_list
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
        print '从远程服务器增加ip地址'
        result = self.server.change_ip_addr(dev_name, ip_and_mask)
        #if result is empty, it means ip address add fail.
        if not result:
            result = self.server.save_new_network(dev_name, ip_and_mask)
            if result:
                print '保存自启动配置失败'
                wx.MessageBox(''.join(result), '保存自启动失败')
        else:
            print '修改失败'
            wx.MessageBox(
                dev_name + '操作失败\n' + ''.join(result),
                '操作ip失败'
            )

    def __enforce_delete_ip(self, (dev_name, ip_and_mask)):
        print '从远程服务器删除ip地址'
        result = self.server.delete_ip_addr(dev_name, ip_and_mask)
        #if result is empty, it means ip address add fail.
        if not result:
            result = self.server.delete_netwok_config(dev_name)
            if result:
                print '保存自启动配置失败'
                wx.MessageBox(''.join(result), '保存自启动失败')
        else:
            print '修改失败'
            wx.MessageBox(
                dev_name + '操作失败\n' + ''.join(result),
                '操作ip失败'
            )

    def click_add(self, event):
        print '点击了增加'
        add_ip_win = GetIPAddrdialog(self)
        result = add_ip_win.show_and_get_new_ip()
        #if user click 'cancel(取消)', then pass
        if not result:
            return 0
        #if user input nothing, and pass.
        if result[0] == '' and result[1] == '/':
            pass
        else:
            self.__ip_info_to_str_list([result])
            self.edit_ip_list.append(('add', result))

    def click_del(self, event):
        print '点击了删除'
        if self.listbox_ip_list.GetSelection() == 0:
            wx.MessageBox(
                '你连这个地址都敢删除，\n弄坏了别来找我。\n反正不关我的事！\n(ー`´ー)',
                '你作死！！'
            )
            wx.MessageBox(
                '怕了吧?后悔还来得及，\n还不赶紧点【取消】?\no(￣ヘ￣o＃)',
                '还作死？'
            )
        #get the info, that will bean deleted.
        #if it did not have a dev name, use default dev name
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
        print '点击了修改'
        #get the ip info from listbox choose
        ip_info = self.listbox_ip_list.GetStringSelection().split()
        if len(ip_info) == 1:
            dev_name = self.default_dev_name.encode('utf-8')
            ip_and_mask = ip_info[0].encode('utf-8')
        else:
            dev_name = ip_info[0].encode('utf-8')
            ip_and_mask = ip_info[1].encode('utf-8')

        #then init a dialog window, and show the ip info.
        add_ip_win = GetIPAddrdialog(self)
        result = add_ip_win.show_and_get_new_ip(dev_name, ip_and_mask)

        #if user click 'cancel(取消)', then pass
        if not result:
            return 0
        #if user input nothing, and pass.
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

class GetIPAddrdialog(basewin.BaseGetIPAddrdialog):

    def show_and_get_new_ip(self, dev_name=None, ip_and_mask=None):
        #if it has any arguments, that means dialog be use for ip addr modify
        if dev_name:
            self.__init_modify_text(dev_name, ip_and_mask)
        #then show the dialog window.
        result = self.ShowModal()
        if result == wx.ID_OK:
            print '点击了确定'
            dev_name = str(self.text_dev_name.GetValue())
            ip_addr = str(self.text_ip_addr.GetValue())
            mask = str(self.text_mask.GetValue())
            return (dev_name, ip_addr+'/'+mask)
        elif result == wx.ID_CANCEL:
            print '点击了取消'

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
        #init all the server's service into list
        self.checklistbox_service.Clear()
        self.checklistbox_service.AppendItems(self.ntsysv_name_list)
        self.checklistbox_service.SetCheckedStrings(self.ntsysv_on_old)
        #if server did not has the xinetd service, hide the listbox and return
        try:
            type(self.xinetd_name_list)
        except NameError:
            self.label_xinetd.Hide()
            self.checklistbox_winetd.Hide()
            self.SetSize((215, 398))
            return 0
        #init all the xinetd service into listbox.
        self.SetSize((215, 520))
        self.checklistbox_winetd.Clear()
        self.checklistbox_winetd.AppendItems(self.xinetd_name_list)
        self.checklistbox_winetd.SetCheckedStrings(self.xinetd_on_old)

    #enforce any information from remote service
    def __enforce_service_info(self):
        ntsysv_info, xinetd_info = self.server.get_chkconfig()
        self.ntsysv_name_list = []
        self.ntsysv_on_old = []
        #init service list from remote server data
        for serv_info in ntsysv_info:
            self.ntsysv_name_list.append(serv_info[0])
            if serv_info[1] == 'on':
                self.ntsysv_on_old.append(serv_info[0])
        #init xinetd list fron data
        #if server did not has the xinetd service, return
        if not xinetd_info:
            return 0
        #if server has any xinetd service, then go on.
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
        #pick up the service that been set 'on'
        set_on_service = [name for name in ntsysv_on_new if name not in self.ntsysv_on_old]
        #pick up the service that been set 'off'
        set_off_service = [name for name in self.ntsysv_on_old if name not in ntsysv_on_new]
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
        print '点击了确定'
        self.__enforce_edit_service()
        self.Destroy()

    def click_cancel(self, event):
        print '点击了取消'
        self.Destroy()

    def double_click_service(self, event):
        print '双击了！'
        service_name = self.checklistbox_service.GetStringSelection().encode('utf-8')
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
        print '点击了ip地址'
        network_win = NetworkWindow(self)
        network_win.Show()
        network_win.init_network_window(self.server)
        network_win.Destroy

    def click_route(self, event):
        print '点击了路由表'
        route_win = RouteWindow(self)
        route_win.Show()

    def click_ntsysv(self, event):
        print '点击了系统服务'
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

