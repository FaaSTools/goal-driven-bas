package at.ac.uibk.smartbuilding.iotdevice.models;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
public class Configuration {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private int frequency;

    @Column(name = "sync_uri", nullable = false)
    private String syncUri;

    @Column(nullable = false)
    private String timestamp;

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public int getFrequency() {
        return frequency;
    }

    public void setFrequency(int frequency) {
        this.frequency = frequency;
    }

    public String getSyncUri() {
        return syncUri;
    }

    public void setSyncUri(String syncUri) {
        this.syncUri = syncUri;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Configuration that)) return false;
        return frequency == that.frequency && Objects.equals(id, that.id) && Objects.equals(syncUri, that.syncUri);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, frequency, syncUri);
    }
}