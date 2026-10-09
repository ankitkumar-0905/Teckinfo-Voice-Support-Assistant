
import requests

API_URL = "http://127.0.0.1:8000/ask"


def ask_rag(question: str) -> str:
    """Send a text question to the RAG API and return its answer."""

    response = requests.post(
        API_URL,
        json={"question": question},
        timeout=180
    )

    response.raise_for_status()
    data = response.json()

    return data["answer"]


if __name__ == "__main__":
    question = input("Enter your question: ")
    answer = ask_rag(question)

    print("\nRAG Answer:")
    print(answer)