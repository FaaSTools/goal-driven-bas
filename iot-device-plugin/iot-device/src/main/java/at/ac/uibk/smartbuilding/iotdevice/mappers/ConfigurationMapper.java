package at.ac.uibk.smartbuilding.iotdevice.mappers;

import at.ac.uibk.smartbuilding.iotdevice.dtos.ConfigurationDto;
import at.ac.uibk.smartbuilding.iotdevice.models.Configuration;

public class ConfigurationMapper {

    public Configuration toModel(ConfigurationDto configurationDto) {
        var configuration = new Configuration();
        configuration.setFrequency(configurationDto.frequency());
        configuration.setSyncUri(configurationDto.syncUri());
        return configuration;
    }

    public ConfigurationDto toDto(Configuration configuration) {
        return new ConfigurationDto(configuration.getFrequency(), configuration.getSyncUri());
    }
}
