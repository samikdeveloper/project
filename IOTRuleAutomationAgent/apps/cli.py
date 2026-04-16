from rule_automation.agent_graph import build_graph


if __name__ == "__main__":
    app = build_graph()

    print("Agent started. Type your commands.")
    while True:
        user_input = input("\nEnter your input in natural language (or type 'exit'): ")
        if user_input.lower() == "exit":
            break

        final_state = app.invoke({"user_input": user_input})
        print("\n--- Final Output ---")
        print(final_state.get("result", {}).get("message", "No message found"))
