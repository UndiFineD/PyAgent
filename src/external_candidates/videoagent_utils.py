def execute_agent_chain(agent_graph, agent_chain, user_input_graph, interactive=False, input_provider=None):
    context = {}
    for user_input_node in user_input_graph:
        value = None
        if interactive:
            if input_provider:
                value = input_provider(user_input_node)
            else:
                value = input(f"请输入 {user_input_node['node']} ({user_input_node.get('description','')}): ")
        else:
            value = user_input_node.get('value')
        for link in user_input_node.get('links', []):
            for agent_name, input_param in link.items():
                context_key = f"{agent_name}.{input_param}"
                context[context_key] = value
    for agent_name in agent_chain:
        agent_config = next((a for a in agent_graph if a.get("node") == agent_name), None)
        if not agent_config:
            raise ValueError(f"Missing agent config for {agent_name}")
        inputs = {}
        for input_param in agent_config.get("inputs", []):
            context_key = f"{agent_name}.{input_param['name']}"
            if context_key not in context:
                raise ValueError(f"Missing required parameter: {context_key}")
            inputs[input_param["name"]] = context[context_key]
        agent_class = agent_config.get('class')
        if not agent_class:
            raise ValueError(f"Agent class for {agent_name} not provided")
        agent_instance = agent_class()
        result = agent_instance.execute(**inputs)
        for output in agent_config.get("outputs", []):
            output_value = result.get(output["name"]) if isinstance(result, dict) else None
            for link in output.get("links", []):
                for target_agent, target_input in link.items():
                    context_key = f"{target_agent}.{target_input}"
                    context[context_key] = output_value
    return context
