import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class VoiceInterface:
    def __init__(self, model_name="gemini-3-flash-preview"):
        self.model = genai.GenerativeModel(model_name)

    def translate_to_mother_tongue(self, text: str, target_language: str) -> str:
        """
        Translates the simple advice into the user's mother tongue, maintaining empathy.
        """
        prompt = f"""
        You are 'The Equalizer', an empathetic rights advocate.
        Translate the following advice into {target_language}.
        
        Rules:
        - Keep the tone helpful, clear, and reassuring.
        - Ensure legal terms are explained or translated accurately for a layperson.
        - Do not lose the meaning of the advice.
        - STRICTLY NO MARKDOWN or formatting (no bold **, no italics *). Plain text only.
        - Keep the advice concise and suitable for listening (speech-friendly).

        Advice to Translate:
        {text}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error during translation: {str(e)}"

    def simulate_audio_input(self, audio_file_path: str) -> str:
        """
        Mock function for STT (Speech-to-Text).
        In production, this would use Google Cloud STT or OpenAI Whisper.
        """
        return "Simulated STT: This is a placeholder for transcribed text from " + audio_file_path

    def simulate_audio_output(self, text: str, target_language: str) -> str:
        """
        Mock function for TTS (Text-to-Speech).
        In production, this would use ElevenLabs or Google Cloud TTS.
        """
        return f"Simulated Audio generated for '{text}' in {target_language}"

# Example Usage
if __name__ == "__main__":
    voice = VoiceInterface()
    advice = "You have the right to dispute this fee within 30 days."
    print("Translating to Spanish...")
    print(voice.translate_to_mother_tongue(advice, "Spanish"))
