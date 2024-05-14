#!/usr/bin/env python3
"""
find_documents.py: Module to provide utility functions
for finding documents in a MongoDB collection.
"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Find documents in the MongoDB collection
     that have the specified topic.

    Args:
        mongo_collection: The MongoDB collection to search.
        topic: The topic to search for.

    Returns:
        A pymongo Cursor object containing the
         documents matching the query.
    """
    try:
        return mongo_collection.find({"topics": topic})
    except Exception as e:
        return e
