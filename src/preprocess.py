# Import required libraries
from langchain_community.document_loaders import CSVLoader
import pandas as pd
import re


# Load CSV using LangChain loader
def load_csv(file_path):
    loader = CSVLoader(file_path=file_path, encoding="utf-8")
    return loader.load()


# Read CSV as DataFrame
def get_dataframe(file_path):
    return pd.read_csv(file_path)


# Split one conversation into individual messages
def split_conversation_text(text):

    # Pattern to identify User messages
    pattern = r"(User\s*\d+\s*:.*?)(?=User\s*\d+\s*:|$)"

    return [
        msg.strip()
        for msg in re.findall(pattern, text, flags=re.DOTALL)
        if msg.strip()
    ]


# Extract messages in chronological order
def extract_messages(df):

    messages = []
    message_id = 1

    # Get conversation column
    conversation_column = df.columns[0]

    # Process each row (each day)
    for row_id, row in df.iterrows():

        conversation = str(row[conversation_column])

        # Split conversation into messages
        split_messages = split_conversation_text(conversation)

        # Store each message separately
        for msg in split_messages:

            messages.append({
                "message_id": message_id,
                "day_row": int(row_id) + 1,
                "text": msg
            })

            message_id += 1

    return messages