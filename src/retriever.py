# Import required libraries
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load lightweight sentence embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load JSON data from file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Retrieve top matching topic checkpoints
def retrieve_relevant_topics(query, topic_file="outputs/topic_checkpoints.json", top_k=3):
    
    # Load topic checkpoints
    topics = load_json(topic_file)

    if not topics:
        return []

    # Use topic summaries for matching
    topic_texts = [topic["summary"] for topic in topics]

    # Convert topics and query into embeddings
    topic_embeddings = model.encode(topic_texts)
    query_embedding = model.encode([query])

    # Calculate similarity between query and topics
    scores = cosine_similarity(query_embedding, topic_embeddings)[0]

    scored_topics = []

    # Store each topic with similarity score
    for i, score in enumerate(scores):
        topic = topics[i]

        scored_topics.append({
            "score": float(score),
            "topic_id": topic["topic_id"],
            "start_message_id": topic["start_message_id"],
            "end_message_id": topic["end_message_id"],
            "summary": topic["summary"],
            "messages": topic["messages"]
        })

    # Return top relevant topics
    return sorted(scored_topics, key=lambda x: x["score"], reverse=True)[:top_k]


# Retrieve top matching messages from selected topics
def retrieve_relevant_messages(query, topics, top_k=5):
    messages = []

    # Collect messages from retrieved topics
    for topic in topics:
        messages.extend(topic.get("messages", []))

    if not messages:
        return []

    # Use message text for matching
    message_texts = [msg["text"] for msg in messages]

    # Convert messages and query into embeddings
    message_embeddings = model.encode(message_texts)
    query_embedding = model.encode([query])

    # Calculate similarity between query and messages
    scores = cosine_similarity(query_embedding, message_embeddings)[0]

    scored_messages = []

    # Store each message with similarity score
    for i, score in enumerate(scores):
        msg = messages[i]

        scored_messages.append({
            "score": float(score),
            "message_id": msg["message_id"],
            "day_row": msg.get("day_row"),
            "text": msg["text"]
        })

    # Return top relevant messages
    return sorted(scored_messages, key=lambda x: x["score"], reverse=True)[:top_k]


# Build complete retrieval context for chatbot
def retrieve_context(query, top_k_topics=3, top_k_messages=5):
    
    # First retrieve relevant topics
    topics = retrieve_relevant_topics(query, top_k=top_k_topics)

    # Then retrieve relevant messages from those topics
    messages = retrieve_relevant_messages(query, topics, top_k=top_k_messages)

    return {
        "query": query,
        "relevant_topics": topics,
        "relevant_messages": messages
    }