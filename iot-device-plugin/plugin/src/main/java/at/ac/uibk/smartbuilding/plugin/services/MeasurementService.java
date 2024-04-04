package at.ac.uibk.smartbuilding.plugin.services;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import at.ac.uibk.smartbuilding.plugin.models.Measurement;
import at.ac.uibk.smartbuilding.plugin.repositories.MeasurementRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.format.DateTimeFormatter;

import java.util.ArrayList;
import java.util.UUID;

@Service
public class MeasurementService {

    private final MeasurementRepository measurementRepository;
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss");

    private final SynchronizationService synchronizationService;

    @Autowired
    public MeasurementService(MeasurementRepository measurementRepository, SynchronizationService synchronizationService) {
        this.measurementRepository = measurementRepository;
        this.synchronizationService = synchronizationService;
    }

    @Transactional
    public boolean save(IMeasurement measurement) {
        var measurementEntity = new Measurement();
        measurementEntity.setTimestamp(String.valueOf(ZonedDateTime.now().format(formatter)));
        measurementEntity.setUnit(measurement.unit().toString());
        measurementEntity.setValue(measurement.value());
        measurementEntity.setSensorId(measurement.sensorId());
        measurementRepository.save(measurementEntity);
        synchronizationService.sync(measurementEntity);
        markAsSynced(measurementEntity);
        return true;
    }

    @Transactional
    public void delete(Long id) {
        var measurementEntity = measurementRepository.getMeasurementById(id);
        measurementRepository.delete(measurementEntity);
    }

    public ArrayList<Measurement> getUnsyncedMeasurements() {
        return measurementRepository.getMeasurementBySyncedEmpty();
    }

    public ArrayList<Measurement> getSyncedMeasurements() {
        return measurementRepository.getMeasurementBySyncedTrue();
    }

    @Transactional
    public void markAsSynced(Measurement measurement) {
        measurement.setSynced(true);
        measurementRepository.save(measurement);
    }
}
