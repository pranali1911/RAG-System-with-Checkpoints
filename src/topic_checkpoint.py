# Import required libraries
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Create a short summary for one topic checkpoint
def create_simple_summary(messages, max_chars=700):
    
    # Collect only non-empty message text
    texts = [msg["text"] for msg in messages if msg["text"].strip()]

    # If no text is available
    if not texts:
        return "No meaningful conversation found."

    # Pick first, middle, and last message for summary
    first = texts[0]
    middle = texts[len(texts) // 2] if len(texts) > 2 else ""
    last = texts[-1]

    # Build summary text
    summary = f"This topic contains {len(texts)} messages. "
    summary += f"Start: {first[:180]} "

    if middle:
        summary += f"Middle: {middle[:180]} "

    summary += f"End: {last[:180]}"

    # Limit summary length
    return summary[:max_chars] + "..." if len(summary) > max_chars else summary


# Detect topic changes and create topic checkpoints
def detect_topic_checkpoints(messages, similarity_threshold=0.08, min_topic_size=5):
    checkpoints = []

    # Return empty list if there are no messages
    if not messages:
        return checkpoints

    # Start first topic
    current_topic_messages = [messages[0]]
    topic_id = 1

    # Keywords used for simple topic detection
    topic_keywords = [
        "job", "resume", "interview", "internship", "career",
        "python", "ai", "ml", "rag", "chatbot", "excel",
        "data", "assignment", "project", "food", "game",
        "english", "email", "application"
    ]

    # Get topic keywords present in a message
    def get_topic_signal(text):
        text = text.lower()
        found = [word for word in topic_keywords if word in text]
        return set(found)

    # Topic signal of first message
    previous_signal = get_topic_signal(messages[0]["text"])

    # Process messages one by one in chronological order
    for i in range(1, len(messages)):
        current_signal = get_topic_signal(messages[i]["text"])

        # Check whether current message is related to previous message
        same_topic = bool(previous_signal.intersection(current_signal))

        # If topic changed and topic has enough messages, save checkpoint
        if not same_topic and len(current_topic_messages) >= min_topic_size:
            checkpoints.append({
                "topic_id": topic_id,
                "start_message_id": current_topic_messages[0]["message_id"],
                "end_message_id": current_topic_messages[-1]["message_id"],
                "message_count": len(current_topic_messages),
                "summary": create_simple_summary(current_topic_messages),
                "messages": current_topic_messages
            })

            # Start new topic
            topic_id += 1
            current_topic_messages = [messages[i]]

        else:
            # Continue current topic
            current_topic_messages.append(messages[i])

        # Update previous topic signal
        previous_signal = current_signal

    # Save last topic checkpoint
    if current_topic_messages:
        checkpoints.append({
            "topic_id": topic_id,
            "start_message_id": current_topic_messages[0]["message_id"],
            "end_message_id": current_topic_messages[-1]["message_id"],
            "message_count": len(current_topic_messages),
            "summary": create_simple_summary(current_topic_messages),
            "messages": current_topic_messages
        })

    return checkpoints


# Save topic checkpoints to JSON file
def save_topic_checkpoints(checkpoints, output_path="outputs/topic_checkpoints.json"):
    
    # Create outputs folder if not available
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save checkpoints in JSON format
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(checkpoints, f, indent=4, ensure_ascii=False)