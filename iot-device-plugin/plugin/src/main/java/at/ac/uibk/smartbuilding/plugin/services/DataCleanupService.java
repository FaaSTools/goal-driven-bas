package at.ac.uibk.smartbuilding.plugin.services;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
public class DataCleanupService {

    MeasurementService measurementService;
    private static final Logger LOGGER = LoggerFactory.getLogger(SynchronizationService.class);

    public DataCleanupService(MeasurementService measurementService) {
        this.measurementService = measurementService;
    }

    // runs at 1 AM every day.
    @Scheduled(cron = "0 0 1 * * ?")
    public void cleanup() {
        var syncedMeasurements = measurementService.getSyncedMeasurements();
        for (var measurement : syncedMeasurements) {
            measurementService.delete(measurement.getId());
        }
        LOGGER.info("Cleaned up {} measurements", syncedMeasurements.size());
    }

}
