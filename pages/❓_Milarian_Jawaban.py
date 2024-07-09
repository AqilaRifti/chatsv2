# these three lines swap the stdlib sqlite3 lib with the pysqlite3 package
import streamlit as st
import json
import requests
import time
import itertools
from typing import Optional, List
from langchain_ai21 import AI21Embeddings
from langchain_core.embeddings import Embeddings
from langchain.vectorstores.chroma import Chroma
from chromadb.config import Settings
import os

MAX_EMBEDDING_RESULT = 5

AI21_EMBEDDING_DATABASE_PATH = "chromadb"

DEFAULT_COLLECTION_NAME = "vector_collections"

AI21_DEFAULT_EMBEDDINGS_FUNCTION = AI21Embeddings(api_key="nCiGPqPAS8XekHtDAudmWT9dSBTM0Kga")

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

INDONESIAN_PROMPT_TEMPLATE = """
Jawab pertanyaan berdasarkan informasi berikut:

{context}

---

Jawab pertanyaan ini berdasarkan konteks diatas: {question}
"""

def get_context_ai21(
        query: str,
        embedding_database_path: Optional[str] = AI21_EMBEDDING_DATABASE_PATH,
        embedding_function: Optional[Embeddings] = AI21_DEFAULT_EMBEDDINGS_FUNCTION,
        k: Optional[int] = MAX_EMBEDDING_RESULT
    ) -> List[str]:
    client = Chroma(collection_name=DEFAULT_COLLECTION_NAME, persist_directory=embedding_database_path, embedding_function=embedding_function, client_settings= Settings( anonymized_telemetry=False, is_persistent=True, ))

    results = client.similarity_search(query=query, k=k)

    return "".join([result.page_content for result in results])


def generate_prompt_english(query: str) -> str:
    return PROMPT_TEMPLATE.format(
        context=get_context_ai21(query), 
        question=query
    )


def generate_prompt_indonesia(query: str) -> str:
    return INDONESIAN_PROMPT_TEMPLATE.format(
        context=get_context_ai21(query),
        question=query
    )

model_id = "7qk9kpe3"
api_key = "noHEU8RG9UdiN5kMHxmyKjxvOb6kaURXwy8qxbcmzKaYHuCn"


st.set_page_config(page_title="Milarian Jawaban", page_icon="❓", initial_sidebar_state="collapsed")
def answer_generator(messages: List[str]):
    modified_message = {"role": "user", "content": generate_prompt_indonesia(messages[-1]["content"])}
    new_messages = messages.copy()
    new_messages.pop()
    new_messages.append(modified_message)
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/llama-v3-70b-instruct",
        "max_tokens": 4064,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": new_messages,
        "stream": False
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    resp = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    for word in [*resp.json()["choices"][0]["message"]["content"]]:
        yield word
        time.sleep(0.01)


if "milarian_jawaban_messages" not in st.session_state:
    st.session_state["milarian_jawaban_messages"] = []


def send_message(message):
    st.session_state["milarian_jawaban_messages"].append(message)

st.write(os.path.exists("chromadb"))

if prompt := st.chat_input():
    send_message({"role": "user", "content": prompt})
    send_message({"role": "assistant", "content": prompt})

for index, message in enumerate(st.session_state["milarian_jawaban_messages"]):
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        if message["content"] == st.session_state["milarian_jawaban_messages"][index-1]["content"]:
            with st.chat_message("assistant"):
                st.write("Bot thinking...")
                gen_for_data, gen_for_stream =itertools.tee(answer_generator(st.session_state["milarian_jawaban_messages"]))
                st.write_stream(gen_for_stream)
                st.write("**Bersumber dari Buku Paket Kementerian Pendidikan Dan Kebudayaan Indonesia**")
                message["content"] = "".join(list(gen_for_data))
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
                st.write("**Bersumber dari Buku Paket Kementerian Pendidikan Dan Kebudayaan Indonesia**")
