import json
import os


def count_keywords(text, keywords):
    return sum(text.count(word) for word in keywords)


def extract_persona(messages):
    texts = [msg["text"] for msg in messages]
    all_text = " ".join(texts).lower()

    persona = {
        "habits": [],
        "personal_facts": [],
        "personality_traits": [],
        "communication_style": {},
        "evidence_note": "Persona is generated only from uploaded conversation signals, not guesses."
    }

    keyword_groups = {
        "career": ["job", "resume", "apply", "interview", "internship", "career", "hiring"],
        "learning": ["explain", "understand", "simple", "easy", "meaning", "how", "why"],
        "direct_output": ["code", "pura code", "full code", "step", "steps", "answer", "complete"],
        "sleep": ["sleep late", "late sleeper", "wake up", "morning routine", "night routine"],
        "food": ["breakfast", "lunch", "dinner", "diet", "food habit", "eat daily"],
        "family": ["father", "mother", "dad", "mom", "sister", "brother", "family", "parents"],
        "pets": ["dog", "cat", "pet", "pets"],
        "relationship": ["friend", "friends", "husband", "wife", "son", "daughter"]
    }

    counts = {
        group: count_keywords(all_text, words)
        for group, words in keyword_groups.items()
    }

    # Habits: only lifestyle/routine habits
    if counts["sleep"] > 3:
        persona["habits"].append({
            "habit": "Shows sleep or daily routine related signals",
            "evidence": "Sleep, wake-up, morning, or night routine signals appear repeatedly."
        })

    if counts["food"] > 3:
        persona["habits"].append({
            "habit": "Shows food or eating routine signals",
            "evidence": "Food, eating, or diet-related routine signals appear repeatedly."
        })

    if not persona["habits"]:
        persona["habits"].append({
            "habit": "No clear lifestyle habit identified",
            "evidence": "The conversations do not contain strong repeated signals about sleep routine, food habits, daily routine, or lifestyle habits."
        })

    # Personal facts: only clear repeated signals
    if counts["family"] > 5:
        persona["personal_facts"].append({
            "fact": "Family-related conversations are present",
            "evidence": "Family-related words such as parents, siblings, or family appear in the uploaded conversations."
        })

    if counts["pets"] > 3:
        persona["personal_facts"].append({
            "fact": "Pet-related conversations are present",
            "evidence": "Pet-related words such as dog, cat, or pets appear in the uploaded conversations."
        })

    if counts["relationship"] > 5:
        persona["personal_facts"].append({
            "fact": "Social or relationship-related conversations are present",
            "evidence": "Words related to friends, children, or relationships appear in the uploaded conversations."
        })

    if not persona["personal_facts"]:
        persona["personal_facts"].append({
            "fact": "No strong personal facts identified",
            "evidence": "The conversations do not contain enough clear repeated signals to safely extract personal facts."
        })

    # Personality traits
    if counts["career"] > 5:
        persona["personality_traits"].append({
            "trait": "Goal-oriented",
            "meaning": "The user often focuses on career, tasks, and completing work.",
            "evidence": "Career, job, resume, interview, or application-related conversations appear repeatedly."
        })

    if counts["learning"] > 5:
        persona["personality_traits"].append({
            "trait": "Learning-oriented",
            "meaning": "The user tries to understand concepts in a simple way.",
            "evidence": "Many messages ask for simple explanations, meanings, and learning support."
        })

    if counts["direct_output"] > 5:
        persona["personality_traits"].append({
            "trait": "Practical",
            "meaning": "The user prefers useful and ready-to-use answers.",
            "evidence": "Several messages request complete code, direct answers, steps, or ready-made solutions."
        })

    if not persona["personality_traits"]:
        persona["personality_traits"].append({
            "trait": "No strong personality trait identified",
            "meaning": "The available conversations do not show enough repeated signals.",
            "evidence": "No strong repeated personality pattern was found."
        })

    # Communication style
    hindi_markers = ["mujhe", "kaise", "krna", "btao", "samjha", "hai", "nahi", "kya"]
    hindi_count = count_keywords(all_text, hindi_markers)

    avg_words = sum(len(t.split()) for t in texts) / len(texts) if texts else 0
    emoji_count = sum(1 for ch in all_text if ord(ch) > 10000)

    persona["communication_style"] = {
        "language": "Hindi-English mixed" if hindi_count > 10 else "Mostly English",
        "message_length": "Short and direct" if avg_words < 25 else "Moderate to detailed",
        "tone": "Task-focused and direct",
        "emoji_usage": "Uses emojis sometimes" if emoji_count > 5 else "Low emoji usage",
        "evidence": {
            "language_evidence": "Hindi-English words appear repeatedly." if hindi_count > 10 else "Most messages are written in English.",
            "message_length_evidence": "Most messages are short and ask for specific help." if avg_words < 25 else "Messages contain moderate detail.",
            "emoji_evidence": "Emoji characters appear multiple times." if emoji_count > 5 else "Very few emoji characters appear in the conversations.",
            "hindi_marker_count": hindi_count,
            "average_words_per_message": round(avg_words, 2),
            "emoji_count": emoji_count
        }
    }

    return persona


def save_persona(persona, output_path="outputs/persona.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(persona, f, indent=4, ensure_ascii=False)