import streamlit as st
from openai import OpenAI
import datetime

# --- 1. CHOIX DE L'ICÔNE DU JOUR ---
liste_emojis = ["🧡", "🌟", "🌿", "☀️", "🌊", "🌸", "🕊️", "💎", "🔥", "🪐"]
jour_actuel = datetime.date.today().toordinal()
icone_du_jour = liste_emojis[jour_actuel % len(liste_emojis)]

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="L'Écho", page_icon=icone_du_jour)

# --- LE CODE "INVISIBLE" (MISE À JOUR) ---
# C'est ici que ça se joue : on cache la barre d'outils (Toolbar) et le bouton Deploy
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stToolbar"] {visibility: hidden !important;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- FONCTION INTELLIGENTE ---
@st.cache_data(ttl=3600*24) 
def generer_pensee_du_jour(date_du_jour, api_key):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": "Génère une citation courte, inspirante et philosophique pour commencer la journée. Une seule phrase."
            }]
        )
        return response.choices[0].message.content
    except:
        return "Chaque jour est une nouvelle chance."

# --- RÉCUPÉRATION CLÉ ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("Clé API", type="password")

# --- AFFICHAGE ---
st.title(f"{icone_du_jour} L'Écho")

if api_key:
    pensee = generer_pensee_du_jour(datetime.date.today(), api_key)
    st.header(f"✨ {pensee}")
else:
    st.subheader("Le miroir qui transforme ta journée.")

st.write("---") 

# --- JOURNAL ---
st.write("Comment te sens-tu aujourd'hui ?")
user_input = st.text_area("Ton espace", height=150, placeholder="Je me sens...")

if st.button("💌 Recevoir ma réponse"):
    if not api_key:
        st.warning("Je ne trouve pas la clé magique...")
    elif not user_input:
        st.warning("Le silence est d'or, mais j'ai besoin de mots.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('Analyse émotionnelle...'):
                prompt = f"""
                Agis comme un ami sage (L'Écho).
                L'utilisateur dit : "{user_input}"
                1. Analyse l'émotion.
                2. Choisis un emoji unique qui correspond le mieux à cette émotion.
                3. Commence ta réponse par cet emoji.
                4. Donne une réponse bienveillante et brève (3 phrases max).
                """
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.success(response.choices[0].message.content)
                st.balloons()
        except Exception as e:
            st.error(f"Erreur : {e}")
