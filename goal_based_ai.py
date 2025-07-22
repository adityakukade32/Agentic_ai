from langchain_community.chat_models import ChatOllama
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import streamlit as st
import fitz
import os
import re

load_dotenv()

# ✅ Initialize Ollama LLM (e.g., using llama3 or mistral, depending on your local setup)
llm = ChatOllama(
    model="llama3",  # or any other model you have downloaded (like "mistral", "codellama", etc.)
    temperature=0.7
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

application_info = {
    "name": None,
    "email": None,
    "skills": None,
}

def extract_text_from_pdf(uploaded_file):
    doc=fitz.open(stream=uploaded_file.read(),filetype="pdf")
    text=""
    for page in doc:
        text +=page.get_text()
    doc.close()
    return text

def extract_info_from_cv(text:str):
    extracted_info={"name":None,"email":None,"skills":None,}    
    name_match=re.search



def extract_application_info(text: str) -> str:
    name_match = re.search(r"(?:my name is|i am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text, re.IGNORECASE)
    email_match = re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", text)
    skills_match = re.search(r"(?:skills are|i know|i can use)\s+(.+)", text, re.IGNORECASE)

    response = []

    if name_match:
        application_info["name"] = name_match.group(1).title()
        response.append("✅ Name Saved.")

    if email_match:
        application_info["email"] = email_match.group(0)
        response.append("✅ Email Saved.")

    if skills_match:
        application_info["skills"] = skills_match.group(1).strip()
        response.append("✅ Skills Saved.")

    if not any([name_match, email_match, skills_match]):
        return "? I couldn't extract any info. Could you please provide your name, email, or skills?"

    return " ".join(response) + " Let me check what else I need."


def check_application_goal(_: str) -> str:
    if all(application_info.values()):
        return f"🎯 You're ready! Name: {application_info['name']}, Email: {application_info['email']}, Skills: {application_info['skills']}"
    else:
        missing = [k for k, v in application_info.items() if not v]
        return f"⏳ Still need: {', '.join(missing)}. Please provide it."


tools = [
    Tool(
        name="extract_application_info",
        func=extract_application_info,
        description="Use this to extract name, email and skills from the user's message."
    ),
    Tool(
        name="check_application_goal",
        func=check_application_goal,
        description="Check if name, email, and skills are provided. If not, tell the user what is missing.",
        return_direct=True
    )
]

SYSTEM_REPORT = """You are a helpful job application assistant.
Your goal is to collect the user's name, email, and skills.
Use the tools provided to extract this information and check whether all data is collected.
Once everything is collected, inform the user that the application info is complete and stop.
"""

agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": SYSTEM_REPORT}
)

print("Hi! I'm your job application assistant. Please tell me your name, email, and skills.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Bye! Good luck.")
        break
    response = agent.invoke({"input": user_input})
    print("Bot:", response["output"])

    if "you're ready" in response["output"].lower():
        print("🎉 Application info complete!")
        break
