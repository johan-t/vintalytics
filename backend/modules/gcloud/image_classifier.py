import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image
import os
import json

MODEL_ID = "gemini-1.5-flash-002"

vertexai.init(project="aihack24ber-8510", location="europe-west2")

generative_multimodal_model = GenerativeModel("gemini-1.5-flash-002")

def classify_image(title: str, image_path: str):
    image = Image.load_from_file(image_path)

    prompt = f"""
    I am trying to make listings of second hand searchable, to do this I need you to classify the clothing items based on their title and image.
    Try to get multiple categories, colors, materials and styles.
    
    Analyze the image and title, then return a JSON object with the following structure:
    {{
        "categories": "string",  // Main categories like "Shoes", "Tops", "Bottoms", "Dresses", "Outerwear", "Accessories"
        "colors": ["string"],  // Array of colors present in the item
        "materials": ["string"],  // Array of materials like "Leather", "Cotton", "Denim"
        "styles": ["string"]  // Array of styles descriptors like "Casual", "Formal", "Sporty"
    }}
    
    The title is: {title}
    
    Return ONLY valid JSON, no additional text.
    """

    response = generative_multimodal_model.generate_content(
        [prompt, image],
        generation_config={
            "temperature": 0.1,  # Lower temperature for more consistent output
            "top_p": 0.8,
            "top_k": 40
        }
    )

    try:
        # Parse the response to ensure it's valid JSON
        # Remove any markdown formatting if present
        clean_response = response.text.replace("```json", "").replace("```", "").strip()
        categories = json.loads(clean_response)
        return categories
    except json.JSONDecodeError:
        print(f"Error parsing JSON: {response.text}")
        # Fallback if response isn't valid JSON
        return {
            "categories": "Other",
            "colors": [],
            "materials": [],
            "styles": []
        }
