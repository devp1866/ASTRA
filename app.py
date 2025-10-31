
import streamlit as st
from utils.agent_core import handle_query_with_memory
from utils.memory_manager import create_new_session, get_recent_messages, clear_session
import time

st.set_page_config(
    page_title="ASTRA | Advanced Support & Task Response Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ==================== GLOBAL CSS STYLING ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ========== Theme Variables ========== */
    :root {
        --primary-bg: #011222;
        --light-grey: #EAF0F6;
        --accent: #0B2545;
        --hover-accent: #1e3a5f;
        --success-green: #10b981;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
    }
    
    /* ========== Global Styles ========== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    a {
        cursor: help !important;
    }
    
    # /* Hide Streamlit Branding */
    # #MainMenu {visibility: hidden;}
    # footer {visibility: hidden;}
    # header {visibility: hidden;}
    
    /* Remove Default Padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    
    /* ========== Sticky Header ========== */
    .app-header {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: linear-gradient(135deg, var(--primary-bg) 0%, var(--accent) 100%);
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border-bottom: 3px solid rgba(74, 144, 226, 0.4);
        animation: slideDown 0.6s ease-out;
    }
    
    @keyframes slideDown {
        from {
            transform: translateY(-100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .app-header h1 {
        color: var(--light-grey) !important;
        margin: 0 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        text-align: center;
    }
    
    .app-header p {
        color: var(--light-grey) !important;
        text-align: center;
        margin: 0.5rem 0 0 0 !important;
        opacity: 0.9;
        font-size: 1rem;
    }
    
    /* ========== Notification Banner ========== */
    .notification-banner {
        background: linear-gradient(135deg, #1e3a5f 0%, #0B2545 100%);
        color: var(--light-grey);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #4A90E2;
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: slideInLeft 0.6s ease-out;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-banner:hover {
        transform: translateX(5px);
        transition: transform 0.3s ease;
    }
    
    /* ========== Sidebar Styling ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary-bg) 0%, var(--accent) 100%);
        border-right: 3px solid rgba(74, 144, 226, 0.4);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Hide Sidebar Scrollbar */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 0px;
    }
    
    [data-testid="stSidebar"] * {
        color: var(--light-grey) !important;
    }
    
    [data-testid="stSidebar"] h2 {
        text-align: center;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin: 1rem 0 !important;
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(74, 144, 226, 0.3);
    }
    
    /* Sidebar Buttons */
    [data-testid="stSidebar"] button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--hover-accent) 100%) !important;
        color: var(--light-grey) !important;
        border: 2px solid rgba(74, 144, 226, 0.5) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.7rem 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2) !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: linear-gradient(135deg, var(--hover-accent) 0%, #2c5f8d 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.5) !important;
    }
    
    /* Page Links */
    [data-testid="stSidebar"] a {
        display: block !important;
        padding: 0.8rem 1rem !important;
        margin: 0.5rem 0 !important;
        background: linear-gradient(135deg, rgba(11, 37, 69, 0.5) 0%, rgba(30, 58, 95, 0.5) 100%) !important;
        border-radius: 10px !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
        font-weight: 600 !important;
        border: 2px solid transparent !important;
    }
    
    [data-testid="stSidebar"] a:hover {
        background: linear-gradient(135deg, var(--hover-accent) 0%, #2c5f8d 100%) !important;
        border-color: rgba(74, 144, 226, 0.6) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* ========== Main Container ========== */
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* ========== Chat Messages ========== */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, var(--primary-bg) 0%, var(--accent) 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        animation: messageSlide 0.4s ease-out;
        transition: all 0.3s ease;
    }
    
    @keyframes messageSlide {
        from {
            transform: translateY(20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    [data-testid="stChatMessage"]:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    /* User Messages */
    [data-testid="stChatMessage"][data-testid-role="user"] {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 5px solid #2196F3;
    }
    
    /* Assistant Messages */
    [data-testid="stChatMessage"][data-testid-role="assistant"] {
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
        border-left: 5px solid var(--accent);
    }
    
    /* ========== Chat Input ========== */
    [data-testid="stChatInput"] {
        border: 2px solid var(--accent) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #4A90E2 !important;
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.3) !important;
    }
    
    /* ========== Status Badge ========== */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.3rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    .status-active {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .status-ended {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .status-messages {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }
    
    /* ========== Success/Info Messages ========== */
    .stSuccess {
        animation: successPulse 0.5s ease-out;
    }
    
    @keyframes successPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .stInfo {
        border-left: 5px solid #4A90E2;
        border-radius: 8px;
    }
    
    /* ========== Divider ========== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(74, 144, 226, 0.5), transparent);
        margin: 1.5rem 0;
    }
    
    /* ========== Sidebar Footer ========== */
    .sidebar-footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(74, 144, 226, 0.2);
    }
    
    .sidebar-footer p {
        margin: 0.3rem 0;
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    /* ========== Welcome Message ========== */
    .welcome-card {
        background: linear-gradient(135deg, white 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 6px solid var(--accent);
        animation: cardSlide 0.6s ease-out;
    }
    
    @keyframes cardSlide {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .welcome-card h3 {
        color: var(--primary-bg);
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .welcome-card p {
        color: var(--text-secondary);
        line-height: 1.6;
        margin: 0.5rem 0;
    }
    
    .welcome-card ul {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .welcome-card li {
        color: var(--text-primary);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION INITIALIZATION ====================
if "session_id" not in st.session_state:
    st.session_state.session_id = create_new_session()
    clear_session(st.session_state.session_id)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = True

# ==================== SIDEBAR ====================
with st.sidebar:
    # Logo
    col_logo = st.columns([1, 2, 1])
    with col_logo[1]:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100)
    
    st.markdown("<h2>ASTRA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.9rem; opacity:0.8; margin-top:-15px;'>Smart AI Assistance</p>", unsafe_allow_html=True)

    
    # Session Controls
    st.subheader("🧠 Session Controls")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🆕 Start New Session", use_container_width=True):
        clear_session(st.session_state.session_id)
        st.session_state.session_id = create_new_session()
        st.session_state.messages = []
        st.session_state.conversation_active = True
        st.success("✅ New session started!")
        time.sleep(0.5)
        st.rerun()
    
    
    # Session Statistics
    st.subheader("📊 Session Stats")
    st.markdown("<br>", unsafe_allow_html=True)
    message_count = len(st.session_state.messages) // 2 if len(st.session_state.messages) > 0 else 0
    
    if st.session_state.conversation_active:
        st.markdown(f'<div class="status-badge status-active">🟢 Status: Active</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-badge status-ended">🔴 Status: Ended</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="status-badge status-messages">💬 Messages: {message_count}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="sidebar-footer">
        <p style='font-size:0.8rem; opacity:0.7;'>Built with ❤️ by</p>
        <p style='font-size:0.95rem; font-weight:600;'>Devkumar Patel</p>
        <p style='font-size:0.75rem; opacity:0.6; margin-top:0.5rem;'>v1.0 | Groq & LangChain</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN HEADER ====================
st.markdown("""
<div class="app-header">
    <h1>🤖 ASTRA - Advanced Support & Task Response Assistant</h1>
    <p>Your intelligent, memory-powered customer support agent</p>
</div>
""", unsafe_allow_html=True)

# ==================== NOTIFICATION BANNER ====================
st.markdown("""
<div class="notification-banner">
    <span style='font-size:1.5rem;'>💡</span>
    <div>
        <strong>Quick Tip:</strong> Type <code style='background:rgba(255,255,255,0.2); padding:0.2rem 0.5rem; border-radius:4px;'>exit</code>
        <code style='background:rgba(255,255,255,0.2); padding:0.2rem 0.5rem; border-radius:4px;'>quit</code>
        <code style='background:rgba(255,255,255,0.2); padding:0.2rem 0.5rem; border-radius:4px;'>end</code> or 
        <code style='background:rgba(255,255,255,0.2); padding:0.2rem 0.5rem; border-radius:4px;'>bye</code> to end the conversation
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== WELCOME MESSAGE ====================
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-card">
        <h3>👋 Welcome to ASTRA!</h3>
        <p>I'm your intelligent support assistant, ready to help you with:</p>
        <ul>
            <li>💬 <strong>Customer Support:</strong> Answering questions about products and services</li>
            <li>🔧 <strong>Technical Issues:</strong> Troubleshooting and problem-solving</li>
            <li>💰 <strong>Billing & Payments:</strong> Account and payment inquiries</li>
            <li>📋 <strong>General Assistance:</strong> Information and guidance on various topics</li>
        </ul>
        <p><strong>Get started</strong> by typing your question or concern in the chat box below. I'll remember our conversation and provide contextual responses.</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== CONVERSATION STATUS ====================
if not st.session_state.conversation_active:
    st.info("💡 The conversation has ended. Click '🆕 Start New Session' in the sidebar to begin a new conversation.")

# ==================== CHAT INTERFACE ====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==================== USER INPUT HANDLING ====================
if st.session_state.conversation_active:
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Check for exit commands
        if user_input.lower().strip() in ["exit", "quit", "bye", "end"]:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            farewell_msg = "👋 Thank you for using ASTRA! The conversation has ended. Click '🆕 Start New Session' in the sidebar to start a new conversation."
            with st.chat_message("assistant"):
                st.markdown(farewell_msg)
            st.session_state.messages.append({"role": "assistant", "content": farewell_msg})
            st.session_state.conversation_active = False
            st.rerun()
        
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get AI response
        with st.spinner("🤔 Thinking..."):
            try:
                result = handle_query_with_memory(st.session_state.session_id, user_input)
                response = result["response"]
            except Exception as e:
                response = f"⚠️ An error occurred: {str(e)}. Please try again or start a new session."
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
else:
    st.chat_input("Type your message here...", disabled=True)