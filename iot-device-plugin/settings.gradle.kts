pluginManagement {
	repositories {
		maven { url = uri("https://repo.spring.io/milestone") }
		maven { url = uri("https://repo.spring.io/snapshot") }
		gradlePluginPortal()
	}
}

rootProject.name = "goal-driven-building-automation"

include(
	"contracts",
	"iot-device",
	"plugin")
