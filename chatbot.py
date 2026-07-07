"""
Exercise 3: CLI Chatbot
A conversational chatbot with history, commands, and error handling.
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv
import google.api_core.exceptions

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("API Key =", api_key)

genai.configure(api_key=api_key)

# Create model with system prompt
model = genai.GenerativeModel(
    'gemini-3.1-flash-lite',
    system_instruction="You are a helpful and friendly assistant. "
    "Keep your responses concise and engaging. "
    "If you don't know something, say so honestly.",
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        max_output_tokens=500,
        top_p=0.95
    )
)

# Start chat session with history
chat = model.start_chat(history=[])


def print_help():
    """Display available commands."""
    print("\n" + "=" * 50)
    print("🤖 Available Commands:")
    print("  /exit    - Exit the chatbot")
    print("  /clear   - Clear conversation history")
    print("  /help    - Show this help message")
    print("  /history - Show conversation summary")
    print("=" * 50)


def clear_history():
    """Clear the chat history."""
    global chat
    chat = model.start_chat(history=[])
    print("\n🧹 Conversation history cleared!")


def show_history():
    """Show a summary of the conversation history."""
    if not chat.history:
        print("\n📭 No conversation history yet.")
        return
    
    print(f"\n📋 Conversation History ({len(chat.history)} messages):")
    for msg in chat.history:
        role = "You" if msg.role == "user" else "AI"
        # Show first 50 chars of each message
        preview = msg.parts[0].text[:50] + "..." if len(msg.parts[0].text) > 50 else msg.parts[0].text
        print(f"  {role}: {preview}")


def main():
    """Main chatbot loop."""
    print("\n" + "=" * 60)
    print("🤖  AI CLI CHATBOT")
    print("=" * 60)
    print("Type your message or type /help for commands")
    print("=" * 60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Handle commands
            if user_input.lower() == "/exit":
                print("\n🤖 AI: Goodbye! Have a great day! 👋")
                break
            
            elif user_input.lower() == "/help":
                print_help()
                continue
            
            elif user_input.lower() == "/clear":
                clear_history()
                continue
            
            elif user_input.lower() == "/history":
                show_history()
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Send message to AI
            print("\n🤖 AI is thinking...", end="", flush=True)
            response = chat.send_message(user_input)
            print("\r", end="")  # Clear the "thinking" message
            
            # Display response
            print(f"\n🤖 AI: {response.text}")
            
            # Show token usage (optional info)
            if response.usage_metadata:
                total = response.usage_metadata.total_token_count
                print(f"\n   ── Tokens used this turn: {total} ──")
        
        except google.api_core.exceptions.PermissionDenied:
            print("\n❌ Error: Invalid API key. Check your .env file.")
            break
        
        except google.api_core.exceptions.ResourceExhausted:
            print("\n❌ Error: Rate limit reached. Please wait 60 seconds.")
            print("   Tip: You can also try a different model like 'gemini-1.5-flash'")
        
        except google.api_core.exceptions.InvalidArgument as e:
            print(f"\n❌ Error: Invalid argument - {e}")
            print("   Tip: Check the model name in the code")
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("   Tip: Check your internet connection and try again")


if __name__ == "__main__":
    main()