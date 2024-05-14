#!/usr/bin/env python3
"""
insert_documents.py: Module to provide utility
 functions for inserting documents into a MongoDB collection.
"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Insert a document into the given MongoDB
     collection.

    Args:
        mongo_collection: The MongoDB collection
        to insert the document into.
        **kwargs: Keyword arguments representing
        the fields and values of the document.

    Returns:
        The ObjectId of the inserted document.
    """
    try:
        return mongo_collection.insert_one(kwargs).inserted_id
    except Exception as e:
        return e
