FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:489.0.0-stable

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    git \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    python3-venv \
    build-essential \
    gnupg \
    software-properties-common \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install Terraform
RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
tee /etc/apt/sources.list.d/hashicorp.list

RUN apt-get update && apt-get install terraform

# Copy the current directory contents into the container at /app
COPY . /app

WORKDIR /app

# Initalize Terraform
RUN terraform init

# Create a virtual environment
RUN python3 -m venv venv

# Install the necessary Python packages
RUN /app/venv/bin/pip install -r /app/requirements.txt

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"
