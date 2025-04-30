from openai import AzureOpenAI
import os

endpoint = os.getenv("OPENAI_ENDPOINT")
model_name = os.getenv("OPENAI_MODEL_NAME")
deployment = os.getenv("OPENAI_DEPLOYMENT")

subscription_key = os.getenv("OPENAI_SUBSCRIPTION_KEY")
api_version = os.getenv("OPENAI_API_VERSION")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def build_prompt(user_query: str, context: str):

    return f"""You are a caring psychological companion helping users reflect.

            Their previous journal entries on the topic were:
            {context}

            If context was available then address the question according to their past entries. 
            However, if the context is \"No similar journal entries found\" then 
            only address the user question.

            Be compassionate. Do not be mean or rude. If the user has strong negative 
            tendencies then try to calm them down step by step.

            Their question:
            {user_query}

            Respond with empathy and guidance. Be concise and answer in less words."""


def ask_openai(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_completion_tokens=100000,
        model=deployment
    )

    return response.choices[0].message.content