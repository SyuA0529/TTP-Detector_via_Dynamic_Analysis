import json
import os

def json_path_search(dirname, json_path_list): # Json 디렉토리 경로를 검색
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        if os.path.isdir(full_filename) : # search child directory
            json_path_search(full_filename, json_path_list)
        else :
            ext = os.path.splitext(full_filename)[-1]
            if ext == '.json': 
                json_path_list.append(full_filename)

# have to change
def rule_extract (json_path_list): # json 파일을 Laod 함
    rule_list=[]
    for rule_path in json_path_list:
        with open(rule_path, 'r') as f:
            json_data = json.load(f)
        rule_list.append(json_data)
    return rule_list

def search_apk(dirname,apk_lst,file_lst): # 해당 디렉토리의 있는 모든 APK를 검색함
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search_apk(full_filename, apk_lst, file_lst)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.apk': 
                    apk_lst.append(full_filename)
                    file_lst.append(filename[:filename.find(".apk")])
    except PermissionError:
        pass