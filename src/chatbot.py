
# Import required libraries
import json
from src.retriever import retrieve_context


# Load persona data from JSON file
def load_persona(persona_file="outputs/persona.json"):
    with open(persona_file, "r", encoding="utf-8") as f:
        return json.load(f)


# Format retrieved topic checkpoints
def format_topics(topics):
    if not topics:
        return "No relevant topic checkpoints found."

    lines = []

    for topic in topics:
        lines.append(
            f"- Topic {topic['topic_id']} "
            f"(messages {topic['start_message_id']}–{topic['end_message_id']}): "
            f"{topic['summary']}"
        )

    return "\n".join(lines)


# Format retrieved message chunks
def format_messages(messages):
    if not messages:
        return "No relevant original messages found."

    lines = []

    for msg in messages:
        lines.append(
            f"- Message {msg['message_id']}: {msg['text'][:300]}"
        )

    return "\n".join(lines)


# Handle persona-related questions
def answer_persona_question(query, persona):
    q = query.lower()

    # Answer habit-related questions
    if "habit" in q or "habits" in q:
        habits = persona.get("habits", [])

        answer = "## User habits found from uploaded conversation signals\n\n"

        if not habits:
            return "No strong habit signals were found."

        for item in habits:
            answer += (
                f"### {item['habit']}\n\n"
                f"**Evidence:** {item['evidence']}\n\n"
            )

        return answer

    # Answer communication style questions
    if (
        "talk" in q
        or "communicate" in q
        or "language" in q
    ):
        style = persona.get("communication_style", {})
        evidence = style.get("evidence", {})

        return (
            "## User communication style based on uploaded conversations\n\n"
            f"- **Language:** {style.get('language')}\n"
            f"- **Message length:** {style.get('message_length')}\n"
            f"- **Tone:** {style.get('tone')}\n"
            f"- **Emoji usage:** {style.get('emoji_usage')}\n\n"
            "## Evidence\n\n"
            f"- Hindi marker count: {evidence.get('hindi_marker_count')}\n"
            f"- Average words per message: {evidence.get('average_words_per_message')}\n"
            f"- Emoji count: {evidence.get('emoji_count')}"
        )

    # Answer personality-related questions
    if (
        "person" in q
        or "personality" in q
        or "kind of person" in q
    ):
        traits = persona.get("personality_traits", [])
        interests = persona.get("interests", [])

        answer = "## Based only on uploaded conversation signals, this user appears to be:\n\n"

        for item in traits:
            answer += (
                f"### {item['trait']}\n"
                f"**Evidence:** {item['evidence']}\n\n"
            )

        if interests:
            answer += "## Recurring interests/topics\n\n"

            for item in interests:
                answer += (
                    f"- {item['interest']}\n\n"
                    f"**Evidence:** {item['evidence']}\n\n"
                )

        return answer

    return None


# Generate final response
def generate_answer(query):

    # Load persona information
    persona = load_persona()

    # Check if question is about persona
    persona_answer = answer_persona_question(query, persona)

    if persona_answer:
        return persona_answer

    # Retrieve relevant context using RAG
    context = retrieve_context(query)

    final_answer = "## Answer based on retrieved conversation data\n\n"

    final_answer += "### Relevant topic checkpoints\n"
    final_answer += format_topics(context["relevant_topics"])

    final_answer += "\n\n### Relevant original messages\n"
    final_answer += format_messages(context["relevant_messages"])

    return final_answer
