# Import required libraries
import json
import os


# Create summary for each 100-message checkpoint
def create_checkpoint_summary(messages, max_chars=700):
    texts = [msg["text"] for msg in messages if msg["text"].strip()]

    # Return if no valid messages are found
    if not texts:
        return "No meaningful messages found."

    # Add first message to summary
    summary = f"This checkpoint contains {len(texts)} chronological messages. "
    summary += f"Start: {texts[0][:180]} "

    # Add middle message if available
    if len(texts) > 2:
        summary += f"Middle: {texts[len(texts)//2][:180]} "

    # Add last message
    summary += f"End: {texts[-1][:180]}"

    # Limit summary length
    return summary[:max_chars] + "..." if len(summary) > max_chars else summary


# Create checkpoints after every 100 messages
def create_message_checkpoints(messages, checkpoint_size=100):
    checkpoints = []

    # Process messages in chunks
    for i in range(0, len(messages), checkpoint_size):
        chunk = messages[i:i + checkpoint_size]

        # Store checkpoint information
        checkpoints.append({
            "checkpoint_id": len(checkpoints) + 1,
            "start_message_id": chunk[0]["message_id"],
            "end_message_id": chunk[-1]["message_id"],
            "message_count": len(chunk),
            "summary": create_checkpoint_summary(chunk),
            "messages": chunk
        })

    return checkpoints


# Save 100-message checkpoints to JSON file
def save_message_checkpoints(
        checkpoints,
        output_path="outputs/message_100_checkpoints.json"
):
    # Create output folder if it does not exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save checkpoints as JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(checkpoints, f, indent=4, ensure_ascii=False)