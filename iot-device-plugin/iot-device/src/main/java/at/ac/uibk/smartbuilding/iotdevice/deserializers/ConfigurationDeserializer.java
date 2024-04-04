package at.ac.uibk.smartbuilding.iotdevice.deserializers;

import at.ac.uibk.smartbuilding.iotdevice.dtos.ConfigurationDto;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonNode;

import java.io.IOException;

public class ConfigurationDeserializer extends JsonDeserializer<ConfigurationDto> {
    @Override
    public ConfigurationDto deserialize(JsonParser jsonParser, DeserializationContext context)
    throws IOException {
        JsonNode rootNode = jsonParser.getCodec().readTree(jsonParser);

        var period = rootNode.get("frequency").asInt();
        var syncUri = rootNode.get("syncUri").asText();

        return new ConfigurationDto(period, syncUri);
    }
}
