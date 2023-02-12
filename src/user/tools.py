from src.db.models import User


def pick_out_permissions(user: User) -> list[str]:
    """Get all user permissions without any repetitions

    Args:
        user (User): any user

    Returns:
        list[str]: list of permissions
    """
    # get all permissions from roles and extract their names
    permissions_subsets: list[list[str]] = [
        list(map(lambda permission: str(permission.name), role.permissions)) for role in user.roles
    ]

    # flat the list of subsets
    # see: https://stackoverflow.com/a/45323085
    permissions: list[str] = []
    for subset in permissions_subsets:
        permissions.extend(subset)

    # remove repetitions and return
    return list(set(permissions))
