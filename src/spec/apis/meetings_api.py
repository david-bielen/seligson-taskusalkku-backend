# coding: utf-8
import os

from functools import lru_cache
from typing import Dict, List, Iterator  # noqa: F401
from abc import ABC, abstractmethod
from uuid import UUID
from datetime import date

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
    HTTPException
)

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.orm import Session

from spec.models.extra_models import TokenModel  # noqa: F401
from spec.models.error import Error
from spec.models.meeting import Meeting
from spec.models.meeting_time import MeetingTime
from impl.security_api import get_token_bearer

router = InferringRouter()


def get_database() -> Iterator[Session]:
    """FastAPI dependency that provides a sqlalchemy session

    Yields:
        Iterator[Session]: sqlalchemy session
    """
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """Returns FastAPI session maker

    Returns:
        FastAPISessionMaker: FastAPI session maker
    """
    database_uri = os.environ["SQLALCHEMY_DATABASE_URL"]
    return FastAPISessionMaker(database_uri)


@cbv(router)
class MeetingsApiSpec(ABC):

    database: Session = Depends(get_database)

    @abstractmethod
    async def create_meeting(
        self,
        meeting: Meeting,
        token_bearer: TokenModel = Security(
            get_token_bearer
        ),
    ) -> Meeting:
        ...

    @router.post(
        "/v1/meetings",
        responses={
            200: {"model": Meeting, "description": "Created Meeting"},
            400: {"model": Error, "description": "Invalid request was sent to the server"},
            403: {"model": Error, "description": "Attempted to make a call with unauthorized client"},
            500: {"model": Error, "description": "Internal server error"},
        },
        tags=["Meetings"],
        summary="Create a meeting.",
    )
    async def create_meeting_spec(
        self,
        meeting: Meeting = Body(None, description="Payload", alias="Meeting"),
        token_bearer: TokenModel = Security(
            get_token_bearer
        ),
    ) -> Meeting:
        """Creates a new meeting."""
        return await self.create_meeting(
            meeting,
            token_bearer
        )

    @abstractmethod
    async def list_meeting_times(
        self,
        start_date: date,
        end_date: date,
        token_bearer: TokenModel = Security(
            get_token_bearer
        ),
    ) -> List[MeetingTime]:
        ...

    @router.get(
        "/v1/meetingTimes",
        responses={
            200: {"model": List[MeetingTime], "description": "List of meeting times"},
            400: {"model": Error, "description": "Invalid request was sent to the server"},
            403: {"model": Error, "description": "Attempted to make a call with unauthorized client"},
            500: {"model": Error, "description": "Internal server error"},
        },
        tags=["Meetings"],
        summary="Lists meeting times",
    )
    async def list_meeting_times_spec(
        self,
        start_date: str = Query(None, description="Start date for the date range", alias="startDate"),
        end_date: str = Query(None, description="End date for the date range", alias="endDate"),
        token_bearer: TokenModel = Security(
            get_token_bearer
        ),
    ) -> List[MeetingTime]:
        """Returns list of meeting times"""
        return await self.list_meeting_times(
            self.to_date(start_date),
            self.to_date(end_date),
            token_bearer
        )

    def to_date(self, isodate: str) -> date:
        """Translates given string to date

        Args:
            isodate (str): date as ISO date string

        Raises:
            HTTPException: bad request HTTPException when isodate is not valid ISO date string

        Returns:
            date: parsed date object
        """
        try:
            return date.fromisoformat(isodate)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date {isodate}"
            )

    def to_uuid(self, hexadecimal_uuid: str) -> UUID:
        """Translates given hex to UUID

        Args:
            hexadecimal_uuid (str): UUID in hexadecimal string

        Raises:
            HTTPException: bad request HTTPException when hexadecimal_uuid is not valid UUID string

        Returns:
            UUID: UUID
        """
        try:
            return UUID(hex=hexadecimal_uuid)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid UUID {hexadecimal_uuid}"
            )
