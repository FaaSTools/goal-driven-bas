
plugins {
	id("goal-driven-building-automation.java-conventions")
	id("org.springframework.boot") version "3.2.0-SNAPSHOT"
	id("io.spring.dependency-management") version "1.1.3"
	id("com.google.cloud.tools.jib") version "3.4.1"
}

version = "0.0.1"
group = "at.ac.uibk.smartbuilding"

jib {
	from {
		image = "eclipse-temurin:21-jre-alpine"
		platforms {
			platform {
				architecture = "arm64"
				os = "linux"
			}
		}
	}
	to {
		image = "aws_account_id.dkr.ecr.region.amazonaws.com/iot-device"
		tags = setOf("latest")
	}
	container {
		jvmFlags = listOf("-Xms512m", "-Xmx512m")
		mainClass = "at.ac.uibk.smartbuilding.iotdevice.ServerApplication"
		ports = listOf("8080")
		volumes = listOf("/app/db")
	}
	extraDirectories {
		paths {
			path {
				setFrom("./data")
				into = "/app/data"
			}
		}
	}
}

dependencies {
	implementation(project(":contracts"))

	implementation("org.springframework.boot:spring-boot-starter-data-jpa")
	implementation("org.springframework.boot:spring-boot-starter-web")

	implementation("org.apache.commons:commons-csv:1.8")

	implementation("org.xerial:sqlite-jdbc:3.44.0.0")
	implementation("org.hibernate.orm:hibernate-community-dialects:6.4.1.Final")

	testImplementation("org.springframework.boot:spring-boot-starter-test")
}
