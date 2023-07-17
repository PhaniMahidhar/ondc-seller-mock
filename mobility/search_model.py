from typing import Any

from pydantic import BaseModel, json_schema

from ondc.context import Context


class Search(BaseModel):
    context: Context
    message: Any


class OnSearch(BaseModel):
    context: Context
    message: Any

