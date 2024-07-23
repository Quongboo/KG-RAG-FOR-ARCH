"""
所有的prompt
"""

graph_nodes_prompt = [
    {"role": "system",
     "content": """
     -目标-
        你的目标是从给定的文档中找到可作为知识图谱构建的实体，并收集实体自身相关的属性信息。
     -步骤-
     1、识别文本中所有实体，对于每一个实体，请提取以下信息：
     -entity_name：实体名称，中文
     -entity_type：实体类型为实体类型之一
     -entity_description:实体简介，描述这个实体是什么
     -entity_info：实体属性，包含所能识别的改实体的所有属性
     将每一个实体格式化为：("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>{tuple_delimiter}<entity_info>)
     
     2、从步骤1中确定的实体，确定彼此”明显相关“的所有对(source_entity, target_entity),对于每一对相关实体，提取如下信息：
     -source_entity：源实体的名称，与步骤1中识别的相同
     -target_entity：目标实体的名称，与步骤1中识别的名称相同
     -relationship_description：对于源实体和目标实体之间存在关联的原因的解释
     -relationship_strength：表示源实体和目标实体之间关系强度的数字分数（1-10）
     将每一个关系格式化为：("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>)
      
     3、以中文返回输出，作为步骤1和2中标识的所有实体和关系的单个列表。使用**{record_delimiter}**作为列表分隔符。
     
     4、完成后，输出{completion_delimiter}
     
     ######################
     -Examples-
     ######################
     
     Example 1:
     Entity_types: [房间名, 技术名, 设备, 其他]
     Text:3.21   医疗工艺设计参数应根据不同医院的要求研究确定，当无相关数据时应符合下列要求：
                1  门诊诊室间数可按日平均门诊诊疗人次/(50人次～60 人次)测算；
                2  急救抢救床数可按急救通过量测算；
                3  1个护理单元宜设40张～50张病床；
                4  手术室间数宜按病床总数每50床或外科病床数每25床~ 30床设置1间；
                5  重症监护病房(ICU)  床数宜按总床位数的2%～3%设 置；
                6  心血管造影机台数可按年平均心血管造影或介入治疗数/ (3例～5例×年工作日数)测量；
                7  日拍片人次达到40人次～50人次时，可设X线拍片机1台；
                8  日胃肠透视人数达到10例～15例时，可设胃肠透视机1 台；
                9_日胸透视人数达到50人次～80人次时，可设胸部透视机 1 台 ；
                10  日心电检诊人次达到60人次～80人次时，可设心电检诊间1间；
                11  日腹部B超人数达到40人次～60人次时，可设腹部B超机1台；
                12  日心血管彩超人数达到15人次～20人次时，可设心血管彩超机1台；
                13  日检诊人数达到10例～15例时，可设十二指肠纤维内窥镜1台。

     ################
     Output:
     ("entity"{tuple_delimiter}"门诊诊室"{tuple_delimiter}"房间名"{tuple_delimiter}"医院门诊的诊断空间"{tuple_delimiter}"{"计算方法": "日平均门诊诊疗人次/(50人次～60人次)"}"){record_delimiter}
     ("entity"{tuple_delimiter}"手术室"{tuple_delimiter}"房间名"{tuple_delimiter}"医院手术空间"{tuple_delimiter}"{"计算方法": "按病床总数每50床或外科病床数每25床~ 30床设置1间"}"){record_delimiter}
     ("entity"{tuple_delimiter}"重症监护病房"{tuple_delimiter}"房间名"{tuple_delimiter}"医院中为危重患者提供专门的救治和监护的病房区域"{tuple_delimiter}"{"计算方法": "床数宜按总床位数的2%～3%设 置"}"){record_delimiter}
     
     ("relationship"{tuple_delimiter}"门诊诊室"{tuple_delimiter}"手术室"{tuple_delimiter}"医院提供医疗服务的重要组成部分，但联系较弱"{tuple_delimiter}3){record_delimiter}
     ("relationship"{tuple_delimiter}"手术室"{tuple_delimiter}"重症监护病房"{tuple_delimiter}"手术室和ICU在医院工艺设计中是两个相对独立的重要组成部分，布局相邻"{tuple_delimiter}6){record_delimiter}

                       """},

    {"role": "user", "content": "实体类型：{}，文本：{}"},

                      ]


