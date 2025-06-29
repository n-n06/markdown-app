from typing import Any

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.exceptions import InvalidPasswordException

from src.auth.models import User
from src.auth.schemas import UserCreate
from src.auth.config import SECRET
from src.auth.db import get_user_db



class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


    async def validate_password(
            self, 
            password: str, 
            user: UserCreate | User
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters long!"
            )
        if user.email.lower() in password.lower():
            raise InvalidPasswordException(
                reason="Password should not contain the email"
            )
        if any((
            password.isalpha(),
            password.islower(),
            password.isupper(),
            password.isnumeric(),
            password.isspace(),
        )):
            raise InvalidPasswordException(
                reason="Password should contain a mix of uppercase " + 
                " and lowercase letters, numbers and symbols"
            )


    async def on_after_register(
            self, user: User, request: Request | None = None
    ) -> None:
        # Any post register logic
        pass


    async def on_after_update(
        self,
        user: User,
        update_dict: dict[str, Any],
        request: Request | None = None,
    ):
        # Post update logic
        pass


    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        pass


    async def on_after_verify(
        self, user: User, request: Request | None = None
    ):
        pass


    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        pass


    async def on_after_reset_password(self, user: User, request: Request | None = None):
        pass

    async def on_before_delete(
        self, user: User, request: Request | None = None
    ):
        pass


    async def on_after_delete(
            self, user: User, request: Request | None = None
    ):
        pass



async def get_user_manager(
        user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
):
    yield UserManager(user_db)
