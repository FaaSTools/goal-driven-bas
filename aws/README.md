# Goal Driven Building Automation System (AWS Part)

This component of the Goal Driven Building Automation system includes microservices for managing IoT devices, plugins, and rules. It is designed to facilitate the scheduling of tasks, plugins' configuration, and management of rules.

## Prerequisites

Before you begin, make sure Docker and Docker Compose are installed on your machine. For installation instructions, visit [Docker's installation guide](https://docs.docker.com/get-docker/) and the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

To start the services, navigate to the project directory and use `docker-compose up -d`.

Additionally, you need to replace the placeholder `DB_CONNECTION_STRING` in the docker-compose with your database's connection string. For example, update the database connection string in your docker-compose file to match the format:
```
mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
```
Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your database's actual credentials and address. 

To stop the services, use `docker-compose down`.

## Services

- **Commissioner**: Ensures that system performs in accordance with the designed rules.
- **Logger**: Logs state of the system.
- **Measurements**: Saves and provides measurements received from plugins on request.
- **Plugin**: Manages plugins' configurations.
- **Plugin Deployer**: Deploys new configuration to the plugin.
- **Rule**: Manages system rules.

Each service is encapsulated in its own Docker container, allowing for independent development, testing, and deployment and predictable environment.

## Built With

- [Python3](https://www.python.org/) - Programming language used for service development.
- [Docker](https://www.docker.com/) - Utilized for containerizing the services.

## Local Usage

Once the services are up and running, they can be accessed through their APIs. For instance, to retrieve measurements, you can send a POST request using any common HTTP client, for example [Postman](https://www.postman.com/). The request should target the following URL with an empty JSON body:

```
http://<your-local-ip-or-hostname>:9027/2015-03-31/functions/function/invocations
```

Ensure the header `Content-Type` is set to `application/json`. This example assumes you are testing Lambda functions locally, which allows for direct API interactions without deploying to AWS Lambda first.

For more detailed guidance on how to test Lambda container images on your local machine, refer to [Testing Lambda Container Images Locally](https://docs.aws.amazon.com/lambda/latest/dg/images-test.html). This documentation provides essential insights into simulating the Lambda environment locally.

## AWS Deployment

Deploying the services on AWS involves several key steps:

- **Upload your Docker Lambda images to Amazon Elastic Container Registry (ECR)**: Begin by pushing your Docker images to ECR. For detailed instructions, refer to the [ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html).

- **Create Lambda functions using your Docker images**: Once your images are in ECR, you can use them to create Lambda functions. Follow the steps outlined in the guide on [Working with Lambda Container Images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html).

- **Configure Environment Variables and VPC Settings for Specific Images**: For those Docker images where the `DB_CONNECTION_STRING` environment variable is defined in the Dockerfile, ensure to:
    - Add this environment variable within the Lambda function's configuration.
    - Place the function within a VPC if it needs to be connected with the database.

