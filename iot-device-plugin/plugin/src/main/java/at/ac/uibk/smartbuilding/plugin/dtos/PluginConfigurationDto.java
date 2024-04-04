package at.ac.uibk.smartbuilding.plugin.dtos;

public record PluginConfigurationDto(
        Long pluginId,
        String name,
        Integer frequency,
        Integer capacity,
        String configUri,
        String measurementUri,
        String cloudUri) {
}
