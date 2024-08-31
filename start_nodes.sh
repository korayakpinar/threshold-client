#!/bin/bash

# Function to start a single service
start_service() {
    service_name=$1
    echo "Starting $service_name..."
    docker-compose up -d --no-deps $service_name
    echo "Waiting for 1 seconds..."
    sleep 30
}

# Start each service sequentially
for i in {1..4}
do
    start_service "threshold_node_$i"
done

echo "All services have been started."
