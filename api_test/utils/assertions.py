from requests import Response
import logging
import pytest_check as check
from jsonschema import validate, ValidationError
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError

class Assertions:

    @staticmethod
    def validate_status_code(response: Response, expected_status_code: int):
        status_code = response.status_code
        logging.info(f"Validating status code: Expected {expected_status_code}, Actual {status_code}")
        check.equal(status_code, expected_status_code)

    @staticmethod
    def validate_json_schema(response: Response, schema: dict):
        try:
            response_json = response.json()
            validate(instance=response_json, schema=schema)
            logging.info("JSON Schema validation passed successfully.")

        except ValueError:
            logging.error("Response body is not a valid JSON")
            check.is_true(False, "Response body is not a valid JSON")

        except ValidationError as e:
            logging.error(f"JSON Schema validation failed: {e.message}")
            check.is_true(False, f"JSON Schema validation failed: {e.message}")



    T = TypeVar("T", bound=BaseModel)
    @staticmethod
    def validate_json_schema_pydantic(json, model: Type[T]) -> Type[T]:
        try:
            validated = model(**json)
            return validated
        except ValidationError as e:
            raise AssertionError(
                f"Schema '{model.__name__}' didn't match.\n"
                f"Error: {e}\n"
                f"Got data: {json}"
            )