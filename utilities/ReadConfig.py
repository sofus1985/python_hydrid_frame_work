import configparser
import os

class ReadConfig:
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configfiles", "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)

    @staticmethod
    def getBrowser():
        return ReadConfig.config["DEFAULT"].get("browser", "chrome")

    @staticmethod
    def getApplicationURL():
        return ReadConfig.config["DEFAULT"].get("url")

    @staticmethod
    def getImplicitWait():
        return int(ReadConfig.config["DEFAULT"].get("implicit_wait", 10))

    @staticmethod
    def getFluentTimeout():
        return int(ReadConfig.config["DEFAULT"].get("fluent_timeout", 20))

    @staticmethod
    def getFluentPoll():
        return float(ReadConfig.config["DEFAULT"].get("fluent_poll", 0.5))
