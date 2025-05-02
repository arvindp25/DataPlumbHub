FROM google/cloud-sdk:alpine

# Install the Pub/Sub emulator
# Install OpenJDK, Python, pip, bash, and Git
RUN apk update && apk add \
    openjdk11 \
    python3 \
    py3-pip \
    bash \
    curl \
    git

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk \
    PATH="$JAVA_HOME/bin:$PATH"

RUN gcloud components install pubsub-emulator --quiet   &&   gcloud components install beta --quiet && \
gcloud config set core/disable_prompts true

WORKDIR /app

RUN git clone https://github.com/googleapis/python-pubsub.git /app/python-pubsub

run python3 -m venv /app/.venv

RUN /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install -r /app/python-pubsub/samples/snippets/requirements.txt

# Copy the start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8085

# Start the emulator with the custom script
CMD ["/start.sh"]
