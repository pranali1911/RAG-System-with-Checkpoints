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

        answer = "## Habits based only on uploaded conversations\n\n"

        if not habits:
            return (
                "## Habits based only on uploaded conversations\n\n"
                "No clear lifestyle habits were identified from the conversations.\n\n"
                "The conversations do not contain enough repeated evidence about sleep routine, "
                "food habits, daily routine, or lifestyle habits."
            )

        for item in habits:
            answer += f"### {item['habit']}\n"
            answer += f"{item['evidence']}\n\n"

        answer += (
            "Note: Repeated topics such as career, Python, AI/ML, or Excel are treated as interests, "
            "not habits."
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

        answer = "## Communication style based only on uploaded conversations\n\n"

        answer += f"### Language\n{style.get('language')}\n\n"
        answer += f"### Message length\n{style.get('message_length')}\n\n"
        answer += f"### Tone\n{style.get('tone')}\n\n"
        answer += f"### Emoji usage\n{style.get('emoji_usage')}\n\n"

        answer += "## Evidence\n\n"
        answer += f"- {evidence.get('language_evidence', 'Language evidence was calculated from uploaded messages.')}\n"
        answer += f"- {evidence.get('message_length_evidence', 'Message length was calculated from uploaded messages.')}\n"
        answer += f"- {evidence.get('emoji_evidence', 'Emoji usage was calculated from uploaded messages.')}\n"

        return answer

    # Answer personality-related questions
    if (
        "person" in q
        or "personality" in q
        or "kind of person" in q
    ):
        traits = persona.get("personality_traits", [])
        interests = persona.get("interests", [])

        answer = "## Based only on uploaded conversations, the user appears to be:\n\n"

        for item in traits:
            answer += f"### {item['trait']}\n"
            answer += f"{item.get('meaning', '')}\n\n"
            answer += f"**Why:** {item['evidence']}\n\n"

        if interests:
            answer += "## Recurring interests/topics\n\n"

            for item in interests:
                answer += f"### {item['interest']}\n"
                answer += f"{item['evidence']}\n\n"

        return answer

    # Answer personal facts questions
    if (
        "personal fact" in q
        or "facts" in q
        or "relationship" in q
        or "family" in q
    ):
        facts = persona.get("personal_facts", [])

        answer = "## Personal facts based only on uploaded conversations\n\n"

        for item in facts:
            answer += f"### {item['fact']}\n"
            answer += f"{item['evidence']}\n\n"

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