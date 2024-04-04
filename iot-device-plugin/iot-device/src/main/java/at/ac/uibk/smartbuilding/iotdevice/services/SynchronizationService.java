package at.ac.uibk.smartbuilding.iotdevice.services;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@Service
public class SynchronizationService {
    private static final Logger LOGGER = LoggerFactory.getLogger(SynchronizationService.class);
    private static final int HTTP_OK = 200;
    private static final int HTTP_MULTIPLE_CHOICES = 300;

    private final ObjectMapper objectMapper;

    @Autowired
    public SynchronizationService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public void synchronizeMeasurements(Iterable<IMeasurement> measurements, String uri) {
        try {
            var json = objectMapper.writeValueAsString(measurements);

            var client = HttpClient.newHttpClient();
            var request = HttpRequest.newBuilder()
                .uri(URI.create(uri))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

            var response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() < HTTP_OK || response.statusCode() >= HTTP_MULTIPLE_CHOICES) {
                throw new RuntimeException("Failed to synchronize measurements with status code: " + response.statusCode());
            }
        } catch (Exception e) {
            LOGGER.error("Send measurement data error: {}", e.getMessage());
        }
        LOGGER.info("Measurements successfully synchronized");
    }
}
