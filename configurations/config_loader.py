import sys
from pathlib import Path
import yaml


class ConfigLoader:
    """ConfigLoader is responsible for loading configuration files.

    Loads files that contain url paths

    Example:
        config_loader = ConfigLoader()
    """

    # Path to files to be Loaded
    CONFIG_BASE_YAML_FILE = Path(__file__).parent / "config_base.yaml"

    try:
        with open(CONFIG_BASE_YAML_FILE, "r", encoding="utf-8") as yaml_file:
            config_base_yaml = yaml.safe_load(yaml_file)
    except FileNotFoundError as fnf_error:
        print(f"File {CONFIG_BASE_YAML_FILE} not found. Aborting Execution.\nSystem Error: {fnf_error}")
        sys.exit(1)
    except yaml.YAMLError as yaml_error:
        print(f"Error loading configuration file. Aborting Execution.\nSystem Error: {yaml_error}")
        sys.exit(1)

    def login_page_url(self) -> str:
        return self.config_base_yaml["environments"]["testing"]["login_page"]

    def products_page_url(self) -> str:
        return self.config_base_yaml["environments"]["testing"]["products_page"]

    def cart_page_url(self) -> str:
        return self.config_base_yaml["environments"]["testing"]["product_cart"]

    def checkout_information_page_url(self):
        return self.config_base_yaml["environments"]["testing"]["checkout_information_page"]

# THIS IS A TESTING AREA


if __name__ == "__main__":
    config_loader = ConfigLoader()
    print(config_loader.login_page_url())
    print(config_loader.products_page_url())
    print(config_loader.cart_page_url())
    print(config_loader.checkout_information_page_url())
