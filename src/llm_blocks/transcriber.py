from google import genai
from google.genai import types

class Transcriber:
    """
    A class to handle speech-to-text transcription using the Google Generative AI API.
    """
    def __init__(self, api_key: str):
        """
        Initializes the Transcriber class.

        Args:
            api_key (str): Your Google Generative AI API key.
        """
        self.client = genai.Client(api_key=api_key)

    def transcribe_audio(self, file_path: str, prompt: str) -> str:
        """
        Transcribes speech from an audio file.

        Args:
            file_path (str): The path to the audio file (e.g., WAV).
            prompt (str): The prompt for transcription.

        Returns:
            str: The transcribed text.
        """
        # Upload the audio file
        # The file is automatically deleted after the transcription is complete.
        myfile = self.client.files.upload(file=file_path)

        # Generate content with the audio file and prompt
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[prompt, myfile]
        )

        # Delete the uploaded file after use
        self.client.files.delete(name=myfile.name)

        return response.text

if __name__ == '__main__':
    # Example Usage (requires a dummy 'out.wav' file for testing)
    # Create a dummy file for testing purposes if it doesn't exist
    # This dummy file won't contain actual audio but allows the script structure to be tested.
    try:
        # Creating an empty or minimal WAV file structure might be necessary
        # for the client.files.upload to accept it, depending on API requirements.
        # For a simple test, just creating an empty file might suffice if the API is lenient.
        with open("out.wav", "a"): # Using "a" to not overwrite if it exists
            pass # Or write a minimal valid WAV header if needed
    except IOError:
        print("Could not create dummy out.wav file.")

    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')

    if api_key:
        transcriber = Transcriber(api_key)
        audio_file = 'out.wav' # Ensure this file exists for testing
        transcription_prompt = 'Generate a *transcript* of the speech. don\'t add any other text or reply in the transcript'

        # Check if the dummy file exists before attempting transcription
        if os.path.exists(audio_file):
            print(f"Transcribing {audio_file}...")
            transcript = transcriber.transcribe_audio(audio_file, transcription_prompt)
            print("Transcription:")
            print(transcript)
        else:
            print(f"Test audio file {audio_file} not found. Cannot run example usage.")

    else:
        print("GEMINI_API_KEY not found. Please set it in your .env file.")