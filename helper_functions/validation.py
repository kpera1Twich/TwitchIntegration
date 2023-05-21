"""Validation methods"""


async def check_for_trusted_members(author: str) -> bool:
    """Checks if the command was sent by a user

    :param author: The username of the user who sent the message
    :type author: str
    :return: Whether the message was sent by that user
    :rtype: bool
    """
    if author in ["kpera1", "xthatxchickx", "e1ndude"]:
        return True
    return False


async def check_for_rights(author: str, allowed_rights: list[str]) -> bool:
    ...
