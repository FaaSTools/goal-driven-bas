# Goal Driven Building Automation System (Frontend)

This component of the smart building automation system provides a user interface for monitoring and managing the system. It's a [Vue.js](https://vuejs.org/) application featuring components for visualizing measurements, configuring system rules, viewing state logs, and plugin management.

## Project Setup

Ensure you have the latest version of [Node.js](https://nodejs.org/) (used version v16.15.0) and npm installed. Then, install the project dependencies:

```sh
npm install
```

For development, compile and hot-reload with:

```sh
npm run dev
```

For production, compile and minify with:

```sh
npm run build
```

## Features

- **Measurement**: Visualizes real-time and historical measurement data from IoT devices.
- **Rule**: Allows users to define and edit rules for the system behavior.
- **Log**: Shows a log of system states, useful for debugging and monitoring.
- **Plugin**: Enables management of system plugins.

## Dependencies

The project relies on:
- [Vue.js](https://vuejs.org/) for the frontend framework.
- [Bootstrap](https://getbootstrap.com/) for styling and components.
- [Axios](https://axios-http.com/) for HTTP requests.

## Configuration

Before running the application, configure your `vite.config.js` file to match your deployment settings, particularly the API endpoints for the backend services.

## Running the Application

After building the application for production, you can serve it using a static file server or integrate it with your backend service. For more details on deployment, check Vue.js's deployment guide [here](https://cli.vuejs.org/guide/deployment.html).
