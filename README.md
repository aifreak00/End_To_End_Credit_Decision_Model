# CI/CD Pipeline Overview

This project implements a continuous integration and continuous deployment (CI/CD) pipeline that streamlines the development, testing, and deployment of machine learning (ML) application. Below, provided an overview of the pipeline stages and the Jenkins freestyle projects that manage each stage.

![CI/CD Pipeline Overview](docs/pipeline.jpg)

## Pipeline Stages

### 1. Code Integration and Dockerization (`1-Github-Docker`)

**Project:** `1-Github-Docker`

- **Trigger:** GitHub webhook on `push` event.
- **Action:** Performs Docker activities, such as building or updating the Docker image based on the latest code pushed to the GitHub repository.
- **Notification:** Sends an email with the Docker activity log to developers.

### 2. Model Training (`2-Training-Project`)

**Project:** `2-Training-Project`

- **Action:** Runs the docker container of the newly built image and performs model training within the container.
- **Notification:** Sends an email with the training logs, providing insights into the training process and outcomes.

### 3. Model Testing (`3-ML-Testing`)

**Project:** `3-ML-Testing`

- **Action:** Initiates the testing of the ML model. Test results are saved into an XML file, which is then copied from the Docker container to the host system for reporting purposes.
- **Notification:** Emails the test report to developers, detailing the performance of the ML model.

### 4. Deployment (`4-Deploy-to-Server`)

**Project:** `4-Deploy-to-Server`

- **Action:** Deploys the FastAPI application, which serves the ML model API. The deployment is completed, and the app becomes available on port 8005.
- **Notification:** Notifies developers of the deployment status and the availability of the app.

## Continuous Feedback Loop

![Jenkins Notification Example](docs/notification.png)

Developers receive feedback through email notifications at each stage of the pipeline, ensuring that any issues can be quickly addressed. This feedback loop enables rapid iteration and a high degree of confidence in the quality and reliability of the application.

![Jenkins Dashboard](docs/freestyle.png)

## Accessing the ML Model API

![FastAPI DOCS](docs/api.png)

Once deployed, users can interact with the ML model API via the FastAPI interface, which is designed to handle incoming requests and provide model inference with high performance.

The above images are snapshots of the pipeline's various components, which illustrate the robust and automated workflow we have established.


# Installation Process

## Docker Commands

This section outlines the steps to containerize and deploy the Credit Decision Model application using Docker.

### Prerequisites

- Docker installed on your machine.
- Docker Hub account (replace `<username>` with your Docker Hub username).

### Building the Docker Image

Build the Docker image from the Dockerfile in the current directory:

```bash
docker build -t <username>/credit_decision_model:latest .
```

### Pushing the Docker Image to Docker Hub

Push the built Docker image to your Docker Hub repository:

```bash
docker push <username>/credit_decision_model:latest
```

### Running the Docker Container

Run the Docker container in detached mode, mapping the container's port to a port on the host:

```bash
docker run -d -it --name credit_model_container -p 8005:8005 <username>/credit_decision_model:latest bash
```

### Executing Commands in the Running Container

Execute the training pipeline script within the container:

```bash
docker exec credit_model_container python prediction_model/training_pipeline.py
```

Run Pytest inside the container, generating a report named PytestResults.xml:

```bash
docker exec credit_model_container pytest -v --junitxml PytestResults.xml --cache-clear
```

### Copying Files from the Container to the Host

Copy the PytestResults.xml file from the container to your host machine:

```bash
docker cp credit_model_container:/code/src/PytestResults.xml .
```

### Running the FastAPI Application Inside the Container

Start the FastAPI application using Uvicorn within the container:

```bash
docker exec -d -w /code credit_model_container uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8005
```

Alternatively, you can directly execute the main Python file if it's set up to run Uvicorn:

```bash
docker exec -d -w /code credit_model_container python main.py
```

This will start the FastAPI application, making it accessible at http://localhost:8005/docs on your local machine.

Replace <username> with your Docker Hub username in the commands above. This setup allows for easy deployment and testing of the Credit Decision Model application within a Dockerized environment.


## Testing the FastAPI Application

Once the application is running, you can send POST requests to the `/prediction_api` endpoint with the appropriate JSON payload. Below is an example using Postman to send a request and receive a prediction response:

![FastAPI Test with Postman](docs/postman.png)

The example JSON payload for the request is:


