#!/usr/bin/env python3
"""
nginx_logs_stats.py: Provides statistics
about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def nginx_logs_stats(mongo_collection, option=None):
    """
    Provide statistics about Nginx logs stored in MongoDB.

    Args:
        mongo_collection: The MongoDB collection
         containing the Nginx logs.
        option: (Optional) If provided, specifies
        a particular HTTP method to get statistics for.

    Returns:
        None
    """
    query = {}
    if option:
        query["method"] = option
    if option:
        value = mongo_collection.count_documents(query)
        print(f"\t{option}: {value}")
        return
    total_logs = mongo_collection.count_documents(query)
    print(f"{total_logs} logs")
    print("Methods:")
    for method in METHODS:
        nginx_logs_stats(mongo_collection, method)
    status_check = mongo_collection.count_documents({"path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    nginx_logs_stats(nginx_collection)
