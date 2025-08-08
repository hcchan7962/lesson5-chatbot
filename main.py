from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import httpx
import os
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()

model = OpenAIModel(
    'openai/gpt-oss-20b:free',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # http_client=httpx.AsyncClient(verify=False)
    ),
)

simple_agent = Agent(
    model=model,
    # 'Be concise, reply with one sentence.' is enough for some models (like openai) to use
    # the below tools appropriately, but others like anthropic and gemini require a bit more direction.
    system_prompt=("""
    You are a secretary, helping users to plan their schedule.
    always ask users to confirm
    """        
    ),
)

@cl.on_chat_start
def on_start():
    cl.user_session.set("agent", simple_agent)

# on message need to do something
@cl.on_message  # decorator
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    response = agent.run_sync(message.content)
    await cl.Message(content=response.output).send()


# response = simple_agent.run_sync("What is today's date?")
# print(response.output)