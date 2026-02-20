import os
import yaml

# 获取项目根路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_yaml(file_name="config.yaml"):
    """读取config文件夹里的yaml配置"""
    # 拼接yaml文件的完整路径
    yaml_path = os.path.join(BASE_PATH, "config", file_name)
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# 全局配置对象（其他文件直接导入用）
config = read_yaml()
BASE_URL = config["base_url"]
LOGIN_DATA = config["login"]
HEADERS = config["headers"]
TEST_CASES = config.get("test_cases", {})
CONTRACT_CASES = TEST_CASES.get("contract", {})