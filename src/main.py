import sys
from src.chatbot import Chatbot

def main():
    print("Initializing Chatbot...")
    bot = Chatbot()
    print("Chatbot: Hello! I am ready to chat. Type 'exit' to end the conversation.")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            result = bot.process_input(user_input)
            
            # Tier 2 Output
            print(f" -> Sentiment: {result['sentiment']['label']} (Score: {result['sentiment']['score']:.2f})")
            print(f"Chatbot: {result['response']}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

    # Tier 1 Output
    print("\n--- Conversation Ended ---")
    summary = bot.get_conversation_summary()
    print(f"Overall conversation sentiment: {summary['label']}")
    print(f"Trend: {summary['trend']}")
    print(f"Average Score: {summary['score']:.2f}")

if __name__ == "__main__":
    main()
