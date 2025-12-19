import streamlit as st
from openai import OpenAI
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="L'Écho", page_icon="🧡")

# Cache le style par défaut (Menu et Footer)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- FONCTION INTELLIGENTE (CACHE) ---
# Cette fonction ne s'exécute qu'une fois par jour pour économiser
@st.cache_data(ttl=3600*24) 
def generer_pensee_du_jour(date_du_jour, api_key):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": "Génère une citation courte, inspirante et philosophique pour commencer la journée. Une seule phrase. Pas de guillemets."
            }]
        )
        return response.choices[0].message.content
    except:
        return "Chaque jour est une nouvelle chance."

# --- RÉCUPÉRATION DE LA CLÉ ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    # Fallback pour le mode local sans secrets
    api_key = st.sidebar.text_input("Clé API", type="password")

# --- AFFICHAGE DE LA PENSÉE ---
st.title("🧡 L'Écho")

if api_key:
    # On appelle la fonction avec la date d'aujourd'hui
    # Si on est le même jour, l'app ressortira la phrase en mémoire instantanément
    pensee = generer_pensee_du_jour(datetime.date.today(), api_key)
    st.header(f"✨ {pensee}")
else:
    st.subheader("Le miroir qui transforme ta journée.")

# --- ZONE JOURNAL ---
st.write("---") # Ligne de séparation
st.write("Comment te sens-tu aujourd'hui ?")
user_input = st.text_area("Ton espace", height=150, placeholder="Je me sens...")

if st.button("💌 Recevoir ma réponse"):
    if not api_key:
        st.warning("Clé manquante !")
    elif not user_input:
        st.warning("Le silence est d'or, mais j'ai besoin de mots pour t'aider.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('Je réfléchis à ta situation...'):
                prompt = f"""
                Agis comme un ami sage et bienveillant (L'Écho).
                L'utilisateur te dit : "{user_input}"
                1. Valide ses émotions.
                2. Donne une perspective positive ou stoïcienne.
                3. Sois bref (3 phrases max) et tutoie-le.
                """
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.success(response.choices[0].message.content)
                st.balloons()
        except Exception as e:
            st.error(f"Oups, une erreur : {e}")
