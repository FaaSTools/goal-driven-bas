package at.ac.uibk.smartbuilding.iotdevice.controllers;

import at.ac.uibk.smartbuilding.iotdevice.contexts.ConfigurationContext;
import at.ac.uibk.smartbuilding.iotdevice.dtos.ConfigurationDto;
import at.ac.uibk.smartbuilding.iotdevice.mappers.ConfigurationMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/configuration")
public class ConfigurationController {

    private static final Logger LOGGER = LoggerFactory.getLogger(ConfigurationController.class);
    private static final ConfigurationMapper MAPPER = new ConfigurationMapper();
    private final ConfigurationContext configurationContext;


    @Autowired
    public ConfigurationController(ConfigurationContext configurationContext) {
        this.configurationContext = configurationContext;
    }

    @PostMapping
    public boolean postConfiguration(@RequestBody ConfigurationDto configurationDto) {
        LOGGER.info("Received configuration: {}", configurationDto);

        var configuration = MAPPER.toModel(configurationDto);
        return configurationContext.saveAndReschedule(configuration);
    }
}
