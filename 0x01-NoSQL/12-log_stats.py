#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


def log_stats():
    """Displays stats about Nginx logs stored in MongoDB"""

    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Access the logs database and nginx collection
    db = client.logs
    collection = db.nginx

    # Count the total number of logs
    total_logs = collection.count_documents({})

    print("{} logs".format(total_logs))

    # Count the number of logs for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    # Count the number of logs for method=GET and path=/status
    status_check_count = collection.count_documents(
            {"method": "GET", "path": "/status"})
    print("{} status check".format(status_check_count))


if __name__ == "__main__":
    log_stats()
