from instance.config import app_config, BaseConfig

def loadConfig(MODE):
    if MODE == 'development':
        return app_config[MODE]
    else:
        return BaseConfig