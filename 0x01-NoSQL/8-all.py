#!/usr/bin/env python3
"""
list_documents.py: Module to provide utility
functions for listing documents in a MongoDB collection.
"""

import pymongo


def list_all(mongo_collection):
    """
    List all documents in the given
    MongoDB collection.

    Args:
        mongo_collection: The MongoDB collection
        to list documents from.

    Returns:
        A list of all documents in the collection.
    """
    try:
        if not mongo_collection:
            return []
        return list(mongo_collection.find())
    except Exception as e:
        return []

