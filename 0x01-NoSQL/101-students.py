#!/usr/bin/env python3
"""
top_students.py: Provides a function to
find top students by average score in MongoDB.
"""


def top_students(mongo_collection):
    """
    Find top students by average score
     in the MongoDB collection.

    Args:
        mongo_collection: The MongoDB
         collection containing student documents.

    Returns:
        A MongoDB aggregation cursor containing
        student documents sorted by average
        score in descending order.
    """
    return mongo_collection.aggregate([
        {"$project": {"name": "$name",
                      "averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}
         }
    ])
