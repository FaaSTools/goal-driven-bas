package at.ac.uibk.smartbuilding.plugin.deserializers;

import at.ac.uibk.smartbuilding.plugin.dtos.IoTDeviceDto;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonNode;

import java.io.IOException;

public final class IoTDeviceDeserializer extends JsonDeserializer<IoTDeviceDto> {
    @Override
    public IoTDeviceDto deserialize(JsonParser jsonParser, DeserializationContext context)
    throws IOException {
        JsonNode rootNode = jsonParser.getCodec().readTree(jsonParser);

        var sensorId = rootNode.get("sensorId").asText();
        var connectUri = rootNode.get("connectUri").asText();
        var isActive = rootNode.get("isActive").asBoolean();

        return new IoTDeviceDto( sensorId, connectUri, isActive);
    }
}
