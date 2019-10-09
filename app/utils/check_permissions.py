from utils.user_getter import get_session_user_permissions


async def is_permitted(request, required_permissions):
    user_permissions = await get_session_user_permissions(request)
    for required_permision in required_permissions:
        if not user_permissions[required_permision]:
            return False
    return user_permissions
