# -*- coding: utf-8 -*-
"""
Created on 2018/10/24 08:00:36

@author: modabao
"""


import tkinter as tk
from tkinter import filedialog  # 必须单独导入

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.io.shapereader as shpreader

from fy4a import FY4A_H5


class GUI(tk.Tk):
    """
    主窗口
    """
    def __init__(self):
        """
        构造初始界面
        """
        super().__init__()
        self.title("FY-4A")
        self.menubar = tk.Menu(self)  # 菜单栏
        self.__make_menubar()
        self.protocol("WM_DELETE_WINDOW", self.exit)
        # 功能区
        self.frame_info = tk.Frame(self)  # 左上信息区
        self.frame_channelbutton = tk.Frame(self)  # 左下通道按钮区
        self.frame_show = tk.Frame(self)  # 图片显示区
        # 左上信息区详细组件
        self.frame_info.label_latlon = tk.Label(self.frame_info,
                                                text="经纬度范围（经纬度为整数）\n"
                                                "lat_S, lat_N, lon_W, lon_E, step:")
        self.geo_range = tk.StringVar(self, "10, 54, 70, 140, 0.1")
        self.frame_info.entry_latlon = tk.Entry(self.frame_info,
                                                textvariable=self.geo_range)
        self.frame_channelbutton.channels = {}
        # self.frame_info.label_step = tk.Label(self.frame_info, text="插值步长：")
        # self.step = tk.StringVar(self, "0.05")
        # self.frame_info.entry_step = tk.Entry(self.frame_info,
        #                                       textvariable=self.step)
        # 调整各组件位置
        self.frame_show.pack(side="right", expand="yes", fill="y")
        self.frame_info.pack(side="top", expand="yes", fill="x")
        self.frame_channelbutton.pack(side="bottom", expand="yes", fill="x")
        self.frame_info.label_latlon.pack(side="top", expand="yes", fill="x")
        self.frame_info.entry_latlon.pack(side="top", expand="yes", fill="x")
        # self.frame_info.label_step.pack(side="left")
        # self.frame_info.entry_step.pack(side="right", expand="yes", fill="x")


    def __make_menubar(self):
        """
        创建菜单栏
        """
        # “文件”
        menu_file = tk.Menu(self.menubar, tearoff=0)
        menu_file.add_command(label="打开", command=self.__menu_open)
        menu_file.add_separator()  # 一个分隔符
        menu_file.add_command(label="关闭", command=self.__menu_close)
        # “帮助”
        menu_help = tk.Menu(self.menubar, tearoff=0)
        menu_help.add_command(label="关于", command=self.__menu_about)
        # 结合
        self.menubar.add_cascade(label="文件", menu=menu_file)
        self.menubar.add_cascade(label="帮助", menu=menu_help)
        # 显示
        self.config(menu=self.menubar)
        
    def __menu_open(self):
        """
        打开文件
        """
        if hasattr(self, "fy4a_h5"):
            self.__menu_close()
        h5name = filedialog.askopenfilename()  # 打开文件对话框
        if not h5name:
            return
        self.fy4a_h5 = FY4A_H5(h5name, channelnames=None)  # 可改进自选通道
        frame = self.frame_channelbutton
        for channelname in self.fy4a_h5.channelnames:
            frame.channels[channelname] = tk.Button(frame,
                                                    text=channelname,
                                                    command=lambda x=channelname: self.__button_draw(x))
            frame.channels[channelname].pack(side="top", expand="yes", fill="x")

    def __menu_about(self):
        """
        菜单栏“关于”
        """
        tk.messagebox.showinfo("关于", "作者：墨大宝\nVerion 0.1\n983248128@qq.com")

    def __menu_close(self):
        """
        关闭已打开的文件
        """
        if hasattr(self, "canvas"):
            del self.fy4a_h5
            self.ax.clear()
            for button in self.frame_channelbutton.channels.values():
                button.destroy()
        # self.frame_show.destroy()

    def __button_draw(self, channelname):
        """
        绘图逻辑
        """
        # 绘图准备
        PlateCarree = ccrs.PlateCarree()
        if hasattr(self, "canvas"):
            self.ax.clear()
        else:
            fig = plt.figure("fig", figsize=(6, 4), dpi=100)
            self.ax = plt.axes(projection=PlateCarree)
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_show)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            toolbar = NavigationToolbar2Tk(self.canvas, self.frame_show)
            toolbar.update()
        # 获取数据
        geo_range = self.geo_range.get()
        if self.fy4a_h5.channels[channelname] is None or self.fy4a_h5.geo_range != eval(geo_range):
            self.fy4a_h5.extract(channelname, geo_range=geo_range)
        channel = self.fy4a_h5.channels[channelname]
        # 绘图
        self.ax.add_geometries(provinces_geometrys, PlateCarree,
                               edgecolor='black', facecolor='None')
        lat_S, lat_N, lon_W, lon_E, step = self.fy4a_h5.geo_range
        halfstep = step / 2
        extent = [lon_W - halfstep, lon_E + halfstep,
                  lat_S - halfstep, lat_N + halfstep]
        im = self.ax.imshow(channel, cmap="gray", transform=PlateCarree, origin='upper',
                            extent=extent)
        self.ax.set_xticks(list(range(lon_W, lon_E+1, 10)), PlateCarree)
        self.ax.set_yticks(list(range(lat_S, lat_N+1, 10)), PlateCarree)
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        self.ax.xaxis.set_major_formatter(lon_formatter)
        self.ax.yaxis.set_major_formatter(lat_formatter)
        self.ax.coastlines()
        plt.colorbar(im, shrink=0.7)
        plt.title(channelname)
        self.canvas.draw()

    def exit(self):
        """
        退出
        """
        del self.fy4a_h5
        self.quit()  # 停止mainloop
        self.destroy()  # 销毁所有部件


if __name__ == '__main__':
    shpname = r"..\data\map\China_province"
    provinces_records = list(shpreader.Reader(shpname).records())
    provinces_geometrys = [x.geometry for x in provinces_records]
    app = GUI()
    app.mainloop()