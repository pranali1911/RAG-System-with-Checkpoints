# Import required libraries
import json
import os


# Count keyword occurrences
def count_keywords(text, keywords):
    return sum(text.count(word) for word in keywords)


# Extract persona only from uploaded CSV messages
def extract_persona(messages):

    # Collect all message texts from uploaded CSV
    texts = [msg["text"] for msg in messages]
    all_text = " ".join(texts).lower()

    # Initialize persona dictionary
    persona = {
        "habits": [],
        "interests": [],
        "personal_facts": [],
        "personality_traits": [],
        "communication_style": {},
        "evidence_note": "Persona is generated only from uploaded CSV conversation signals."
    }

    # Keywords for different categories
    keyword_groups = {
        "career": ["job", "resume", "apply", "interview", "internship", "career", "hiring"],
        "learning": ["explain", "understand", "simple", "easy", "meaning", "how", "why"],
        "technical": ["python", "ai", "ml", "machine learning", "rag", "chatbot", "streamlit"],
        "data_excel": ["excel", "data", "analysis", "formula", "pivot", "dashboard"],
        "direct_output": ["code", "pura code", "full code", "step", "steps", "answer", "complete"]
    }

    # Count keyword signals
    counts = {
        group: count_keywords(all_text, words)
        for group, words in keyword_groups.items()
    }

    # Habits = repeated behavior, not topics
    if counts["learning"] > 5:
        persona["habits"].append({
            "habit": "Frequently asks for simple explanations and learning support",
            "evidence": f"Learning-related terms appeared {counts['learning']} times."
        })

    if counts["direct_output"] > 5:
        persona["habits"].append({
            "habit": "Frequently asks for direct outputs, code, or step-by-step guidance",
            "evidence": f"Direct-output related terms appeared {counts['direct_output']} times."
        })

    # Interests = repeated discussion topics
    if counts["career"] > 5:
        persona["interests"].append({
            "interest": "Career, jobs, resumes, interviews, and applications",
            "evidence": f"Career-related terms appeared {counts['career']} times."
        })

    if counts["technical"] > 5:
        persona["interests"].append({
            "interest": "Technical topics such as Python, AI/ML, RAG, and chatbots",
            "evidence": f"Technical terms appeared {counts['technical']} times."
        })

    if counts["data_excel"] > 3:
        persona["interests"].append({
            "interest": "Data analysis, Excel, formulas, dashboards, and analytics",
            "evidence": f"Data/Excel-related terms appeared {counts['data_excel']} times."
        })

    # Personality traits based only on repeated CSV signals
    if counts["career"] > 5:
        persona["personality_traits"].append({
            "trait": "Goal-oriented",
            "evidence": "Repeated career and application-related conversations were found."
        })

    if counts["learning"] > 5:
        persona["personality_traits"].append({
            "trait": "Learning-oriented",
            "evidence": "Repeated requests for explanations and learning support were found."
        })

    if counts["direct_output"] > 5:
        persona["personality_traits"].append({
            "trait": "Practical",
            "evidence": "Repeated requests for ready-to-use answers, code, and steps were found."
        })

    # Communication style
    hindi_markers = ["mujhe", "kaise", "krna", "btao", "samjha", "hai", "nahi", "kya"]
    hindi_count = count_keywords(all_text, hindi_markers)

    avg_words = sum(len(t.split()) for t in texts) / len(texts) if texts else 0
    emoji_count = sum(1 for ch in all_text if ord(ch) > 10000)

    persona["communication_style"] = {
        "language": "Hindi-English mixed" if hindi_count > 10 else "Mostly English",
        "message_length": "Short and direct" if avg_words < 25 else "Moderate to detailed",
        "tone": "Direct and task-focused",
        "emoji_usage": "Uses emojis sometimes" if emoji_count > 5 else "Low emoji usage",
        "evidence": {
            "hindi_marker_count": hindi_count,
            "average_words_per_message": round(avg_words, 2),
            "emoji_count": emoji_count
        }
    }

    return persona


# Save persona data as JSON file
def save_persona(persona, output_path="outputs/persona.json"):

    # Create output folder if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save persona file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(persona, f, indent=4, ensure_ascii=False)