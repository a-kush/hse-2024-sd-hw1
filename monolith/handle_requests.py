from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import threading
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

import time

######## assign

assign_producer = KafkaProducer(
        bootstrap_servers='localhost:9092',  # Update this to your Kafka server address
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize to JSON string
    )

def handle_assign_order_request(order_id: str, executer_id: str, locale: str) -> str:
    # Kafka producer configuration
    # Create the event
    event = {
        'order_id': order_id,
        'executer_id': executer_id,
        'locale': locale
    }

    # Topic to produce messages to
    topic = "order-assignments"
    
    try:
        # Send the message to Kafka
        future = assign_producer.send(topic, value=event)
        # Block until a single message is sent (or timeout)
        future.get(timeout=10)
        print("INFO: Message sent successfully.")
    except Exception as e:
        print(f"ERROR: Failed to send message: {e}")
        return "failure"
    finally:
        assign_producer.close()

    return "success"


######## acquire

# Executor for individual request processing
batch_executor = ThreadPoolExecutor(max_workers=10)

# This list will hold batches of requests
batch_requests = []
batch_size = 8
batch_lock = threading.Lock()

def get_order_by_executor(executer_id: str):
    # This function simulates getting an order_id from a database
    # In a real scenario, you would have a database call here
    time.sleep(0.5)  # Simulate network/database delay
    
    return f"order_id_for_{executer_id}"

def process_batch_of_requests(requests):
    results = []

    # Use ThreadPoolExecutor to process each request in the batch in parallel
    with ThreadPoolExecutor() as executor:
        future_to_executer_id = {executor.submit(get_order_by_executor, executer_id): executer_id for executer_id in requests}

        for future in as_completed(future_to_executer_id):
            executer_id = future_to_executer_id[future]
            try:
                order_id = future.result()
                results.append((executer_id, order_id))
            except Exception as e:
                results.append((executer_id, f"Error: {e}"))

    return results

def handle_acquire_order_request(executer_id: str):
    with batch_lock:
        batch_requests.append(executer_id)
        if len(batch_requests) >= batch_size:  # If the batch is ready
            # Process the batch and wait for the results
            batch_copy = batch_requests.copy()
            batch_requests.clear()
            future = batch_executor.submit(process_batch_of_requests, batch_copy)
            results = future.result()  # Wait for completion and get the results
            return results
        
######## cancel

# Producer configuration for cancellations
cancel_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Update this to your Kafka server address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize to JSON string
)

def handle_cancel_order_request(order_id: str) -> str:
    # Create the event for cancellation
    event = {
        'order_id': order_id
    }

    # Topic to produce cancellation messages to
    topic = "order-cancellations"
    
    try:
        # Send the cancellation message to Kafka
        future = cancel_producer.send(topic, value=event)
        # Block until a single message is sent (or timeout)
        future.get(timeout=10)
        print("INFO: Cancellation message sent successfully.")
    except Exception as e:
        print(f"ERROR: Failed to send cancellation message: {e}")
        return "failure"

    return "success"
