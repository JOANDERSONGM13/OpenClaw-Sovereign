from brain import BrainRouter

def test_handshake():
    print("Testing Handshake58 (SN58) Consultant...")
    
    try:
        brain = BrainRouter()
        if not hasattr(brain, 'consult_specialist'):
            print("❌ BrainRouter missing 'consult_specialist' method.")
            return

        query = "detailed quantum mechanics derivation of schrodinger equation"
        print(f"Consulting on: {query}")
        
        response = brain.consult_specialist(query)
        print(f"\nResponse Received:\n{response}\n")
        
        if "SN58 Specialist Response" in response:
            print("✅ Handshake consultant is active and responding (Mock/Real).")
        else:
            print("❌ Invalid response format from Handshake.")
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    test_handshake()
