import subprocess
import os
import shutil

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

# 參數定義
platform = "web-mobile"
md5Cache = "true"
scene_uid = "664dcaf1-b7ea-42bc-947d-3272d43b737f"
config_path = "D:\\SVN\\Cocos\\tools\\Build\\buildConfig_web-mobile.json"
engine_path = "D:\\SVN\\Cocos\\core\\3.5.2"
proj_root = "D:\\SVN\\Cocos"
gid_list = input('輸入GID:').split(' ')
output_root = "D:\\下載點\\Html5_device"

# 執行update
subprocess.run(
    f'TortoiseProc.exe /command:update /path:"{proj_root}" /closeonend:1')
	
# 依序發布
for gid in gid_list:
    # 刪除原產物------------------------------------------------------------
    safe_remove_dir(f"{output_root}\\{gid}")

    # 執行CocosCreator------------------------------------------------------------
    if gid == '1092':
        engine_path = "D:\\SVN\\Cocos\\core\\3.6.3"
    os.chdir(f"{engine_path}")
    print(f"開始編譯 build {gid}")
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

print('done!')
input("F")