nodes_match_prompt=[
    {"role": "system",
     "content": """
    -目标-
        你的目标是识别用户问题之中的实体，并将其与输入的实体名称做匹配
    -步骤-
    1、仔细阅读用户问题，识别用户问题中所有涉及的实体，对于每一个实体，请提取以下信息：
    -user_entity_name：实体名称，中文
    将每一个实体格式化为：("user"{tuple_delimiter}<user_entity_name>)


    2、从步骤1中确定的用户相关的实体，与输入的实体名称做匹配，提取如下信息：
    -match_entity_name：匹配上的实体名称，与输入的实体名称相同
    -match_strength：表示匹配上的实体和用户问题之间关系强度的数字分数（1-10）
    
    将每一个关系格式化为：("match"{tuple_delimiter}<match_entity_name>{tuple_delimiter}<match_strength>)

    3、以中文返回输出，作为步骤1和2中标识的所有实体和匹配的单个列表。使用**{record_delimiter}**作为列表分隔符。

    4、完成后，输出{completion_delimiter}

    ######################
    -Examples-
    ######################

    Example 1:
    user_question: 医院诊疗室如何设计？
    entity_input: ["病房","诊查室","手术室","卫生间","综合医院","门诊","住院部","太平间","绿化景观","门诊诊室","诊室"]

    ################
    Output:
    
    ("user"{tuple_delimiter}"诊疗室"){record_delimiter}
    
    ("match"{tuple_delimiter}"诊室"{tuple_delimiter}"9"){record_delimiter}
    ("match"{tuple_delimiter}"门诊诊室"{tuple_delimiter}"8"){record_delimiter}
    ("match"{tuple_delimiter}"诊查室"{tuple_delimiter}"6"){record_delimiter}
    
                      """},

    {"role": "user", "content": "entity_input：{}，user_question：{}"},
]

answer_prompt = [
    {"role": "system",
     "content": """
    -目标-
        你的目标是根据所提供的知识信息，回答用户的问题
    -步骤-
    1、仔细阅读用户问题，深刻理解用户问题的意图；
    2、点明用户问题中可能包含的专业名词名称呼（来源于匹配到的名词为），在所提提供的知识信息为查到到与用户问题相关的部分；
    3、根据步骤2所查找到的信息，回答用户的问题，回答的格式如下：
    -question_answer：回答的内容，中文
    将回答格式化为：("answer"{tuple_delimiter}<question_answer>{tuple_delimiter})
    4、完成后，输出{completion_delimiter}
    
    -注意-
    1、你的回答必须来源于知识信息，不得随意编造
    2、如果用户的问题在知识信息中没有，请告诉用户你不知道，无法回答
    

    ######################
    -Examples-
    ######################

    Example 1:
    用户的问题为: 医院大厅如何设计？
    知识信息为: ['"门诊大厅"的描述为"医院接待门诊病人的主要区域"，"门诊大厅"的信息为：{'防火分区面积': '地上部分允许最大建筑面积应为4000m²', '装修材料': '不燃或难燃材料'}；与其有密切联系的关系有['"门诊大厅"与"病房"的联系强度为7；关系为："门诊大厅是病人初次接触的地方，而病房是病人接受进一步治疗的地方，两者在医院流程中相连"，']', '"候诊厅"的描述为"医院中患者等待就诊的区域"，"候诊厅"的信息为：{'设施': '音量调节装置, 触摸屏信息查询终端, 大型彩色显示屏'}；与其有密切联系的关系有['"门诊大厅"与"病房"的联系强度为7；关系为："门诊大厅是病人初次接触的地方，而病房是病人接受进一步治疗的地方，两者在医院流程中相连"，', '"候诊厅"与"护士站"的联系强度为7；关系为："候诊厅和护士站在医院中通常相邻，护士站负责管理候诊厅的秩序和服务"，']', '"医院首层"的描述为"医院建筑的首层，通常包括对外出入口、收费及挂号处等重要区域"，"医院首层"的信息为：{'设置': '视频监控系统，包括各对外出入口、收费及挂号处、财务及出院结算处、贵重药品库、电梯轿厢、各楼层的电梯厅及人员活动较多的场所设置摄像机'}；与其有密切联系的关系有['"门诊大厅"与"病房"的联系强度为7；关系为："门诊大厅是病人初次接触的地方，而病房是病人接受进一步治疗的地方，两者在医院流程中相连"，', '"候诊厅"与"护士站"的联系强度为7；关系为："候诊厅和护士站在医院中通常相邻，护士站负责管理候诊厅的秩序和服务"，', '"医院首层"与"贵重药品库"的联系强度为7；关系为："医院首层和贵重药品库都是医院安全监控的重点区域，通过视频监控系统进行联动"，']']

    ################
    Output:
    ("answer"{tuple_delimiter}<你的问题中的"医院大厅"可能所指的是"门诊大厅"或"候诊厅",其两者在设计中的要点为：
                                1、防火安全：
                                门诊大厅的地上部分允许最大建筑面积应为4000m²。
                                装修材料应使用不燃或难燃材料。
                                2、功能布局：
                                门诊大厅是医院接待门诊病人的主要区域。
                                应考虑与病房的连接，因为门诊大厅是病人初次接触的地方，而病房是病人接受进一步治疗的地方。
                                3、候诊区设施：
                                设置音量调节装置。
                                安装触摸屏信息查询终端。
                                配备大型彩色显示屏。
                                4、安全监控：
                                在医院首层安装视频监控系统，包括对外出入口、收费及挂号处等重要区域。
                                5、其他考虑：
                                设计时应考虑与护士站的邻近关系，因为护士站负责管理候诊厅的秩序和服务。
                                这些设计要点旨在确保医院大厅的安全性、功能性和便利性，为患者提供舒适的就医环境。
>{tuple_delimiter})



                      """},

    {"role": "user", "content": "用户的问题为：{}，匹配到的名词为：{}，知识信息为：{}"},
]


