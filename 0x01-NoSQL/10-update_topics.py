#!/usr/bin/env python3
"""
update_documents.py: Module to provide utility functions
 for updating documents in a MongoDB collection.
"""

import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Update the 'topics' field of documents matching
     the given name in the MongoDB collection.

    Args:
        mongo_collection: The MongoDB collection to
        update documents in.
        name: The name of the documents to update.
        topics: The new topics to set.

    Returns:
        A pymongo UpdateResult object containing
         information about the update operation.
    """
    try:
        return mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
        )
    except Exception as e:
        return e
