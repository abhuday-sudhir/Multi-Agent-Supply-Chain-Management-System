import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm():
    """
    Get LLM configured for Google Gemini.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Create a .env file (see .env.example) and set GEMINI_API_KEY."
        )

    # ChatGoogleGenerativeAI reads the API key from `GOOGLE_API_KEY` by default.
    # We set it here so users can keep a project-specific `GEMINI_API_KEY`.
    os.environ.setdefault("GOOGLE_API_KEY", api_key)

    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        temperature=0.0,
    )


def verify_tracing():
    """Verify LangSmith tracing is configured correctly."""
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    api_key = os.getenv("LANGCHAIN_API_KEY")
    project = os.getenv("LANGCHAIN_PROJECT", "default")
    
    if tracing_enabled and api_key:
        print(f"✓ LangSmith tracing enabled")
        print(f"  Project: {project}")
        print(f"  Endpoint: {os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')}")
        return True
    else:
        print("⚠ LangSmith tracing disabled")
        return False
