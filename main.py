from utils.memory_manager import create_new_session, clear_session
from utils.agent_core import handle_query_with_memory

session_id = create_new_session()  # unique every time
clear_session(session_id)

print("🤖 Conversational AI Agent Ready!\n")

while True:
    user_input = input("👤 You: ").strip()
    if user_input.lower() in ["exit", "quit", "Bye"]:
        print("👋 Session ended.")
        break

    result = handle_query_with_memory(session_id, user_input)
    print(f"🤖 Agent ({result['intent']}): {result['response']}\n")
