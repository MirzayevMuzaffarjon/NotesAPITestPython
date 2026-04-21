"""Test assertion utilities."""
import logging
from typing import Type, TypeVar, Any

import pytest_check as check
from jsonschema import validate, ValidationError as JsonSchemaValidationError
from pydantic import BaseModel, ValidationError as PydanticValidationError
from requests import Response


T = TypeVar("T", bound=BaseModel)


class Assertions:
    """Assertion helpers for API testing."""
    
    @staticmethod
    def validate_status_code(response: Response, expected_status_code: int) -> None:
        """Validate HTTP response status code.
        
        Args:
            response: HTTP response object.
            expected_status_code: Expected status code.
        """
        actual_status_code = response.status_code
        logging.info(
            f"Validating status code: Expected {expected_status_code}, "
            f"Actual {actual_status_code}"
        )
        check.equal(actual_status_code, expected_status_code)
    
    @staticmethod
    def validate_json_schema(response: Response, schema: dict) -> None:
        """Validate response JSON against a schema.
        
        Args:
            response: HTTP response object.
            schema: JSON schema dictionary.
        """
        try:
            response_json = response.json()
            validate(instance=response_json, schema=schema)
            logging.info("JSON Schema validation passed successfully.")
            
        except ValueError:
            logging.error("Response body is not a valid JSON")
            check.is_true(False, "Response body is not a valid JSON")
            
        except JsonSchemaValidationError as e:
            logging.error(f"JSON Schema validation failed: {e.message}")
            check.is_true(False, f"JSON Schema validation failed: {e.message}")
    
    @staticmethod
    def validate_json_schema_pydantic(json_data: dict, model: Type[T]) -> T:
        """Validate JSON data against a Pydantic model.
        
        Args:
            json_data: Dictionary with JSON data.
            model: Pydantic model class.
            
        Returns:
            Validated Pydantic model instance.
            
        Raises:
            AssertionError: If validation fails.
        """
        try:
            validated = model(**json_data)
            return validated
        except PydanticValidationError as e:
            raise AssertionError(
                f"Schema '{model.__name__}' didn't match.\n"
                f"Error: {e}\n"
                f"Got data: {json_data}"
            )
    
    @staticmethod
    def validate_to_equality(a: Any, b: Any, msg: str = None) -> None:
        """Validate that two values are equal.
        
        Args:
            a: First value.
            b: Second value.
            msg: Optional custom error message.
        """
        default_msg = f"Validation failed: {a} != {b}"
        logging.info(f"Validating equality: {a} == {b}")
        check.equal(a=a, b=b, msg=msg or default_msg)