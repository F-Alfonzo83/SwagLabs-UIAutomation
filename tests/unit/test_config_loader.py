from configurations.config_loader import ConfigLoader, UserRole

config = ConfigLoader()


def test_user_roles_match_config():
    yaml_roles = set(config.users)
    user_role = set(role.value for role in UserRole)
    assert yaml_roles == user_role
