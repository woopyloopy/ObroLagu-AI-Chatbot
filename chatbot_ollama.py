import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from music_api import search_song

# PAGE CONFIG

st.set_page_config(
    page_title="🎧 ObroLagu",
    page_icon="🎵",
    layout="wide"
)

# CUSTOM CSS

st.markdown("""
<style>

.main > div{
    max-width:950px;
    margin:auto;
}

.block-container{
    padding-top:2rem;
}

h1{
    text-align:center;
}

[data-testid="stSidebar"]{
    background:#white;
}

[data-testid="stChatMessage"]{

    border-radius:15px;
    padding:15px;
    margin-bottom:12px;
    border:1px solid #2c2c2c;

}

.song-card{

    background:#181818;
    border-radius:15px;
    padding:15px;
    border:1px solid #303030;
    margin-bottom:10px;

}

.footer{

    text-align:center;
    color:gray;
    margin-top:30px;

}

</style>
""", unsafe_allow_html=True)

# SESSION

if "messages" not in st.session_state:

    st.session_state.messages=[]

    st.session_state.messages.append(

        SystemMessage("""

Kamu adalah ObroLagu.
Kamu adalah AI Music Assistant.
Tugasmu:
- Merekomendasikan lagu
- Merekomendasikan artist
- Merekomendasikan album
- Merekomendasikan playlist
- Menjelaskan genre musik
- Menjawab dalam Bahasa Indonesia
- Ramah
- Santai
- Gunakan data iTunes jika tersedia.

""")

    )

if "favorite_artist" not in st.session_state:

    st.session_state.favorite_artist="Belum ada"

if "mode" not in st.session_state:

    st.session_state.mode="🎵 Cari Lagu"

# SIDEBAR

with st.sidebar:

    st.title("🎧 ObroLagu")

    st.caption("Cari Rekomendasi Lagu Favoritmu")

    st.markdown("---")

    st.subheader("📂 Menu")

    if st.button(
        "🎵 Cari Lagu",
        use_container_width=True
    ):
        st.session_state.mode="🎵 Cari Lagu"

    if st.button(
        "🎤 Cari Artist",
        use_container_width=True
    ):
        st.session_state.mode="🎤 Cari Artist"

    if st.button(
        "💿 Cari Album",
        use_container_width=True
    ):
        st.session_state.mode="💿 Cari Album"

    if st.button(
        "😊 Playlist Mood",
        use_container_width=True
    ):
        st.session_state.mode="😊 Playlist Mood"

    st.markdown("---")
    st.success(
        f"Mode Aktif:\n\n{st.session_state.mode}"
    )

    st.markdown("---")
    temperature=st.slider(

        "Creativity",
        0.0,
        2.0,
        0.7

    )

    st.markdown("---")

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages=[]

        st.session_state.messages.append(

            SystemMessage("""
            Kamu adalah ObroLagu.
            Gunakan Bahasa Indonesia.
            Jawab dengan santai.

""")

        )

        st.rerun()


# HEADER
# WELCOME

if len(st.session_state.messages)==1:

   st.markdown(
"""
<div class="welcome-card">

<h2>👋 Selamat Datang!</h2>

<p>
Aku bisa membantu:
</p>

<p>
🎵 Cari Lagu<br>
🎤 Cari Artist<br>
💿 Cari Album<br>
😊 Playlist sesuai mood
</p>


<p>
<b>Contoh:</b><br>
• Lagu Coldplay<br>
• Lagu buat belajar<br>
• Lagu galau<br>
• Album Taylor Swift
</p>

</div>

""",

unsafe_allow_html=True
)

# DISPLAY CHAT
for message in st.session_state.messages:

    if isinstance(message,HumanMessage):

        with st.chat_message(
            "user",
            avatar="🙂"
        ):

            st.markdown(
                message.content
            )

    elif isinstance(message,AIMessage):

        with st.chat_message(
            "assistant",
            avatar="🎧"
        ):

            st.markdown(
                message.content
            )

# PLACEHOLDER INPUT

if st.session_state.mode=="🎵 Cari Lagu":

    placeholder="Contoh: Lagu Coldplay"

elif st.session_state.mode=="🎤 Cari Artist":

    placeholder="Contoh: Taylor Swift"

elif st.session_state.mode=="💿 Cari Album":

    placeholder="Contoh: Album Parachutes"

else:

    placeholder="Contoh: Lagu buat workout"

prompt=st.chat_input(placeholder)

# CHATBOT LOGIC

if prompt:

    # -------------------------------
    # Tampilkan pesan user
    # -------------------------------

    with st.chat_message(
        "user",
        avatar="🙂"
    ):
        st.markdown(prompt)

    st.session_state.messages.append(
        HumanMessage(prompt)
    )


    # Ollama

    llm = ChatOllama(
        model="llama3.2",
        temperature=temperature
    )

    with st.spinner("🎵 Sedang mencari rekomendasi..."):

        songs = []
        # Panggil iTunes API sesuai mode

        if st.session_state.mode in [
            "🎵 Cari Lagu",
            "🎤 Cari Artist",
            "💿 Cari Album"
        ]:

            songs = search_song(prompt)

        # Jika ada hasil iTunes
        if songs:

            st.markdown("## 🎵 Hasil Pencarian")

            context = ""

            for song in songs:

                st.markdown(f"""
<div class="song-card">

### 🎵 {song['track']}

👤 **Artist :** {song['artist']}
💿 **Album :** {song['album']}

</div>
""",
unsafe_allow_html=True)

                context += f"""

Lagu : {song['track']}
Artist : {song['artist']}
Album : {song['album']}

"""
            prompt_ai = f"""
Kamu adalah ObroLagu.
User bertanya:
{prompt}
Favorite Artist user:
{st.session_state.favorite_artist}
Berikut data lagu dari iTunes:
{context}
Gunakan data tersebut.
Jelaskan lagu-lagu tersebut.
Berikan rekomendasi artist lain yang mirip.
Berikan rekomendasi lagu lain.
Jawab menggunakan Bahasa Indonesia.
Gunakan bahasa santai.
Gunakan emoji secukupnya.
"""

            response = llm.invoke(
                st.session_state.messages +
                [HumanMessage(prompt_ai)]
            )

        # Playlist berdasarkan mood

        elif st.session_state.mode == "😊 Playlist Mood":

            mood_prompt = f"""

User meminta playlist.

Mood:

{prompt}
Favorite Artist:

{st.session_state.favorite_artist}
Berikan playlist sekitar 10 lagu.
Jelaskan alasan memilih lagu tersebut.
Jawab dalam Bahasa Indonesia.

"""

            response = llm.invoke(

                st.session_state.messages +

                [HumanMessage(mood_prompt)]

            )
        # Chat biasa

        else:

            response = llm.invoke(
                st.session_state.messages
            )

    result = response.content

    # Tampilkan jawaban AI

    with st.chat_message(
        "assistant",
        avatar="🎧"
    ):

        st.markdown(result)

    st.session_state.messages.append(
        AIMessage(result)
    )

# FOOTER

st.markdown("---")

st.markdown(
"""
<div class="footer">

🎧 <b>ObroLagu</b>

</div>
""",
unsafe_allow_html=True
)