package at.ac.uibk.smartbuilding.plugin.controllers;

import at.ac.uibk.smartbuilding.plugin.dtos.IoTDeviceDto;
import at.ac.uibk.smartbuilding.plugin.mappers.IoTDeviceMapper;
import at.ac.uibk.smartbuilding.plugin.services.IoTDeviceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/devices")
public class IoTDeviceController {
    private final static IoTDeviceMapper MAPPER = new IoTDeviceMapper();
    private final IoTDeviceService ioTDeviceService;

    @Autowired
    public IoTDeviceController(IoTDeviceService ioTDeviceService) {
        this.ioTDeviceService = ioTDeviceService;
    }

    @PostMapping
    public void postIoTDevice(@RequestBody IoTDeviceDto iotDeviceDto) {
        var device = MAPPER.toModel(iotDeviceDto);
        ioTDeviceService.save(device);
    }

    @GetMapping("/{id}")
    public IoTDeviceDto getIoTDevice(@PathVariable String id) {
        var device = ioTDeviceService.getIoTDevice(id);
        return new IoTDeviceDto(device.getSensorId(), device.getConnectUri(), device.isActive());
    }

    @GetMapping
    public List<IoTDeviceDto> getAllIoTDevices() {
        return ioTDeviceService.getAllIoTDevices().stream().map(MAPPER::toDto).toList();
    }

    @DeleteMapping("/{id}")
    public void deleteIoTDevice(@PathVariable String id) {
        ioTDeviceService.delete(id);
    }
}
