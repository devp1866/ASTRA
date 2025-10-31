
import streamlit as st

st.set_page_config(
    page_title="About ASTRA",
    page_icon="ℹ️",
    layout="wide"
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
        max-width: 100% !important;
    }
    
    /* ========== Sticky Header ========== */
    .app-header {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: linear-gradient(135deg, var(--primary-bg) 0%, var(--accent) 100%);
        padding: 1.5rem 2rem;
        margin: -1rem 8rem 2rem 8rem;
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
        margin-left: 320px !important;
        padding: 2rem !important;
    }
    
    /* ========== Content Cards ========== */
    .info-card {
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border-left: 6px solid var(--accent);
        transition: all 0.3s ease;
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
    
    .info-card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transform: translateY(-5px);
    }
    
    .info-card h2 {
        color: var(--primary-bg) !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 3px solid var(--accent);
        padding-bottom: 0.5rem;
    }
    
    .info-card h3 {
        color: var(--accent) !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    .info-card p {
        color: var(--text-secondary) !important;
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
        margin-bottom: 1rem !important;
    }
    
    /* ========== Feature List ========== */
    .feature-list {
        list-style: none;
        padding-left: 0;
        margin: 1rem 0;
    }
    
    .feature-list li {
        padding: 0.8rem 0 0.8rem 2.5rem;
        position: relative;
        transition: all 0.3s ease;
        color: var(--text-primary) !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }
    
    .feature-list li:hover {
        transform: translateX(5px);
    }
    
    .feature-list li::before {
        content: "✓";
        position: absolute;
        left: 0;
        top: 0.8rem;
        width: 1.5rem;
        height: 1.5rem;
        background: linear-gradient(135deg, #4A90E2, #2196f3);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
    }
    
    /* ========== Tech Stack Items ========== */
    .tech-item {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid var(--accent);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .tech-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .tech-item:hover::before {
        left: 100%;
    }
    
    .tech-item:hover {
        transform: translateX(10px);
        box-shadow: 0 4px 16px rgba(11, 37, 69, 0.15);
    }
    
    .tech-item strong {
        color: var(--primary-bg) !important;
        font-size: 1.15rem !important;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .tech-item p {
        color: #555 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
    
    /* ========== Profile Section ========== */
    .profile-container {
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .profile-container img {
        border-radius: 50%;
        border: 5px solid var(--accent);
        box-shadow: 0 8px 24px rgba(11, 37, 69, 0.3);
        transition: all 0.3s ease;
    }
    
    .profile-container img:hover {
        transform: scale(1.05) rotate(3deg);
        box-shadow: 0 12px 32px rgba(74, 144, 226, 0.4);
    }
    
    /* ========== Contact Links ========== */
    .contact-link {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem 0.5rem 0.5rem 0;
        background: linear-gradient(135deg, var(--accent) 0%, var(--hover-accent) 100%);
        color: white !important;
        text-decoration: none;
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(11, 37, 69, 0.3);
    }
    .name-link {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem 0.5rem 0.5rem 0;
        background: linear-gradient(135deg, var(--accent) 0%, var(--hover-accent) 100%);
        color: white !important;
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(11, 37, 69, 0.3);
    }
    .name-link:hover {
        background: linear-gradient(135deg, var(--hover-accent) 0%, #2c5f8d 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.5);
        color: white !important;
    }
    .contact-link:hover {
        background: linear-gradient(135deg, var(--hover-accent) 0%, #2c5f8d 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.5);
        color: white !important;
    }
    
    /* ========== Quote Box ========== */
    .quote-box {
        background: linear-gradient(135deg, var(--primary-bg) 0%, var(--accent) 100%);
        color: var(--light-grey);
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        font-size: 1.6rem;
        font-style: italic;
        font-weight: 300;
        margin-top: 3rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .quote-box::before {
        content: '"';
        position: absolute;
        top: -20px;
        left: 20px;
        font-size: 5rem;
        opacity: 0.1;
        font-family: Georgia, serif;
    }
    
    .quote-box::after {
        content: '"';
        position: absolute;
        bottom: -60px;
        right: 20px;
        font-size: 5rem;
        opacity: 0.1;
        font-family: Georgia, serif;
    }
    
    /* ========== Divider ========== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(74, 144, 226, 0.5), transparent);
        margin: 1.5rem 0;
    }
    
    /* ========== Footer ========== */
    html, body, .main, .block-container {
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    /* Allow content to grow and push footer down */
    .block-container {
        flex: 1;
    }

    /* Footer styling */
    .footer-section {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(1,18,34,0.05) 0%, rgba(11,37,69,0.05) 100%);
        border-top: 2px solid rgba(74,144,226,0.2);
        border-radius: 12px 12px 0 0;
        width: 100%;
        color: #011222;
        font-weight: 500;
    }
    
    .footer-section p {
        margin: 0.5rem 0;
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
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    
    # Logo
    col_logo = st.columns([1, 2, 1])
    with col_logo[1]:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100)
    
    st.markdown("<h2>ASTRA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.9rem; opacity:0.8; margin-top:-15px;'>Smart AI Assistance</p>", unsafe_allow_html=True)
    
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
    <h1>ℹ️ About ASTRA & Developer</h1>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    # About ASTRA-AI Section
    st.markdown("""
    <div class="info-card">
        <h2>🚀 ASTRA : Advanced Support & Task Response Assistant</h2>
        <p>
            ASTRA is a next-generation conversational AI assistant designed to revolutionize 
            customer support and task management.
        </p>
        <ul class="feature-list">
            <li><strong>Intelligent Customer Support:</strong> Handles complex queries with advanced natural language understanding and contextual reasoning</li>
            <li><strong>Technical Troubleshooting:</strong> Provides detailed, step-by-step solutions for technical issues with precision and clarity</li>
            <li><strong>Payment & Service Management:</strong> Assists with billing inquiries, subscription management, and account-related concerns</li>
            <li><strong>Persistent Memory:</strong> Remembers conversation history and user preferences for truly personalized interactions across sessions</li>
        </ul>
        <h3>Why Choose ASTRA?</h3>
        <p>
            Traditional chatbots forget context and provide generic responses. ASTRA is different. 
            With advanced memory management powered by MongoDB and intelligent orchestration through 
            LangChain, every conversation builds on previous interactions, creating a seamless and 
            personalized support experience.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Technology Stack Section
    st.markdown("""
    <div class="info-card">
        <h2>⚙️ Technology Stack</h2>
        <p style="margin-bottom:1.5rem;">
            Built with enterprise-grade technologies ensuring optimal performance, 
            scalability, and reliability for production deployment:
        </p>
        <div class="tech-item">
            <strong>🧠 Groq LLM (LLaMA 3.3 70B)</strong>
        </div>
        <div class="tech-item">
            <strong>🔗 LangChain Framework</strong>
        </div>
        <div class="tech-item">
            <strong>💾 MongoDB Database</strong>
        </div>
        <div class="tech-item">
            <strong>🌐 Streamlit Interface</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Developer Profile Section
    st.markdown("""
    <div class="info-card">
        <h2>👨‍💻 Developer Profile</h2>
        <div class="profile-container">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="150">
        </div>
        <div style='text-align:center;'>
            <a href="https://devp1866.framer.website" class="name-link">Devkumar Patel</a>
        </div>
        <h3 style='margin-top:2rem; text-align:center; margin-bottom:1rem;'>Get in Touch</h3>
        <div style='text-align:center;'>
            <a href="https://github.com/devp1866" target="_blank" class="contact-link">💻 GitHub</a>
            <a href="https://linkedin.com/in/devp1866" target="_blank" class="contact-link">🔗 LinkedIn</a>
            <a href="mailto:devp1866@gmail.com" class="contact-link">📧 Email</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== QUOTE BOX ====================
st.markdown("""
<div class="quote-box">
    Smart Assistance. Human Connection.<br>
    <span style='font-size:1.1rem; margin-top:1rem; display:block; font-style:normal; opacity:0.85;'>
        Building AI that understands, remembers, and truly assists.
    </span>
</div>
""", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer-section">
    <p style='font-size:1.1rem; font-weight:600; color:var(--light-grey);'>© 2025 ASTRA</p>
    <p style='font-size:0.95rem; color:#6b7280;'>Developed with ❤️ by Devkumar Patel</p>
    <p style='font-size:0.85rem; color:#9ca3af; margin-top:0.5rem;'>Version 1.0 | Powered by Groq & LangChain</p>
</div>
""", unsafe_allow_html=True)