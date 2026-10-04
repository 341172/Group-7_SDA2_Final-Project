"""Run this any time to confirm data is landing in MongoDB Atlas."""

from atlas_config import get_atlas_db

COLLECTIONS = [
    "purchase_transactions", "fraud_alerts",
    "engagement_events", "engagement_alerts",
    "inventory_events", "inventory_alerts",
    "device_events", "device_alerts",
    "all_events", "all_alerts",          # the combined (unified) collections
]

if __name__ == "__main__":
    client, db = get_atlas_db()
    for name in COLLECTIONS:
        print(f"{name:24s} {db[name].count_documents({}):>8,} docs")
    client.close()
