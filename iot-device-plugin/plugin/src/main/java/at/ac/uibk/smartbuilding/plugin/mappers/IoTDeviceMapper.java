package at.ac.uibk.smartbuilding.plugin.mappers;

import at.ac.uibk.smartbuilding.plugin.dtos.IoTDeviceDto;
import at.ac.uibk.smartbuilding.plugin.models.IoTDevice;
import org.springframework.stereotype.Component;

@Component
public class IoTDeviceMapper {

    public IoTDevice toModel(IoTDeviceDto ioTDeviceDto) {
        var device = new IoTDevice();
        device.setConnectUri(ioTDeviceDto.connectUri());
        device.setSensorId(ioTDeviceDto.sensorId());
        device.setActive(ioTDeviceDto.isActive());
        return device;
    }

    public IoTDeviceDto toDto(IoTDevice ioTDevice) {
        return new IoTDeviceDto(ioTDevice.getSensorId(), ioTDevice.getConnectUri(), ioTDevice.isActive());
    }
}
