package at.ac.uibk.smartbuilding.plugin.configs;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import at.ac.uibk.smartbuilding.plugin.deserializers.IoTDeviceDeserializer;
import at.ac.uibk.smartbuilding.plugin.deserializers.MeasurementDeserializer;
import at.ac.uibk.smartbuilding.plugin.dtos.IoTDeviceDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.module.SimpleModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class JacksonConfig {

    @Bean
    @Primary
    public ObjectMapper objectMapper() {
        var objectMapper = new ObjectMapper();
        var module = new SimpleModule();
        module.addDeserializer(IMeasurement.class, new MeasurementDeserializer());
        module.addDeserializer(IoTDeviceDto.class, new IoTDeviceDeserializer());
        objectMapper.registerModule(module);
        return objectMapper;
    }
}
