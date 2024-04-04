# Goal Driven Building Automation System (IoT Device and Plugin Part)

## Description

This component of the smart building automation system simulates real hardware of IoT devices and plugins.

## Getting Started

### Dependencies

- **Spring Boot**: For the application framework.
- **Hibernate**: ORM tool for database access.
- **SQLite JDBC**: JDBC driver for SQLite database access.
- **Apache Commons CSV**: For CSV file processing.

Refer to the official documentation of these technologies for more information.

### Installing

1. Ensure you have Java (used version 21.0.1) and Docker installed on your system.
2. Clone the repository.
3. Run `./gradlew build` to build the project.

### Executing the Program

1. Start the IoT device server with `./gradlew :iot-device:run`.
2. Start the plugin server with `./gradlew :plugin:run`.

### Building and Deploying Docker Images

1. Create Docker images using `jibDockerBuild` (task in Gradle) within both the iot-device and plugin modules.
2. Deploy and run the images on AWS using Elastic Container Service (ECS) and Elastic Container Registry (ECR). For detailed information, visit [Getting Started with Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started.html) and [Deploy Docker Containers on Amazon ECS](https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/).

### Configuring IoT Devices

After deploying the containers, configure the plugins to recognize IoT devices. This can be done using POST requests via Postman to the endpoint ``` http://<plugin-container-network>/api/devices ``` with the following JSON object:
```json
{
    "sensorId": "sensor1",
    "connectUri": "http://<iot-device-container-network>/api/configuration",
    "isActive": true
}
```

Repeat this step for each IoT device and ensure the plugins' URLs in the database reflect the actual network connections.