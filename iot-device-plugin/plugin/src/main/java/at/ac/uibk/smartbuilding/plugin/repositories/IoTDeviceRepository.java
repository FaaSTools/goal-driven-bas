package at.ac.uibk.smartbuilding.plugin.repositories;

import at.ac.uibk.smartbuilding.plugin.models.IoTDevice;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface IoTDeviceRepository extends JpaRepository<IoTDevice, Long> {
    IoTDevice getIoTDeviceBySensorId(String sensorId);
}
