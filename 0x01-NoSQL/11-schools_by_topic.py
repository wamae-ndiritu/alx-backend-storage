#!/usr/bin/env python3
"""
Get schools having the topic
"""


def schools_by_topic(mongo_collection, topic):
    """Return the list of schools having a specific topic."""
    return list(mongo_collection.find({"topics": topic}))
