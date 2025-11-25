import datetime
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from utils.db import get_collection
from utils.memory_manager import get_memory, save_to_memory


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Create Groq LLM instance
llm = ChatGroq(
    groq_api_key=groq_api_key,
    temperature=0.6,  # Slightly higher for natural tone
    model="llama-3.3-70b-versatile"
)


chats = get_collection("chats")
queries = get_collection("queries")
knowledge = get_collection("knowledge_base")



# Advanced Intent Detection (Context-Aware)
def detect_intent_llm(user_input, context=""):
    """
    Uses Groq to classify user intent based on message and history.
    Adds fallback reasoning if confidence is unclear.
    """
    prompt = ChatPromptTemplate.from_template("""
    You are a highly intelligent intent detection AI.
    Given the user's latest message and conversation context,
    identify the most likely intent.

    Possible intents:
    - payment_issue → related to refunds, billing, failed transactions, or balance.
    - technical_query → related to code, errors, AI, APIs, Python, data, MongoDB, etc.
    - general_query → casual talk, greetings, opinions, small requests.
    - feedback → appreciation, complaints, or improvement suggestions.

    Return ONLY one of: payment_issue | technical_query | general_query | feedback
    Context:
    {context}
    Query:
    {query}

    Think step-by-step but output only the final intent name.
    """)

    chain = prompt | llm
    try:
        result = chain.invoke({"query": user_input, "context": context}).content.strip().lower()
        if result not in ["payment_issue", "technical_query", "general_query", "feedback"]:
            result = "general_query"
    except Exception:
        result = "general_query"
    return result



# Conversational Agent with Adaptive Memory
def handle_query_with_memory(session_id, user_input):
    
    memory = get_memory(session_id) # Retrieve previous memory
    context = "\n".join([f"{m['role']}: {m['message']}" for m in memory[-6:]]) if memory else ""
    last_topic = memory[-1]["message"] if memory else ""

    intent = detect_intent_llm(user_input, context) # Detect user intent

    system_prompt = f"""
    You are **ASTRA**, an empathetic, human-like AI support assistant with a warm personality.
    You remember what users said earlier, learn from each chat, and improve your responses.
    
    💬 Personality Traits:
    - Friendly, confident, and emotionally intelligent.
    - Uses short, natural sentences that sound conversational.
    - Balances logic and empathy. Never sound robotic.

    🧠 Memory Behavior:
    - Recall past user details or preferences from previous turns naturally.
    - Connect current topics to what was previously discussed if relevant.
    - Never restate the same generic advice unless new info appears.

    🎯 Intent-based Strategy:
    - **payment_issue** → empathize, guide clearly, suggest actionable steps.
    - **technical_query** → explain concepts or fixes with clarity; include brief code or reasoning.
    - **general_query** → keep it human, curious, maybe ask a small follow-up.
    - **feedback** → thank user, reflect on feedback, and show appreciation.

    ⚙️ Output Style:
    - Speak like a helpful expert, not a bot.
    - Be concise but not dry.
    - use pointers where needed.
    - If user repeats the same question, respond with slight variation and context awareness.

    Example tone:
    “That’s a great point — let’s dig into it together.” or “Got it, let’s sort this out quickly.”

    Previous context:
    {context}

    Last topic: {last_topic}
    """

    prompt = ChatPromptTemplate.from_template("""
    {system_prompt}

    User: {user_input}

    Assistant:
    """)
    chain = prompt | llm

    try:
        answer = chain.invoke({
            "system_prompt": system_prompt,
            "context": context,
            "user_input": user_input
        }).content.strip()
    except Exception as e:
        answer = f"Sorry, there was an internal issue generating a response: {str(e)}"

    save_to_memory(session_id, "user", user_input)
    save_to_memory(session_id, "assistant", answer)

    #Database Logging
    queries.insert_one({
        "session_id": session_id,
        "user_query": user_input,
        "agent_response": answer,
        "intent": intent,
        "timestamp": datetime.datetime.utcnow()
    })

    return {
        "response": answer,
        "intent": intent,
        "context_used": context,
    }


def save_feedback_db(session_id, feedback_text, rating=None):
    """Store user feedback into MongoDB for long-term improvement."""
    queries.insert_one({
        "session_id": session_id,
        "feedback": feedback_text,
        "rating": rating,
        "timestamp": datetime.datetime.utcnow()
    })
    return True
