from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import asyncio
from aiohttp import ClientSession, ClientResponse, TCPConnector
from aiohttp.client_exceptions import ClientConnectionError
from .errors import (
    BadRequest,
    LoginFailure,
    Unauthorised,
    NonImplementedError,
    UnknownError,
    ServiceUnavailable,
)
import ujson

if TYPE_CHECKING:
    from ...bot import Bot


async def client_error(resp: ClientResponse):
    if resp.status == 429:
        json = await resp.json()
        await asyncio.sleep(json["retry_after"])

    elif resp.status == 400:
        text = await resp.text()
        raise BadRequest(text, resp.status)

    elif resp.status == 401:
        text = await resp.text()
        raise LoginFailure(text, resp.status)

    elif resp.status == 403:
        text = await resp.text()
        raise Unauthorised(text, resp.status)

    else:
        text = await resp.text()
        raise UnknownError(text, resp.status)


async def server_error(resp: ClientResponse):
    if resp.status == 501:
        text = await resp.text()
        raise NonImplementedError(text, resp.status)

    if resp.status == 503:
        text = await resp.text()
        raise ServiceUnavailable(text, resp.status)

    text = await resp.text()
    raise UnknownError(text, resp.status)


class DiscordHttp:
    ROOT = "https://canary.discord.com/api/v9"

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.token: Optional[str] = None
        self.fingerprint: Optional[str] = None
        self.cookie: Optional[str] = None
        self.session: Optional[ClientSession] = None

    async def create_session(self):
        headers = {
            "Accept-Encoding":
            "gzip, deflate, br",
            "user-agent": ("Mozilla/5.0 (Windows NT 10.0; WOW64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "discord/1.0.9016 Chrome/108.0.5359.215 "
                           "Electron/22.3.12 Safari/537.36"),
            "Content-Type":
            "application/json",
            "X-Discord-Locale":
            "en-GB",
            "X-context-properties":
            ("eyJsb2NhdGlvbiI6Ikludml0ZSBCdXR0b24gRW1iZWQiLCJsb2N"
             "hdGlvbl9ndWlsZF9pZCI6bnVsbCwibG9jYXRpb25fY2hhbm5lbF9pZCI"
             "6IjEwOTkwOTMxODEy"
             "NTUxNDM1MjUiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjEsImxvY2F0"
             "aW9uX21lc3NhZ2VfaWQiOiIxMTE2NTE0MDMyODk2MTgwMjU0In0="),
            "connection":
            "keep-alive",
            "Sec-Fetch-Dest":
            "empty",
            "Sec-Fetch-Mode":
            "cors",
            "Sec-Fetch-Site":
            "same-origin",
            "sec-ch-ua-platform":
            '"Windows"',
            "origin":
            "https://discord.com",
            "DNT":
            "1",
            "referrer-policy":
            "strict-origin-when-cross-origin",
            "x-debug-options": ("logGatewayEvents,"
                                "logOverlayEvents,"
                                "logAnalyticsEvents,"
                                "bugReporterEnabled"),
            "x-discord-timezone":
            "Europe/London",
            "TE":
            "trailers",
        }
        additional_headers = {}
        if (self.token is not None) and (self.fingerprint is not None):
            additional_headers = {
                "authorization": self.token,
                "x-fingerprint": self.fingerprint,
            }
        elif self.token is not None:
            additional_headers = {"authorization": self.token}

        elif self.fingerprint is not None:
            additional_headers = {"x-fingerprint": self.fingerprint}

        headers.update(additional_headers)
        return ClientSession(
            headers=headers,
            connector=TCPConnector(
                ssl=False,
                keepalive_timeout=10,
                ttl_dns_cache=204,
                limit=0,
                limit_per_host=0,
            ),
            trust_env=False,
            skip_auto_headers=None,
            json_serialize=ujson.dumps,
            auto_decompress=True,
        )

    async def get_fingerprint(self):
        self.fingerprint = (await self.request("GET",
                                               "/experiments"))["fingerprint"]

    async def get_cookie(self):
        if self.session is None:
            self.session = await self.create_session()

        resp = await self.session.request("GET", "https://discord.com")
        dcf = (
            resp.cookies["__dcfduid"].coded_value
            if resp.cookies.get("__dcfduid") is not None
            else ""
        )
        sdc = (
            resp.cookies["__sdcfduid"].coded_value
            if resp.cookies.get("__sdcfduid") is not None
            else ""
        )
        cfr = (
            resp.cookies["__cfruid "].coded_value
            if resp.cookies.get("__cfruid") is not None
            else ""
        )
        self.cookie = f"__dcfduid={dcf};__sdcfduid={sdc};__cfruid={cfr}"

    async def static_login(self, token: str):
        self.token = token
        return await self.request("GET",
                                  "/users/@me",
                                  headers={"authorization": token})

    async def close(self):
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def request(self, method: str, endpoint: str, **kwargs):
        while True:
            try:
                if self.session is not None:
                    resp = await self.session.request(method,
                                                      self.ROOT + endpoint,
                                                      **kwargs)
                    if resp.ok:
                        return await resp.json()

                    if 399 < resp.status < 500:
                        await client_error(resp)

                    if 499 < resp.status < 600:
                        await server_error(resp)

                else:
                    self.session = await self.create_session()

            except ClientConnectionError:
                await self.close()
                self.session = await self.create_session()
