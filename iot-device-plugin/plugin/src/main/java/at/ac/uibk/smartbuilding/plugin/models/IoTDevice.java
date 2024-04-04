package at.ac.uibk.smartbuilding.plugin.models;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "iot_device")
public final class IoTDevice {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "sensor_id", nullable = false)
    private String sensorId;

    @Column(name = "connect_uri", nullable = false)
    private String connectUri;

    @Column(name = "is_active", nullable = false)
    private boolean isActive;

    @Column(nullable = false)
    private String timestamp;

    public IoTDevice() {

    }

    public Long getId() {
        return id;
    }

    public String getSensorId() {
        return sensorId;
    }

    public void setSensorId(String sensorId) {
        this.sensorId = sensorId;
    }

    public String getConnectUri() {
        return connectUri;
    }

    public void setConnectUri(String connectUri) {
        this.connectUri = connectUri;
    }

    public boolean isActive() {
        return isActive;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof IoTDevice ioTDevice)) return false;
        return isActive() == ioTDevice.isActive() && Objects.equals(getId(), ioTDevice.getId()) && Objects.equals(getSensorId(), ioTDevice.getSensorId()) && Objects.equals(getConnectUri(), ioTDevice.getConnectUri()) && Objects.equals(getTimestamp(), ioTDevice.getTimestamp());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getId(), getSensorId(), getConnectUri(), isActive(), getTimestamp());
    }
}
