# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class BaseLoginDialog
###########################################################################

class BaseLoginDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"登陆窗", pos = wx.DefaultPosition, size = wx.Size( 241,264 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer2 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.label_ip_addr = wx.StaticText( self, wx.ID_ANY, u"服务器IP：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.label_ip_addr.Wrap( -1 )
		gSizer2.Add( self.label_ip_addr, 0, wx.ALL, 5 )
		
		self.text_ip_addr = wx.TextCtrl( self, wx.ID_ANY, u"127.0.0.1", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer2.Add( self.text_ip_addr, 0, wx.ALL, 5 )
		
		self.label_port = wx.StaticText( self, wx.ID_ANY, u"端口:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.label_port.Wrap( -1 )
		gSizer2.Add( self.label_port, 0, wx.ALL, 5 )
		
		self.text_port = wx.TextCtrl( self, wx.ID_ANY, u"2222", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gSizer2.Add( self.text_port, 0, wx.ALL, 5 )
		
		self.label_user_name = wx.StaticText( self, wx.ID_ANY, u"用户名：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.label_user_name.Wrap( -1 )
		gSizer2.Add( self.label_user_name, 0, wx.ALL, 5 )
		
		self.text_user_name = wx.TextCtrl( self, wx.ID_ANY, u"lenovo", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer2.Add( self.text_user_name, 0, wx.ALL, 5 )
		
		self.label_password = wx.StaticText( self, wx.ID_ANY, u"密码：", wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.label_password.Wrap( -1 )
		gSizer2.Add( self.label_password, 0, wx.ALL, 5 )
		
		self.text_password = wx.TextCtrl( self, wx.ID_ANY, u"lenovopassword", wx.DefaultPosition, wx.Size( 100,-1 ), wx.TE_PASSWORD )
		gSizer2.Add( self.text_password, 0, wx.ALL, 5 )
		
		bSizer2.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		m_sdbSizer4 = wx.StdDialogButtonSizer()
		self.m_sdbSizer4OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer4.AddButton( self.m_sdbSizer4OK )
		self.m_sdbSizer4Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer4.AddButton( self.m_sdbSizer4Cancel )
		m_sdbSizer4.Realize();
		bSizer2.Add( m_sdbSizer4, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_sdbSizer4Cancel.Bind( wx.EVT_BUTTON, self.click_cancel )
		self.m_sdbSizer4OK.Bind( wx.EVT_BUTTON, self.click_login )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def click_cancel( self, event ):
		event.Skip()
	
	def click_login( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseMainWindow
###########################################################################

class BaseMainWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 292,400 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer4 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.label_ip = wx.StaticText( self, wx.ID_ANY, u"ip地址:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_ip.Wrap( -1 )
		fgSizer4.Add( self.label_ip, 0, wx.ALL, 5 )
		
		self.text_ip_addr = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TE_READONLY )
		fgSizer4.Add( self.text_ip_addr, 0, wx.ALL, 5 )
		
		self.label_sys_release = wx.StaticText( self, wx.ID_ANY, u"系统版本:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_sys_release.Wrap( -1 )
		fgSizer4.Add( self.label_sys_release, 0, wx.ALL, 5 )
		
		self.text_sys_reslease = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 180,-1 ), wx.TE_READONLY )
		fgSizer4.Add( self.text_sys_reslease, 0, wx.ALL, 5 )
		
		self.label_hostname = wx.StaticText( self, wx.ID_ANY, u"主机名：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_hostname.Wrap( -1 )
		fgSizer4.Add( self.label_hostname, 0, wx.ALL, 5 )
		
		self.text_hostname = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_READONLY )
		fgSizer4.Add( self.text_hostname, 0, wx.ALL, 5 )
		
		self.label_iptables = wx.StaticText( self, wx.ID_ANY, u"防火墙：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_iptables.Wrap( -1 )
		fgSizer4.Add( self.label_iptables, 0, wx.ALL, 5 )
		
		gbSizer7 = wx.GridBagSizer( 0, 0 )
		gbSizer7.SetFlexibleDirection( wx.BOTH )
		gbSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.text_iptables = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer7.Add( self.text_iptables, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.button_iptable_control = wx.Button( self, wx.ID_ANY, u"修改", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.button_iptable_control, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		fgSizer4.Add( gbSizer7, 1, wx.EXPAND, 5 )
		
		self.label_ip_forward = wx.StaticText( self, wx.ID_ANY, u"ip转发：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_ip_forward.Wrap( -1 )
		fgSizer4.Add( self.label_ip_forward, 0, wx.ALL, 5 )
		
		gbSizer8 = wx.GridBagSizer( 0, 0 )
		gbSizer8.SetFlexibleDirection( wx.BOTH )
		gbSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.text_ip_forward = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer8.Add( self.text_ip_forward, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		choice_ip_forwardChoices = [ u"关闭", u"打开" ]
		self.choice_ip_forward = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_ip_forwardChoices, 0 )
		self.choice_ip_forward.SetSelection( 0 )
		gbSizer8.Add( self.choice_ip_forward, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		fgSizer4.Add( gbSizer8, 1, wx.EXPAND, 5 )
		
		self.lable_selinux = wx.StaticText( self, wx.ID_ANY, u"selinux:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lable_selinux.Wrap( -1 )
		fgSizer4.Add( self.lable_selinux, 0, wx.ALL, 5 )
		
		gbSizer9 = wx.GridBagSizer( 0, 0 )
		gbSizer9.SetFlexibleDirection( wx.BOTH )
		gbSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.text_selinux = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer9.Add( self.text_selinux, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		choice_selinuxChoices = [ u"enforcing", u"permissive", u"disabled" ]
		self.choice_selinux = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_selinuxChoices, 0 )
		self.choice_selinux.SetSelection( 0 )
		gbSizer9.Add( self.choice_selinux, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		fgSizer4.Add( gbSizer9, 1, wx.EXPAND, 5 )
		
		self.button_network = wx.Button( self, wx.ID_ANY, u"IP地址", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.button_network, 0, wx.ALL, 5 )
		
		self.button_ntsysv = wx.Button( self, wx.ID_ANY, u"系统服务", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.button_ntsysv, 0, wx.ALL, 5 )
		
		self.button_route = wx.Button( self, wx.ID_ANY, u"路由表", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.button_route, 0, wx.ALL, 5 )
		
		self.button_host = wx.Button( self, wx.ID_ANY, u"hosts修改", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.button_host, 0, wx.ALL, 5 )
		
		self.button_sys_info = wx.Button( self, wx.ID_ANY, u"系统监控", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.button_sys_info, 0, wx.ALL, 5 )
		
		self.button_bash = wx.Button( self, wx.ID_ANY, u"远程命令", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.button_bash, 0, wx.ALL, 5 )
		
		bSizer9.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.text_iptables.Bind( wx.EVT_LEFT_DCLICK, self.double_click_iptables )
		self.button_iptable_control.Bind( wx.EVT_BUTTON, self.click_iptable_control )
		self.choice_ip_forward.Bind( wx.EVT_CHOICE, self.choise_ip_forward_control )
		self.choice_selinux.Bind( wx.EVT_CHOICE, self.choice_selinux_control )
		self.button_network.Bind( wx.EVT_BUTTON, self.click_network )
		self.button_ntsysv.Bind( wx.EVT_BUTTON, self.click_ntsysv )
		self.button_route.Bind( wx.EVT_BUTTON, self.click_route )
		self.button_host.Bind( wx.EVT_BUTTON, self.click_hosts )
		self.button_sys_info.Bind( wx.EVT_BUTTON, self.click_system_info )
		self.button_bash.Bind( wx.EVT_BUTTON, self.click_bash )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def double_click_iptables( self, event ):
		event.Skip()
	
	def click_iptable_control( self, event ):
		event.Skip()
	
	def choise_ip_forward_control( self, event ):
		event.Skip()
	
	def choice_selinux_control( self, event ):
		event.Skip()
	
	def click_network( self, event ):
		event.Skip()
	
	def click_ntsysv( self, event ):
		event.Skip()
	
	def click_route( self, event ):
		event.Skip()
	
	def click_hosts( self, event ):
		event.Skip()
	
	def click_system_info( self, event ):
		event.Skip()
	
	def click_bash( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseNetworkWindow
###########################################################################

class BaseNetworkWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 519,296 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		gbSizer4 = wx.GridBagSizer( 0, 0 )
		gbSizer4.SetFlexibleDirection( wx.BOTH )
		gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gSizer6 = wx.GridSizer( 2, 2, 0, 0 )
		
		listbox_devChoices = []
		self.listbox_dev = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,100 ), listbox_devChoices, wx.LB_SINGLE )
		gSizer6.Add( self.listbox_dev, 0, wx.ALL, 5 )
		
		self.text_dev_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.text_dev_name.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		gSizer6.Add( self.text_dev_name, 0, wx.ALL, 5 )
		
		self.button_monitor = wx.Button( self, wx.ID_ANY, u"流量监控", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.button_monitor, 0, wx.ALL, 5 )
		
		gbSizer4.Add( gSizer6, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.label_mac = wx.StaticText( self, wx.ID_ANY, u"硬件地址：", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.label_mac.Wrap( -1 )
		bSizer11.Add( self.label_mac, 0, wx.ALL, 5 )
		
		self.label_mtu = wx.StaticText( self, wx.ID_ANY, u"mtu:", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.label_mtu.Wrap( -1 )
		bSizer11.Add( self.label_mtu, 0, wx.ALL, 5 )
		
		self.label_speed = wx.StaticText( self, wx.ID_ANY, u"接口速率：", wx.DefaultPosition, wx.Size( -1,25 ), 0 )
		self.label_speed.Wrap( -1 )
		bSizer11.Add( self.label_speed, 0, wx.ALL, 5 )
		
		self.label_ip_addr = wx.StaticText( self, wx.ID_ANY, u"IP地址：", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.label_ip_addr.Wrap( -1 )
		bSizer11.Add( self.label_ip_addr, 0, wx.ALL, 5 )
		
		gbSizer4.Add( bSizer11, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.text_mac = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_READONLY )
		bSizer12.Add( self.text_mac, 0, wx.ALL, 5 )
		
		self.text_mtu = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer12.Add( self.text_mtu, 0, wx.ALL, 5 )
		
		self.text_speed = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer12.Add( self.text_speed, 0, wx.ALL, 5 )
		
		self.text_ip_addr = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		bSizer12.Add( self.text_ip_addr, 0, wx.ALL, 5 )
		
		self.button_modify = wx.Button( self, wx.ID_ANY, u"修改", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.button_modify, 0, wx.ALL, 5 )
		
		gbSizer4.Add( bSizer12, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		bSizer10.Add( gbSizer4, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.listbox_dev.Bind( wx.EVT_LISTBOX, self.click_listbox_dev )
		self.button_monitor.Bind( wx.EVT_BUTTON, self.click_button_monitor )
		self.button_modify.Bind( wx.EVT_BUTTON, self.click_modify )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def click_listbox_dev( self, event ):
		event.Skip()
	
	def click_button_monitor( self, event ):
		event.Skip()
	
	def click_modify( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseHostsEditor
###########################################################################

class BaseHostsEditor ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"hosts编辑", pos = wx.DefaultPosition, size = wx.Size( 470,380 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer12 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.text_hosts = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 450,300 ), wx.TE_MULTILINE )
		fgSizer12.Add( self.text_hosts, 0, wx.ALL, 5 )
		
		
		fgSizer12.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		gbSizer7 = wx.GridBagSizer( 0, 0 )
		gbSizer7.SetFlexibleDirection( wx.BOTH )
		gbSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.button_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.button_ok, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.button_cancel = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.button_cancel, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		fgSizer12.Add( gbSizer7, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer12 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_ok.Bind( wx.EVT_BUTTON, self.click_ok )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.click_cancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def click_ok( self, event ):
		event.Skip()
	
	def click_cancel( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseDevMonitor
###########################################################################

class BaseDevMonitor ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"网络监控窗", pos = wx.DefaultPosition, size = wx.Size( 411,266 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer14 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer15 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText43 = wx.StaticText( self, wx.ID_ANY, u"收取数据：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )
		fgSizer15.Add( self.m_staticText43, 0, wx.ALL, 5 )
		
		self.label_receive_bytes = wx.StaticText( self, wx.ID_ANY, u"----------------------", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_receive_bytes.Wrap( -1 )
		fgSizer15.Add( self.label_receive_bytes, 0, wx.ALL, 5 )
		
		self.m_staticText47 = wx.StaticText( self, wx.ID_ANY, u"收取速率：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )
		fgSizer15.Add( self.m_staticText47, 0, wx.ALL, 5 )
		
		self.label_receive_speed = wx.StaticText( self, wx.ID_ANY, u"----------------------", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_receive_speed.Wrap( -1 )
		fgSizer15.Add( self.label_receive_speed, 0, wx.ALL, 5 )
		
		fgSizer14.Add( fgSizer15, 1, wx.EXPAND, 5 )
		
		fgSizer17 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer17.SetFlexibleDirection( wx.BOTH )
		fgSizer17.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText45 = wx.StaticText( self, wx.ID_ANY, u"发送数据：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )
		fgSizer17.Add( self.m_staticText45, 0, wx.ALL, 5 )
		
		self.label_transmit_bytes = wx.StaticText( self, wx.ID_ANY, u"---------------", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_transmit_bytes.Wrap( -1 )
		fgSizer17.Add( self.label_transmit_bytes, 0, wx.ALL, 5 )
		
		self.m_staticText49 = wx.StaticText( self, wx.ID_ANY, u"发送速率：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )
		fgSizer17.Add( self.m_staticText49, 0, wx.ALL, 5 )
		
		self.label_transmit_speed = wx.StaticText( self, wx.ID_ANY, u"---------------", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_transmit_speed.Wrap( -1 )
		fgSizer17.Add( self.label_transmit_speed, 0, wx.ALL, 5 )
		
		fgSizer14.Add( fgSizer17, 1, wx.EXPAND, 5 )
		
		bSizer17.Add( fgSizer14, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer17 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class BaseDevModifyDialog
###########################################################################

class BaseDevModifyDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"ip地址管理", pos = wx.DefaultPosition, size = wx.Size( 380,280 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer3 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.label_ip_list = wx.StaticText( self, wx.ID_ANY, u"地址列表：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_ip_list.Wrap( -1 )
		fgSizer3.Add( self.label_ip_list, 0, wx.ALL, 5 )
		
		listbox_ip_listChoices = []
		self.listbox_ip_list = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,150 ), listbox_ip_listChoices, wx.LB_SINGLE )
		fgSizer3.Add( self.listbox_ip_list, 0, wx.ALL, 5 )
		
		fgSizer2.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.button_add = wx.Button( self, wx.ID_ANY, u"增加", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.button_add, 0, wx.ALL, 5 )
		
		self.button_modify = wx.Button( self, wx.ID_ANY, u"修改", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.button_modify, 0, wx.ALL, 5 )
		
		self.button_del = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.button_del, 0, wx.ALL, 5 )
		
		fgSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer9.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		m_sdbSizer5 = wx.StdDialogButtonSizer()
		self.m_sdbSizer5OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer5.AddButton( self.m_sdbSizer5OK )
		self.m_sdbSizer5Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer5.AddButton( self.m_sdbSizer5Cancel )
		m_sdbSizer5.Realize();
		bSizer9.Add( m_sdbSizer5, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.listbox_ip_list.Bind( wx.EVT_LISTBOX, self.click_list_box )
		self.listbox_ip_list.Bind( wx.EVT_LISTBOX_DCLICK, self.double_click_list_box )
		self.button_add.Bind( wx.EVT_BUTTON, self.click_add )
		self.button_modify.Bind( wx.EVT_BUTTON, self.click_modify )
		self.button_del.Bind( wx.EVT_BUTTON, self.click_del )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def click_list_box( self, event ):
		event.Skip()
	
	def double_click_list_box( self, event ):
		event.Skip()
	
	def click_add( self, event ):
		event.Skip()
	
	def click_modify( self, event ):
		event.Skip()
	
	def click_del( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseGetIPAddrdialog
###########################################################################

class BaseGetIPAddrdialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"ip地址配置窗口", pos = wx.DefaultPosition, size = wx.Size( 344,225 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer5 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.label_dev_name = wx.StaticText( self, wx.ID_ANY, u"驱动器名：\n(例如: eth0:1)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_dev_name.Wrap( -1 )
		fgSizer5.Add( self.label_dev_name, 0, wx.ALL, 5 )
		
		self.text_dev_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		fgSizer5.Add( self.text_dev_name, 0, wx.ALL, 5 )
		
		self.label_ip_addr = wx.StaticText( self, wx.ID_ANY, u"IP地址：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_ip_addr.Wrap( -1 )
		fgSizer5.Add( self.label_ip_addr, 0, wx.ALL, 5 )
		
		self.text_ip_addr = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer5.Add( self.text_ip_addr, 0, wx.ALL, 5 )
		
		self.label_netmask = wx.StaticText( self, wx.ID_ANY, u"子网掩码：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_netmask.Wrap( -1 )
		fgSizer5.Add( self.label_netmask, 0, wx.ALL, 5 )
		
		self.text_mask = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		fgSizer5.Add( self.text_mask, 0, wx.ALL, 5 )
		
		bSizer4.Add( fgSizer5, 1, wx.EXPAND, 5 )
		
		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();
		bSizer4.Add( m_sdbSizer3, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class BaseRouteWindow
###########################################################################

class BaseRouteWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"系统路由状态", pos = wx.DefaultPosition, size = wx.Size( 423,435 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.label_kernel = wx.StaticText( self, wx.ID_ANY, u"直达路由:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_kernel.Wrap( -1 )
		bSizer6.Add( self.label_kernel, 0, wx.ALL, 5 )
		
		self.label_kernel_tips = wx.StaticText( self, wx.ID_ANY, u"                   网段             |     接口     |     接口地址", wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.label_kernel_tips.Wrap( -1 )
		bSizer6.Add( self.label_kernel_tips, 0, wx.ALL, 5 )
		
		listbox_kernelChoices = []
		self.listbox_kernel = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), listbox_kernelChoices, wx.LB_SINGLE )
		bSizer6.Add( self.listbox_kernel, 0, wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer6.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.label_route = wx.StaticText( self, wx.ID_ANY, u"路由:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_route.Wrap( -1 )
		bSizer6.Add( self.label_route, 0, wx.ALL, 5 )
		
		self.label_route_tips = wx.StaticText( self, wx.ID_ANY, u"                      网段                 |     接口     |     网关地址", wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.label_route_tips.Wrap( -1 )
		bSizer6.Add( self.label_route_tips, 0, wx.ALL, 5 )
		
		fgSizer12 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		listbox_routeChoices = []
		self.listbox_route = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,100 ), listbox_routeChoices, wx.LB_SINGLE )
		fgSizer12.Add( self.listbox_route, 0, wx.ALL, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.button_add = wx.Button( self, wx.ID_ANY, u"增加", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.button_add, 0, wx.ALL, 5 )
		
		self.button_modify = wx.Button( self, wx.ID_ANY, u"修改", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.button_modify, 0, wx.ALL, 5 )
		
		self.button_del = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.button_del, 0, wx.ALL, 5 )
		
		fgSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer6.Add( fgSizer12, 1, wx.EXPAND, 5 )
		
		gbSizer4 = wx.GridBagSizer( 0, 0 )
		gbSizer4.SetFlexibleDirection( wx.BOTH )
		gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.button_apply = wx.Button( self, wx.ID_ANY, u"应用", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer4.Add( self.button_apply, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.button_cancel = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer4.Add( self.button_cancel, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		bSizer6.Add( gbSizer4, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_add.Bind( wx.EVT_BUTTON, self.click_add )
		self.button_modify.Bind( wx.EVT_BUTTON, self.click_modify )
		self.button_del.Bind( wx.EVT_BUTTON, self.click_del )
		self.button_apply.Bind( wx.EVT_BUTTON, self.click_apply )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.click_cancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def click_add( self, event ):
		event.Skip()
	
	def click_modify( self, event ):
		event.Skip()
	
	def click_del( self, event ):
		event.Skip()
	
	def click_apply( self, event ):
		event.Skip()
	
	def click_cancel( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseGetRoutedialog
###########################################################################

class BaseGetRoutedialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"静态路由配置窗口", pos = wx.DefaultPosition, size = wx.Size( 336,204 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer5 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.label_net = wx.StaticText( self, wx.ID_ANY, u"路由目网段：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_net.Wrap( -1 )
		gSizer5.Add( self.label_net, 0, wx.ALL, 5 )
		
		self.text_net = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer5.Add( self.text_net, 0, wx.ALL, 5 )
		
		self.label_mask = wx.StaticText( self, wx.ID_ANY, u"网络子网掩码：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_mask.Wrap( -1 )
		gSizer5.Add( self.label_mask, 0, wx.ALL, 5 )
		
		self.text_mask = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer5.Add( self.text_mask, 0, wx.ALL, 5 )
		
		self.label_gateway = wx.StaticText( self, wx.ID_ANY, u"网关IP地址：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_gateway.Wrap( -1 )
		gSizer5.Add( self.label_gateway, 0, wx.ALL, 5 )
		
		self.text_gateway = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer5.Add( self.text_gateway, 0, wx.ALL, 5 )
		
		bSizer4.Add( gSizer5, 1, wx.EXPAND, 5 )
		
		m_sdbSizer4 = wx.StdDialogButtonSizer()
		self.m_sdbSizer4OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer4.AddButton( self.m_sdbSizer4OK )
		self.m_sdbSizer4Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer4.AddButton( self.m_sdbSizer4Cancel )
		m_sdbSizer4.Realize();
		bSizer4.Add( m_sdbSizer4, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class BaseSysServiceWindow
###########################################################################

class BaseSysServiceWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"系统服务", pos = wx.DefaultPosition, size = wx.Size( 215,500 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u" 启用 |  服务名", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		bSizer8.Add( self.m_staticText26, 0, wx.ALL, 5 )
		
		checklistbox_serviceChoices = [ u"1" ];
		self.checklistbox_service = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,300 ), checklistbox_serviceChoices, wx.LB_NEEDED_SB )
		self.checklistbox_service.SetToolTipString( u"勾选为自启动服务。\n双击服务名可以直接管理服务。\n人均选择哦！O(∩_∩)O~" )
		
		bSizer8.Add( self.checklistbox_service, 0, wx.ALL, 5 )
		
		self.label_xinetd = wx.StaticText( self, wx.ID_ANY, u"启用 | xinetd服务名", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_xinetd.Wrap( -1 )
		bSizer8.Add( self.label_xinetd, 0, wx.ALL, 5 )
		
		checklistbox_winetdChoices = [ u"1" ];
		self.checklistbox_winetd = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,100 ), checklistbox_winetdChoices, wx.LB_NEEDED_SB )
		self.checklistbox_winetd.SetToolTipString( u"xinetd能看不能碰哦，勾上代表已经自启动了。\n想启动新的服务？自己想办法吧……\nO(∩_∩)O~" )
		
		bSizer8.Add( self.checklistbox_winetd, 0, wx.ALL, 5 )
		
		gbSizer3 = wx.GridBagSizer( 0, 0 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.button_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.button_ok, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.button_cancel = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.button_cancel, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		bSizer8.Add( gbSizer3, 1, wx.EXPAND, 5 )
		
		bSizer13.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer13 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.checklistbox_service.Bind( wx.EVT_LISTBOX_DCLICK, self.double_click_service )
		self.button_ok.Bind( wx.EVT_BUTTON, self.click_ok )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.click_cancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def double_click_service( self, event ):
		event.Skip()
	
	def click_ok( self, event ):
		event.Skip()
	
	def click_cancel( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseServiceControl
###########################################################################

class BaseServiceControl ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"服务控制", pos = wx.DefaultPosition, size = wx.Size( 315,194 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, u"服务状态显示：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		bSizer14.Add( self.m_staticText28, 0, wx.ALL, 5 )
		
		self.text_status = wx.TextCtrl( self, wx.ID_ANY, u"123123123", wx.DefaultPosition, wx.Size( 300,-1 ), wx.TE_MULTILINE|wx.TE_READONLY )
		self.text_status.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
		self.text_status.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		bSizer14.Add( self.text_status, 0, wx.ALL, 5 )
		
		gbSizer4 = wx.GridBagSizer( 0, 0 )
		gbSizer4.SetFlexibleDirection( wx.BOTH )
		gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.button_start = wx.Button( self, wx.ID_ANY, u"启用服务", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer4.Add( self.button_start, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.button_stop = wx.Button( self, wx.ID_ANY, u"停止服务", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer4.Add( self.button_stop, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.button_status = wx.Button( self, wx.ID_ANY, u"查看服务状态", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer4.Add( self.button_status, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		bSizer14.Add( gbSizer4, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer14 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_start.Bind( wx.EVT_BUTTON, self.click_start )
		self.button_stop.Bind( wx.EVT_BUTTON, self.click_stop )
		self.button_status.Bind( wx.EVT_BUTTON, self.click_status )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def click_start( self, event ):
		event.Skip()
	
	def click_stop( self, event ):
		event.Skip()
	
	def click_status( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseSystemInfoWindow
###########################################################################

class BaseSystemInfoWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"系统信息", pos = wx.DefaultPosition, size = wx.Size( 441,354 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer7 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer10 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, u"系统时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		fgSizer10.Add( self.m_staticText29, 0, wx.ALL, 5 )
		
		self.text_time_value = wx.TextCtrl( self, wx.ID_ANY, u"time", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer10.Add( self.text_time_value, 0, wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer10.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer10.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText46 = wx.StaticText( self, wx.ID_ANY, u"内存使用：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )
		fgSizer10.Add( self.m_staticText46, 0, wx.ALL, 5 )
		
		
		fgSizer10.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText48 = wx.StaticText( self, wx.ID_ANY, u"总内存：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText48.Wrap( -1 )
		fgSizer10.Add( self.m_staticText48, 0, wx.ALL, 5 )
		
		self.text_memory_size = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer10.Add( self.text_memory_size, 0, wx.ALL, 5 )
		
		self.m_staticText47 = wx.StaticText( self, wx.ID_ANY, u"空闲量：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )
		fgSizer10.Add( self.m_staticText47, 0, wx.ALL, 5 )
		
		self.text_memory_free = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer10.Add( self.text_memory_free, 0, wx.ALL, 5 )
		
		bSizer16.Add( fgSizer10, 1, wx.EXPAND, 5 )
		
		fgSizer11 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer11.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer11.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.label_cpu = wx.StaticText( self, wx.ID_ANY, u"cpu使用：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_cpu.Wrap( -1 )
		fgSizer11.Add( self.label_cpu, 0, wx.ALL, 5 )
		
		self.gauge_cpu_persent = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 120,-1 ), wx.GA_HORIZONTAL )
		self.gauge_cpu_persent.SetValue( 10 ) 
		fgSizer11.Add( self.gauge_cpu_persent, 0, wx.ALL, 5 )
		
		self.m_staticText35 = wx.StaticText( self, wx.ID_ANY, u"用户占用：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )
		fgSizer11.Add( self.m_staticText35, 0, wx.ALL, 5 )
		
		self.text_usr_cpu = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer11.Add( self.text_usr_cpu, 0, wx.ALL, 5 )
		
		self.m_staticText361 = wx.StaticText( self, wx.ID_ANY, u"系统占用：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText361.Wrap( -1 )
		fgSizer11.Add( self.m_staticText361, 0, wx.ALL, 5 )
		
		self.text_sys_cpu = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer11.Add( self.text_sys_cpu, 0, wx.ALL, 5 )
		
		self.m_staticText44 = wx.StaticText( self, wx.ID_ANY, u"剩余比：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )
		fgSizer11.Add( self.m_staticText44, 0, wx.ALL, 5 )
		
		self.text_free_cpu = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer11.Add( self.text_free_cpu, 0, wx.ALL, 5 )
		
		bSizer16.Add( fgSizer11, 1, wx.EXPAND, 5 )
		
		fgSizer7.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		fgSizer9 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer9.SetFlexibleDirection( wx.BOTH )
		fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gbSizer6 = wx.GridBagSizer( 0, 0 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		listbox_hard_diskChoices = []
		self.listbox_hard_disk = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 125,100 ), listbox_hard_diskChoices, 0 )
		gbSizer6.Add( self.listbox_hard_disk, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.gauge_used_persent = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL|wx.GA_VERTICAL )
		self.gauge_used_persent.SetValue( 10 ) 
		gbSizer6.Add( self.gauge_used_persent, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		fgSizer9.Add( gbSizer6, 1, wx.EXPAND, 5 )
		
		
		fgSizer9.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		fgSizer91 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer91.SetFlexibleDirection( wx.BOTH )
		fgSizer91.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1000 = wx.StaticText( self, wx.ID_ANY, u"总容量:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1000.Wrap( -1 )
		fgSizer91.Add( self.m_staticText1000, 0, wx.ALL, 5 )
		
		self.text_size = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer91.Add( self.text_size, 0, wx.ALL, 5 )
		
		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"已使用空间：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		fgSizer91.Add( self.m_staticText31, 0, wx.ALL, 5 )
		
		self.text_used = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer91.Add( self.text_used, 0, wx.ALL, 5 )
		
		self.m_staticText32 = wx.StaticText( self, wx.ID_ANY, u"剩余空间：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		fgSizer91.Add( self.m_staticText32, 0, wx.ALL, 5 )
		
		self.text_avail = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer91.Add( self.text_avail, 0, wx.ALL, 5 )
		
		self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"占用百分比：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		fgSizer91.Add( self.m_staticText41, 0, wx.ALL, 5 )
		
		self.text_use_persent = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer91.Add( self.text_use_persent, 0, wx.ALL, 5 )
		
		self.m_staticText33 = wx.StaticText( self, wx.ID_ANY, u"挂载点：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )
		fgSizer91.Add( self.m_staticText33, 0, wx.ALL, 5 )
		
		self.text_mounted = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer91.Add( self.text_mounted, 0, wx.ALL, 5 )
		
		fgSizer9.Add( fgSizer91, 1, wx.EXPAND, 5 )
		
		fgSizer7.Add( fgSizer9, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer7 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.listbox_hard_disk.Bind( wx.EVT_LISTBOX, self.show_singel_hard_disk_info )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def show_singel_hard_disk_info( self, event ):
		event.Skip()
	

###########################################################################
## Class BaseBashIminatorWindow
###########################################################################

class BaseBashIminatorWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"远程命令窗", pos = wx.DefaultPosition, size = wx.Size( 623,479 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.text_bash_show = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 600,400 ), wx.TE_MULTILINE|wx.TE_READONLY )
		self.text_bash_show.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		self.text_bash_show.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer17.Add( self.text_bash_show, 0, wx.ALL, 5 )
		
		gbSizer10 = wx.GridBagSizer( 0, 0 )
		gbSizer10.SetFlexibleDirection( wx.BOTH )
		gbSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"命令输入：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		gbSizer10.Add( self.m_staticText51, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.text_cmd_input = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.TE_PROCESS_ENTER )
		gbSizer10.Add( self.text_cmd_input, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.button_ok = wx.Button( self, wx.ID_ANY, u"执行", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer10.Add( self.button_ok, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		bSizer17.Add( gbSizer10, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer17 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.text_cmd_input.Bind( wx.EVT_TEXT_ENTER, self.enter_cmd )
		self.button_ok.Bind( wx.EVT_BUTTON, self.click_button_ok )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def enter_cmd( self, event ):
		event.Skip()
	
	def click_button_ok( self, event ):
		event.Skip()
	

