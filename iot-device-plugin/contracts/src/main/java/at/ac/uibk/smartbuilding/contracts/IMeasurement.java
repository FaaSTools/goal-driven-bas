package at.ac.uibk.smartbuilding.contracts;

import java.time.ZonedDateTime;

/**
 * Measurement interface representing a generic measurement with a value, timestamp, and sensor ID.
 * This interface defines the contract for any object that represents a measurable
 * quantity.
 */
public interface IMeasurement {

    /**
     * Retrieves the value of the measurement.
     * This method returns the value of the measurement, encapsulated as a Quantity
     * object that includes both the numerical value and its unit of measurement.
     *
     * @return The value of the measurement.
     */
    double value();

    MeasurementUnit unit();

    /**
     * Retrieves the timestamp of when the measurement was taken.
     * This method returns a {@link ZonedDateTime} object representing the timestamp at
     * which the measurement was taken.
     *
     * @return The timestamp of the measurement.
     */
    ZonedDateTime timestamp();

    /**
     * Retrieves the sensor ID associated with the measurement.
     * This method returns a {@link String} object that uniquely identifies the sensor
     * from which the measurement originates.
     *
     * @return The ID of the sensor.
     */
    String sensorId();
}

