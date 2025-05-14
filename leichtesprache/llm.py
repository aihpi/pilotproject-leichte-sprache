import logging, os
import requests, json
from urllib.parse import urljoin
from typing import List
from leichtesprache.parameters import LLMBASEURL, MODEL

logging.basicConfig(format=os.getenv("LOG_FORMAT", "%(asctime)s [%(levelname)s] %(message)s"))
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))

# ============== LLM (Ollama) =================================================


def llm_generate(
    prompt: str,
    model: str = MODEL,
    top_k: int = 2,
    top_p: float = 0.9,
    temp: float = 0.2,  # Parameterwerte angepasst (Stand 30.04.2025)
) -> str:
    url = urljoin(LLMBASEURL, "generate")
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temp, "top_p": top_p, "top_k": top_k},
    }

    try:
        r = requests.post(url, json=data)
        response_dic = json.loads(r.text)
        return response_dic.get("response", "")

    except Exception as e:
        logger.error(f"Exception: {e}")
        logger.debug(f"url:{url}")
        logger.debug(f"Request data:{data}")
        logger.debug(f"Response:{r}")


def list_local_models() -> List:

    url = urljoin(LLMBASEURL, "tags")

    try:
        r = requests.get(url)
        response_dic = json.loads(r.text)
        models_names = [model.get("name") for model in response_dic.get("models")]
        return models_names

    except Exception as e:
        logger.error(f"Exception: {e}\nResponse:{response_dic}")


if __name__ == "__main__":
    print("Local models:")
    print(list_local_models())
    print("\nQuick test of LLM")
    print("Model:", MODEL)
    prompt = "Hi, who are you and what can you do?"
    print("Prompt:", prompt)
    response = llm_generate(prompt)
    print("Response:")
    print(response)
