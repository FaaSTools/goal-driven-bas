package at.ac.uibk.smartbuilding.plugin.controllers;

import at.ac.uibk.smartbuilding.plugin.dtos.PluginConfigurationDto;
import at.ac.uibk.smartbuilding.plugin.mappers.PluginConfigurationMapper;
import at.ac.uibk.smartbuilding.plugin.services.IoTDeviceService;
import at.ac.uibk.smartbuilding.plugin.services.PluginConfigurationService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/configuration")
public class PluginConfigurationController {

    private static final Logger LOGGER = LoggerFactory.getLogger(MeasurementController.class);
    private final PluginConfigurationService pluginConfigurationService;
    private final IoTDeviceService iotDeviceService;
    private final static PluginConfigurationMapper MAPPER = new PluginConfigurationMapper();
    Map<String, Object> response = new HashMap<>();

    @Autowired
    public PluginConfigurationController(PluginConfigurationService pluginConfigurationService, IoTDeviceService iotDeviceService) {
        this.pluginConfigurationService = pluginConfigurationService;
        this.iotDeviceService = iotDeviceService;
    }

    @PostMapping
    public ResponseEntity<?> postPluginConfiguration(@RequestBody PluginConfigurationDto pluginConfigurationDto) {
        var pluginConfiguration = MAPPER.toModel(pluginConfigurationDto);
        var pluginReconfigureResult = pluginConfigurationService.save(pluginConfiguration);

        iotDeviceService.reconfigure(pluginConfiguration.getFrequency(), pluginConfiguration.getMeasurementUri());

        if (!pluginReconfigureResult) {
            LOGGER.error("Plugin configuration not saved");
            response.put("responseCode", 500);
            response.put("responseMessage", "Error saving plugin configuration");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
         else {
            LOGGER.info("Plugin configuration saved");
            response.put("responseCode", 200);
            response.put("responseMessage", "Plugin configuration saved");
            return ResponseEntity.ok(response);
        }


    }

}
