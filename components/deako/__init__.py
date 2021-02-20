"""The Deako integration."""
import asyncio
import json
from telnetlib import Telnet
import uuid

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS = ["light"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Deako component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Deako from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = DeakoClient("172.17.18.125")

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class DeakoClient:
    def __init__(self, host):
        self._host = host

    async def control(self, target, power, **kwargs):
        with Telnet(self._host, 23) as tn:
            await self._send(
                tn,
                "CONTROL",
                target=target.upper(),
                state={"power": power, "dim": 100},
            )
            response = await self._receive(tn)
        return response

    async def deviceList(self):
        devices = []
        with Telnet(self._host, 23) as tn:
            await self._send(tn, "DEVICE_LIST")
            response = await self._receive(tn)
            number_of_devices = int(response["data"]["number_of_devices"])
            for _ in range(1, number_of_devices):
                response = await self._receive(tn)
                devices.append(response)
        return {device["data"]["uuid"]: device["data"] for device in devices}

    async def _send(self, client, command, **kwargs):
        message = f'{{"transactionId": "{uuid.uuid4()}", "type": "{command}", "dst": "deako", "src": "hass", "data": {json.dumps(kwargs)}}}\r\n'
        client.write(
            bytes(
                message,
                "ascii",
            )
        )

    async def _receive(self, client):
        response = json.loads(client.read_until(b"\r\n"))
        return response
