import streamlit as st
import requests

# URL del backend FastAPI
BACKEND_URL = "http://127.0.0.1:5000/menu"
#BACKEND_URL = "https://menu-mensa-elis.onrender.com/menu"

# Funzione per ottenere il menù dal back-end
def ottieni_menu():
    try:
        risposta = requests.get(BACKEND_URL)
        if risposta.status_code == 200:
            return risposta.json()
        else:
            return [{"nome": "Impossibile ottenere il menù dal server!"}]
    except requests.exceptions.RequestException:
        return [{"nome": "Back-end non disponibile!"}]

# Stile della pagina
st.set_page_config(page_title="Menù del Giorno", page_icon="🍽️", layout="centered")
st.markdown(
    """
    <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
        }
        .dish-name {
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF;
        }
        .ingredients {
            font-size: 14px;
            color: #AAAAAA;
        }
        .alert-red {
            color: #FF0000;
            font-weight: bold;
        }
        .alert-green {
            color: #00FF00;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🍽️ Menù del Giorno")

# Mostra il menù
menu = ottieni_menu()

for categoria in menu:
    st.header(categoria["categoria"])

    for piatto in categoria["pietanze"]:
        st.markdown(f"<div class='dish-name'>- {piatto['nome']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='ingredients'>({piatto['ingredienti']})</div>", unsafe_allow_html=True)

        # Indicazioni per lattosio e glutine
        if piatto["contiene_lattosio"]:
            st.markdown(f"<div class='alert-red'>⚠ Contiene Lattosio</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-green'>✔ Senza Lattosio</div>", unsafe_allow_html=True)

        if piatto["contiene_glutine"]:
            st.markdown(f"<div class='alert-red'>⚠ Contiene Glutine</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-green'>✔ Senza Glutine</div>", unsafe_allow_html=True)

        st.write("---")  # Separatore tra i piatti
