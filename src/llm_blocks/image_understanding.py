from google import genai
from google.genai import types

class ImageUnderstanding:
    """
    A class to handle image-to-text generation using the Google Generative AI API.
    """
    def __init__(self, api_key: str):
        """
        Initializes the ImageCaptioner class.

        Args:
            api_key (str): Your Google Generative AI API key.
        """
        self.client = genai.Client(api_key=api_key)

    def understand_image(self, file_path: str, prompt: str) -> str:
        """
        Generates a text caption for an image.

        Args:
            file_path (str): The path to the image file.
            prompt (str): The prompt for generating the caption.

        Returns:
            str: The generated text caption.
        """
        my_file = self.client.files.upload(file=file_path)

        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[my_file, prompt],
        )
        
        # Delete the uploaded file after use
        self.client.files.delete(name=my_file.name)

        return response.text

if __name__ == '__main__':
    # Example Usage (requires a dummy 'output.png' file for testing)
    # Create a dummy file for testing purposes if it doesn't exist
    try:
        with open(r"D:\GAN_AI\projects\Egyptian-Tourism-Guide-Multimodal-Agent-\src\llm_blocks\generated_images\20250608_160905_cat_and_dog_.png", "x") as f:
            pass
    except FileExistsError:
        pass

    # Replace with your actual API key or load from .env
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if api_key:
        understanding = ImageUnderstanding(api_key)
        # Ensure 'output.png' exists for this example to work
        caption = understanding.understand_image(r"D:\GAN_AI\projects\Egyptian-Tourism-Guide-Multimodal-Agent-\src\llm_blocks\generated_images\20250608_160905_cat_and_dog_.png", "describe this image.")
        print(caption)
    else:
        print("GEMINI_API_KEY not found. Please set it in your .env file.") 