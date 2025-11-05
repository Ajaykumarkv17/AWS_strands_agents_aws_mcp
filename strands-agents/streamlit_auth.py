#!/usr/bin/env python3
"""Streamlit UI with AWS Cognito OAuth2 and Streaming"""

import streamlit as st
import requests
import os
import time
from typing import Dict, Optional
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Memory-Enabled AI Agent", page_icon="🧠", layout="wide")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# AWS Cognito OAuth2 Configuration
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")  # e.g., https://your-domain.auth.us-east-1.amazoncognito.com
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

if COGNITO_DOMAIN and CLIENT_ID:
    AUTHORIZE_URL = f"{COGNITO_DOMAIN}/oauth2/authorize"
    TOKEN_URL = f"{COGNITO_DOMAIN}/oauth2/token"
    REVOKE_URL = f"{COGNITO_DOMAIN}/oauth2/revoke"
    oauth2 = OAuth2Component(
        CLIENT_ID,
        CLIENT_SECRET or "",
        AUTHORIZE_URL,
        TOKEN_URL,
        TOKEN_URL,
        REVOKE_URL
    )
else:
    oauth2 = None

st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stChatMessage {
        border-radius: 15px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    [data-testid="stChatMessageContent"] {
        padding: 0.5rem;
    }
    [data-testid="stChatMessageContent"] p {
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 0.5rem;
    }
    .memory-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        font-size: 0.9rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .tool-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_id" not in st.session_state:
        st.session_state.user_id = "default"
    if "token_checked" not in st.session_state:
        st.session_state.token_checked = False

def call_api(endpoint: str, method: str = "GET", data: Optional[Dict] = None):
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return {"success": False}

def get_response(prompt: str, user_id: str):
    """Get API response with proper error handling"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"messages": [{"role": "user", "content": prompt}], "user_id": user_id},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result.get("message", "No response")
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. The agent is taking longer than expected. Please try again."
    except requests.exceptions.RequestException as e:
        return f"⚠️ Connection error: {str(e)}"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def login_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("# 🧠 Memory-Enabled AI Agent")
    st.markdown("### Powered by Amazon Nova & Bedrock")
    st.markdown("---")
    
    if oauth2:
        # Check if we have a token from OAuth callback
        if not st.session_state.token_checked:
            result = oauth2.authorize_button(
                "🔐 Sign in with AWS Cognito",
                REDIRECT_URI,
                "openid",
                pkce="S256",
                use_container_width=True,
                key="oauth_button"
            )
            
            if result and 'token' in result:
                st.session_state.token = result['token']
                st.session_state.authenticated = True
                st.session_state.token_checked = True
                
                # Extract user info from token
                try:
                    import jwt
                    decoded = jwt.decode(result['token']['id_token'], options={"verify_signature": False})
                    st.session_state.user_id = decoded.get('email', decoded.get('sub', 'user'))
                except:
                    st.session_state.user_id = "user"
                
                st.rerun()
        else:
            st.info("✅ Authentication successful! Redirecting...")
            time.sleep(0.5)
            st.rerun()
    else:
        st.warning("⚠️ Cognito not configured")
        st.markdown("### Demo Mode")
        with st.form("demo_login"):
            username = st.text_input("Username", placeholder="Enter your name")
            submit = st.form_submit_button("🚀 Start Demo", use_container_width=True)
            if submit and username:
                st.session_state.authenticated = True
                st.session_state.user_id = username
                st.session_state.token_checked = True
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Memory Features</h3>
            <div class="tool-badge">Remembers your name</div>
            <div class="tool-badge">Learns preferences</div>
            <div class="tool-badge">Maintains context</div>
            <div class="tool-badge">Personalizes responses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🛠️ Available Tools</h3>
            <div class="tool-badge">Calculator</div>
            <div class="tool-badge">Current time</div>
            <div class="tool-badge">AWS account info</div>
            <div class="tool-badge">S3 bucket listing</div>
            <div class="tool-badge">System information</div>
        </div>
        """, unsafe_allow_html=True)

def main_app():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# 🧠 Memory-Enabled AI Agent")
        st.markdown(f"**User:** `{st.session_state.user_id}`")
    with col2:
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            st.session_state.authenticated = False
            st.session_state.messages = []
            st.session_state.token_checked = False
            st.rerun()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🧠 Memory Management")
        st.markdown("*Your AI remembers across sessions*")
        
        if st.button("📥 Load My Memories", use_container_width=True, type="secondary"):
            with st.spinner("Loading memories..."):
                result = call_api("/memory", "POST", {"user_id": st.session_state.user_id})
                if result.get("success"):
                    memories = result.get("memories", [])
                    if memories:
                        st.markdown("### Stored Memories:")
                        for mem in memories[:5]:
                            st.markdown(f'<div class="memory-card">💭 {mem.get("memory", "")}</div>', unsafe_allow_html=True)
                    else:
                        st.info("No memories yet. Start chatting!")
        
        if st.button("🗑️ Clear All Memories", use_container_width=True):
            if call_api(f"/memory/{st.session_state.user_id}", "DELETE").get("success"):
                st.success("✅ Memories cleared!")
        
        st.divider()
        st.markdown("## 🛠️ Available Tools")
        st.markdown("""
        - 🧮 **Calculator** - Math operations
        - ⏰ **Current Time** - Get current time
        - ☁️ **AWS Account** - Account info
        - 🪣 **S3 Buckets** - List buckets
        - 💻 **System Info** - System details
        """)
        
        st.divider()
        st.markdown("## 💡 Try Asking")
        st.markdown("""
        - *"My name is [name] and I like [topic]"*
        - *"What's my name?"*
        - *"Calculate 25 * 48"*
        - *"What time is it?"*
        - *"List my S3 buckets"*
        """)
    
    # Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("💬 Ask me anything... I'll remember our conversation!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                response = get_response(prompt, st.session_state.user_id)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    init_session()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
