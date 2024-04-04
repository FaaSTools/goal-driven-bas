package at.ac.uibk.smartbuilding.iotdevice.contexts;

import at.ac.uibk.smartbuilding.iotdevice.models.Configuration;
import at.ac.uibk.smartbuilding.iotdevice.services.ConfigurationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.time.Duration;

@Component
public class ConfigurationContext {
    private final ConfigurationService configurationService;
    private final SchedulerContext schedulerContext;

    @Autowired
    public ConfigurationContext(ConfigurationService configurationService, SchedulerContext schedulerContext) {
        this.configurationService = configurationService;
        this.schedulerContext = schedulerContext;
    }

    public boolean saveAndReschedule(Configuration configuration) {
        configurationService.save(configuration);
        var newPeriod = configuration.getFrequency();
        schedulerContext.reschedule(Duration.ofSeconds(newPeriod));
        return true;
    }
}
