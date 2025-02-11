# coding: utf-8

from fastapi_utils.cbv import cbv
from spec.apis.system_api import SystemApiSpec, router as system_api_router


@cbv(system_api_router)
class SystemApiImpl(SystemApiSpec):

    async def ping(self) -> str:
        return "pong"
