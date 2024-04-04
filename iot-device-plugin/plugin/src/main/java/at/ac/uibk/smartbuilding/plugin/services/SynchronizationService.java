package at.ac.uibk.smartbuilding.plugin.services;

import at.ac.uibk.smartbuilding.plugin.models.Measurement;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@Service
public class SynchronizationService {

    private final ObjectMapper objectMapper;
    private static final int HTTP_OK = 200;
    private static final int HTTP_MULTIPLE_CHOICES = 300;
    private static final Logger LOGGER = LoggerFactory.getLogger(SynchronizationService.class);
    private final PluginConfigurationService pluginConfigurationService;

    public SynchronizationService(ObjectMapper objectMapper, PluginConfigurationService pluginConfigurationService) {
        this.objectMapper = objectMapper;
        this.pluginConfigurationService = pluginConfigurationService;
    }

    public void sync(Measurement measurement) {
        try {
            ObjectNode jsonObject = objectMapper.createObjectNode();
            var syncUri = pluginConfigurationService.getCloudUri();
            var pluginId = pluginConfigurationService.getPluginId();

            jsonObject.put("measurementUnit", measurement.getUnit());
            jsonObject.put("value", measurement.getValue());
            jsonObject.put("timestamp", measurement.getTimestamp());
            jsonObject.put("pluginId", pluginId);

            var client = HttpClient.newHttpClient();
            var request = HttpRequest.newBuilder()
                    .uri(URI.create(syncUri))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonObject.toString()))
                    .build();

            var response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() < HTTP_OK || response.statusCode() >= HTTP_MULTIPLE_CHOICES) {
                throw new RuntimeException("Failed to synchronize measurements with status code: " + response.statusCode());
            }
        } catch (Exception e) {
            LOGGER.error("Send measurement data error: {}", e.getMessage());
        }

        LOGGER.info("Measurement with id {} has been synced", measurement.getId());
    }
}
