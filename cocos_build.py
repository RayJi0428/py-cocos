import subprocess
import os
import shutil
import threading
import time
'''
發布產物生成ver.txt
'''
def generate_ver_txt(build_root):
    list = os.listdir(f'{build_root}\\assets\\main')
    for file_name in list:
        if 'index.' in file_name:
            js_file_name = file_name
            break
    f = open(f'{build_root}/ver.txt', 'w')
    f.write(js_file_name)
    f.close()

# 安全刪除
def safe_remove_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

# 編譯1個遊戲
def build_one_game(gid):
    global gid_list
    # 刪除原產物------------------------------------------------------------
    safe_remove_dir(f"{output_root}\\{gid}")

    # 執行CocosCreator------------------------------------------------------------
    os.chdir(f"{engine_path}")
    print(f"開始多執行緒編譯 build {gid}")
    subprocess.run(
        f'CocosCreator --project {proj_root}\{gid} --build configPath="{config_path}"'
    )

    # 生成ver.txt------------------------------------------------------------
    print(f"生成ver.txt")
    build_root = f'{proj_root}\\{gid}\\build\\game'
    generate_ver_txt(build_root)

    #重新以GID命名------------------------------------------------------------
    print(f"搬移檔案")
    build_root_rename = f'{proj_root}\\{gid}\\build\\{gid}'
    safe_remove_dir(build_root_rename)
    os.rename(build_root, build_root_rename)
    
    # 搬到下載點
    shutil.move(build_root_rename, f'{output_root}')

    # 多執行緒變數鎖
    lock.acquire()
    build_complete()
    lock.release()

# 建立一條執行緒
def make_one_thread(gid):
    global thread_count
    thread_count += 1
    t = threading.Thread(target=build_one_game, kwargs=dict(gid=gid))
    t.start()

# 一款編譯完成
def build_complete():
    global thread_count
    thread_count -= 1
    # 執行緒上限3個,一款完成再處理下一款
    if len(gid_list) > 0:
        make_one_thread(gid_list.pop(0))
    elif thread_count == 0:
        global begin
        end = time.perf_counter()
        input(f'全部編譯完成 費時{int(end-begin)}秒')


# 參數定義
platform = "web-mobile"
md5Cache = "true"
scene_uid = "664dcaf1-b7ea-42bc-947d-3272d43b737f"
config_path = "D:\\SVN\\Cocos\\tools\\Build\\buildConfig_web-mobile.json"
engine_path = "D:\\SVN\\Cocos\\core\\3.6.3"
proj_root = "D:\\SVN\\Cocos"
default_list = [1035,1077,1078,1080,1090,1092,1093]
thread_limit_max = 5
lock = threading.Lock()

gid_input = input('輸入GID(編共用直接ENTER):')
if gid_input == "":
    #輸入空白全部編譯
    gid_list = default_list
else:
    gid_list = gid_input.split(' ')
print(f"編譯遊戲清單 = {gid_list}")
output_root = "D:\\下載點\\Html5_device"
# 執行update-----------------------------------------------------------
process = subprocess.Popen( f'TortoiseProc.exe /command:update /path:"{proj_root}" /closeonend:1',
                     shell=True,
                     stdout=subprocess.PIPE)
#等待完成
process.communicate()

begin = time.perf_counter()
thread_count = 0
#一次最多處理3款遊戲
while len(gid_list) > 0 and (thread_count < thread_limit_max):
    make_one_thread(gid_list.pop(0))