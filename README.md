# RedShell-AI

RedShell-AI is a personal prototype project where I experimented with integrating ChatGPT with the Kali Linux terminal. It's designed to help automate and streamline penetration testing tasks using natural language instructions.

You can interact with the assistant either from the **terminal** or via a simple **web interface** (built with Streamlit).

<iframe width="560" height="315" src="https://www.youtube.com/embed/o0WdLFRJ2Cs" frameborder="0" allowfullscreen></iframe>


## Features

- Translate natural language instructions into Kali Linux commands using ChatGPT.
- Execute commands and see their real-time output (especially useful for tools like `nmap`, `gobuster`, `nikto`, etc.).
- Maintain conversation history for context.
- Available in both CLI and web versions.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/DobleGIT/RedShell-AI.git
cd RedShell-AI
```

2. Create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your OpenAI API key:
   - Create a `.env` file in the root directory.
   - Add this line (replace with your actual key):

```
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME = "gpt-4o"
```

5. Run the terminal version:

```bash
python3 main.py
```

6. Run the web version:

```bash
streamlit run app.py
```

## Notes

- **Warning:** This tool does not include command filtering or restrictions. It will run whatever the LLM generates. For example, commands like `sudo rm -rf /` would be executed if allowed by the system.


## License

MIT License.