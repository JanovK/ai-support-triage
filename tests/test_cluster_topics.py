import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from cluster_topics import assign_clusters, extract_keywords_by_cluster

def test_assign_clusters_labels():
    tickets = [{"subject": "Login failed", "body": "Can't log in", "cluster_id": -1} for _ in range(3)]
    cluster_labels = [0, 0, 1]
    result = assign_clusters(tickets, cluster_labels)
    assert result[0]["cluster_id"] == 0
    assert result[2]["cluster_id"] == 1

def test_extract_keywords():
    tickets = [
        {"subject": "Login issue", "body": "Forgot password", "cluster_id": 0},
        {"subject": "Cannot log in", "body": "Access denied", "cluster_id": 0},
        {"subject": "Tracking issue", "body": "Order not found", "cluster_id": 1}
    ]
    keywords = extract_keywords_by_cluster(tickets, top_n=3)
    assert 0 in keywords
    assert "login" in keywords[0] or "password" in keywords[0]
