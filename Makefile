# Variables
APP_NAME = my-mitmproxy-app
DOCKERFILE = Dockerfile
PORT = 52233
ECR_REPO = 352611772821.dkr.ecr.us-east-2.amazonaws.com/core/hocuspocus

# Check if Docker is installed
DOCKER_CHECK = $(shell docker --version > /dev/null 2>&1 && echo "yes" || echo "no")

# Default target
.PHONY: all
all: build run

# Function to wait for the dpkg lock
define wait_for_dpkg
    @echo "Waiting for dpkg lock to be released..."
    @while ! (sudo fuser /var/lib/dpkg/lock >/dev/null 2>&1); do sleep 1; done
    @while ! (sudo fuser /var/lib/apt/lists/lock >/dev/null 2>&1); do sleep 1; done
    @while ! (sudo fuser /var/cache/apt/archives/lock >/dev/null 2>&1); do sleep 1; done
endef

# Install Docker if it's not installed
.PHONY: install_docker
install_docker:
ifeq ($(DOCKER_CHECK), no)
	@echo "Docker is not installed. Installing Docker..."
	$(wait_for_dpkg)
	@sudo apt-get update -qq
	@sudo apt-get install -y -qq apt-transport-https ca-certificates curl software-properties-common
	@curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	@sudo add-apt-repository "deb [arch=$(shell dpkg --print-architecture)] https://download.docker.com/linux/ubuntu $(shell lsb_release -cs) stable"
	$(wait_for_dpkg)
	@sudo apt-get update -qq
	@sudo apt-get install -y -qq docker-ce
	@echo "Docker has been installed."
else
	@echo "Docker is already installed."
endif

# Build Docker image for linux/amd64
.PHONY: buildlinux
buildlinux: $(DOCKERFILE) requirements.txt
	$(MAKE) install_docker
	@echo "Building Docker image for linux/amd64..."
	docker build --platform linux/amd64 -t $(APP_NAME) .

# Build Docker image
.PHONY: build
build: $(DOCKERFILE) requirements.txt
	$(MAKE) install_docker
	@echo "Building Docker image..."
	docker build -t $(APP_NAME) .

# Run Docker container
.PHONY: run
run:
	@echo "Running Docker container..."
	docker run -v /Users/tushartimande/code/hocuspocus/tmp:/tmp -p $(PORT):$(PORT) $(APP_NAME)

# Pull Docker image from ECR
.PHONY: pull
pull:
	@echo "Pulling Docker image from ECR..."
	docker pull --platform linux/amd64 $(ECR_REPO):latest
	docker tag $(ECR_REPO):latest $(APP_NAME):latest

# Push Docker image to ECR
.PHONY: push
push: buildlinux
	@echo "Pushing Docker image to ECR..."
	docker tag $(APP_NAME):latest $(ECR_REPO):latest
	docker push $(ECR_REPO):latest

# Run Docker container for linux/amd64
.PHONY: runlinux
runlinux: pull
	@echo "Running Docker container for linux/amd64..."
	docker run --platform linux/amd64 -v /home/ubuntu/code/tmp:/tmp -p $(PORT):$(PORT) $(APP_NAME)

# Login to ECR
.PHONY: login
login:
	@echo "Logging in to ECR..."
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $(ECR_REPO)