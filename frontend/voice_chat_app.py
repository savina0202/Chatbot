import gradio as gr
import requests
import os
import tempfile
from datetime import datetime

# Backend API configuration
API_BASE_URL = "http://localhost:8002"
#CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
CHAT_ENDPOINT = f"{API_BASE_URL}/voice-query"
CHAT_HISTORY_ENDPOINT = f"{API_BASE_URL}/chathist"

def record_and_chat(audio_file):
    """
    Record voice, send to backend API, and return the response audio
    """
    if audio_file is None:
        return None, "Please record your voice first."
    
    try:
        # Prepare the audio file for upload
        with open(audio_file, "rb") as f:
            files = {"audio": (os.path.basename(audio_file), f, "audio/wav")}
            
            # Make API call to backend
            response = requests.post(CHAT_ENDPOINT, files=files)
            
            if response.status_code == 200:
                # Save the response audio to a temporary file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"response_{timestamp}.wav"
                output_path = os.path.join(tempfile.gettempdir(), output_filename)
                
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                # Get chat history for display
                try:
                    history_response = requests.get(CHAT_HISTORY_ENDPOINT)
                    if history_response.status_code == 200:
                        chat_history = history_response.json()
                        
                        # Debug: Print raw chat history to understand the structure
                        print(f"Raw chat history: {chat_history}")
                        
                        # Filter out duplicate messages and format properly
                        if chat_history:
                            # Remove duplicates based on text content
                            seen_messages = set()
                            unique_messages = []
                            
                            for msg in chat_history:
                                message_key = f"{msg['role']}:{msg['text']}"
                                if message_key not in seen_messages:
                                    seen_messages.add(message_key)
                                    unique_messages.append(msg)
                            
                            # Take the last 6 unique messages for display
                            recent_messages = unique_messages[-6:] if len(unique_messages) >= 6 else unique_messages
                            
                            formatted_history = "\n".join([
                                f"{'👤 You' if msg['role'] == 'user' else '🤖 AI'}: {msg['text']}"
                                for msg in recent_messages
                            ])
                        else:
                            formatted_history = "No conversation history yet"
                    else:
                        formatted_history = "Unable to fetch chat history"
                except Exception as e:
                    formatted_history = f"Error fetching chat history: {str(e)}"
                    print(f"Error in chat history formatting: {e}")
                
                return output_path, formatted_history
            else:
                return None, f"API Error: {response.status_code} - {response.text}"
                
    except Exception as e:
        return None, f"Error: {str(e)}"



def clear_history():
    """
    Clear the chat history display
    """
    return ""

def clear_backend_history():
    """
    Clear the backend conversation history
    """
    try:
        response = requests.post(f"{API_BASE_URL}/clear_history/")
        if response.status_code == 200:
            return "Backend history cleared successfully"
        else:
            return f"Failed to clear backend history: {response.status_code}"
    except Exception as e:
        return f"Error clearing backend history: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Voice Chat Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎤 Voice Chat Assistant")
    gr.Markdown("Record your voice and get an AI response!")
    
    # Main content in two columns side by side
    with gr.Row():
        # Left column - Record Your Voice section
        with gr.Column(scale=1):
            gr.Markdown("## 🎙️ Record Your Voice")
            
            # Audio input
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Click to record",
                format="wav",
                interactive=True
            )
            
            # Send button below the audio input
            send_btn = gr.Button("🚀 Send to AI", variant="primary")
            
            # Control buttons
            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear History", variant="secondary")
                clear_backend_btn = gr.Button("🧹 Clear Backend", variant="secondary")
            
            # Status display
            status_display = gr.Textbox(
                label="Status",
                interactive=False,
                placeholder="Ready to record..."
            )
        
        # Right column - AI Response section
        with gr.Column(scale=1):
            gr.Markdown("## 🤖 AI Response")
            audio_output = gr.Audio(
                label="AI Response Audio",
                interactive=False,
                type="filepath"
            )
    
    # Chat history display below both sections
    gr.Markdown("## 💬 Recent Conversation")
    chat_history = gr.Textbox(
        label="Chat History",
        interactive=False,
        lines=8,
        max_lines=12,
        placeholder="Your conversation will appear here..."
    )
    
    # Event handlers
    send_btn.click(
        fn=record_and_chat,
        inputs=[audio_input],
        outputs=[audio_output, chat_history]
    )
    
    clear_btn.click(
        fn=clear_history,
        outputs=[chat_history]
    )
    
    clear_backend_btn.click(
        fn=clear_backend_history,
        outputs=[status_display]
    )
    
    # Auto-update status
    audio_input.change(
        fn=lambda x: "Voice recorded! Click 'Send to AI' to get response." if x else "Ready to record...",
        inputs=[audio_input],
        outputs=[status_display]
    )

if __name__ == "__main__":
    print("🎤 Starting Voice Chat Assistant...")
    print(f"🌐 Backend API: {API_BASE_URL}")
    print("📱 Frontend will be available at: http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
