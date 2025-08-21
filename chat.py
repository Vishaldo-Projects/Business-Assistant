# Fix OpenMP duplicate library issue BEFORE any other imports
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"  # Limit OpenMP threads to prevent conflicts

import uuid
from pathlib import Path
from typing import List, Dict, Generator
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import gradio as gr
import json

# Environment and model configuration
load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')
MODEL = 'gemini-1.5-flash'
LOG_FILE = "chat_history.log"
CONVERSATION_HISTORY_FILE = "conversation_history.json"

# API key validation
if google_api_key:
    print(f"[OK] Google API Key found, starting with {google_api_key[:8]}...")
else:
    print("[ERROR] Google API Key not set. It's required for this application.")
    exit()

# Initialize Gemini API
genai.configure(api_key=google_api_key)

# System prompt for Business Assistant personality
system_message = (
    "You are a professional Business AI Assistant, designed to help entrepreneurs, business owners, and professionals with their business needs. 💼\n\n"
    "Your expertise includes:\n"
    "- Business strategy and planning\n"
    "- Market research and analysis\n"
    "- Financial planning and budgeting\n"
    "- Marketing and digital marketing strategies\n"
    "- Operations management and optimization\n"
    "- Human resources and team management\n"
    "- Sales strategies and customer relationship management\n"
    "- Legal and compliance guidance (general advice only)\n"
    "- Technology solutions for business\n"
    "- Startup guidance and scaling strategies\n\n"
    "Your communication style:\n"
    "- Professional yet approachable\n"
    "- Provide actionable, practical advice\n"
    "- Use business terminology appropriately\n"
    "- Offer structured solutions with clear steps\n"
    "- Ask clarifying questions when needed\n"
    "- Provide examples and case studies when relevant\n"
    "- Stay current with business trends and best practices\n"
    "- Be encouraging while being realistic about challenges\n\n"
    "Always maintain a professional demeanor while being helpful and supportive in achieving business goals."
)

# Text logging with timestamps for debugging
def log_conversation(user_msg: str, bot_msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"--- Conversation at {timestamp} ---\n")
        f.write(f"User: {user_msg}\n")
        f.write(f"Business Assistant: {bot_msg}\n\n")

