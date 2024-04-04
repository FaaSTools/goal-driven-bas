package at.ac.uibk.smartbuilding.iotdevice.services;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import at.ac.uibk.smartbuilding.contracts.MeasurementUnit;
import at.ac.uibk.smartbuilding.iotdevice.models.Measurement;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class MeasurementService {
    private static final Logger LOGGER = LoggerFactory.getLogger(MeasurementService.class);
    private static final String PATH_TO_MEASUREMENTS = "app/data/2023-03-24_10 24_influxdb_data.csv";
    private int currentIndex = 0;
    private List<Measurement> measurementsCache;

    public MeasurementService() {
        loadMeasurements();
    }

    private void loadMeasurements() {
        measurementsCache = new ArrayList<>();
        try (Reader reader = new FileReader(PATH_TO_MEASUREMENTS);
             CSVParser csvParser = new CSVParser(reader, CSVFormat.DEFAULT)) {
            for (var csvRecord : csvParser) {
                try {
                    if (!csvRecord.get(0).startsWith("#") && !csvRecord.get(1).startsWith("result")) {
                        var timestamp = ZonedDateTime.parse(csvRecord.get(5));
                        var value = Double.parseDouble(csvRecord.get(6));
                        var measurementUnit = MeasurementUnit.valueOf(csvRecord.get(8).toUpperCase());
                        var sensorID = csvRecord.get(10);
                        measurementsCache.add(new Measurement(value, measurementUnit, timestamp, sensorID));
                    }
                } catch (Exception e) {
                    LOGGER.error("Processing record error: {}", csvRecord);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException("Error reading measurements from CSV", e);
        }
    }

    public IMeasurement getMeasurement() {
        if (currentIndex >= measurementsCache.size()) {
            return null;
        }
        return measurementsCache.get(currentIndex++);
    }
}
