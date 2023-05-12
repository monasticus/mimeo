"""The Mimeo HTTP Consumer module.

It exports only one class:
    * HttpConsumer
        A Consumer implementation sending data in HTTP requests.
"""
from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Collection, Generator

import aiohttp
from aiohttp import ClientSession

from mimeo.config.mimeo_config import MimeoOutput
from mimeo.consumers import Consumer

logger = logging.getLogger(__name__)


class HttpConsumer(Consumer):
    """A Consumer implementation sending data in HTTP requests.

    This Consumer is instantiated for the 'http' output direction
    and sends data produced by Mimeo in an HTTP request body
    using Mimeo Output Details.

    Methods
    -------
    consume
        Send data generated by Mimeo in an HTTP request.

    Attributes
    ----------
    method : str
        An HTTP request method
    url : str
        An URL address to send the HTTP request
    """

    def __init__(
            self,
            output: MimeoOutput,
    ):
        """Initialize HTTPConsumer class.

        Parameters
        ----------
        output : MimeoOutput
            Configured Mimeo Output Details
        """
        self.method = output.method
        self.url = HttpConsumer.__build_url(output)
        self.__auth = aiohttp.BasicAuth(output.username, output.password, "utf-8")

    async def consume(
            self,
            data: Collection | Generator,
    ):
        """Send data generated by Mimeo in an HTTP request.

        It is an implementation of Consumer's abstract method.

        Parameters
        ----------
        data : Collection | Generator
            Stringified data generated by Mimeo
        """
        async def send_request(sess: ClientSession, data_unit: str):
            req_id = str(uuid.uuid4())
            logger.info("Sending request %s %s [%s]", self.method, self.url, req_id)
            resp = await sess.request(
                self.method,
                self.url,
                auth=self.__auth,
                data=data_unit,
                headers={"Content-Type": "application/xml"})
            logger.info("[%s] Status: %s", req_id, resp.status)

        async with ClientSession() as s:
            await asyncio.gather(*[send_request(s, d) for d in data])

    @staticmethod
    def __build_url(
            output: MimeoOutput,
    ) -> str:
        """Build a URL based on Mimeo Output Details.

        It populates a URL template using configured output details.
        When port is not configured - it uses host and endpoint values.
        Otherwise, host is followed by the colon and port.

        Parameters
        ----------
        output : MimeoOutput
            Configured Mimeo Output Details

        Returns
        -------
        str
            A valid URL address
        """
        if output.port is None:
            return f"{output.protocol}://{output.host}{output.endpoint}"
        return f"{output.protocol}://{output.host}:{output.port}{output.endpoint}"
