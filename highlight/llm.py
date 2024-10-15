def list_llms(config: dict):
    """List all Large Language Models available in the configuration"""
    llms = []
    for provider, spec in config["llm"].items():
        for model in spec["models"]:
            llms.append(f"{provider}: {model}")
    return llms
