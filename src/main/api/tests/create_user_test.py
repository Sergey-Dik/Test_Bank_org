import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.db.crud.user_crud import UserCrudDb
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.generators.test_data_strategy import with_unique_username
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.utils.api_assertions import assert_bad_request, assert_ok_model


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.smoke
    def test_create_user_valid(self, api_manager: ApiManager, db_session: Session):
        create_user_request = with_unique_username(RandomModelGenerator.generate(CreateUserRequest))
        response = api_manager.admin_steps.create_user(create_user_request)
        result = assert_ok_model(response, CreateUserResponse)
        api_manager.admin_steps.register_created_user(result)

        assert create_user_request.username == result.username, "Username should match request"
        assert create_user_request.role == result.role, "Role should match request"
        DbAssertions.assert_user_exists(db_session, create_user_request.username)

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Max1", "Pas!sw0rд"),
            ("Max2", "Pas!sw0"),
            ("Max3", "pas!sw0rd"),
            ("Max4", "PASSSWORD"),
            ("Max5", "PAS!WORD"),
        ],
    )
    def test_create_user_invalid(
        self,
        db_session: Session,
        username: str,
        password: str,
        api_manager: ApiManager,
    ):
        create_user_request = CreateUserRequest(
            username=username, password=password, role="ROLE_USER"
        )
        response = api_manager.admin_steps.create_invalid_user(create_user_request)
        assert_bad_request(response)
        user_from_db = UserCrudDb.get_user_by_username(db_session, username)
        assert user_from_db is None, "Invalid user must not be stored in DB"
