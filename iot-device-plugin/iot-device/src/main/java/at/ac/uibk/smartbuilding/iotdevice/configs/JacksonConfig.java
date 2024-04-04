package at.ac.uibk.smartbuilding.iotdevice.configs;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import at.ac.uibk.smartbuilding.iotdevice.deserializers.ConfigurationDeserializer;
import at.ac.uibk.smartbuilding.iotdevice.deserializers.MeasurementDeserializer;
import at.ac.uibk.smartbuilding.iotdevice.dtos.ConfigurationDto;
import at.ac.uibk.smartbuilding.iotdevice.serializers.MeasurementSerializer;
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
        module.addSerializer(IMeasurement.class, new MeasurementSerializer());
        module.addDeserializer(ConfigurationDto.class, new ConfigurationDeserializer());
        objectMapper.registerModule(module);
        return objectMapper;
    }
}
