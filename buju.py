import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
# 实例化创建应用程序窗口
root = ttk.Window(
    title="bodyMotion",  # 设置窗口的标题
    themename="cosmo",  # 设置主题
    size=(1200, 945),  # 窗口的大小
    position=(700, 300),  # 窗口所在的位置
    minsize=(0, 0),  # 窗口的最小宽高
    maxsize=(10000, 5000),  # 窗口的最大宽高
    alpha=1,  # 设置窗口的透明度(0.0完全透明）
)


# 在窗口上创建一个菜单栏（最上方的菜单栏横条）
menubar = ttk.Menu(root)

# 摄像头权限
def question():
    Messagebox.ok("bodyMotion将获取调用摄像头的权限。", "访问权限", True)  # 内容，标题，提示音
    import bodyMotion
# 启动
menubar.add_cascade(label='启动', command=question)

# 设置
filemenu = ttk.Menu(menubar)
# 添加一个菜单项
menubar.add_cascade(label='设置', menu=filemenu)
# 和上面定义菜单一样，不过此处是在设置上创建一个空的菜单
submenu = ttk.Menu(filemenu)
# 添加一个展开下拉菜单，并把下面的子菜单嵌入给它
filemenu.add_cascade(label='个性化', menu=submenu, underline=0)
# 定义一个子菜单条
submenu.add_command(label="背景颜色")
submenu.add_command(label="字体大小")
submenu.add_command(label="透明度")

# 查找
elsemenu = ttk.Menu(menubar)
menubar.add_cascade(label='查找', menu=elsemenu)
elsemenu.add_command(label="上一个")
elsemenu.add_command(label="下一个")
elsemenu.add_command(label="文字替换")

# 选项
othermenu = ttk.Menu(menubar)
menubar.add_cascade(label='选项', menu=othermenu)
othermenu.add_command(label="显示")
othermenu.add_command(label="语言")
othermenu.add_command(label="高级选项")
# 添加一条分割线
othermenu.add_separator()
othermenu.add_command(label="自定义功能")

# 帮助
def connect():
    Messagebox.okcancel(message='联系方式：123xxxx5678')
help = ttk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='帮助', menu=help)
help.add_command(label='联系我们', command=connect)

# 退出
menubar.add_cascade(label='退出', command=root.quit)


# 将菜单配置给窗口
root.config(menu=menubar)

root.mainloop()