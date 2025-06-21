import gradio as gr
import os
from PIL import Image
import tempfile
import base64
from google import genai
from google.genai import types
from datetime import datetime
from src.llm_blocks.transcriber import Transcriber
from src.llm_blocks.talker import Talker
from src.llm_blocks.image_understanding import ImageUnderstanding
from src.llm_blocks.artist import Artist
from src.tools.get_attraction_info import get_attraction_info
from src.tools.get_food_recommendations import get_food_recommendations
from src.tools.get_transportation_info import get_transportation_info
from src.tools.get_current_weather_egypt import get_current_weather_egypt
import io
import time

# Initialize API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
client = genai.Client(api_key=api_key)

# System message for the agent
SYSTEM_MESSAGE = """You are an expert Egyptian Tourism Guide AI assistant. Your role is to help travelers explore Egypt by providing:

1. **Attraction Information**: Details about historical sites, museums, and landmarks
2. **Food Recommendations**: Traditional Egyptian cuisine and where to find it  
3. **Transportation**: How to get around Egypt efficiently and safely
4. **Cultural Tips**: Local customs, etiquette, and practical advice
5. **Weather Information**: Current conditions and what to expect

**How to Use Tools:**
- When a user asks a question, first determine if one of the available tools can provide the answer.
- If a relevant tool exists, you must call it with the correct parameters derived from the user's query.
- Use the tool outputs to construct your final response to the user.
- If no tool is suitable for the user's query, answer from your general knowledge.

**Tool Specifics:**

*   **`get_attraction_info(attraction_name: str)`**
    *   **Purpose:** Provides detailed information about a specific Egyptian tourist attraction.
    *   **Parameter:** `attraction_name` (string) - The name of the attraction.
    *   **Keywords:** Use full or partial names for attractions like:
        *   "Pyramids of Giza"
        *   "Valley of the Kings"
        *   "Bibliotheca Alexandrina"
        *   "Abu Simbel Temples"
        *   "Khan el-Khalili Bazaar"
    *   **Example Call:** If the user asks, "Tell me about the pyramids," call the tool with `attraction_name="Pyramids of Giza"`.

*   **`get_food_recommendations(dish_name: str = "")`**
    *   **Purpose:** Recommends traditional Egyptian dishes.
    *   **Parameter:** `dish_name` (string, optional) - The name of the dish.
    *   **Keywords:** Use dish names like:
        *   "Koshari"
        *   "Ful Medames"
        *   "Mahshi"
    *   **Behavior:** If `dish_name` is empty, the tool returns a general list of must-try dishes.
    *   **Example Call:** For "What is Koshari?", call with `dish_name="Koshari"`.

*   **`get_transportation_info(transport_type: str = "")`**
    *   **Purpose:** Offers guidance on transportation options in Egypt.
    *   **Parameter:** `transport_type` (string, optional) - The mode of transport.
    *   **Keywords:** Use terms like:
        *   "Cairo Metro"
        *   "Uber" or "Careem"
        *   "Nile River Cruise"
    *   **Behavior:** If `transport_type` is empty, the tool returns general information about various options.
    *   **Example Call:** For "How does the metro work in Cairo?", call with `transport_type="Cairo Metro"`.

*   **`get_current_weather_egypt()`**
    *   **Purpose:** Provides a general overview of current weather conditions across major regions in Egypt.
    *   **Parameters:** This tool takes no parameters.
    *   **Behavior:** It returns weather information based on whether it is currently summer or a cooler season in Egypt.
    *   **Example Call:** If the user asks, "What's the weather like?", simply call `get_current_weather_egypt()`.

Always be helpful, accurate, and culturally respectful. Use the available tools to provide specific information. Keep responses informative but concise. Include relevant emojis to make responses more engaging.

When users upload images, analyze them for Egyptian content and provide relevant tourism advice."""

# Initialize components
transcriber = Transcriber(api_key=api_key)
talker = Talker(api_key=api_key)
image_understanding = ImageUnderstanding(api_key=api_key)
artist = Artist()


