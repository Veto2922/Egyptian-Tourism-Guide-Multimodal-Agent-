from PIL import Image
from io import BytesIO
import requests
from together import Together
from IPython.display import Image as DisplayImage, display
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

class Artist:
    """
    A class to handle text-to-image generation using the Together API.
    """
    def __init__(self, output_dir: str = "generated_images"):
        """
        Initializes the Artist class.

        Args:
            output_dir (str): Directory where generated images will be saved. Defaults to "generated_images".
        """
        self.output_dir = output_dir
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def generate_image(self, prompt: str, save_image: bool = True) -> Image.Image:
        """
        Generates an image based on a text prompt and optionally saves it.

        Args:
            prompt (str): The text prompt for image generation.
            save_image (bool): Whether to save the generated image. Defaults to True.

        Returns:
            PIL.Image.Image: The generated image.
        """
        client = Together()

        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            steps=4
        )

        img_url = response.data[0].url
        img_data = requests.get(img_url).content
        image = Image.open(BytesIO(img_data))

        if save_image:
            # Generate filename using timestamp and sanitized prompt
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt[:30])
            filename = f"{timestamp}_{safe_prompt}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            # Save the image
            image.save(filepath)
            print(f"Image saved to: {filepath}")

        return image

if __name__ == '__main__':
    # Example Usage
    artist_generator = Artist()
    image = artist_generator.generate_image("cat and dog ")
    display(image)