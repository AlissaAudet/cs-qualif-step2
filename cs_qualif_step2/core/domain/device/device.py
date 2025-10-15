from logging import raiseExceptions

import app
import hashlib
import re

from cs_qualif_step2.config.get_device_service import device_repository
from cs_qualif_step2.core.domain.device.device_id import DeviceId
from cs_qualif_step2.core.domain.device.devicefactory import DeviceFactory

class Device:
    def __init__(self,
        device_id: DeviceId,
        macAddress: str,
        model: str,
        firmwareVersion: str,
        serialNumber: str,
        displayName: str,
        location: str,
        timezone: str
    ) -> None:
        self.__device_id = device_id
        self.__macAddress: str = macAddress
        self.__model: str = model
        self.__firmwareVersion: str = firmwareVersion
        self.__serialNumber: str = serialNumber
        self.__displayName: str = displayName
        self.__location: str = location
        self.__timezone: str = timezone

    def get_device_id(self) -> DeviceId:
        return self.__device_id

    def get_mac_address(self) -> str:
        return self.__macAddress



