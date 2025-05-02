#!/bin/bash

# Start the Pub/Sub emulator in the background
gcloud beta emulators pubsub start  --quiet --host-port=0.0.0.0:8085 --project=fake-project &
EMULATOR_PID=$!

# Wait for emulator to start
sleep 5

# Set environment variables to use the emulator
export PUBSUB_EMULATOR_HOST=localhost:8085

# Create the topic and subscription
gcloud beta emulators pubsub env-init

python publisher.py fake-project create topic/test


# Wait so the emulator doesn't exit immediately
wait $EMULATOR_PID
