#!/usr/bin/env python3
"""nginx_logs_stats.py: Provides statistics about Nginx logs stored in MongoDB."""

from pymongo import MongoClient


def nginx_logs_stats():
    """Provides statistics about Nginx logs stored in MongoDB."""
    client = MongoClient()
    collection = client.logs.nginx

    num_of_logs = collection.count_documents({})
    print(f"{num_of_logs} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_checks = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_checks} status check")

    print("IPs:")
    top_ips = collection.aggregate([
        {"$group":
         {
             "_id": "$ip",
             "count": {"$sum": 1}
         }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for top_ip in top_ips:
        count = top_ip.get("count")
        ip_address = top_ip.get("ip")
        print(f"\t{ip_address}: {count}")

if __name__ == "__main__":
    nginx_logs_stats()
