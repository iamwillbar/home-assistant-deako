import asyncio
from datetime import timedelta
import logging

import async_timeout
import voluptuous as vol

from .const import DOMAIN

from homeassistant.components.light import LightEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    async def async_update_data():
        try:
            async with async_timeout.timeout(10):
                return await client.deviceList()
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="light",
        update_method=async_update_data,
        update_interval=timedelta(seconds=5),
    )

    await coordinator.async_refresh()

    async_add_entities(
        DeakoLight(coordinator, v, client) for (k, v) in enumerate(coordinator.data)
    )


class ApiError(Exception):
    pass


class DeakoLight(CoordinatorEntity, LightEntity):
    def __init__(self, coordinator, uuid, client):
        super().__init__(coordinator)
        self._client = client
        self._uuid = uuid

    @property
    def unique_id(self):
        return self._uuid

    @property
    def name(self):
        return self.coordinator.data[self.unique_id]["name"]

    @property
    def is_on(self):
        return self.coordinator.data[self.unique_id]["state"]["power"]

    async def async_turn_on(self, **kwargs):
        await self._client.control(self._uuid, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self._client.control(self._uuid, False)
        await self.coordinator.async_request_refresh()
