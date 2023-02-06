"""
cocos工具
"""
#https://openpyxl.readthedocs.io/en/stable/tutorial.html#
from tkinter import *
import tkinter.filedialog
import shutil
import os  # 檔案
import json  # JSON
import subprocess  # 子進程
import smtplib  # email
from time import sleep
import data as data
import re
# --------------------------------------------------------------------------------
# encrypt
# https://stackoverflow.com/questions/39509741/python-or-libreoffice-save-xlsx-file-encrypted-with-password
# https://stackoverflow.com/questions/36122496/password-protecting-excel-file-using-python

# email
# https://www.runoob.com/python/python-email.html
# SMTP(Simple Mail Transfer Protocol)
# --------------------------------------------------------------------------------


def printState(string):
    logText.insert(END, string + "\n")
    logText.see(END)
    root.update()

def build():
    print("A")

def loadScene():
    """開啟檔案"""
    global file_path
    file_path = tkinter.filedialog.askopenfilename()

    # 尚未選擇檔案
    if file_path == '':
        return

    global meta_list
    meta_list = {}

    global file_name
    file_name = os.path.basename(file_path)
    printState(f'=====================================================')
    printState(f'選擇scene:{file_path}')

    # 讀取.meta
    printState(f'開始蒐集meta')
    file_root = re.match('.+/assets/', file_path)[0]
    findMeta(file_root)

    # 讀取scene
    printState(f'開始讀取scene')
    global scene_json
    with open(file_path, "r", encoding="utf-8") as file:
        scene_json = json.load(file)
    parseList(scene_json, '')
    printState(f'完成')


def parseDict(container, parent):
    # 解析scene
    for key in container:
        data = container[key]
        # key含有__uuid__
        if '__uuid__' in key:
            uuid = data
            if uuid not in meta_list:
                printState(f'{parent}找不到uuid {uuid}')
        elif type(data) is list:
            # printState(f'解析{key}')
            parseList(data, f'{parent}/{key}')
        elif type(data) is dict:
            # printState(f'解析{key}')
            parseDict(data, f'{parent}/{key}')


def parseList(list, parent):
    for i in range(0, len(list)):
        data = list[i]
        if type(data) is dict:
            parseDict(data, parent)


def findMeta(root):
    # 尋找META檔
    print(f'root = {root}')
    file_list = os.listdir(root)
    for file_name in file_list:
        file_url = f'{root}/{file_name}'
        if os.path.isdir(file_url):
            findMeta(file_url)
        elif '.meta' in file_name:
            with open(file_url, "r") as meta_file:
                meta_json = json.load(meta_file)
                parseMeta(meta_json)


def parseMeta(meta_json):
    uuid = meta_json['uuid']
    global meta_list
    meta_list[uuid] = meta_json
    if 'subMetas' in meta_json:
        for subMetaKey in meta_json['subMetas']:
            parseMeta(meta_json['subMetas'][subMetaKey])
# Main===================================================================


meta_list = {}
scene_json = None
file_path = ""
file_name = ""
config = {}
tmp_files = []
root = Tk()
root.title(f'{data.exe_title} v{data.exe_ver}')
root.geometry(f'{data.window_w}x{data.window_h}')
root.resizable(False, False)
# root.configure(bg='#00ccff')

# 編版
# stick:NSWE上下左右
build_btn = Button(root, text="發版", width=9, command=build)
build_btn.grid(row=0, column=0, padx=5, pady=5, stick=W)
# 檢查
file_btn = Button(root, text="檢查Scene", width=9, command=loadScene)
file_btn.grid(row=1, column=0, padx=5, pady=0, stick=W)
# 狀態欄
logText = Text(root, width=77, height=30, relief="groove")
logText.grid(row=0, column=1, rowspan=10, padx=5, pady=5, stick=N+S+W+E)

printState("初始化完成")

root.mainloop()
