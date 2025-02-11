# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401


class PortfolioSummary(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    PortfolioSummary - a model defined in OpenAPI

        subscriptions: The subscriptions of this PortfolioSummary.
        redemptions: The redemptions of this PortfolioSummary.
    """
    subscriptions: int
    redemptions: int


PortfolioSummary.update_forward_refs()
