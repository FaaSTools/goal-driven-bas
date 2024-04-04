package at.ac.uibk.smartbuilding.iotdevice.repositories;

import at.ac.uibk.smartbuilding.iotdevice.models.Configuration;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ConfigurationRepository extends JpaRepository<Configuration, Integer> {
    @Query(value = "SELECT * FROM Configuration ORDER BY id DESC LIMIT 1", nativeQuery = true)
    Optional<Configuration> findLatestConfiguration();
}
