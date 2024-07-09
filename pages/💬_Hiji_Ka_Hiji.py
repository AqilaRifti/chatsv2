import streamlit as st
import json
import requests
import time
import itertools

model_id = "7qk9kpe3"
api_key = "noHEU8RG9UdiN5kMHxmyKjxvOb6kaURXwy8qxbcmzKaYHuCn"
st.set_page_config(page_title="Hiji Ka Hiji", page_icon="💬", initial_sidebar_state="collapsed")

def vertex_generator(messages: str):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/mixtral-8x22b-instruct",
        "max_tokens": 1000,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [{"role": "user", "content": "Kamu adalah seorang teman yang akan menemani dan membantu saya mulai dari sekarang"}, {"role": "assistant", "content": "Baik saya akan menjadi temanmu, ada yang bisa saya bantu?"}, *messages],
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


if "hiji_ka_hiji_messages" not in st.session_state:
    st.session_state["hiji_ka_hiji_messages"] = []


def send_message(message):
    st.session_state["hiji_ka_hiji_messages"].append(message)



if prompt := st.chat_input():
    send_message({"role": "user", "content": prompt})
    send_message({"role": "assistant", "content": prompt})

for index, message in enumerate(st.session_state["hiji_ka_hiji_messages"]):
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        if message["content"] == st.session_state["hiji_ka_hiji_messages"][index-1]["content"]:
            with st.chat_message("assistant"):
                st.write("Bot thinking...")
                gen_for_data, gen_for_stream =itertools.tee(vertex_generator(st.session_state["hiji_ka_hiji_messages"]))
                st.write_stream(gen_for_stream)
                message["content"] = "".join(list(gen_for_data))
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])