import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini (Ensure this is handled centrally in a real app, but fine here for modularity)
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class DocumentSimplifier:
    def __init__(self, model_name="gemini-3-flash-preview"):
        self.model = genai.GenerativeModel(model_name)

    def simplify_text(self, text_content: str = None, image_data: bytes = None, mime_type: str = None) -> str:
        """
        Simplifies complex legal jargon into plain language from text or images.
        """
        instruction = """
        You are 'The Equalizer', a helpful interpreter.
        Rewrite the following text from the document (provided as text or image) so that a 5th grader can understand it.
        
        Rules:
        - Remove all jargon (or explain it simply).
        - Keep the sentences short.
        - Tone: Friendly, clear, and reassuring.
        - Maintain the original meaning but make it accessible.
        """

        content = [instruction]
        if text_content:
            content.append(f"Text to Simplify:\n{text_content}")
        
        if image_data:
            content.append({
                "mime_type": mime_type,
                "data": image_data
            })

        try:
            response = self.model.generate_content(content)
             # Handle blocked content
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback and response.prompt_feedback.block_reason:
                 return f"Error: Simplification blocked due to: {response.prompt_feedback.block_reason}"

            return response.text
        except Exception as e:
            return f"Error during simplification: {str(e)}"

# Example Usage
if __name__ == "__main__":
    simplifier = DocumentSimplifier()
    sample_text = "The party of the first part shall herewith indemnify the party of the second part..."
    print("Simplifying sample text...")
    print(simplifier.simplify_text(sample_text))
