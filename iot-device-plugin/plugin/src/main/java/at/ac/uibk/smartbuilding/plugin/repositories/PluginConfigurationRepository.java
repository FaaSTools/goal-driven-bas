package at.ac.uibk.smartbuilding.plugin.repositories;

import at.ac.uibk.smartbuilding.plugin.models.PluginConfiguration;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PluginConfigurationRepository extends JpaRepository<PluginConfiguration, Long> {

    @Query(value = "SELECT distinct(plugin_id) FROM plugin_configuration", nativeQuery = true)
    Long getPluginId();

    @Query(value = "SELECT * FROM plugin_configuration ORDER BY id DESC LIMIT 1", nativeQuery = true)
    Optional<PluginConfiguration> getConfiguration();

}
