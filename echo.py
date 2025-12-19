import streamlit as st
from openai import OpenAI
import datetime

# --- 1. CONFIGURATION ET PALETTE DE CŒURS ---
# On remplace les objets par une variété de cœurs
liste_coeurs = ["🧡", "❤️", "💖", "💗", "💓", "💝", "🤍", "❤️‍🔥", "💟"]
jour_actuel = datetime.date.today().toordinal()

# Le cœur change chaque jour, mais reste toujours un cœur
coeur_du_jour = liste_coeurs[jour_actuel % len(liste_coeurs)]

st.set_page_config(page_title="L'Écho", page_icon=coeur_du_jour)

# --- 2. LE CODE INVISIBLE (NETTOYAGE) ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stToolbar"] {display: none !important;}
            .stDeployButton {display: none !important;}
            [data-testid="stDecoration"] {display: none !important;}
            [data-testid="stStatusWidget"] {display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3. FONCTION IA ---
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

# --- 4. CLÉ API ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("Clé API", type="password")

# --- 5. AFFICHAGE PRINCIPAL ---
# On affiche le cœur du jour en grand
st.title(f"{coeur_du_jour} L'Écho")

if api_key:
    pensee = generer_pensee_du_jour(datetime.date.today(), api_key)
    st.header(f"✨ {pensee}")
else:
    st.subheader("Le miroir qui transforme ta journée.")

st.write("---") 

# --- 6. JOURNAL INTELLIGENT ---
st.write("Comment te sens-tu aujourd'hui ?")
user_input = st.text_area("Ton espace", height=150, placeholder="Je me sens...")

# C'est ici que l'icône va changer selon l'humeur DANS la réponse
if st.button("💌 Recevoir ma réponse"):
    if not api_key:
        st.warning("Clé manquante...")
    elif not user_input:
        st.warning("Le silence est d'or, mais j'ai besoin de mots.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('Je t\'écoute...'):
                prompt = f"""
                Agis comme un ami sage (L'Écho).
                L'utilisateur dit : "{user_input}"
                1. Analyse l'émotion.
                2. Choisis un emoji qui correspond (par exemple 🌤️ si espoir, 🌧️ si triste, 🎉 si joie).
                3. Commence ta réponse par cet emoji.
                4. Réponds avec bienveillance (3 phrases max).
                """
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                # On affiche la réponse
                st.success(response.choices[0].message.content)
                st.balloons()
        except Exception as e:
            st.error(f"Erreur : {e}")
