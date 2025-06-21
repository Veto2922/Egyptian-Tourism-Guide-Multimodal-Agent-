# Egyptian Tourism Guide - Multimodal AI Assistant

A sophisticated multimodal AI assistant designed to help tourists explore the wonders of Egypt through a rich, interactive interface. This agent leverages cutting-edge generative AI to understand text, voice, and images, providing comprehensive guidance on attractions, cuisine, transportation, and more.

## ✨ Features

- **🗣️ Multimodal Chat**: Interact with the agent via text, voice (speech-to-text), or by uploading images for analysis.
- **🛠️ Tool-Powered Assistance**: The agent uses a set of specialized tools to fetch real-time, accurate information on:
  - **🏛️ Attractions**: Get details on historical sites like the Pyramids of Giza, Valley of the Kings, and more.
  - **🍲 Food**: Receive recommendations for traditional Egyptian dishes like Koshari and Ful Medames.
  - **🚗 Transportation**: Find information on getting around using the Cairo Metro, ride-sharing apps, or Nile Cruises.
  - **☀️ Weather**: Get current weather overviews for major Egyptian regions.
- **🔊 Text-to-Speech**: Enable audio responses to have the assistant speak back to you, creating a more engaging experience.
- **🎨 AI Art Generator**: Generate beautiful, unique images from text descriptions using an integrated AI artist.
- **⚡ Quick Actions**: Use predefined example questions to quickly explore the agent's capabilities.
- **🎨 Modern UI**: A clean and beautiful user interface built with Gradio.

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.8+
- An API key for Gemini (`GEMINI_API_KEY`)
- An API key for Together AI (`TOGETHER_API_KEY`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Egyptian-Tourism-Guide-Multimodal-Agent.git
    cd Egyptian-Tourism-Guide-Multimodal-Agent
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root directory of the project and add your API keys:
    ```
    GEMINI_API_KEY="your_gemini_api_key_here"
    TOGETHER_API_KEY="your_together_api_key_here"
    ```

### Running the Application

Once the installation is complete, you can run the application with the following command:

```bash
python app2.py
```

The application will start, and you can access it by opening the URL provided in your terminal (usually `http://127.0.0.1:7860` or `http://0.0.0.0:7860`).

## Project Structure

```
.
├── app2.py                  # Main Gradio application entry point
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── generated_images/        # Directory for AI-generated art
└── src/
    ├── llm_blocks/          # Core AI model functionalities
    │   ├── artist.py        # Generates images from text
    │   ├── image_understanding.py # Analyzes uploaded images
    │   ├── talker.py        # Handles text-to-speech
    │   └── transcriber.py   # Handles speech-to-text
    └── tools/               # Agent tools for specific information
        ├── get_attraction_info.py
        ├── get_food_recommendations.py
        ├── get_transportation_info.py
        └── get_current_weather_egypt.py
```

## How It Works

The application uses a **Google Gemini flash 2.0** model as the core of the agent. The agent is configured with a system prompt that defines its persona as an Egyptian tourism guide and instructs it on how to use a set of available tools. When a user sends a message, the agent decides whether to answer directly or use one of its tools to get specific information.

- **Gradio UI**: Provides the interactive, multimodal frontend.
- **LLM Blocks**: These modules are classes that wrap the client calls to the generative AI APIs for specific tasks like talking, transcribing, and generating images.
- **Tools**: These are simple Python functions that the agent can call to retrieve structured data about Egypt.

---

Contributions are welcome! Please feel free to fork the repository, make changes, and submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the web application framework
- OpenAI for AI capabilities
- All contributors and users of this project