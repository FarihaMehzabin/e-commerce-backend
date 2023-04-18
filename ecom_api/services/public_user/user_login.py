from ecom_api.services.hashing import Hashing
from ecom_api.models.data_table_models.public_user.user_login_result import (
    UserLoginResultDataModel,
)
from ecom_api.db.user_db import UserDB


class UserLoginService:
    def __init__(self):
        self.user_db = UserDB()
        self.hash = Hashing()

    def user_login(self, user):
        data = self.user_db.get_user_by_username(user.username)

        if data is not None:
            hash = data[4]
            
            response = UserLoginResultDataModel(
                self.hash.compare_pass(user.password, hash),
                f"Logged in! Welcome :) {user.username}",
                False,
                data[0],
            )
            return response

        return UserLoginResultDataModel(
            False, "Invalid Credentials. Please try again.", True
        )
