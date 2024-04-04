package at.ac.uibk.smartbuilding.plugin.dtos;

public record IoTDeviceDto (
        String sensorId,
        String connectUri,
        boolean isActive) { }
