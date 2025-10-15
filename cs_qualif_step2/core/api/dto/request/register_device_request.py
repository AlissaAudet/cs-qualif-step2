import re

import app
from pydantic import BaseModel, validator

from cs_qualif_step2.config.get_device_service import device_repository
from cs_qualif_step2.core.api.handler.invalid_input_exception_handler import invalid_input_exception_handler
from cs_qualif_step2.core.domain.device.exception import DeviceWithSameMacAddressException, invalidMacAddressException, invalid_input_exception
from cs_qualif_step2.core.domain.device.device_id import DeviceId
from cs_qualif_step2.core.domain.device.devicefactory import DeviceFactory


class DeviceRegistrationRequest(BaseModel):
    macAddress: str
    model: str
    firmwareVersion: str
    serialNumber: str
    displayName: str = None
    location: str = None
    timezone: str = None

    @validator('macAddress', 'model', 'firmwareVersion', 'serialNumber')
    def not_empty(cls, v):
        if v is None or v.strip() == '':
            raise ValueError('Field cannot be empty or null')
        return v


valid_mac_format = re.compile("^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")

@app.route('api/v1/devices', methods=['POST'])
@app.post("/registerDevice", status_code=200)
def create_device(macAddress: str,
                  model: str, firmwareVersion: str,
                  serialNumber: str,
                  displayName: str,
                  location: str,
                  timezone: str):
    device_id = DeviceId.generate()
    Device = DeviceFactory().create_device(
        device_id=device_id,
        macAddress=macAddress,
        model=model,
        firmwareVersion=firmwareVersion,
        serialNumber=serialNumber,
        displayName=displayName,
        location=location,
        timezone=timezone
    )

    if device_repository.find_by_mac_address(macAddress=macAddress) is not None:
        device_repository.save(Device)
    else:
         raise DeviceWithSameMacAddressException("409 Conflict - MAC address déjà existante dans le système")

    if valid_mac_format.match(macAddress) is None:
        raise invalidMacAddressException("400 Bad Request - Format MAC address invalide (doit être XX:XX:XX:XX:XX:XX)")

    if not all([macAddress, model, firmwareVersion, serialNumber, location, timezone]):
        raise invalid_input_exception("400 Bad Request - Champs obligatoires manquants (macAddress, model, firmwareVersion, serialNumber, location, timezone)")

    if not all([isinstance(field, str) for field in [macAddress, model, firmwareVersion, serialNumber, displayName, location, timezone]]):
        raise invalid_input_exception("400 Bad Request - Valeurs vides ("", null) dans les champs obligatoires")
    return {"message": "Device est enregistré", "device": Device.get_device_id()}

