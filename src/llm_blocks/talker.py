import wave
import simpleaudio as sa
import base64
from google import genai
from google.genai import types

class Talker:
    """
    A class to handle text-to-speech generation and playback using the Google Generative AI API.
    """
    def __init__(self, api_key: str):
        """
        Initializes the Talker class.

        Args:
            api_key (str): Your Google Generative AI API key.
        """
        self.client = genai.Client(api_key=api_key)

    def _write_wave_file(self, filename: str, pcm_data: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
        """
        Writes PCM audio data to a WAV file.

        Args:
            filename (str): The name of the output WAV file.
            pcm_data (bytes): The PCM audio data.
            channels (int): Number of audio channels.
            rate (int): Frame rate (samples per second).
            sample_width (int): Sample width in bytes.
        """
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)

    def speak(self, message: str, output_filename: str = 'out.wav'):
        """
        Converts text message to speech and plays it.

        Args:
            message (str): The text message to convert to speech.
            output_filename (str): The name of the file to save the generated audio.
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=message,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Leda',
                            )
                        )
                    ),
                )
            )

            if not response.candidates or not response.candidates[0].content:
                print("No content returned in response.")
                return

            audio_part = response.candidates[0].content.parts[0]

            if not hasattr(audio_part, 'inline_data') or not audio_part.inline_data:
                print("No inline_data found in audio_part.")
                return

            # Assuming the data is already PCM and not base64 encoded based on the original code
            data = audio_part.inline_data.data

            self._write_wave_file(output_filename, data)

            wave_obj = sa.WaveObject.from_wave_file(output_filename)
            play_obj = wave_obj.play()
            play_obj.wait_done()

        except Exception as e:
            print("An error occurred:", e)

if __name__ == '__main__':
    # Example Usage
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')

    if api_key:
        talker_instance = Talker(api_key)
        text_to_speak = "Hello, how are you today?"
        print(f"Speaking: {text_to_speak}")
        talker_instance.speak(f"Say cheerfully:: {text_to_speak}")
    else:
        print("GEMINI_API_KEY not found. Please set it in your .env file.") 