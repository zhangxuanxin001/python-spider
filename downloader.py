# -*- coding: UTF-8 -*-
import requests
from contextlib import closing
import wx
import wx.xrc


class Frame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(300, 100), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_static = wx.StaticText(self, wx.ID_ANY, u"下载链接", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_static.Wrap(-1)
        fgSizer2.Add(self.m_static, 0, wx.ALL, 5)

        self.m_input = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_input, 0, wx.ALL, 5)

        fgSizer1.Add(fgSizer2, 1, wx.EXPAND, 5)

        self.m_start = wx.Button(self, wx.ID_ANY, u"开始下载", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.m_start, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer2.Add(fgSizer1, 1, wx.EXPAND, 5)

        self.m_gauge1 = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.m_gauge1.SetValue(0)
        bSizer2.Add(self.m_gauge1, 0, wx.ALL, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_start.Bind(wx.EVT_BUTTON, self.start_click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def start_click(self, event):
        event.Skip()


class MianWindow(Frame):
    def start_click(self, event):
        url = self.m_input.GetValue()
        filename = url.split('/')[-1]  # 文件名取以"/"分割取最后一个
        i = 1
        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])  # 文件大小
            if response.status_code == 200:
                print('文件大小:%0.2f KB' % (content_size / chunk_size))
                with open(filename, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        self.m_gauge1.SetValue(i * 100.0 * chunk_size / content_size)  # 显示进度条
                        i += 1
            else:
                print('链接异常')
        print("下载完成")


if __name__ == '__main__':
    app = wx.App()
    main_win = MianWindow(None)
    main_win.Show()
    app.MainLoop()
