import os
from dotenv import load_dotenv
from openai import OpenAI
from scanner_cv.search import search_context


def build_prompt(context, user_question):
    return f"""Dato il seguente contesto {context} rispondi alla domanda dell'utente {user_question}
spiegando che nel file individuato c'e' il profilo piu' adatto."""


def ask_assistant(user_question):
    load_dotenv(".env")
    openai_key = os.environ["OPENAI_API_KEY"]

    client = OpenAI(api_key=openai_key)

    context = search_context(user_question)
    prompt = build_prompt(context, user_question)

    completion = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {
                "role" : "system",
                "content" : "Sei un assistente HR, specializzato nella ricerca di profili professionali adatti a specifiche richieste. Rispondi in modo conciso e professionale."
            },
            {
                "role" : "user",
                "content" : prompt
            }
            
        ]
    )

    return completion.choices[0].message.content

def main():
    while True:
        user_question = input("Che profilo stai cercando? > ").strip()

        if not user_question:
            continue
        if user_question.lower() in ["exit", "quit" , "esci"]:
            break

        answer = ask_assistant(user_question)
        print(f"Risposta dell'assistente: {answer}\n")

if __name__ == "__main__":
    main()