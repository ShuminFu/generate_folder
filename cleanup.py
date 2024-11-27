import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD


class FilePathApp:
    def __init__(self, master):
        self.master = master
        self.master.title("拖动文件获取路径")
        self.master.geometry("500x400")
        self.master.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        style.configure("TButton", font=("Helvetica", 12))
        style.configure("TRadiobutton", font=("Helvetica", 12), background="#f0f0f0")

        self.label = ttk.Label(master, text="请拖动文件或文件夹到此处")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(master, width=50)
        self.entry.pack(pady=10)

        self.operation_var = tk.StringVar(value="copy")

        self.copy_radio = ttk.Radiobutton(master, text="复制文件", variable=self.operation_var, value="copy")
        self.copy_radio.pack(pady=5)

        self.move_radio = ttk.Radiobutton(master, text="剪切文件", variable=self.operation_var, value="move")
        self.move_radio.pack(pady=5)

        self.start_button = ttk.Button(master, text="开始", command=self.process_files)
        self.start_button.pack(pady=10)

        self.target_label = ttk.Label(master, text="")
        self.target_label.pack(pady=10)

        self.text_frame = ttk.Frame(master)
        self.text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(self.text_frame, wrap=tk.WORD, height=10, font=("Helvetica", 10))
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area.config(yscrollcommand=self.scrollbar.set)

        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

    def update_target_dir(self, paths):
        if isinstance(paths, str):
            paths = [paths]

        # 使用集合来存储唯一的目标目录
        target_dirs = set()

        for path in paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    dir_name, file_name = os.path.split(path)
                    base_name = file_name.rsplit('_', 1)[0]
                    target_dir = os.path.join(dir_name, base_name)
                else:  # 文件夹情况
                    target_dir = path + "_processed"
                target_dirs.add(target_dir)

        if target_dirs:
            # 将集合转换为排序列表以保持显示顺序一致
            sorted_dirs = sorted(target_dirs)
            target_text = "目标目录:\n" + "\n".join(f"- {dir}" for dir in sorted_dirs)
            self.target_label.config(text=target_text)
        else:
            self.target_label.config(text="无效的路径")

    def drop(self, event):
        paths = event.data.split()  # 分割多个文件路径
        # 移除可能的花括号并处理每个路径
        paths = [path.strip('{}') for path in paths]

        # 将所有路径以分号分隔显示在输入框中
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ';'.join(paths))

        # 更新所有文件的目标目录显示
        self.update_target_dir(paths)

    def process_files(self):
        paths = self.entry.get().split(';')
        for path in paths:
            path = path.strip('{}')
            if not os.path.exists(path):
                self.log_message(f"无效的路径: {path}")
                continue

            if os.path.isfile(path):
                self.process_single_file(path)
            else:
                self.process_directory(path)

    def process_single_file(self, file_path):
        dir_name, file_name = os.path.split(file_path)
        base_name = file_name.rsplit('_', 1)[0]
        target_dir = os.path.join(dir_name, base_name)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        self.process_files_with_prefix(dir_name, base_name, target_dir)

    def process_directory(self, dir_path):
        # 创建处理后的目标目录
        target_base_dir = dir_path + "_processed"
        if not os.path.exists(target_base_dir):
            os.makedirs(target_base_dir)

        # 获取目录中所有文件的前缀集合
        prefixes = set()
        for file_name in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_name)):
                prefix = file_name.rsplit('_', 1)[0]
                prefixes.add(prefix)

        # 处理每个前缀的文件
        for prefix in prefixes:
            target_dir = os.path.join(target_base_dir, prefix)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            self.process_files_with_prefix(dir_path, prefix, target_dir)

    def process_files_with_prefix(self, source_dir, prefix, target_dir):
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            if item.startswith(prefix) and os.path.isfile(source_path):
                target_path = os.path.join(target_dir, item)
                if not os.path.exists(target_path):
                    if self.operation_var.get() == "copy":
                        shutil.copy(source_path, target_dir)
                    else:
                        shutil.move(source_path, target_dir)
                    self.log_message(f"已{'复制' if self.operation_var.get() == 'copy' else '剪切'}: {item}")
                else:
                    self.log_message(f"文件 {item} 已存在，跳过。")

    def log_message(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FilePathApp(root)
    root.mainloop()