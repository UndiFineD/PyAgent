# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\utils.py


def execute_agent_chain(agent_graph, agent_chain, user_input_graph):
    # 1. 初始化上下文
    context = {}

    # 2. 处理用户输入
    user_inputs = {}
    for user_input_node in user_input_graph:
        # 获取用户输入值（这里需要实际的前端交互，此处用模拟数据）
        value = input(
            f"请输入 {user_input_node['node']} ({user_input_node['description']}): "
        )

        # 将用户输入映射到各个Agent的输入参数
        for link in user_input_node["links"]:
            for agent_name, input_param in link.items():
                context_key = f"{agent_name}.{input_param}"
                context[context_key] = value

    # 3. 按顺序执行Agent链
    for agent_name in agent_chain:
        # 获取Agent配置信息
        agent_config = next(
            agent for agent in agent_graph if agent["node"] == agent_name
        )

        # 4. 准备输入参数
        inputs = {}
        for input_param in agent_config["inputs"]:
            context_key = f"{agent_name}.{input_param['name']}"

            if context_key not in context:
                raise ValueError(f"Missing required parameter: {context_key}")

            inputs[input_param["name"]] = context[context_key]

        # 5. 实例化并执行Agent
        agent_class = get_agent_class(agent_name)
        agent_instance = agent_class()
        result = agent_instance.execute(**inputs)

        # 6. 处理输出参数
        for output in agent_config["outputs"]:
            output_value = result.get(output["name"])

            # 将输出值连接到下游Agent的输入
            for link in output["links"]:
                for target_agent, target_input in link.items():
                    context_key = f"{target_agent}.{target_input}"
                    context[context_key] = output_value

    return context
