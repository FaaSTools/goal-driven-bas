package at.ac.uibk.smartbuilding.plugin.repositories;

import at.ac.uibk.smartbuilding.contracts.IMeasurement;
import at.ac.uibk.smartbuilding.plugin.models.Measurement;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.UUID;

@Repository
public interface MeasurementRepository extends JpaRepository<Measurement, UUID> {
    @Query(value = "SELECT * FROM measurement WHERE is_synced is null", nativeQuery = true)
    ArrayList<Measurement> getMeasurementBySyncedEmpty();

    @Query(value = "SELECT * FROM measurement WHERE is_synced = true", nativeQuery = true)
    ArrayList<Measurement> getMeasurementBySyncedTrue();

    Measurement getMeasurementById(Long id);


}
