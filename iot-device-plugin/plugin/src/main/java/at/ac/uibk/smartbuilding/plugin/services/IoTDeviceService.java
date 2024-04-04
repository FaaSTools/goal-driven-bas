package at.ac.uibk.smartbuilding.plugin.services;

import at.ac.uibk.smartbuilding.plugin.models.IoTDevice;
import at.ac.uibk.smartbuilding.plugin.repositories.IoTDeviceRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.ZonedDateTime;
import java.util.List;

@Service
public class IoTDeviceService {
    private final IoTDeviceRepository ioTDeviceRepository;
    private final PluginConfigurationService pluginConfigurationService;
    private static final Logger LOGGER = LoggerFactory.getLogger(IoTDeviceService.class);

    @Autowired
    public IoTDeviceService(IoTDeviceRepository ioTDeviceRepository, PluginConfigurationService pluginConfigurationService) {
        this.ioTDeviceRepository = ioTDeviceRepository;
        this.pluginConfigurationService = pluginConfigurationService;
    }


    public void save(IoTDevice ioTDevice) {
        ioTDevice.setTimestamp(ZonedDateTime.now().toString());
        ioTDeviceRepository.save(ioTDevice);
        var syncUri = pluginConfigurationService.getMeasurementUri();
        if (syncUri != null) {
            var frequency = pluginConfigurationService.getFrequency();
            reconfigureIoTDevice(ioTDevice, frequency, syncUri);
        }
    }

    private void reconfigureIoTDevice(IoTDevice device, Integer frequency, String syncUri) {
        var json = "{\"frequency\":" + frequency + ",\"syncUri\":\"" + syncUri + "\"}";
        LOGGER.info("Reconfiguring IoT device SENSOR_ID: {} ID: {} with frequency {} and syncUri {}", device.getSensorId(), device.getId(), frequency, syncUri);
        try {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(device.getConnectUri()))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(json))
                    .build();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            LOGGER.info("IoT device SENSOR_ID: {} ID: {} was successfully reconfigured {}", device.getSensorId(), device.getId(), response.body());
        } catch (Exception e) {
            LOGGER.error("Reconfigure IoT device SENSOR_ID: {} ID: {} error: {}", device.getSensorId(), device.getId(), e.getMessage());
        }
    }

    public void delete(String sensorId) {
        IoTDevice device = ioTDeviceRepository.getIoTDeviceBySensorId(sensorId);
        ioTDeviceRepository.delete(device);
    }

    public List<IoTDevice> getAllIoTDevices() {
        return ioTDeviceRepository.findAll();
    }

    public IoTDevice getIoTDevice(String sensorID) {
        return ioTDeviceRepository.getIoTDeviceBySensorId(sensorID);
    }

    public void reconfigure(Integer frequency, String syncUri) {
        List<IoTDevice> devices = ioTDeviceRepository.findAll();
        if (devices.isEmpty()) {
            LOGGER.info("No IoT devices to reconfigure");
            return;
        }
        for (var device : devices) {
            reconfigureIoTDevice(device, frequency, syncUri);
        }
        LOGGER.info("IoT devices reconfigured");
    }
}
