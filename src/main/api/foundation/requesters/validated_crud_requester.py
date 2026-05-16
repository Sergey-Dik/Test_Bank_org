from typing import Optional

from requests import Response

from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.requester_allure import attach_validated_model
from src.main.api.models.base_model import BaseModel


class ValidatedCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self._crud = CrudRequester(request_spec, endpoint, response_spec)

    def get(self, path_suffix: str = "") -> BaseModel:
        response = self._crud.get(path_suffix)
        model = self.endpoint.response_model.model_validate(response.json())
        attach_validated_model(model)
        return model

    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        response = self._crud.post(model)
        validated = self.endpoint.response_model.model_validate(response.json())
        attach_validated_model(validated)
        return validated

    def delete(self, resource_id: int) -> Response:
        return self._crud.delete(resource_id)
