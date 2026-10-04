"""
consumer.py - single entry point for all four stream consumers.

Starts the four alert consumers in parallel. Each one reads its Kafka topic,
stores every event in MongoDB Atlas (database 'fmcd_streaming'), and writes
alerts to its alerts collection, which the Atlas Charts dashboards read.

  Stream 1  customer-purchase-data    -> purchase_transactions / fraud_alerts
  Stream 2  digital-engagement-data   -> engagement_events     / engagement_alerts
  Stream 3  inventory-logistics-data  -> inventory_events      / inventory_alerts
  Stream 4  device-service-data       -> device_events         / device_alerts

Every consumer ALSO writes each event to `all_events` and each alert to
`all_alerts` in one common format (see unified.py). Those two collections
combine the four data sources for the final-project dashboard.

Run:  python consumer.py        (Ctrl+C to stop)
"""

import threading
import time

import device_alert_consumer
import engagement_alert_consumer
import fraud_alert_consumer
import inventory_alert_consumer

CONSUMERS = {
    "Stream 1 - Purchase Fraud": fraud_alert_consumer,
    "Stream 2 - Digital Engagement": engagement_alert_consumer,
    "Stream 3 - Inventory & Delivery": inventory_alert_consumer,
    "Stream 4 - Smart Appliance": device_alert_consumer,
}


def main():
    for name, module in CONSUMERS.items():
        threading.Thread(target=module.main, name=name, daemon=True).start()
        print(f"Started consumer: {name}")
    print("\nAll 4 consumers running -> MongoDB Atlas. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all consumers.")


if __name__ == "__main__":
    main()
