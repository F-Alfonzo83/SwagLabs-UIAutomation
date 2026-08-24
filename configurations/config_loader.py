import sys
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class User:
    username: str
    password: str


class ConfigLoader:
    """ConfigLoader is responsible for loading configuration files.

    Loads files that contain url paths

    Example:
        config_loader = ConfigLoader()
    """
    # Path to files to be Loaded

    def __init__(self):
        self.PATHS_YAML_FILE = Path(__file__).parent / "config_base.yaml"
        self.USERS_YAML_FILE = Path(__file__).parent / "public_users.yaml"

        self.paths = self.yaml_file_loader(self.PATHS_YAML_FILE)
        self.users = self.yaml_file_loader(self.USERS_YAML_FILE)

    @staticmethod
    def yaml_file_loader(yaml_file_location: Path) -> dict:
        try:
            with open(yaml_file_location, "r", encoding="utf-8") as yaml_file:
                loaded_yaml_file = yaml.safe_load(yaml_file)
        except FileNotFoundError as fnf_error:
            print(f"File {yaml_file_location} not found. Aborting Execution.\nSystem Error: {fnf_error}")
            sys.exit(1)
        except yaml.YAMLError as yaml_error:
            print(f"Error loading configuration file. Aborting Execution.\nSystem Error: {yaml_error}")
            sys.exit(1)
        return loaded_yaml_file

    def login_page_url(self) -> str:
        return self.paths["environments"]["testing"]["login_page"]

    def products_page_url(self) -> str:
        return self.paths["environments"]["testing"]["products_page"]

    def cart_page_url(self) -> str:
        return self.paths["environments"]["testing"]["product_cart"]

    def checkout_information_page_url(self):
        return self.paths["environments"]["testing"]["checkout_information_page"]

    def checkout_overview_page_url(self):
        return self.paths["environments"]["testing"]["checkout_overview_page"]

    def checkout_complete_page_url(self):
        return self.paths["environments"]["testing"]["checkout_complete_page"]

    def get_user(self, user_role: str):
        try:
            selected_user = self.users[user_role]
        except KeyError:
            print(f"User role {user_role} not found. Exiting now")
            sys.exit(1)

        user_creds = User(username=selected_user["username"],
                          password=selected_user["password"])
        return user_creds


# THIS IS A TESTING AREA
if __name__ == "__main__":
    config_loader = ConfigLoader()
    print(config_loader.login_page_url())
    print(config_loader.products_page_url())
    print(config_loader.cart_page_url())
    print(config_loader.checkout_information_page_url())
    print(config_loader.checkout_overview_page_url())
    print(config_loader.checkout_complete_page_url())
    print(config_loader.paths)
    print(config_loader.users)
    print(config_loader.get_user("standard_user"))
