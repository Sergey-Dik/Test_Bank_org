from typing import Any, List

from requests import Response

from src.main.api.specs.contract_specs import ContractSpecs


class BaseSteps:
    def __init__(self, created_obj: List[Any]):
        self.created_obj = created_obj

    @staticmethod
    def _assert_error_contract(response: Response) -> None:
        ContractSpecs.assert_error_payload(response.json())
