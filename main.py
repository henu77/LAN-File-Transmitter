import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


class FileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件传输应用")

        # 文件路径变量
        self.file_path = tk.StringVar()

        # 创建界面元素
        self.create_widgets()

    def create_widgets(self):
        # 选择文件按钮
        select_file_button = tk.Button(self.root, text="选择文件", command=self.select_file)
        select_file_button.pack(pady=10)

        # 显示文件路径的标签
        file_path_label = tk.Label(self.root, textvariable=self.file_path)
        file_path_label.pack(pady=10)

        # 输入IP地址和端口
        ip_label = tk.Label(self.root, text="IP 地址:")
        ip_label.pack()

        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack()

        port_label = tk.Label(self.root, text="端口:")
        port_label.pack()

        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        # 发送按钮
        send_button = tk.Button(self.root, text="发送文件", command=self.send_file)
        send_button.pack(pady=10)

    def select_file(self):
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename()

        # 更新文件路径变量
        self.file_path.set(file_path)

    def send_file(self):
        # 获取IP地址和端口
        ip_address = self.ip_entry.get()
        port = self.port_entry.get()

        # 获取文件路径
        file_path = self.file_path.get()

        # 在这里添加文件传输的代码，可以使用Socket等方式进行实现

        # 提示用户文件发送成功
        messagebox.showinfo("成功", "文件发送成功！")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferApp(root)
    root.mainloop()