def create_chat_session():
    """Creates a new chat session."""
    return client.chats.create(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(
            tools=[
                get_attraction_info,
                get_food_recommendations, 
                get_transportation_info,
                get_current_weather_egypt
            ],
            system_instruction=SYSTEM_MESSAGE
        )
    )

def handle_user_message(user_input, chat_history, image_upload, chat_session, tts_on):
    """
    Processes user input (text, audio, image) and streams the response.
    """
    try:
        content = []
        display_message = user_input
        
        # Handle image upload
        if image_upload:
            try:
                pil_image = Image.open(image_upload)
                content.append(pil_image)
                # Display the uploaded image in the chat
                chat_history.append(((image_upload,), None)) 
                
                # If there's no text with the image, create a default message
                if not user_input or not user_input.strip():
                    display_message = "Analyze this image in the context of Egyptian tourism."
                    content.append(display_message)
            except Exception as e:
                chat_history.append([f"Error processing image: {str(e)}", None])
                return chat_history, chat_session, None, None
        elif user_input and user_input.strip():
            content.append(user_input)
        else:
            # No new input - return unchanged state
            return chat_history, chat_session, None, None

        # Add user's message to chat for display and set placeholder for response
        chat_history.append([display_message, "🤔 Thinking..."])
        yield chat_history, chat_session, None, None

        # Send message to Gemini and get response
        try:
            response = chat_session.send_message_stream(content)
            assistant_response = ""
            for chunk in response:
                if chunk.text:  # Check if chunk has text
                    assistant_response += chunk.text
                    chat_history[-1][1] = assistant_response
                    yield chat_history, chat_session, None, None
        except Exception as e:
            assistant_response = f"❌ An error occurred: {str(e)}"
            chat_history[-1][1] = assistant_response
            yield chat_history, chat_session, None, None

        # After getting the full response, generate audio if TTS is enabled
        audio_output = None
        if tts_on and assistant_response and assistant_response.strip():
            try:
                gr.Info("🔊 Generating audio response...")
                audio_output = talker.speak(assistant_response)
            except Exception as e:
                gr.Warning(f"Could not generate audio: {e}")

        yield chat_history, chat_session, None, audio_output
        
    except Exception as e:
        # Handle any unexpected errors
        error_message = f"❌ Unexpected error: {str(e)}"
        if chat_history:
            chat_history[-1][1] = error_message
        else:
            chat_history.append(["Error", error_message])
        yield chat_history, chat_session, None, None


def clear_history():
    """Clears the chat history and resets the session."""
    try:
        return [], create_chat_session()
    except Exception as e:
        gr.Error(f"Failed to reset session: {e}")
        return [], None

# --- Gradio UI ---
custom_css = """
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.gradio-container {
    font-family: 'Poppins', sans-serif;
}
#main-header {
    background: linear-gradient(135deg, #ff9a56 0%, #ffad56 100%);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    color: white;
}
#main-title {
    font-size: 3rem;
    font-weight: 700;
}
#chatbot {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    min-height: 500px;
}
.gradio-container button {
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}
"""

