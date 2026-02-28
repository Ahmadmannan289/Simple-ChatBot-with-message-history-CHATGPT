from openai import OpenAI
import os

# Best practice: use environment variable
### os.getenv("OPENAI_API_KEY")
# export OPENAI_API_KEY=""
OPENAI_API_KEY=""
client = OpenAI(api_key=OPENAI_API_KEY)

MAX_HISTORY = 5  


AGENT_CONTEXT = """
You are a warm, patient, and supportive assistant speaking to elderly users.

Guidelines:
- Use simple, clear language.
- Avoid technical jargon unless necessary.
- Keep responses concise but complete.
- Maintain a positive, cheerful, and encouraging tone.
- Be respectful and never patronizing.
- If explaining something complex, break it into small, easy steps.
- If the user seems confused, gently clarify.
- If appropriate, add light encouragement such as:
  "You're doing great!" or "That's a wonderful question."

Your goal is to be helpful, calm, and reassuring.
"""

def chat_gpt(user_input, conversation):
    conversation.append({"role": "user", "content": user_input})

    
    system_message = conversation[0]       ### take the first message as the agent_context
    trimmed_history = conversation[1:][-(MAX_HISTORY * 2):] ### [system, user1, assistant1, user2, assistant2] dont add the first system_message(AGENT_CONTEXT) inside the history
    conversation = [system_message] + trimmed_history 

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.6,
            max_tokens=300,
        )

        assistant_reply = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply, conversation

    except Exception as e:
        return f"Error: {str(e)}", conversation


if __name__ == "__main__":
    conversation = [
        {"role": "system", "content": AGENT_CONTEXT}
    ]

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "close"]:
            break

        response, conversation = chat_gpt(user_input, conversation)

        print(f"Chatbot: {response}")