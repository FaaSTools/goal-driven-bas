package at.ac.uibk.smartbuilding.iotdevice.deserializers;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import at.ac.uibk.smartbuilding.contracts.MeasurementUnit;
import at.ac.uibk.smartbuilding.iotdevice.dtos.MeasurementDto;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonNode;

import java.io.IOException;
import java.time.ZonedDateTime;

public final class MeasurementDeserializer extends JsonDeserializer<IMeasurement> {

    @Override
    public IMeasurement deserialize(JsonParser jsonParser, DeserializationContext context)
    throws IOException {
        JsonNode rootNode = jsonParser.getCodec().readTree(jsonParser);

        var quantityValue = rootNode.get("value").asDouble();
        var quantityUnit = MeasurementUnit.valueOf(rootNode.get("unit").asText());

        var timestamp = ZonedDateTime.parse(rootNode.get("timestamp").asText());
        var sensorId = rootNode.get("sensorId").asText();

        return new MeasurementDto(quantityValue, quantityUnit, timestamp, sensorId);
    }
}
