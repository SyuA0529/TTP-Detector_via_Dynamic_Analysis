from androguard.core import androconf

def get_permissions(a,apk_filepath): # 모든 영역의 Permission을 획득함
    if androconf.is_android(apk_filepath):
        perm_list= [] 
        xml_= a.get_android_manifest_axml().get_xml() # android manifest.xml에서 복호화
        for line in xml_.decode('utf-8').split("\n"): 
            if line.find("android.permission") > 0 : #Permission 문자열에 있는 Line을 획득 
                perm_line=line[line.find('android.permission'):]
                perm_list.append(perm_line[:perm_line.find('"')])
            if line.find("Android.permission") > 0 : 
                perm_line=line[line.find('Android.permission'):] # Permission에는 앞에 대문자 A로 진행됨
                perm_list.append(perm_line[:perm_line.find('"')])
        return perm_list
    if a.ret_type == "DEX":
        return []
    
