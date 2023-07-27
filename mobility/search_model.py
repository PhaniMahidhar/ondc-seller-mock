from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, json_schema

from ondc.context import Context


class Search(BaseModel):
    context: Context
    message: Any


class OnSearch(BaseModel):
    context: Context
    message: Any


class Select(BaseModel):
    context: Context
    message: Any


class OnSelect(BaseModel):
    context: Context
    message: Any
