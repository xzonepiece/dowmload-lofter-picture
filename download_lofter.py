# -*- coding: utf-8 -*-
"""
该程序可以从lofter上爬取图片
"""
import re
import requests
import wx
import os
os.mkdir('pic_lofter')
def pic_download(event):
    home_html = text_addr.GetValue()
    n = int(text_page.GetValue())-1
    html = requests.get(home_html).text
    post_url = re.findall(r'"img" href="(.*?)"',html,re.S)
    i = 1
    for post in post_url:
        post_html = requests.get(post).text
        pic_url = re.findall(r'img src="(.*?)"',post_html,re.S)
        for url in pic_url:
            if not re.search(r'imgsize',url) :
                print "now downloading: "+url
                pic = requests.get(url)
                fp = open('pic_lofter//' + str(i) + '.jpg','wb')
                fp.write(pic.content)
                fp.close()
                i += 1
                for j in range(n):
                    page_next = re.search(r'"next" href="(.*?)"',html,re.S).group(1)
                    page_html = home_html + '/'+ page_next
                    html = requests.get(page_html).text
                    post_url = re.findall(r'"img" href="(.*?)"',html,re.S)
                    for post in post_url:
                        post_html = requests.get(post).text
                        pic_url = re.findall(r'img src="(.*?)"',post_html,re.S)
                        for url in pic_url:
                            if not re.search(r'imgsize',url):
                                print "now downloading: "+url
                                pic = requests.get(url)
                                fp = open('pic_lofter//' + str(i) + '.jpg','wb')
                                fp.write(pic.content)
                                fp.close()
                                i += 1
    wx.MessageBox('Download Complete','Info',wx.OK|wx.ICON_INFORMATION)

# GUI界面

app = wx.App()
win = wx.Frame(None,title='Download the Pictures of LOFTER',size=(400,200))
bkg = wx.Panel(win)

font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
font.SetPointSize(9)

address = wx.StaticText(bkg,label='the Address of Blog:')
address.SetFont(font)
page_num = wx.StaticText(bkg,label='the Number of Pages:')
page_num.SetFont(font)
text_addr = wx.TextCtrl(bkg)
text_page = wx.TextCtrl(bkg)
loadButton = wx.Button(bkg,label='download',size=(100,50))
loadButton.Bind(wx.EVT_BUTTON,pic_download)

vbox = wx.BoxSizer(wx.VERTICAL)

hbox1 = wx.BoxSizer()
hbox1.Add(address,proportion=0,flag=wx.RIGHT,border=10)
hbox1.Add(text_addr,proportion=1)
vbox.Add(hbox1,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,border=10)

vbox.Add((-1,20))

hbox2 = wx.BoxSizer()
hbox2.Add(page_num,proportion=0,flag=wx.RIGHT,border=10)
hbox2.Add(text_page,proportion=1)
vbox.Add(hbox2,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=10)

vbox.Add((-1,20))

vbox.Add(loadButton,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=50)

bkg.SetSizer(vbox)
win.Show()
app.MainLoop()
