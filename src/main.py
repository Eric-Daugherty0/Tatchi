from assistant import TatchiAssistant 

def main(): 
    # This is initializing the AI Tatchi (Building the robot)
    tatchi = TatchiAssistant()

    print("=" * 40)
    print("       Tatchi AI ASSISTANT")
    print("=" * 40)
    print("Tatchi is online.")
    print("Type 'quit' to exit.")
    print()

    # The statment to keep the robot running indefinitely until told to quit. 
    while True:
        # Storing the users input.
        user_input = input("You: ")

        if user_input.lower() == "quit":
            print("Tatchi: Goodbye.")
            break

        if user_input.lower().startswith("remember:"):
            memory = user_input[9:].strip()

            if memory:
                tatchi.remember(memory)
                print("Tatchi: I'll remember that.")
            else:
                print("Tatchi: What would you like me to remember?")

            print()
            continue

        try: 
            # The response that asks Tatchi the question.
            response = tatchi.ask(user_input)
            print(f"Tatchi: {response}")
            print()

        except Exception as error:
            print(f"Tatchi Error: {error}")

if __name__ == "__main__":
    main()