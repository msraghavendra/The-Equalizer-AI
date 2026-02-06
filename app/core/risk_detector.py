import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Warning: GOOGLE_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)

class RiskDetector:
    def __init__(self, model_name="gemini-3-flash-preview"):
        self.model = genai.GenerativeModel(model_name)

    def analyze_document(self, text_content: str = None, image_data: bytes = None, mime_type: str = None) -> str:
        """
        Analyzes the provided text or image for legal risks, hidden fees, and unfair clauses.
        """
        instruction = """
        You are 'The Equalizer', an expert rights advocate and legal analyst.
        Analyze the following document (provided as text or image). 
        Identify:
        1. High Risk Clauses (in red flags)
        2. Hidden Fees or Overcharges
        3. Unfair or Ambiguous Terms
        
        Provide the output in a clear, simple bulleted list. 
        Explain *why* each item is a risk in simple terms (5th grade reading level).
        """

        content = [instruction]
        if text_content:
            content.append(f"Document Text:\n{text_content}")
        
        if image_data:
            content.append({
                "mime_type": mime_type,
                "data": image_data
            })

        try:
            response = self.model.generate_content(content)
            # Gemini response might be blocked if safety settings are triggered, handle gracefully
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback and response.prompt_feedback.block_reason:
                 return f"Error: Analysis blocked due to safety reason: {response.prompt_feedback.block_reason}"
            
            return response.text
        except Exception as e:
            return f"Error during analysis: {str(e)}"

# Example Usage
if __name__ == "__main__":
    detector = RiskDetector()
    sample_text = "The service provider reserves the right to increase fees by 50% without prior notice."
    print("Analyzing sample text...")
    print(detector.analyze_document(sample_text))
