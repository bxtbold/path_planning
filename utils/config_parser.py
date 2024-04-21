import os
import yaml


def get_package_directory():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def load_configs():
    package_dir = get_package_directory()
    config_dir = f"{package_dir}/config.yaml"
    with open(config_dir, "r") as file:
        data = yaml.safe_load(file)
        return data["path_planning"]
