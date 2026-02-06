import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class ActionEngine:
    def __init__(self, model_name="gemini-3-flash-preview"):
        self.model = genai.GenerativeModel(model_name)
    
    def generate_document(self, template_path: str, case_details: dict, region: str = "Global") -> str:
        """
        Fills a legal template with specific case details using Gemini.
        """
        try:
            with open(template_path, 'r') as f:
                template_content = f.read()
        except FileNotFoundError:
            return f"Error: Template not found at {template_path}"

        prompt = f"""
        You are 'The Equalizer', a legal assistant.
        Fill in the following template with the provided case details.
        
        Rules:
        - The user is located in: {region}. Adjust legal terminology, laws referenced, and tone to match the legal standards of this region.
        - Replace placeholders (like [Name], [Date]) with the provided details.
        - Improve the [Explanation] section to sound professional and persuasive based on the 'User's Story'.
        - Keep the formatting formal.

        Template:
        {template_content}

        Case Details:
        {case_details}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error during document generation: {str(e)}"

# Example Usage
if __name__ == "__main__":
    engine = ActionEngine()
    details = {
        "Your Name": "John Doe",
        "Citation Number": "12345678",
        "Date of Citation": "2023-10-27",
        "User's Story": "I parked there because the sign was covered by a bush. I couldn't see the 'No Parking' rule."
    }
    # Assuming the template is in app/templates/parking_appeal_template.txt
    # Adjust path for testing if running from root
    import os
    path = os.path.join(os.getcwd(), 'app', 'templates', 'parking_appeal_template.txt')
    print("Generating Appeal Letter...")
    print(engine.generate_document(path, details))
