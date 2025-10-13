"""Vinorage API Client."""

from __future__ import annotations

import re
import socket
from typing import Any

import aiohttp
import async_timeout


class VinorageApiClientError(Exception):
    """Exception to indicate a general API error."""


class VinorageApiClientCommunicationError(
    VinorageApiClientError,
):
    """Exception to indicate a communication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    response.raise_for_status()


class VinorageApiClient:
    """Vinorage API Client for local network communication."""

    def __init__(
        self,
        host: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the Vinorage API Client."""
        self._host = host
        self._session = session
        self._base_url = f"http://{host}"

    async def async_get_data(self) -> dict[str, Any]:
        """Get data from the device by scraping the HTML page."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(self._base_url)
                _verify_response_or_raise(response)
                html = await response.text()

                # Parse the LED brightness value from the HTML
                # Looking for: <input id="level" ... value="X" ...>
                led_match = re.search(r'id="level"[^>]*value="(\d+)"', html)
                led_brightness = int(led_match.group(1)) if led_match else 0

                return {
                    "led_brightness": led_brightness,
                }

        except TimeoutError as exception:
            msg = f"Timeout error fetching information from {self._host}"
            raise VinorageApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information from {self._host}: {exception}"
            raise VinorageApiClientCommunicationError(msg) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = (
                f"Unexpected error fetching information from {self._host}: {exception}"
            )
            raise VinorageApiClientError(msg) from exception

    async def async_set_led_brightness(self, brightness: int) -> None:
        """Set the LED brightness (0-100)."""
        if not 0 <= brightness <= 100:
            msg = f"Brightness must be between 0 and 100, got {brightness}"
            raise ValueError(msg)

        try:
            async with async_timeout.timeout(10):
                response = await self._session.post(
                    f"{self._base_url}/led_set",
                    data={"level": brightness},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                _verify_response_or_raise(response)

        except TimeoutError as exception:
            msg = f"Timeout setting LED brightness on {self._host}"
            raise VinorageApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error setting LED brightness on {self._host}: {exception}"
            raise VinorageApiClientCommunicationError(msg) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = (
                f"Unexpected error setting LED brightness on {self._host}: {exception}"
            )
            raise VinorageApiClientError(msg) from exception

    async def async_control_actuator(self, command: int) -> None:
        """
        Control the cellar actuator.

        Args:
            command: 0 = stop, 1 = up, 2 = down
        """
        if command not in (0, 1, 2):
            msg = f"Command must be 0 (stop), 1 (up), or 2 (down), got {command}"
            raise ValueError(msg)

        try:
            async with async_timeout.timeout(10):
                response = await self._session.post(
                    f"{self._base_url}/act_control",
                    data={"act": command},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                _verify_response_or_raise(response)

        except TimeoutError as exception:
            msg = f"Timeout controlling actuator on {self._host}"
            raise VinorageApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error controlling actuator on {self._host}: {exception}"
            raise VinorageApiClientCommunicationError(msg) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Unexpected error controlling actuator on {self._host}: {exception}"
            raise VinorageApiClientError(msg) from exception
