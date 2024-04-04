package at.ac.uibk.smartbuilding.iotdevice;

import at.ac.uibk.smartbuilding.iotdevice.contexts.SchedulerContext;
import at.ac.uibk.smartbuilding.iotdevice.services.ConfigurationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class SchedulerRunner implements ApplicationRunner {
    private final SchedulerContext schedulerContext;
    private final ConfigurationService configurationService;

    @Autowired
    public SchedulerRunner(SchedulerContext schedulerContext, ConfigurationService configurationService) {
        this.schedulerContext = schedulerContext;
        this.configurationService = configurationService;
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        var period = configurationService.getPeriod();
        schedulerContext.reschedule(period);
    }
}
