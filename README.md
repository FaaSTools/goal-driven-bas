# Goal Driven Building Automation System

## Info
This project is being developed as part of the bachelor's thesis "Serverless goal-driven building automation".

## Project Structure

This repository is organized into three components:

### 1. IoT Device and Plugin Part

- **Description**: Simulates IoT devices and plugins.
- **Technologies Used**: Spring Boot, Hibernate, SQLite JDBC, Apache Commons CSV.
- **Setup Instructions**: `iot-device-plugin/README.md`.

### 2. Frontend

- **Description**: Provides the user interface for system monitoring and management, showcasing data from IoT devices and allowing rule configuration.
- **Technologies Used**: Vue.js, Bootstrap, Axios.
- **Setup Instructions**: `frontend/README.md`.

### 3. AWS

- **Description**: Specifies microservices for commissioning, plugin configuration deployment, collection of measurements, rule and state management.
- **Technologies Used**: Python, Docker.
- **Setup Instructions**: `aws/README.md`.
