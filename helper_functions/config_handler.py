"""Handles the configs for the app"""
from json import load
from typing import Callable

from twitchio.ext.commands import Context

with open("configs-user.json") as config_file:
    CONFIGS: dict = load(config_file)


def check_for_config(config: str) -> bool:
    """Checks if the given config is enabled or not.

    Config categories are split with a "."

    :param config: The config to check
    :type config: str
    :return: Whether the config is enabled or not
    :rtype: bool
    """

    categories = config.split(".")

    current_category = CONFIGS
    for index, category in enumerate(categories):
        if category in current_category.keys() and index != len(categories) - 1:
            current_category = current_category[category]
        elif category in list(current_category.keys()):
            return current_category[category]
        else:
            # The config is not known, return false
            return False


def enable_function_with_config(*args, config: str):
    """Enables the chained functions if the given config is enabled.

    Configs categories are split with a "."

    :param config: The config to check
    :type config: Whether the config is enabled or not
    :return:
    :rtype:
    """

    if check_for_config(config):

        def decorator(func: Callable) -> Callable:
            return func

        return decorator
    return blank_function


def enable_function_if_any_config(*args, config: list[str]):
    """Enables the chained functions if any of the given configs are enabled.

    Configs categories are split with a "."

    :param config: The config to check
    :type config: Whether the config is enabled or not
    :return:
    :rtype:
    """

    if any([check_for_config(config) for config in config]):

        def decorator(func: Callable) -> Callable:
            return func

        return decorator
    return blank_function


def blank_function(*args, **kwargs):
    """A blank function which allows the code to still run when a function is disabled via config

    :return:
    :rtype:
    """
    pass
