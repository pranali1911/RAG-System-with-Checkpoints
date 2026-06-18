# Conversation Memory & Persona Chatbot

A lightweight Retrieval-Augmented Generation (RAG) chatbot that reads uploaded chat conversations and lets you ask questions about them — what topics came up, what the person is like, how they communicate, and more.

The project runs entirely offline for its core logic using embeddings, keyword signals, and simple heuristics. No external APIs are required.

---

## What It Does

Upload a CSV file where each row represents one day's conversation. The system processes messages chronologically and builds two things:

1. **A searchable memory** of conversations using topic checkpoints and 100-message checkpoints.
2. **A persona profile** containing habits, personality traits, communication style, and personal facts.

Once processed, you can ask questions like:

* *What kind of person is this user?*
* *What are their habits?*
* *How do they communicate?*
* *What topics do they discuss most often?*
* *Did they mention anything about Python or interviews?*

---

## Project Structure

```text
.
├── src/
│   ├── loader.py          # CSV loading and message extraction
│   ├── checkpointer.py    # Topic checkpoints and 100-message checkpoints
│   ├── persona.py         # Persona extraction from conversation signals
│   ├── retriever.py       # Embedding-based retrieval
│   └── generator.py       # Answer generation
│
├── outputs/
│   ├── topic_checkpoints.json
│   ├── message_100_checkpoints.json
│   └── persona.json
│
├── pipeline.py
├── app.py
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/pranali1911/RAG-System-with-Checkpoints.git
cd RAG-System-with-Checkpoints
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the Dataset

Place the CSV file inside the project directory.

Each row should contain one day's conversation.

Messages inside a row should follow a format similar to:

```text
User 1: Hello
User 2: Hi

User 1: How are you?
User 2: Fine
```

### 4. Process the Conversations

```bash
python pipeline.py --input your_file.csv
```

### 5. Start the Chatbot

```bash
streamlit run app.py
```

---

## How Each Part Works

# Part 1 — Building the RAG System

### Topic Checkpoints

The system tracks how conversations evolve over time instead of treating the entire dataset as one large block.

Each message is checked for topic signals such as:

* `job`
* `resume`
* `python`
* `ai`
* `data`
* `project`

When consecutive messages stop sharing these signals, a topic change is detected.

Each topic checkpoint stores:

* Start message ID
* End message ID
* Topic summary

Example:

```text
Topic 1 → Messages 1–28
Resume building and job applications

Topic 2 → Messages 29–61
Python coding and debugging

Topic 3 → Messages 62–90
Excel formulas and data cleaning
```

The approach is intentionally lightweight and does not rely on clustering or LLM calls.

---

### 100-Message Checkpoints

These checkpoints are independent of topic checkpoints.

After every 100 messages, the system creates a checkpoint containing:

* Start message ID
* End message ID
* Number of messages
* Summary
* Original messages

These checkpoints provide an additional retrieval layer when information is spread across large conversations.

---

### Retrieval

When a user asks a question, the system:

1. Embeds the query using Sentence Transformers.
2. Compares it with topic checkpoint summaries.
3. Retrieves the top matching topics.
4. Retrieves the most relevant messages from those topics.
5. Combines both into the final context used to generate the answer.

The embedding model used is:

```text
all-MiniLM-L6-v2
```

Since everything runs locally, there are no API calls or rate limits.

---

# Part 2 — Persona Extraction

The persona is built entirely from conversation signals.

No assumptions or external knowledge are used.

Information is stored in:

```text
outputs/persona.json
```

---

### Habits

Repeated patterns observed across conversations.

Examples:

* Frequently asks for simple explanations.
* Prefers step-by-step guidance.
* Requests complete code solutions.

---

### Personal Facts

Information is extracted only when strong evidence exists.

Examples include repeated mentions of:

* Family
* Relationships
* Pets
* Daily routines

Single occurrences are ignored to avoid unreliable conclusions.

---

### Personality Traits

Traits are inferred from recurring conversation patterns.

Examples:

* Goal-oriented
* Learning-oriented
* Practical

Each trait is supported by evidence found in the conversations.

---

### Communication Style

The system analyzes:

* Language usage
* Message length
* Emoji usage
* Overall tone

The communication profile is derived directly from textual signals.

---

# Part 3 — The Chatbot

Questions about the user are answered directly from the persona profile.

Examples:

* *What kind of person is this user?*
* *What are their habits?*
* *How do they communicate?*

Questions about events or topics use the retrieval pipeline.

Examples:

* *What did they discuss about Python?*
* *Did they mention any job interviews?*
* *What topics appeared most frequently?*

---

## Dependencies

```text
sentence-transformers
scikit-learn
langchain-community
pandas
```

The model

```text
all-MiniLM-L6-v2
```

is downloaded automatically during the first run and occupies approximately 80 MB.

---

## Live Demo

### Hosted Application

The Streamlit application is available here:

https://rag-system-with-checkpoints-jmyqrvkvlwpumydfds6mqc.streamlit.app/

### GitHub Repository

Source code:

https://github.com/pranali1911/RAG-System-with-Checkpoints

### Video Walkthrough

Complete demo video:

https://www.loom.com/share/44d6e7df903441b386d7ae8fdd20d987

---

## Screenshots

### Chatbot Interface

<img width="1722" height="912" alt="Chatbot Interface" src="https://github.com/user-attachments/assets/a164e499-706b-4e4b-8e2c-6bc5deb0f7e7" />

### Persona Extraction and Question Answering

<img width="1917" height="947" alt="Persona Extraction Output" src="https://github.com/user-attachments/assets/0fcfc876-cdac-42c7-994c-7424bf5d7fbe" />

---

## Limitations Worth Knowing

* Topic detection is keyword-based, so it may miss subtle topic shifts.
* Persona extraction requires repeated evidence before a signal is accepted.
* The 100-message summaries are intentionally simple.
* Hindi detection relies on common markers and may not capture every variation.

These trade-offs keep the system lightweight and allow it to run fully offline without external APIs.

---

## Technologies Used

* Python
* Pandas
* Scikit-learn
* Sentence Transformers
* LangChain Community
* Streamlit
* JSON

---

## Future Improvements

* Add FAISS-based vector storage.
* Improve topic segmentation.
* Support multiple users.
* Enhance persona extraction.
* Add conversation visualization.

---

## License

This project is intended for educational and research purposes.
