from api import *

# extract only those that have a sequence
def generate_graph(rule_api_list, api_node_graph) :
    # api_info : [instance, method, parameter]
    api_node_graph_len = len(api_node_graph)
    for depth in range(api_node_graph_len - 1, 0, -1) :
            prev_check_type = rule_api_list[depth - 1][2] # next_check_type
            remain_prev_apis = [] # list of prev api which call cur api
            remain_cur_apis = [] # list of cur api which called by prev api
            
            # for each cur api
            for cur_api_node in api_node_graph[depth] :
                for prev_api_node in api_node_graph[depth - 1] :
                    if cur_api_node.line_num <= prev_api_node.line_num :
                        continue
                    
                    # check prev api and cur api is called by same instance
                    if prev_check_type == "instance_instance" :
                        if cur_api_node.info[0] == prev_api_node.info[0] :
                            cur_api_node.prev_api_list.append(prev_api_node)
                            if not cur_api_node in remain_cur_apis :
                                remain_cur_apis.append(cur_api_node)
                            if not prev_api_node in remain_prev_apis :
                                remain_prev_apis.append(prev_api_node)

                    # check prev api's instance is in cur api's parameter
                    elif prev_check_type ==  "instance_parameter" :
                        if prev_api_node.info[0] in cur_api_node.info[2] :
                            cur_api_node.prev_api_list.append(prev_api_node)
                            if not cur_api_node in remain_cur_apis :
                                remain_cur_apis.append(cur_api_node)
                            if not prev_api_node in remain_prev_apis :
                                remain_prev_apis.append(prev_api_node)
                    
                    # check prev api's return is cur api's parameter
                    elif prev_check_type == "return_instance" :
                        if prev_api_node.info[3] == cur_api_node.info[0] :
                            cur_api_node.prev_api_list.append(prev_api_node)
                            if not cur_api_node in remain_cur_apis :
                                remain_cur_apis.append(cur_api_node)
                            if not prev_api_node in remain_prev_apis :
                                remain_prev_apis.append(prev_api_node)
                            
                    # if prev_check_type is None, nothing to check
                    else :
                        cur_api_node.prev_api_list.append(prev_api_node)
                        if not cur_api_node in remain_cur_apis :
                            remain_cur_apis.append(cur_api_node)
                        if not prev_api_node in remain_prev_apis :
                            remain_prev_apis.append(prev_api_node)
            
            # delete cur api which not called by prev apis
            api_node_graph[depth] = remain_cur_apis
            # delete prev api which not call cur apis
            api_node_graph[depth - 1] = remain_prev_apis

def dynamic_analysis(dynamic_rule_list, out_dir_d) :
    # GET API LIST BY DYNAMIC ANALYSIS
    file_content = ""
    with open(out_dir_d + "\\api-list.txt", "r") as api_list_file :
        file_content = api_list_file.read()
    file_content = file_content.split("\n")
    detected_rule_list = []
    # CHECK API SEQUENCE
    # for each rule
    for json_data in dynamic_rule_list :
        # extract rule
        rule_api_list = []
        for i in json_data["api"] :
            api_info = [get_api_info(i["class"], i["method"], i["descriptor"]), i["parameter"], i["next_check_type"]]
            rule_api_list.append(api_info)
        
        # cur_api_info : [instance_id, method, parameter, "return"]
        # rule_api_info : [method, parameter, next_check_type]
        api_node_graph = [[] for i in range(len(rule_api_list))]
        for line_num in range(len(file_content)) :
            line = file_content[line_num]
            if not line.startswith("class ") :
                continue
            for depth in range(len(rule_api_list)) :
                cur_api_node = api_node(depth, line, line_num)
                # error
                if check_same_api(cur_api_node.info[1], rule_api_list[depth][0]) :
                    # check parameter
                    # parameter sequence does not check in there
                    if "__instance__" not in rule_api_list[depth][1]  : 
                        # check parameter in rule is in cur_api_info's parameter
                        if not len(rule_api_list[depth][1]) == 0 :
                            is_parameter_ok = True
                            for each_param in rule_api_list[depth][1] :
                                each_param = each_param.replace(" ", "")
                                cur_param = each_param.split("|")
                                if not any(param in cur_api_node.info[2] for param in cur_param) :
                                    is_parameter_ok = False
                                    break
                            if not is_parameter_ok :
                                continue
                    if not cur_api_node in api_node_graph[depth] :
                        api_node_graph[depth].append(cur_api_node)
                        break
                    
        # generate diagraph
        generate_graph(rule_api_list, api_node_graph)
        
        # remain api nodes which have sequence to depth 0
        sequence_node_list = api_node_graph[len(api_node_graph) - 1]
        for root_node in sequence_node_list :
            root_node.delete_uncomplete_prev_api()
        remaining_complete_sequence(sequence_node_list)
        
        if len(sequence_node_list) == 0 :
            continue # sequence does not exist
        
        # sequence is exist
        # print sequence
        print(json_data["Technique"])
        for sequence_node in sequence_node_list :
            sequence_node.print_sequence()
            print("===================================")
        print()
        # append current rule to detected rule
        detected_rule_list.append(json_data)
    
    return detected_rule_list