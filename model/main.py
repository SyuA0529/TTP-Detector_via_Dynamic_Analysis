import signal
import subprocess
import time
from file import *
from static_analysis import *
from dynamic_analysis import *
import json

def analysis(filepath, rule_dir, out_dir) :
    # load APK files
    apk_lst=[]
    file_lst=[]
    search_apk(filepath, apk_lst, file_lst)
    
    # 1. LOAD JSON RULES
    json_path_list = []
    json_path_search(rule_dir, json_path_list)
    rule_list = rule_extract(json_path_list)
    
    # for each APK files
    for n in range(0, len(apk_lst)): 
        # analysis each applicatoin
        print("===================================")
        print("APK file: ", apk_lst[n])
        apk_filepath = apk_lst[n]
        
        out_dir_s = os.path.abspath(out_dir) + "\\" + file_lst[n] + "\\" # report의 디렉토리를 생성
        out_dir_d = os.path.abspath(out_dir_s) + "\\dynamic"
        
        # 3. DO STATIC ANALYSIS
        print("===================================")
        print("Start Static Analysis\n")
        dynamic_rule_list, app_package= static_analysis(apk_filepath, rule_list)
        
        # if rule exist which pass permission check, do dynamic analysis
        if len(dynamic_rule_list) == 0:
            print("Detected Rule is not exist\n")
            continue # all rules do not pass permission check
        
        print("===================================")
        print("App package:", app_package)
        print("===================================")
        
        # 4. DO DYNAMIC ANALYSIS
        print("Detected Rule List by Static Analysis")
        for dynamic_rule in dynamic_rule_list :
            print(dynamic_rule["Technique"])
        
        print("===================================")
        print("Start Dynamic Analysis\n")
        
        # apk is same -> app is not uninstalled
        with open(os.devnull, 'w') as tempf:
            cmd = "droidbot -a " + os.path.abspath(apk_lst[n]) + " -o " + os.path.abspath(out_dir_s) + "\\dynamic"
            process = subprocess.Popen(cmd, shell = False, stdin = tempf, stdout = tempf, stderr = tempf)
            try :
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                subprocess.call(['taskkill', '/F', '/T', '/PID',  str(process.pid)], stdin = tempf, stdout = tempf, stderr = tempf)
                #os.kill(process.pid, signal.CTRL_C_EVENT)
            except :
                print("wtf")
                
            # uninstall app
            subprocess.call(["adb", "uninstall", "io.github.ylimit.droidbotapp"], stdin = tempf, stdout = tempf, stderr = tempf)
            subprocess.call(["adb", "uninstall", app_package], stdin = tempf, stdout = tempf, stderr = tempf)
        
        detected_rule_list = dynamic_analysis(dynamic_rule_list, out_dir_d)
        if len(detected_rule_list) == 0 :
            print()
        
        # 5. REPORT
        print("Detected Rule List")
        for detected_rule in detected_rule_list :
            print(detected_rule["Technique"])
            
        print("===================================\n\n")
        time.sleep(5)
        

def main() :
    analysis("./apks", "./rules", "./results")
    
if __name__ == "__main__" :
    main()