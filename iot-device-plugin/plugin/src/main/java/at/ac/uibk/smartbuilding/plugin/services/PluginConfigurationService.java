package at.ac.uibk.smartbuilding.plugin.services;

import at.ac.uibk.smartbuilding.plugin.models.PluginConfiguration;
import at.ac.uibk.smartbuilding.plugin.repositories.PluginConfigurationRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Optional;

@Service
public class PluginConfigurationService {

    private final static Integer DEFAULT_PERIOD = 10;
    private static final String SYNC_URI = "https://y5g26uoeyc.execute-api.us-east-1.amazonaws.com/createMeasurement";

    private final ZoneId zoneId = ZoneId.of("Europe/Vienna");
    private final PluginConfigurationRepository pluginConfigurationRepository;

    @Autowired
    public PluginConfigurationService(PluginConfigurationRepository pluginConfigurationRepository) {
        this.pluginConfigurationRepository = pluginConfigurationRepository;
    }

    @Transactional
    public boolean save(PluginConfiguration pluginConfiguration) {
        var pluginConfigurationEntity = new PluginConfiguration();
        pluginConfigurationEntity.setPluginId(pluginConfiguration.getPluginId());
        pluginConfigurationEntity.setName(pluginConfiguration.getName());
        pluginConfigurationEntity.setFrequency(pluginConfiguration.getFrequency());
        pluginConfigurationEntity.setCapacity(pluginConfiguration.getCapacity());
        pluginConfigurationEntity.setConfigUri(pluginConfiguration.getConfigUri());
        pluginConfigurationEntity.setMeasurementUri(pluginConfiguration.getMeasurementUri());
        pluginConfigurationEntity.setCloudUri(pluginConfiguration.getCloudUri());
        pluginConfigurationEntity.setTimestamp(String.valueOf(ZonedDateTime.now(zoneId)));

        pluginConfigurationRepository.save(pluginConfigurationEntity);
        return true;
    }

    public Long getPluginId() {
        var configuration = pluginConfigurationRepository.getConfiguration();
        return configuration.map(PluginConfiguration::getPluginId).orElse(null);
    }

    public Integer getFrequency() {
        Optional<PluginConfiguration> pluginConfiguration = pluginConfigurationRepository.getConfiguration();
        return pluginConfiguration.map(PluginConfiguration::getFrequency).orElse(DEFAULT_PERIOD);
    }


    public String getMeasurementUri() {
        Optional<PluginConfiguration> pluginConfiguration = pluginConfigurationRepository.getConfiguration();
        return pluginConfiguration.map(PluginConfiguration::getMeasurementUri).orElse(null);
    }

    public String getCloudUri() {
        Optional<PluginConfiguration> pluginConfiguration = pluginConfigurationRepository.getConfiguration();
        return pluginConfiguration.map(PluginConfiguration::getCloudUri).orElse(SYNC_URI);
    }

}
