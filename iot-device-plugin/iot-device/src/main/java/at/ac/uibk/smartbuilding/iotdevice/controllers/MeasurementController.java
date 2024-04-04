package at.ac.uibk.smartbuilding.iotdevice.controllers;

import at.ac.uibk.smartbuilding.iotdevice.services.MeasurementService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
@RequestMapping("/api/measurement")
public class MeasurementController {

    private final MeasurementService measurementService;

    @Autowired
    public MeasurementController(MeasurementService measurementService) {
        this.measurementService = measurementService;
    }

    @GetMapping
    public String getMeasurement() throws IOException {
        var measurement = measurementService.getMeasurement();
        var payloadMapper = new ObjectMapper().registerModule(new JavaTimeModule());
        payloadMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);

        return payloadMapper.writeValueAsString(measurement);
    }
}
