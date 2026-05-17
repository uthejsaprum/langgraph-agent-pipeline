from langchain_openai import ChatOpenAI   # from langchain_core import ChatOpenAI
llm=ChatOpenAI(model="gpt-5.5-2026-04-23")
# print(llm.invoke("i have created AWS ec2 instance through terraform cli now i want stop all 3 instance with terraform command how can i do that Note: i dont want to destroy them i just want to stop them").content)

from operator import itemgetter

from langchain_openai.chat_models import ChatOpenAI

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.runnables import (
    RunnableLambda,
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: list[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: list[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

# Here we use a global variable to store the chat message history.
# This will make it easier to inspect it to see the underlying results.
store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

history = get_by_session_id("1")
history.add_message(AIMessage(content="hello"))
# print(store)  # noqa: T201


from typing import Optional

# from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant who's good at {ability}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# chain = prompt | ChatOpenAI(model='gpt-5.4-mini-2026-03-17')

chain = prompt | llm


chain_with_history = RunnableWithMessageHistory(
    chain,
    # Uses the get_by_session_id function defined in the example
    # above.
    get_by_session_id,
    input_messages_key="question",
    history_messages_key="history",
)

# print(
#     chain_with_history.invoke(  # noqa: T201
#         {"ability": "math", "question": "What does cosine mean?"},
#         config={"configurable": {"session_id": "foo"}},
#     )
# )

# # Uses the store defined in the example above.
# print(store)  # noqa: T201

is_game_on=True

while is_game_on:
        question=input("please tell me how can I assist you !!!!\n")
        if question.lower()=='quit':
             is_game_on=False
        else:
                print("this is the response from system -------------------------------------------------------\n")
                print(
                chain_with_history.invoke(  # noqa: T201
                        {"ability": "math", "question": question},
                        config={"configurable": {"session_id": "foo"}},
                ).content
        )



# print(store)  # noqa: T201