import re

class ComplianceManager:
    def __init__(self):
        # Basic patterns for demonstration. 
        # In production, use more robust libraries like Microsoft Presidio.
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b'
        }

    def redact_pii(self, text: str) -> str:
        """
        Redacts Personally Identifiable Information (PII) from the text.
        """
        redacted_text = text
        for pii_type, pattern in self.patterns.items():
            redacted_text = re.sub(pattern, f"[REDACTED {pii_type.upper()}]", redacted_text)
        
        return redacted_text

# Example Usage
if __name__ == "__main__":
    compliance = ComplianceManager()
    sample_text = "Contact me at 555-123-4567 or john.doe@example.com."
    print("Redacting PII...")
    print(compliance.redact_pii(sample_text))