# Persistent conversation storage for session continuity
def save_conversation_history(history: List[Dict]):
    try:
        with open(CONVERSATION_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving conversation history: {e}")

def load_conversation_history() -> List[Dict]:
    try:
        if os.path.exists(CONVERSATION_HISTORY_FILE):
            with open(CONVERSATION_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading conversation history: {e}")
    return []

# Convert Gradio message format to Gemini API format
def convert_gradio_history_to_gemini(history: List[Dict]) -> List[Dict]:
    messages = []
    for message in history:
        role = "model" if message["role"] == "assistant" else "user"
        messages.append({"role": role, "parts": [message["content"]]})
    return messages

# Streaming chat response handler
def chat(message: str, history: List[Dict]) -> Generator[str, None, None]:
    try:
        model = genai.GenerativeModel(
            model_name=MODEL,
            system_instruction=system_message
        )
        gemini_history = convert_gradio_history_to_gemini(history)
        chat_session = model.start_chat(history=gemini_history)
        response = chat_session.send_message(message, stream=True)

        full_response = ""
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                yield full_response

    except Exception as e:
        error_msg = f"💼 I apologize, but I'm experiencing technical difficulties: {str(e)}. Please try again."
        yield error_msg

# Main chat interaction pipeline
def run_chat_interaction(
    text_message: str,
    history_messages: List[Dict]
) -> Generator[tuple[List[Dict], List[Dict], str], None, None]:
    text_message = (text_message or "").strip()

    if not text_message:
        yield history_messages, history_messages, ""
        return

    # Add user message to conversation
    history_messages = history_messages + [{"role": "user", "content": text_message}]
    yield history_messages, history_messages, ""

    # Stream AI response
    full_response = ""
    is_first_chunk = True
    for response_chunk in chat(text_message, history_messages[:-1]):
        full_response = response_chunk
        if is_first_chunk:
            history_messages = history_messages + [{"role": "assistant", "content": response_chunk}]
            is_first_chunk = False
        else:
            history_messages = history_messages[:-1] + [
                {"role": "assistant", "content": response_chunk}
            ]
        yield history_messages, history_messages, ""

    # Persist conversation data
    if full_response:
        log_conversation(text_message, full_response)
        save_conversation_history(history_messages)

    yield history_messages, history_messages, ""

# Generate conversation analytics for UI display
def get_conversation_summary(history: List[Dict]) -> str:
    if not history:
        return "No previous business consultations found."
    
    conversation_count = len([msg for msg in history if msg["role"] == "user"])
    last_conversation = ""
    
    if len(history) >= 2:
        last_user_msg = next((msg["content"] for msg in reversed(history) if msg["role"] == "user"), "")
        last_bot_msg = next((msg["content"] for msg in reversed(history) if msg["role"] == "assistant"), "")
        
        if last_user_msg and last_bot_msg:
            last_conversation = f"\nLast consultation:\nYou: {last_user_msg[:100]}{'...' if len(last_user_msg) > 100 else ''}\nAssistant: {last_bot_msg[:100]}{'...' if len(last_bot_msg) > 100 else ''}"
    
    return f"Total consultations: {conversation_count}{last_conversation}"

# Application entry point
if __name__ == "__main__":
    # Validate API connection before starting UI
    try:
        model = genai.GenerativeModel(MODEL)
        test_response = model.generate_content("Hello")
        print("[OK] Gemini API connection successful!")
    except Exception as e:
        print(f"[ERROR] Gemini API connection failed: {e}")
        exit("Please check your Google API key and internet connection.")

    # Initialize with existing conversation data
    initial_history = load_conversation_history()

    # Gradio interface configuration
    with gr.Blocks(title="Business AI Assistant", theme=gr.themes.Default()) as demo:
        
        gr.Markdown("""
        # 💼 Business AI Assistant
        ## Your Professional Business Consultant & Strategy Advisor
        
        **Specialized Services:**
        - 📈 Business Strategy & Planning
        - 💰 Financial Analysis & Budgeting  
        - 🎯 Marketing & Sales Strategies
        - 🏢 Operations & Management
        - 🚀 Startup Guidance & Scaling
        - 📊 Market Research & Analytics
        """)

        # Main chat interface
        chatbot = gr.Chatbot(
            type="messages",
            height=500,
            show_label=False,
            value=initial_history,
            placeholder="Ask me about your business challenges, strategies, or growth opportunities..."
        )

        # Application state management
        state = gr.State(value=initial_history)

        # Conversation analytics display
        with gr.Row():
            history_summary = gr.Textbox(
                label="📊 Consultation History Summary",
                value=get_conversation_summary(initial_history),
                interactive=False,
                lines=3
            )

        # Primary input controls
        with gr.Row():
            text_input = gr.Textbox(
                placeholder="Describe your business challenge or question...",
                scale=4,
                show_label=False,
                lines=3
            )
            send_btn = gr.Button("Send 📤", variant="primary", scale=1)

        # Utility controls
        with gr.Row():
            clear_btn = gr.Button("🗑️ New Session", variant="secondary")
            refresh_summary_btn = gr.Button("🔄 Refresh Summary", variant="secondary")

        # Business consultation examples
        gr.Examples(
            examples=[
                ["Help me create a business plan for my startup idea"],
                ["What's the best marketing strategy for a small local business?"],
                ["How do I price my products competitively?"],
                ["What should I consider when hiring my first employee?"],
                ["How can I improve my cash flow management?"],
                ["What digital marketing channels should I focus on?"],
                ["How do I scale my business without losing quality?"],
                ["What are the key metrics I should track for my business?"],
                ["How can I improve customer retention?"],
                ["What's the best way to conduct market research?"],
                ["Help me analyze my business competition"],
                ["How do I create an effective sales funnel?"]
            ],
            inputs=[text_input]
        )

        # UI event handlers
        def clear_chat():
            return [], [], "", "New consultation session started! How can I help you with your business today? 💼"

        def refresh_summary(current_history):
            return get_conversation_summary(current_history)

        def update_summary_after_chat(history):
            return get_conversation_summary(history)

        # Event binding for input submission
        text_submit = text_input.submit(
            fn=run_chat_interaction,
            inputs=[text_input, state],
            outputs=[chatbot, state, text_input],
            queue=True
        ).then(
            fn=update_summary_after_chat,
            inputs=[state],
            outputs=[history_summary]
        )
        
        # Event binding for send button
        send_click = send_btn.click(
            fn=run_chat_interaction,
            inputs=[text_input, state],
            outputs=[chatbot, state, text_input],
            queue=True
        ).then(
            fn=update_summary_after_chat,
            inputs=[state],
            outputs=[history_summary]
        )

        # Utility button events
        clear_btn.click(
            fn=clear_chat,
            outputs=[chatbot, state, text_input, history_summary]
        )

        refresh_summary_btn.click(
            fn=refresh_summary,
            inputs=[state],
            outputs=[history_summary]
        )

        # Business categories and services
        with gr.Accordion("🎯 Business Services Categories", open=False):
            gr.Markdown("""
            ### 📈 Strategy & Planning
            - Business model development
            - Strategic planning & goal setting
            - Competitive analysis
            - SWOT analysis & risk assessment
            
            ### 💰 Finance & Accounting  
            - Financial planning & forecasting
            - Budgeting & cost management
            - Pricing strategies
            - Investment & funding advice
            
            ### 🎯 Marketing & Sales
            - Digital marketing strategies
            - Brand development
            - Customer acquisition & retention
            - Sales funnel optimization
            
            ### 🏢 Operations & Management
            - Process optimization
            - Team building & HR
            - Supply chain management
            - Quality control systems
            
            ### 🚀 Growth & Scaling
            - Market expansion strategies
            - Partnership development
            - Technology implementation
            - Performance metrics & KPIs
            """)

        # User documentation
        gr.Markdown("""
        ---
        ### 💼 How to Use Your Business Assistant:
        
        1. **Describe Your Challenge**: Be specific about your business situation, industry, and goals
        2. **Get Expert Advice**: Receive professional guidance with actionable steps
        3. **Ask Follow-ups**: Dive deeper into strategies and implementation details
        4. **Track Progress**: Use the summary to see your consultation history
        
        ### 🎯 Best Practices:
        - **Be Specific**: Include context like industry, business size, and current challenges
        - **Ask Follow-ups**: Don't hesitate to ask for clarification or deeper insights
        - **Implementation Focus**: Ask for step-by-step guidance and timelines
        - **Use Examples**: Try the example questions to explore different business areas
        
        ### 📊 What I Can Help With:
        ✅ Business strategy and planning  
        ✅ Marketing and sales strategies  
        ✅ Financial planning and analysis  
        ✅ Operations and management  
        ✅ Startup guidance and scaling  
        ✅ Market research and competition analysis  
        
        **Note**: This assistant provides general business guidance. For legal, tax, or specialized professional advice, consult qualified professionals.
        """)

    # Launch application server
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )