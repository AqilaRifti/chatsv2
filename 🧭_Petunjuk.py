import sys
import streamlit as st
sys.path.append("")
# these three lines swap the stdlib sqlite3 lib with the pysqlite3 package
st.set_page_config(
    page_title="Petunjuk",
    page_icon="🧭",
)

st.write("# Selamat Datang! 👋")

st.markdown(
    """
    Asisten Pelajar Indonesia menyediakan berbagai AI untuk membantu para penggunanya dalam berbagai 
    urusan yang dihadapi.
    ### Nama AI dan kegunaannya:
    - ❓ Milarian Jawaban -> Cari jawaban dengan instan
    - 👩‍🏫 Siasat Ngajar -> Rancang strategi mengajar untuk guru
    - 💬 Hiji Ka Hiji -> AI untuk mengobrol dan menemani berbagai hal

    #### **👈 Langsung saja di coba** untuk melihat berbagai kemampuan API!
"""
)