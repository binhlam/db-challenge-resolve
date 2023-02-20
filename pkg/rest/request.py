# -*- encoding: utf-8 -*-
from jsonschema import validate, ValidationError, SchemaError


class BaseValidation:
    @classmethod
    def validate_schema(cls, req, schema):
        try:
            validate(req, schema)
        except (ValidationError, SchemaError) as e:
            return False, e.message

        return True, None
