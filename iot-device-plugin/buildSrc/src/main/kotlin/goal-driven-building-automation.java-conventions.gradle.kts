plugins {
    id("java")
}

group = "at.ac.uibk.smartbuilding"
version = "0.0.1-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_20
}

repositories {
    mavenCentral()
    maven { url = uri("https://repo.spring.io/milestone") }
    maven { url = uri("https://repo.spring.io/snapshot") }
}

dependencies {
    testImplementation("junit:junit:4.13")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
