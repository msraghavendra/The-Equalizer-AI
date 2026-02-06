import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.risk_detector import RiskDetector
from app.core.simplifier import DocumentSimplifier

def test_phase1():
    print("Testing Phase 1 Modules...")
    
    # Test Risk Detector
    print("\n[Risk Detector]")
    detector = RiskDetector()
    sample_risk_text = "The service provider reserves the right to increase fees by 50% without prior notice."
    try:
        result = detector.analyze_document(sample_risk_text)
        print("Analysis Result:")
        print(result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"Risk Detector Error: {e}")

    # Test Simplifier
    print("\n[Simplifier]")
    simplifier = DocumentSimplifier()
    sample_complex_text = "The party of the first part shall herewith indemnify the party of the second part."
    try:
        result = simplifier.simplify_text(sample_complex_text)
        print("Simplification Result:")
        print(result[:100] + "..." if len(result) > 100 else result)
    except Exception as e:
        print(f"Simplifier Error: {e}")

if __name__ == "__main__":
    test_phase1()