with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange", secondary_hue="blue"), css=custom_css) as demo:
    # State management
    chat_session = gr.State(create_chat_session)
    
    # Header
    with gr.Row():
        gr.HTML("""
            <div id="main-header">
                <h1 id="main-title">🏛️ Egyptian Tourism Guide</h1>
                <p>Your AI-powered companion for exploring the wonders of Egypt</p>
            </div>
        """)

    with gr.Row(equal_height=True):
        # Main chat column
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                avatar_images=(None, "https://i.imgur.com/3f4s5gU.png"), # Assistant avatar
                height=600,
                show_label=False,
            )
            
            with gr.Row():
                image_upload = gr.UploadButton("📷", file_types=["image"], scale=1)
                audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤", scale=1)
                text_input = gr.Textbox(
                    scale=5,
                    show_label=False,
                    placeholder="Ask me anything about Egyptian tourism... 🗣️",
                    container=False,
                )
                submit_btn = gr.Button("▶️", variant="primary", scale=1)
                
        # Sidebar column
        with gr.Column(scale=1):
            with gr.Accordion("🎨 AI Art Generator", open=False):
                art_prompt = gr.Textbox(label="Image Description", placeholder="e.g., A cat wearing a pharaoh's headdress")
                generate_art_btn = gr.Button("Generate Image")
                art_output = gr.Image(label="Generated Art")

            with gr.Accordion("⚡ Quick Actions", open=False):
                quick_questions = [
                    "Tell me about the Pyramids of Giza",
                    "What's the weather like in Cairo?",
                    "Recommend some Egyptian street food",
                    "How do I get around in Cairo?",
                    "What is Koshari?",
                    "Tell me about the Abu Simbel Temples"
                ]
                quick_question_dd = gr.Dropdown(quick_questions, label="Example Questions")
                ask_quick_btn = gr.Button("Ask")

            with gr.Accordion("⚙️ Settings & Actions", open=True):
                tts_enabled = gr.Checkbox(label="🔊 Enable Text-to-Speech", value=False)
                clear_btn = gr.Button("🗑️ Clear Chat History")
            
            tts_output = gr.Audio(label="Assistant's Voice", autoplay=True, visible=False)
    
    # --- Event Handlers ---
    
    # Gather all inputs for the message handler
    message_inputs = [text_input, chatbot, image_upload, chat_session, tts_enabled]
    
    # Define outputs based on TTS setting
    tts_message_outputs = [chatbot, chat_session, image_upload, tts_output]

    # Main chat submission logic
    def submit_and_clear(user_input, chat_history, image_upload, chat_session, tts_enabled):
        # Process the message
        last_result = None
        try:
            for result in handle_user_message(user_input, chat_history, image_upload, chat_session, tts_enabled):
                last_result = result
                yield result
            # Clear the image_upload after processing (if we got any results)
            if last_result is not None:
                yield last_result[0], last_result[1], None, last_result[3]  # Clear image_upload as well
        except Exception as e:
            # If there's an error, return the current state without changes
            yield chat_history, chat_session, None, None

    submit_event = submit_btn.click(
        submit_and_clear,
        inputs=message_inputs,
        outputs=tts_message_outputs,
    ).then(lambda: gr.update(value=""), outputs=text_input)

    text_input.submit(
        submit_and_clear,
        inputs=message_inputs,
        outputs=tts_message_outputs,
    ).then(lambda: gr.update(value=""), outputs=text_input)

    # Clear chat
    clear_btn.click(
        clear_history, 
        inputs=[], 
        outputs=[chatbot, chat_session]
    )

    # AI Art Generator
    def generate_art(prompt):
        if not prompt or not prompt.strip():
            raise gr.Error("Please enter a prompt for the image.")
        try:
            gr.Info("🎨 Generating your masterpiece...")
            image_path = artist.generate_image(prompt)
            return image_path
        except Exception as e:
            raise gr.Error(f"Failed to generate image: {e}")

    generate_art_btn.click(
        generate_art,
        [art_prompt],
        [art_output]
    )
    
    # Quick Actions
    def handle_quick_question(question, chat_history, chat_session, tts_on):
        if not question:
            return chat_history, chat_session, None, None
        # Re-use the main message handler for quick questions
        for response in handle_user_message(question, chat_history, None, chat_session, tts_on):
            yield response

    ask_quick_btn.click(
        handle_quick_question,
        [quick_question_dd, chatbot, chat_session, tts_enabled],
        tts_message_outputs
    )
    
    # Audio Transcription
    def transcribe_audio(audio_file):
        if audio_file:
            try:
                gr.Info("🎤 Transcribing audio...")
                # Fixed method call - using .transcribe instead of .transcribe_audio
                transcribed_text = transcriber.transcribe(audio_file)
                return transcribed_text if transcribed_text else ""
            except Exception as e:
                gr.Error(f"Audio transcription failed: {e}")
                return ""
        return ""
        
    audio_input.change(
        transcribe_audio,
        [audio_input],
        [text_input],
    )


if __name__ == "__main__":
    demo.launch(debug=True, server_name="0.0.0.0", server_port=7860)