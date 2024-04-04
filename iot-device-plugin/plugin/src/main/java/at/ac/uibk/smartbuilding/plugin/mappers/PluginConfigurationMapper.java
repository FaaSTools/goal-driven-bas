package at.ac.uibk.smartbuilding.plugin.mappers;

import at.ac.uibk.smartbuilding.plugin.dtos.PluginConfigurationDto;
import at.ac.uibk.smartbuilding.plugin.models.PluginConfiguration;
import org.springframework.stereotype.Component;

@Component
public class PluginConfigurationMapper  {
    public PluginConfiguration toModel(PluginConfigurationDto pluginConfigurationDto) {
        var pluginConfiguration = new PluginConfiguration();
        pluginConfiguration.setPluginId(pluginConfigurationDto.pluginId());
        pluginConfiguration.setName(pluginConfigurationDto.name());
        pluginConfiguration.setFrequency(pluginConfigurationDto.frequency());
        pluginConfiguration.setCapacity(pluginConfigurationDto.capacity());
        pluginConfiguration.setConfigUri(pluginConfigurationDto.configUri());
        pluginConfiguration.setMeasurementUri(pluginConfigurationDto.measurementUri());
        pluginConfiguration.setCloudUri(pluginConfigurationDto.cloudUri());
        return pluginConfiguration;
    }

    public PluginConfigurationDto toDto(PluginConfiguration pluginConfiguration) {
        return new PluginConfigurationDto(
                pluginConfiguration.getPluginId(),
                pluginConfiguration.getName(),
                pluginConfiguration.getFrequency(),
                pluginConfiguration.getCapacity(),
                pluginConfiguration.getConfigUri(),
                pluginConfiguration.getMeasurementUri(),
                pluginConfiguration.getCloudUri()
        );
    }
}
