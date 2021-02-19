import json
import logging
from telnetlib import Telnet
import uuid

import voluptuous as vol

from homeassistant.components.light import LightEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    client = DeakoClient("172.17.18.125")
    devices = client.deviceList()
    lights = [DeakoLight(client, device) for device in devices]
    async_add_entities(lights)


class DeakoClient:
    def __init__(self, host):
        self._host = host

    def control(self, target, power, **kwargs):
        tn = Telnet(self._host, 23)
        self._send(
            tn,
            "CONTROL",
            target=target.upper(),
            state={"power": power, "dim": 100},
        )
        response = self._receive(tn)
        tn.close()
        return response

    def deviceList(self):
        tn = Telnet(self._host, 23)
        self._send(tn, "DEVICE_LIST")
        response = self._receive(tn)
        number_of_devices = int(response["data"]["number_of_devices"])
        devices = []
        for _ in range(1, number_of_devices):
            response = self._receive(tn)
            devices.append(response)
        tn.close()
        return devices

    def _send(self, client, command, **kwargs):
        message = f'{{"transactionId": "{uuid.uuid4()}", "type": "{command}", "dst": "deako", "src": "hass", "data": {json.dumps(kwargs)}}}\r\n'
        print(message)
        client.write(
            bytes(
                message,
                "ascii",
            )
        )

    def _receive(self, client):
        response = json.loads(client.read_until(b"\r\n"))
        return response


class DeakoLight(LightEntity):
    def __init__(self, client, response):
        self._client = client
        self._uuid = response["data"]["uuid"]
        self._name = response["data"]["name"]
        self._state = response["data"]["state"]["power"]

    @property
    def unique_id(self):
        return self._uuid

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        self._client.control(self._uuid, True)
        self._state = True

    def turn_off(self, **kwargs):
        self._client.control(self._uuid, False)
        self._state = False
