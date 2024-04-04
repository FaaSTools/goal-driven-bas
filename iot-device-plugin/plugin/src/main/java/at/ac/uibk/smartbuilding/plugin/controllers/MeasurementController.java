package at.ac.uibk.smartbuilding.plugin.controllers;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import at.ac.uibk.smartbuilding.plugin.services.MeasurementService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/measurements")
public class MeasurementController {

    private static final Logger LOGGER = LoggerFactory.getLogger(MeasurementController.class);
    private final MeasurementService measurementService;

    public MeasurementController(MeasurementService measurementService) {
        this.measurementService = measurementService;
    }

    @PostMapping
    public ResponseEntity<String> receiveMeasurement(@RequestBody Iterable<IMeasurement> measurements) {
        var result = true;
        String sensorId = "";
        for (var measurement : measurements) {
            result = measurementService.save(measurement);
            sensorId = measurement.sensorId();
        }
        if (result) {
            LOGGER.info("Measurement received and successfully saved from sensor id: {}", sensorId);
            return ResponseEntity.ok("Measurement received and successfully saved");
        } else {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Measurement received but not saved");
        }
    }
}

