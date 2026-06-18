# RAG-System-with-Checkpoints

# RAG System with Checkpoints and Persona Chatbot

## Overview

This project implements an end-to-end Retrieval-Augmented Generation (RAG) system for analyzing conversation datasets. The system processes conversations chronologically, detects topic changes, creates topic checkpoints, generates message checkpoints, extracts user persona information, and provides a chatbot interface for answering questions about the user.

The chatbot combines topic summaries, message chunks, and persona information to generate meaningful answers based only on the uploaded conversation dataset.

The project does not rely on external LLM APIs and uses lightweight embedding models for semantic retrieval.

---

# Problem Statement

Given a CSV file containing conversations, where each row represents one day's conversation, the objective is to:

* Process conversations in chronological order.
* Detect topic changes dynamically.
* Create topic checkpoints.
* Generate summaries for every 100 messages.
* Extract user persona information.
* Build a chatbot that answers questions using retrieved context and persona data.

---

# Features

* Chronological message processing
* Dynamic topic checkpoint generation
* Independent 100-message checkpoints
* Semantic retrieval using embeddings
* Persona extraction from conversations
* Streamlit chatbot interface
* JSON output generation
* Lightweight architecture without external APIs

---

# Project Architecture

```text
CSV Dataset
      │
      ▼
Preprocessing
      │
      ▼
Chronological Messages
      │
      ├──────────────► Topic Checkpoints
      │
      ├──────────────► 100 Message Checkpoints
      │
      └──────────────► Persona Extraction
                            │
                            ▼
                    persona.json
                            │
                            ▼
                  Semantic Retrieval
                            │
                            ▼
                       Chatbot
```

---

# Folder Structure

```text
rag_system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│
├── outputs/
│     ├── topic_checkpoints.json
│     ├── message_100_checkpoints.json
│     └── persona.json
│
└── src/
      ├── __init__.py
      ├── preprocess.py
      ├── topic_checkpoint.py
      ├── message_checkpoint.py
      ├── persona_extractor.py
      ├── retriever.py
      └── chatbot.py
```

---

# Part 1: RAG System with Checkpoints

## Chronological Processing

The CSV dataset is processed message by message while preserving chronological order.

Each row corresponds to one day's conversation.

The preprocessing stage:

1. Reads the CSV file.
2. Splits conversations into individual messages.
3. Assigns unique message IDs.
4. Maintains the original order of messages.

---

# Topic Checkpoints

The entire conversation is not treated as one topic.

Instead, topic changes are detected during processing.

Whenever a topic shift occurs:

* A new topic checkpoint is created.
* Start and end message IDs are stored.
* A topic summary is generated.

Example:

```text
Topic 1 → messages 1–25 → summary

Topic 2 → messages 26–60 → summary

Topic 3 → messages 61–90 → summary
```

---

# Topic Change Detection

Topic changes are detected using topic keyword signals.

The system compares consecutive messages.

If:

* topic signals no longer overlap, and
* the current topic has enough messages,

then a new topic checkpoint is created.

This ensures that unrelated conversations are separated into different topic segments.

---

# 100 Message Checkpoints

Independent checkpoints are generated for every 100 chronological messages.

Each checkpoint contains:

* Start message ID
* End message ID
* Number of messages
* Summary
* Original messages

These checkpoints are independent of topic checkpoints.

---

# Retrieval System

The chatbot follows a two-stage retrieval process.

## Stage 1: Topic Retrieval

Relevant topic summaries are retrieved from topic checkpoints.

---

## Stage 2: Message Retrieval

Relevant message chunks are retrieved from the selected topics.

---

## Stage 3: Context Construction

Retrieved topic summaries and message chunks are combined to form the final context.

This context is then used to answer the user query.

---

# Embedding Model

The project uses:

### SentenceTransformer

Model:

```text
all-MiniLM-L6-v2
```

The embeddings are compared using cosine similarity.

This provides semantic retrieval without relying on external APIs.

---

# Part 2: Persona Extraction

Persona information is generated only from uploaded conversation signals.

No external knowledge or hardcoded personal information is used.

The system stores persona information in JSON format.

---

## Habits

Habits represent repeated behavioral patterns observed in conversations.

Examples:

* Frequently asks for simple explanations.
* Frequently requests code and step-by-step guidance.

---

## Interests

Recurring topics discussed by the user.

Examples:

* Career and jobs
* AI and Machine Learning
* Data analysis and Excel

---

## Personality Traits

Traits inferred from repeated conversation signals.

Examples:

* Goal-oriented
* Learning-oriented
* Practical

---

## Communication Style

The system identifies:

* Language
* Message length
* Tone
* Emoji usage

---

## Personal Facts

Personal facts are extracted only when strong evidence exists in the conversations.

---

# Part 3: Chatbot

The chatbot answers questions such as:

### What kind of person is this user?

### What are their habits?

### How do they talk?

The chatbot uses:

* Topic checkpoints
* Message checkpoints
* Persona JSON

to generate responses.

---

# Output Files

## topic_checkpoints.json

Stores topic segments and their summaries.

---

## message_100_checkpoints.json

Stores summaries for every 100 messages.

---

## persona.json

Stores:

* Habits
* Interests
* Personality traits
* Communication style
* Personal facts

---

# Technologies Used

* Python
* Streamlit
* Pandas
* Scikit-learn
* Sentence Transformers
* LangChain Community
* JSON

---

# Installation

Clone the repository:

```bash
git clone https://github.com/pranali1911/RAG-System-with-Checkpoints.git
```

Move to project directory:

```bash
cd RAG-System-with-Checkpoints
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

# Hosted Application

https://rag-system-with-checkpoints-jmyqrvkvlwpumydfds6mqc.streamlit.app/

---

# GitHub Repository

https://github.com/pranali1911/RAG-System-with-Checkpoints

---

# Demo Video

Loom Link:

(Add Loom video URL here)

---

# Screenshots

<img width="1722" height="912" alt="Screenshot 2026-06-18 182242" src="https://github.com/user-attachments/assets/a164e499-706b-4e4b-8e2c-6bc5deb0f7e7" />



<img width="1912" height="946" alt="image" src="https://github.com/user-attachments/assets/b239d314-1938-4712-b354-2ec459ab5a32" />



---

# Author

**Pranali Rahangdale**

MCA Graduate | Python Developer | AI/ML Enthusiast
