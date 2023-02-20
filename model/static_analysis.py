from androguard.core.analysis import analysis
from androguard.misc import AnalyzeAPK, AnalyzeDex

from permission import *
from api import *

# check permission
def first_stage (a, apk_filepath, check_perm_list) :
    target_permissions= get_permissions(a, apk_filepath)
    for perm_list in check_perm_list : 
        if not any(perm in target_permissions for perm in perm_list) :
            return False
    return True

def static_analysis(apk_filepath, rule_list) :
    # 2. EXTRACT STATIC FEATURE BY ANDROGUARD
    a, _, dx = AnalyzeAPK(apk_filepath) 
    dynamic_check_rule_list = []
    
    # for each rule
    for json_data in rule_list :
        # prepare for analyze apk
        check_permission_list = []
        for perm in json_data["permission"] :
            check_permission_list.append(perm.split(" | "))
                
        core_api_list=[]
        for i in json_data["api"]:
            # [class name, method name, [parameter type list], return type]
            core_api_list.append(get_api_info(i["class"], i["method"], i["descriptor"]))
                
        # check permission
        if not first_stage(a, apk_filepath, check_permission_list) :
            continue
        
        # if rule pass first stage, re-analyze by dynamic analysis
        dynamic_check_rule_list.append(json_data) 
    return dynamic_check_rule_list, a.get_package()