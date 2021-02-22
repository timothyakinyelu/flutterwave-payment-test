from instance.config import app_config, BaseConfig

def loadConfig(MODE):
    try:
        if MODE == 'staging':
            return app_config[MODE]
        else:
            return app_config[MODE]
    except ImportError:
        return BaseConfig