```json
{
  "rate": 22.0,
  "amount": 25000.0,
  "purpose": "Personal",
  "period": 48,
  "cus_age": 45,
  "gender": "Male",
  "education_level": "Educated",
  "marital_status": "Married",
  "has_children": "Yes",
  "living_situation": "Independent",
  "total_experience": 120,
  "income": 7500.0,
  "job_sector": "Private",
  "DTI": 32.5,
  "APR": 33.3,
  "ccr_tot_mounth_amt": 1500.0,
  "ccr_payed_loan_tot_amt": 20000.0,
  "ccr_act_loan_tot_rest_amt": 10000.0
}

```

## AWS EC2 Instance Setup for MLOps


![EC2 Instance Summary](docs/EC2_instance.png)

To ensure that our MLOps pipeline is robust and scalable, we leverage AWS EC2 instances. This section guides you through the setup of an EC2 instance which will serve as the host for our Docker and Jenkins installations.

### Prerequisites

- An active AWS account
- Access permissions to manage EC2 instances within your AWS account

### Launching an EC2 Instance

1. **AMI Selection**: We start by selecting an Ubuntu Server image; for this project, we used "Ubuntu 22.04 LTS" for its stability and long-term support.

2. **Instance Type**: Choose a `t2.medium` instance type. This instance provides an optimal balance between compute, memory, and networking resources, and is suitable for medium-level workloads.

3. **Instance Configuration**: By default, we launch a single instance. Adjust the network settings or roles as required by your project's needs.

4. **Storage Setup**: Attach a minimum of 30 GiB storage to ensure sufficient space for all our Docker images, Jenkins configurations, and other essential data.

5. **Security Group Settings**: We establish a new security group with rules that allow SSH access. Ensure to also allow traffic on port 8080 for Jenkins, and any other ports your services may need.

6. **Review & Launch**: Confirm that all configurations are correct, and proceed to launch your instance.

### Accessing Your Instance

Post-launch, you'll be prompted to choose an existing key pair or create a new one. This key pair is critical for SSH access into your EC2 instance securely.

Here's a sample command to SSH into your instance:

```bash
ssh -i /path/to/your-key.pem ubuntu@<Your-EC2-Instance-Public-DNS>

```


## Installing Jenkins on EC2 Ubuntu Instance

This guide assumes that you are using an Ubuntu Server for your EC2 instance. Follow the steps below to install Jenkins.

### Adding Jenkins to the Package Repository

First, add the Jenkins repository key to your system with the following command:

```bash
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
```

Next, add the Jenkins repository to the package sources list:

```bash
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
```

Update your package index and install Jenkins:

```bash
sudo apt-get update
sudo apt-get install jenkins
```

Jenkins requires Java in order to run. Install OpenJDK 17:

```bash
sudo apt update
sudo apt install fontconfig openjdk-17-jre
```

Verify the Java installation:

```bash
java -version
```

You should see output similar to:

```bash
openjdk version "17.0.8" 2023-07-18
OpenJDK Runtime Environment (build 17.0.8+7-Debian-1deb12u1)
OpenJDK 64-Bit Server VM (build 17.0.8+7-Debian-1deb12u1, mixed mode, sharing)
```

To start Jenkins and enable it to run on system boot:

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

If Jenkins has started successfully, you should see a status indicating it is active.

By default, Jenkins runs on port 8080. Access Jenkins by entering http://<Your-EC2-Instance-Public-DNS>:8080 in a web browser. 

To get password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
![Unlock Jenkins](docs/jenkins.png)


## Install Docker Engine on Ubuntu

### Set up Docker's apt repository.

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

### To install the latest version, run:
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Verify that the Docker Engine installation is successful by running the hello-world image.
```bash
sudo docker run hello-world
```


### To manage Docker as a non-root user and to allow Jenkins to run Docker commands, you need to add users to the Docker group:

```bash
sudo usermod -a -G docker jenkins
sudo usermod -a -G docker $USER
```

## Setting Up GitHub Webhooks for Jenkins

To integrate Jenkins with your GitHub repository, you'll need to set up a webhook that triggers a Jenkins build whenever changes are pushed to the repository.

1. Navigate to your repository on GitHub.
2. Go to Settings > Webhooks.
3. Click on Add webhook.
4. In the Payload URL field, enter the following URL, replacing <public-ipv4-address> with your EC2 instance's public IPv4 address:


```bash
http://<public-ipv4-address>:8080/github-webhook/
```
5. Select application/json for the Content type.
6. Choose which events you would like to trigger the webhook.
7. Click on Add webhook to save the settings.

Now, Jenkins will receive a notification from GitHub and start a build whenever the specified events occur in your repository.


# waiting for specific events to occur
