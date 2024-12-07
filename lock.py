import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet

# 全局变量，用于控制任务是否取消
cancel_task = False

# 生成密钥并保存
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("成功", "密钥已生成！")

# 加载密钥
def load_key():
    if not os.path.exists("key.key"):
        messagebox.showerror("错误", "密钥文件不存在，请先生成密钥！")
        return None
    with open("key.key", "rb") as key_file:
        return key_file.read()

# 加密文件
def encrypt_file(file_path, cipher):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        encrypted_data = cipher.encrypt(file_data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
    except Exception as e:
        print(f"文件加密失败：{file_path}\n{e}")

# 解密文件
def decrypt_file(file_path, cipher):
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
    except Exception as e:
        print(f"文件解密失败：{file_path}\n{e}")

# 多线程处理加密/解密任务
def process_folder_task(folder_path, cipher, is_encrypt, progress_bar, progress_window):
    global cancel_task
    cancel_task = False  # 重置取消标志

    files = []
    for root, dirs, file_names in os.walk(folder_path):
        for file in file_names:
            files.append(os.path.join(root, file))
    
    total_files = len(files)
    progress_bar["maximum"] = total_files

    for index, file_path in enumerate(files):
        if cancel_task:  # 检测取消标志
            messagebox.showwarning("操作中断", "操作已被取消！")
            progress_window.destroy()
            return

        if is_encrypt:
            encrypt_file(file_path, cipher)
        else:
            decrypt_file(file_path, cipher)
        progress_bar["value"] = index + 1
        progress_window.update_idletasks()

    messagebox.showinfo("成功", "操作已完成！")
    progress_window.destroy()

# 取消任务
def cancel_processing():
    global cancel_task
    cancel_task = True

# 处理文件夹加密/解密，带进度条和多线程
def process_folder(is_encrypt):
    folder_path = filedialog.askdirectory(title="选择文件夹")
    if not folder_path:
        return

    key = load_key()
    if not key:
        return
    cipher = Fernet(key)

    # 显示进度条窗口
    progress_window = tk.Toplevel()
    progress_window.title("处理进度")
    tk.Label(progress_window, text="处理中，请稍候...").pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
    progress_bar.pack(pady=10)

    cancel_button = tk.Button(progress_window, text="取消", command=cancel_processing, bg="red", fg="white")
    cancel_button.pack(pady=10)

    # 启动新线程处理任务
    threading.Thread(
        target=process_folder_task,
        args=(folder_path, cipher, is_encrypt, progress_bar, progress_window),
        daemon=True
    ).start()

# 主界面
def main():
    root = tk.Tk()
    root.title("文件夹加密工具")
    root.geometry("400x300")

    tk.Label(root, text="文件夹加密工具", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="生成密钥", command=generate_key, width=20, height=2, bg="lightblue").pack(pady=10)
    tk.Button(root, text="加密文件夹", command=lambda: process_folder(is_encrypt=True), width=20, height=2, bg="lightgreen").pack(pady=10)
    tk.Button(root, text="解密文件夹", command=lambda: process_folder(is_encrypt=False), width=20, height=2, bg="orange").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
