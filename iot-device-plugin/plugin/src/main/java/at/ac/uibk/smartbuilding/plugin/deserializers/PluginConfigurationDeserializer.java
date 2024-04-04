package at.ac.uibk.smartbuilding.plugin.deserializers;

import at.ac.uibk.smartbuilding.plugin.dtos.PluginConfigurationDto;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonNode;

import java.io.IOException;

public final class PluginConfigurationDeserializer extends JsonDeserializer<PluginConfigurationDto> {
    @Override
    public PluginConfigurationDto deserialize(JsonParser jsonParser, DeserializationContext context)
    throws IOException {
        JsonNode rootNode = jsonParser.getCodec().readTree(jsonParser);

        var pluginId = rootNode.get("pluginId").asLong();
        var name = rootNode.get("name").asText();
        var frequency = rootNode.get("frequency").asInt();
        var capacity = rootNode.get("capacity").asInt();
        var cloudUri = rootNode.get("cloudUri").asText();
        var measurementUri = rootNode.get("measurementUri").asText();
        var configUri = rootNode.get("configUri").asText();

        return new PluginConfigurationDto(pluginId, name, frequency, capacity, cloudUri, measurementUri, configUri);
    }
}
