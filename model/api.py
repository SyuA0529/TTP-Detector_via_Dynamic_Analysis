sdk_list=["Landroid/","Landroidx/","Ljava/","Ljavax/","Landroid/support/v7","Landroid/support/v4"]

def is_sdk_by_str (class_name) :  # 만일 Class 몇이 문자열일 경우 SDK 인지 구별하는 함수
    for j in range (0,len(sdk_list)):
        if class_name.__contains__(sdk_list[j]) :
            return True 
    return False

def get_api_info(class_name, method_name, descriptor) :
    parameter = descriptor[descriptor.index("(") + 1 : descriptor.index(")")].split(" ")
    return_type = descriptor[descriptor.index(")") + 1: ]
    if len(parameter) == 1 and parameter[0] == "" :
        return [class_name, method_name, [], return_type]
    return [class_name, method_name, parameter, return_type]

def get_api_descriptor(parameter, return_type) :
    return "(" + " ".join(parameter) + ")" + return_type

def parse_dynamic_api(line) :
    # ["instance_id", "method", "parameter", "return"]
    data = line.split("|")
    for i in range(len(data)) :
        data[i] = data[i].strip()
    if "@" in data[0] :
        instance_info = data[0].split("@")
        return ["@" + instance_info[1], get_api_info(data[1], data[2], data[3]), data[4], data[5]], instance_info[0]
    else :
        return ["", get_api_info(data[1], data[2], data[3]), data[4], data[5]], data[0]
    
def check_same_api(cur_api_info, rule_api_info) :
    # check api's class name
    if cur_api_info[0] != rule_api_info[0] :
        return False
    # check api's method name
    if cur_api_info[1] != rule_api_info[1] :
        return False
    # check api's parameter type
    if len(cur_api_info[2]) != len(rule_api_info[2]) :
        return False
    parameter_check = True
    for i in range(len(rule_api_info[2])) :
        if rule_api_info[2][i] == "DontCare" or cur_api_info[2][i] == "DontCare":
            continue
        elif cur_api_info[2][i] != rule_api_info[2][i] :
            parameter_check = False
            break
    if not parameter_check :
        return False
    # check api's return type
    if cur_api_info[3] != rule_api_info[3] :
        return False
    return True

class api_node :
    def __init__(self, depth, line, line_num) :
        self.depth = depth
        self.line = line
        self.info, self.instance_class = parse_dynamic_api(line)
        self.line_num = line_num
        self.prev_api_list = []
        
    def print_sequence(self) :
        if self.depth == 0 :
            print("[" + str(self.depth) + "]", self.__str__())
        else :
            print("[" + str(self.depth) + "]", self.__str__())
            for prev_api in self.prev_api_list :
                prev_api.print_sequence()
    
    def get_smali(self) :  
        class_name = self.info[1][0]
        method_name = self.info[1][1]
        descriptor = get_api_descriptor(self.info[1][2], self.info[1][3])
        return class_name + "->" + method_name + descriptor
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return self.instance_class + self.info[0] + " | " + self.get_smali() + " | " + self.info[2] + " | " + self.info[3]
    
    def __eq__(self, __o: object) -> bool:
        return self.line == __o.line

    def is_exist_prev_api(self) -> bool :
        if self.depth == 0 :
            return True
        return len(self.prev_api_list) > 0
    
    def delete_uncomplete_prev_api(self) :
        if self.depth == 0 :
            return
        # delete node that does not have a sequence
        remaining_complete_sequence(self.prev_api_list)

def remaining_complete_sequence(root_node_list) :
    delete_node_list = []
    for root_node in root_node_list :
        root_node.delete_uncomplete_prev_api()
        if not root_node.is_exist_prev_api() : 
            delete_node_list.append(root_node)
    for delete_node in delete_node_list :
        root_node_list.remove(delete_node)