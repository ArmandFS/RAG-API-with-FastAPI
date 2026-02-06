import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_query(question, keyword):
    print(f"Testing: {question}")
    try:
        response = requests.post(f"{BASE_URL}/query", params={"q": question}, timeout=10)
        response.raise_for_status()
        
        answer = response.json().get("answer", "").lower()
        if keyword.lower() in answer:
            print(f"✅ Passed: Found '{keyword}'")
        else:
            print(f"❌ Failed: Keyword '{keyword}' not in answer: {answer}")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Connection Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_query("What is Kubernetes?", "container")
    test_query("What is NextWork?", "maximus")
    print("\n🚀 All semantic tests passed!")
