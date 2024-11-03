# Install the required libraries if not already installed

# Import necessary modules
from diffusers import StableDiffusionPipeline
import torch
from rembg import remove
import io

# Load the model
model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"  # Change to other models as needed
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to("cuda")  # For faster performance on GPUs

pipe.enable_freeu(s1=0.9, s2=0.2, b1=1.5, b2=1.6)

# Generate an image
prompt = "Give me a image of  a funny hat with it being the only single object and it being horizontal and  (no background or transparent background) with no people"
generated_image = pipe(prompt,negative_prompt="humans,blurred images,background",guidance_scale=3.5,num_inference_steps=63,height=200, width=400).images[0]
#generated_image.show()  # Display the image


# Convert the generated image to bytes for rembg compatibility
input_image_bytes = io.BytesIO()
generated_image.save(input_image_bytes, format="PNG")
input_image_bytes.seek(0)

# Use rembg to remove the background
output_image_bytes = remove(input_image_bytes.read())

# Load the background-removed image for display
with open("mustache.png", "wb") as f:
    f.write(output_image_bytes)

# Optional: To display the image if needed
from PIL import Image
output_image = Image.open(io.BytesIO(output_image_bytes))


