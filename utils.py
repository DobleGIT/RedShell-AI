import subprocess
import re
import sys
from config import LLM_PROVIDER

if LLM_PROVIDER == "openai":
    from llm.openai_llm import get_response_from_history
# elif LLM_PROVIDER == "ollama":
#     from llm.ollama_llm import get_response_from_history  # future

def run_command(command: str) -> str:
    # Execute shell command with real-time output
    buffer = []
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    for line in process.stdout:
        print(line, end="")
        buffer.append(line)
    process.stdout.close()
    process.wait()
    return "".join(buffer).strip()

def clean_code_fences(text: str) -> str:
    # Remove markdown code blocks or inline backticks
    fence_pattern = re.compile(r"```(?:bash)?\s*([\s\S]*?)\s*```", re.IGNORECASE)
    match = fence_pattern.search(text)
    if match:
        return match.group(1).strip()
    simple_pattern = re.compile(r"`([^`]+)`")
    match2 = simple_pattern.search(text)
    if match2:
        return match2.group(1).strip()
    return text.strip()

def get_command(user_input: str) -> str:
    # Convert NL instruction into a valid shell command
    prompt = f"""Convierte la siguiente instrucción en un comando válido de Kali Linux.
    Solo responde con el comando. No expliques nada.

    Instrucción: {user_input}"""
    response = get_response_from_history([{"role": "user", "content": prompt}])
    return clean_code_fences(response)

def get_full_chat_response(user_input: str, history=None) -> str:
    # Get full LLM reply with updated context
    if history is None:
        history = []
    history.append({"role": "user", "content": user_input})
    response = get_response_from_history(history)
    history.append({"role": "assistant", "content": response})
    return response.strip()
