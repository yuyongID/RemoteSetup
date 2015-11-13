#!/usr/bin/env python
#coding=UTF-8
import wx
import sys
import basewin
import commands

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

    def click_modify(self, event):
        print '点击了修改网络'
        dev_modify_win = DevModifyDialog(self)
        dev_modify_win.show_and_get_ip_restul()
        
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

    def show_and_get_ip_restul(self):
        result = self.ShowModal()
        if result == wx.ID_OK:
            print '点击了确定'
        elif result == wx.ID_CANCEL:
            print '点击了取消'
        
    def click_add(self, event):
        print '点击了增加'
        add_ip_win = GetIPAddrdialog(self)
        add_ip_win.show_and_get_new_ip()

    def click_del(self, event):
        print '点击了删除'

    def click_modify(self, event):
        print '点击了修改'
        add_ip_win = GetIPAddrdialog(self)
        add_ip_win.show_and_get_new_ip()

class GetIPAddrdialog(basewin.BaseGetIPAddrdialog):

    def show_and_get_new_ip(self):
        result = self.ShowModal()
        if result == wx.ID_OK:
            print '点击了确定'
        elif result == wx.ID_CANCEL:
            print '点击了取消'

class SysServiceWindow(basewin.BaseSysServiceWindow):

    def click_ok(self, event):
        print '点击了确定'

    def click_cancel(self, event):
        print '点击了取消'
        self.Destroy()


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

    def click_route(self, event):
        print '点击了路由表'
        route_win = RouteWindow(self)
        route_win.Show()

    def click_ntsysv(self, event):
        print '点击了系统服务'
        ntsysv_win = SysServiceWindow(self)
        ntsysv_win.Show()

if __name__ == '__main__':
    app = wx.App()
    main_win = MainWindow(None)
    main_win.call_login_window()
    main_win.connect_and_get_info()
    main_win.Show()
    app.MainLoop()

