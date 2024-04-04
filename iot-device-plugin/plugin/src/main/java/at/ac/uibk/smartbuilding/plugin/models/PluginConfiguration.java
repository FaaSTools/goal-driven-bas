package at.ac.uibk.smartbuilding.plugin.models;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
public class PluginConfiguration {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "plugin_id", nullable = false)
    private Long pluginId;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private Integer frequency;

    @Column(nullable = false)
    private Integer capacity;

    @Column(name = "config_uri", nullable = false)
    private String configUri;

    @Column(name = "measurement_uri", nullable = false)
    private String measurementUri;

    @Column(name = "cloud_uri", nullable = false)
    private String cloudUri;

    @Column(nullable = false)
    private String timestamp;

    public PluginConfiguration() {
    }

    public Long getId() {
        return id;
    }

    public Long getPluginId() {
        return pluginId;
    }

    public void setPluginId(Long pluginId) {
        this.pluginId = pluginId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getFrequency() {
        return frequency;
    }

    public void setFrequency(Integer frequency) {
        this.frequency = frequency;
    }

    public Integer getCapacity() {
        return capacity;
    }

    public void setCapacity(Integer capacity) {
        this.capacity = capacity;
    }

    public String getConfigUri() {
        return configUri;
    }

    public void setConfigUri(String connectConfigUri) {
        this.configUri = connectConfigUri;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getMeasurementUri() {
        return measurementUri;
    }

    public void setMeasurementUri(String measurementUri) {
        this.measurementUri = measurementUri;
    }

    public String getCloudUri() {
        return cloudUri;
    }

    public void setCloudUri(String cloudUri) {
        this.cloudUri = cloudUri;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PluginConfiguration that = (PluginConfiguration) o;
        return Objects.equals(id, that.id) && Objects.equals(pluginId, that.pluginId) && Objects.equals(name, that.name) && Objects.equals(frequency, that.frequency) && Objects.equals(capacity, that.capacity) && Objects.equals(configUri, that.configUri) && Objects.equals(timestamp, that.timestamp);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, pluginId, name, frequency, capacity, configUri, timestamp);
    }

}
