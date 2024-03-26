#!/usr/bin/env python3
"""
all students sorted by average score
"""


def top_students(mongo_collection):
    """Returns all students sorted by average score"""

    # Define an empty list to store student data
    students_data = []

    # Iterate over each document in the collection
    for student in mongo_collection.find():
        # Extract student name and topics
        name = student.get('name')
        topics = student.get('topics')

        # Calculate the total score and count of topics for each student
        total_score = sum(topic.get('score', 0) for topic in topics)
        total_topics = len(topics)

        # Calculate the average score
        average_score = total_score / total_topics if total_topics != 0 else 0

        # Add the student data to the list
        students_data.append({
            '_id': student.get('_id'),
            'name': name,
            'averageScore': average_score
        })

    # Sort the students based on their average scores in descending order
    sorted_students = sorted(students_data,
                             key=lambda x: x['averageScore'], reverse=True)

    return sorted_students
