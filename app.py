# Import required libraries
import streamlit as st
import os

# Import project modules
from src.preprocess import get_dataframe, extract_messages
from src.topic_checkpoint import detect_topic_checkpoints, save_topic_checkpoints
from src.message_checkpoint import create_message_checkpoints, save_message_checkpoints
from src.persona_extractor import extract_persona, save_persona
from src.chatbot import generate_answer


# Set Streamlit page configuration
st.set_page_config(
    page_title="Kastack RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)


# App title and description
st.title("🤖 Kastack RAG Chatbot with Checkpoints")
st.write("Upload conversation CSV, process messages chronologically, and ask questions about the user.")


# Create required folders
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# Upload CSV file
uploaded_file = st.file_uploader("Upload conversations.csv", type=["csv"])


# If file is uploaded
if uploaded_file is not None:
    file_path = "data/conversations.csv"

    # Save uploaded file locally
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("CSV uploaded successfully!")

    # Start processing after button click
    if st.button("Process Conversations"):
        progress = st.progress(0)
        status = st.empty()

        try:
            # Step 1: Read CSV
            status.info("Step 1/5: Reading CSV...")
            df = get_dataframe(file_path)
            progress.progress(20)

            # Step 2: Extract chronological messages
            status.info("Step 2/5: Splitting conversations into chronological messages...")
            messages = extract_messages(df)
            progress.progress(40)

            # Step 3: Create topic checkpoints
            status.info("Step 3/5: Detecting topic checkpoints...")
            topic_checkpoints = detect_topic_checkpoints(messages)
            save_topic_checkpoints(topic_checkpoints)
            progress.progress(65)

            # Step 4: Create 100-message checkpoints
            status.info("Step 4/5: Creating 100-message checkpoints...")
            message_checkpoints = create_message_checkpoints(messages)
            save_message_checkpoints(message_checkpoints)
            progress.progress(85)

            # Step 5: Extract persona
            status.info("Step 5/5: Extracting persona JSON...")
            persona = extract_persona(messages)
            save_persona(persona)
            progress.progress(100)

            # Store processing status
            st.session_state["processed"] = True

            status.success("✅ Processing completed successfully!")

            # Show processing summary
            st.subheader("Processing Summary")
            st.write("Total messages:", len(messages))
            st.write("Topic checkpoints:", len(topic_checkpoints))
            st.write("100-message checkpoints:", len(message_checkpoints))

            # Show generated output files
            st.subheader("Generated Files")
            st.write("✅ outputs/topic_checkpoints.json")
            st.write("✅ outputs/message_100_checkpoints.json")
            st.write("✅ outputs/persona.json")

        except Exception as e:
            status.error("❌ Processing failed.")
            st.exception(e)


# Chatbot section
st.divider()

st.header("💬 Chatbot")

query = st.text_input(
    "Ask a question",
    placeholder="Example: What kind of person is this user?"
)


# Generate chatbot answer
if st.button("Ask Bot"):

    # Check empty question
    if query.strip() == "":
        st.warning("Please enter a question.")

    # Check whether persona file exists
    elif not os.path.exists("outputs/persona.json"):
        st.error("Please upload and process CSV first.")

    else:
        try:
            answer = generate_answer(query)

            st.subheader("Answer")
            st.markdown(answer)

        except Exception as e:
            st.error("Something went wrong while generating answer.")
            st.exception(e)