package at.ac.uibk.smartbuilding.iotdevice.contexts;

import at.ac.uibk.smartbuilding.iotdevice.services.ConfigurationService;
import at.ac.uibk.smartbuilding.iotdevice.services.MeasurementService;
import at.ac.uibk.smartbuilding.iotdevice.services.SynchronizationService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.TaskScheduler;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.CancellationException;
import java.util.concurrent.ScheduledFuture;

@Component
public class SchedulerContext {
    private static final Logger LOGGER = LoggerFactory.getLogger(SchedulerContext.class);
    private final MeasurementService measurementService;
    private final SynchronizationService synchronizationService;
    private final ConfigurationService configurationService;
    private final TaskScheduler taskScheduler;
    private ScheduledFuture<?> scheduledSynchronization;

    @Autowired
    public SchedulerContext(
            MeasurementService measurementService,
            SynchronizationService synchronizationService,
            TaskScheduler taskScheduler,
            ConfigurationService configurationService
    ) {
        this.measurementService = measurementService;
        this.synchronizationService = synchronizationService;
        this.taskScheduler = taskScheduler;
        this.configurationService = configurationService;
    }

    public void reschedule(Duration period) {
        if (scheduledSynchronization != null && !scheduledSynchronization.isDone()) {
            try {
                scheduledSynchronization.cancel(false);
                scheduledSynchronization.get();
            } catch (CancellationException e) {
                // Task was cancelled, do nothing
                LOGGER.info("Task was cancelled.");
            } catch (Exception e) {
                LOGGER.error("Reschedule error: {}", e.getMessage());
            }
        }

        if (period.isPositive()) {
            scheduledSynchronization = taskScheduler.scheduleAtFixedRate(
                    this::synchronizeMeasurements,
                    Instant.now(),
                    period
            );
        }
    }

    private void synchronizeMeasurements() {
        var measurement = measurementService.getMeasurement();
        var measurements = List.of(measurement);
        String uri = configurationService.getSyncUri();
        synchronizationService.synchronizeMeasurements(measurements, uri);
    }
}
