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

        self.label = ttk.Label(master, text="请拖动文件到此处")
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

    def drop(self, event):
        file_path = event.data
        self.entry.delete(0, tk.END)
        self.entry.insert(0, file_path)
        self.update_target_dir(file_path)

    def update_target_dir(self, file_path):
        if os.path.isfile(file_path):
            dir_name, file_name = os.path.split(file_path)
            base_name = file_name.rsplit('_', 1)[0]
            target_dir = os.path.join(dir_name, base_name)
            self.target_label.config(text=f"目标目录: {target_dir}")
        else:
            self.target_label.config(text="无效的文件路径")

    def process_files(self):
        file_path = self.entry.get()
        if not os.path.isfile(file_path):
            self.log_message("无效的文件路径")
            return

        dir_name, file_name = os.path.split(file_path)
        base_name = file_name.rsplit('_', 1)[0]
        target_dir = os.path.join(dir_name, base_name)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for item in os.listdir(dir_name):
            source_path = os.path.join(dir_name, item)
            if item.startswith(base_name) and os.path.isfile(source_path):
                target_path = os.path.join(target_dir, item)
                if not os.path.exists(target_path):
                    if self.operation_var.get() == "copy":
                        shutil.copy(source_path, target_dir)
                    else:
                        shutil.move(source_path, target_dir)
                else:
                    self.log_message(f"文件 {target_path} 已存在，跳过。")

        self.log_message(f"文件已{'复制' if self.operation_var.get() == 'copy' else '剪切'}到 {target_dir}")

    def log_message(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FilePathApp(root)
    root.mainloop()