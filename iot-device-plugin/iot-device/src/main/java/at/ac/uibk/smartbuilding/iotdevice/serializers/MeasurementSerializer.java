package at.ac.uibk.smartbuilding.iotdevice.serializers;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;

import java.io.IOException;

public class MeasurementSerializer extends JsonSerializer<IMeasurement> {
    @Override
    public void serialize(IMeasurement measurement, JsonGenerator jsonGenerator, SerializerProvider serializers)
    throws IOException {
        jsonGenerator.writeStartObject();
        jsonGenerator.writeNumberField("value", measurement.value());
        jsonGenerator.writeStringField("unit", measurement.unit().toString());
        jsonGenerator.writeStringField("timestamp", measurement.timestamp().toString());
        jsonGenerator.writeStringField("sensorId", measurement.sensorId());
        jsonGenerator.writeEndObject();
    }
}
