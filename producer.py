"""
producer.py - single entry point for all four data simulators.

Starts the four producers in parallel, each streaming simulated Retail FMCD
events into its own Kafka topic. Run:  python producer.py   (Ctrl+C to stop)
"""

import threading
import time

import engagement_producer
import inventory_producer
import iot_service_producer
import purchase_fraud_producer

PRODUCERS = [purchase_fraud_producer, engagement_producer, inventory_producer, iot_service_producer]


def main():
    for module in PRODUCERS:
        threading.Thread(target=module.main, daemon=True).start()
    print("\nAll 4 producers streaming to Kafka. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all producers.")


if __name__ == "__main__":
    main()
