
from assistant import TatchiAssistant


def main():
    # This initializes Tatchi's AI assistant.
    tatchi = TatchiAssistant()

    print("=" * 40)
    print("       TATCHI AI ASSISTANT")
    print("=" * 40)
    print("Tatchi is online.")
    print("Type 'quit' to exit.")
    print()

    # Keep Tatchi running until the user tells it to quit.
    while True:

        # Get the user's input.
        user_input = input("You: ")

        # Allow the user to shut Tatchi down.
        if user_input.lower() == "quit":
            print("Tatchi: Goodbye.")
            break

        try:

            # Ask Tatchi whether this information
            # is important enough to remember.

            if tatchi.should_remember(user_input):

                # Extract only the useful information
                # from the user's message.

                memory = tatchi.extract_memory(user_input)

                # Try to save the memory.
                # remember() returns True if it was saved
                # and False if it already exists.

                saved = tatchi.remember(memory)

                if saved:
                    print("Tatchi: I'll remember that.")
                else:
                    print("Tatchi: I already remember that.")

            # Send the user's message to Tatchi's AI brain.

            response = tatchi.ask(user_input)

            # Display Tatchi's response.
            print(f"Tatchi: {response}")
            print()

        except Exception as error:
            print(f"Tatchi Error: {error}")


if __name__ == "__main__":
    main()

