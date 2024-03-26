#!/usr/bin/env python3
"""
Displays stats
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
    print('Methods:')
    for method in methods:
        count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    # Count the number of logs for method=GET and path=/status
    status_check_count = collection.count_documents(
            {"method": "GET", "path": "/status"})
    print("{} status check".format(status_check_count))

    # Count the occurrences of each IP address
    ip_counts = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Print the top 10 IP addresses
    print("IPs:")
    for ip_count in ip_counts:
        ip = ip_count["_id"]
        count = ip_count["count"]
        print("\t{}: {}".format(ip, count))


if __name__ == "__main__":
    log_stats()
