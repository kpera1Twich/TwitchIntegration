"""Validation methods"""


async def check_for_user(author: str, user: str = "kpera1") -> bool:
    """Checks if the command was sent by a user

    :param author: The username of the user who sent the message
    :type author: str
    :param user: The username of the user
    :type user: str
    :return: Whether the message was sent by that user
    :rtype: bool
    """
    if author == user:
        return True
    return False
