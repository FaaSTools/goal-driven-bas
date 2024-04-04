package at.ac.uibk.smartbuilding.iotdevice.models;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import at.ac.uibk.smartbuilding.contracts.MeasurementUnit;

import java.time.ZonedDateTime;

public record Measurement(
    double value,
    MeasurementUnit unit,
    ZonedDateTime timestamp,
    String sensorId) implements IMeasurement { }
