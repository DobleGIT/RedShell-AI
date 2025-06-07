import streamlit as st
import subprocess
import shlex
import os
import signal
from utils import get_command, get_full_chat_response

st.set_page_config(page_title="RedShell-AI", page_icon="🧠")
st.title("RedShell-AI")
st.markdown(
    """
    Bienvenido a **Exploit-Shell-AI**.  
    Este prototipo te permite interactuar con la terminal de Kali Linux a través de lenguaje natural usando ChatGPT.

    - Escribe instrucciones normales para chatear con el modelo.
    - Escribe instrucciones que comiencen con `!` para que se traduzcan en comandos de Kali y se ejecuten.

    **Ejemplos:**
    - `! escanea los puertos de scanme.nmap.org`
    - `! lanza un gobuster para encontrar directorios`
    - `¿Qué es una vulnerabilidad RCE?`

    ---
    """,
    unsafe_allow_html=True
)

# Init session state
if "history" not in st.session_state:
    st.session_state.history = []
if "process" not in st.session_state:
    st.session_state.process = None
if "output_buffer" not in st.session_state:
    st.session_state.output_buffer = ""

# Render history
for role, content in st.session_state.history:
    if role == "system":
        continue
    if role == "user":
        st.chat_message("user").write(content)
    else:
        if "\n" in content:
            st.chat_message("assistant").code(content, language="bash")
        else:
            st.chat_message("assistant").write(content)

# Input
prompt = st.chat_input("Escribe tu mensaje o un comando con '!'")

# Handle input
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.history.append(("user", prompt))

    if prompt.startswith("!"):
        instruction = prompt[1:].strip()
        command = get_command(instruction)
        exec_msg = f"Ejecutando comando: {command}"
        st.chat_message("assistant").write(exec_msg)
        st.session_state.history.append(("assistant", exec_msg))

        if st.session_state.process:
            try:
                pgid = os.getpgid(st.session_state.process.pid)
                os.killpg(pgid, signal.SIGTERM)
                os.killpg(pgid, signal.SIGKILL)
            except Exception:
                pass
            st.session_state.process = None

        args = shlex.split(command)
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            start_new_session=True
        )
        st.session_state.process = proc
        st.session_state.output_buffer = ""
        output_container = st.chat_message("assistant").empty()

        for line in proc.stdout:
            st.session_state.output_buffer += line
            output_container.code(st.session_state.output_buffer, language="bash")

        proc.stdout.close()
        proc.wait()
        st.session_state.process = None
        st.session_state.history.append(("assistant", st.session_state.output_buffer))

    else:
        history_for_llm = [
            {"role": role, "content": content}
            for role, content in st.session_state.history
        ]
        response = get_full_chat_response(prompt, history=history_for_llm)
        st.chat_message("assistant").write(response)
        st.session_state.history.append(("assistant", response))

# Stop button
if st.session_state.process:
    if st.button("Stop"):
        try:
            pgid = os.getpgid(st.session_state.process.pid)
            os.killpg(pgid, signal.SIGTERM)
            os.killpg(pgid, signal.SIGKILL)
        except Exception:
            pass
        st.session_state.process = None
