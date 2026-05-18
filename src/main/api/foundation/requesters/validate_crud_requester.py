from typing import Optional

from requests import Response

from src.main.api.foundation.crud_endpoint import CrudEndpoint
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.requester_allure import attach_validated_model
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.requester import Requester


class ValidateCrudRequester(HttpRequester):
    def __init__(
        self,
        request_spec: dict[str, str],
        endpoint: CrudEndpoint,
        response_spec,
    ):
        super().__init__(request_spec, endpoint, response_spec)
        self._requester = Requester(request_spec, endpoint, response_spec)

    def get(self, path_suffix: str = "") -> BaseModel:
        response = self._requester.get(path_suffix)
        model = self.endpoint.response_model.model_validate(response.json())
        attach_validated_model(model)
        return model

    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        response = self._requester.post(model)
        validated = self.endpoint.response_model.model_validate(response.json())
        attach_validated_model(validated)
        return validated

    def delete(self, resource_id: int) -> Response:
        return self._requester.delete(resource_id)
