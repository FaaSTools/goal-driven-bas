package at.ac.uibk.smartbuilding.iotdevice.services;

import at.ac.uibk.smartbuilding.iotdevice.models.Configuration;
import at.ac.uibk.smartbuilding.iotdevice.repositories.ConfigurationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.ZonedDateTime;

@Service
public class ConfigurationService {
    private final static Integer DEFAULT_PERIOD = 30;
    private final static String DEFAULT_SYNC_URI = "http://localhost:8081/api/measurements";
    private final ConfigurationRepository configurationRepository;

    @Autowired
    public ConfigurationService(ConfigurationRepository configurationRepository) {
        this.configurationRepository = configurationRepository;
    }

    public void save(Configuration configuration) {
        configuration.setTimestamp(ZonedDateTime.now().toString());
        configurationRepository.save(configuration);
    }

    public Duration getPeriod() {
        var period = configurationRepository.findLatestConfiguration()
                .map(Configuration::getFrequency)
                .orElse(DEFAULT_PERIOD);
        return Duration.ofSeconds(period);
    }

    public String getSyncUri() {
        return configurationRepository.findLatestConfiguration()
                .map(Configuration::getSyncUri)
                .orElse(DEFAULT_SYNC_URI);
    }
}
