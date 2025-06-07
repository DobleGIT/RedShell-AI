from utils import get_command, run_command, get_full_chat_response

def main():
    print("RedShell-AI chat started. Type 'exit' to quit.\n")
    chat_history = []

    while True:
        try:
            user_input = input("You > ").strip()
            if user_input.lower() in ["exit", "salir", "quit"]:
                print("Exiting RedShell-AI...")
                break

            if user_input.startswith("!"):
                nl_instruction = user_input[1:].strip()
                command = get_command(nl_instruction)
                print(f"\n>>> Executing shell command:\n{command}\n")
                output = run_command(command)
                print()
                chat_history.append({"role": "user", "content": f"[EXEC] {command}"})
                chat_history.append({"role": "assistant", "content": output})
            else:
                chat_history.append({"role": "user", "content": user_input})
                response = get_full_chat_response(user_input, history=chat_history)
                print(f"\nLLM > {response}\n")

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}\n")

if __name__ == "__main__":
    main()
