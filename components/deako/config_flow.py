"""Config flow for Deako."""
from homeassistant import config_entries
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


async def _async_has_devices(hass) -> bool:
    """Return if there are devices that can be discovered."""
    # TODO Check if there are any devices that can be discovered in the network.
    devices = [
        "172.17.18.125"
    ]  # await hass.async_add_executor_job(my_pypi_dependency.discover)
    return len(devices) > 0


config_entry_flow.register_discovery_flow(
    DOMAIN, "Deako", _async_has_devices, config_entries.CONN_CLASS_UNKNOWN
)
