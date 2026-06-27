import google.generativeai as genai
from PIL import Image


def analyze_image(image_path, google_api_key):

    try:

        genai.configure(
            api_key=google_api_key
        )

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        image = Image.open(image_path)

        prompt = """
Analyze this image for research purposes.

Return in this format:

### Main Subject
- ...

### Objects Detected
- ...

### Text Found
- ...

### Key Insights
- ...

### Research Relevance
- ...

### Keywords
- ...

Use bullet points only.
Do not write long paragraphs.
"""

        response = model.generate_content(
            [prompt, image]
        )

        return response.text

    except Exception as e:

        return f"Image Analysis Error: {e}"