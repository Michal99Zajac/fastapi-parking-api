class RoleDoesntExistException(Exception):
    """
    Role in the database doesn't exist exception
    """

    def __init__(self) -> None:
        self.status = 503
        self.message = "Role doesn't exist"
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    """
    User in the database already exists
    """

    def __init__(self) -> None:
        self.message = "User already exists"
        self.status = 409
        super().__init__(self.message)
