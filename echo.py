import streamlit as st
from openai import OpenAI
import datetime

# --- 1. CONFIGURATION ET CŒURS ---
liste_coeurs = ["🧡", "❤️", "💖", "💗", "💓", "💝", "🤍", "❤️‍🔥", "💟"]
jour_actuel = datetime.date.today().toordinal()
coeur_du_jour = liste_coeurs[jour_actuel % len(liste_coeurs)]

# Changement du nom dans l'onglet du navigateur
st.set_page_config(page_title="L'Écho de ton Coeur", page_icon=coeur_du_jour)

# --- 2. LE STYLE (CSS) ---
hide_streamlit_style = """
            <style>
            /* Cache les menus techniques */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stToolbar"] {display: none !important;}
            .stDeployButton {display: none !important;}
            [data-testid="stDecoration"] {display: none !important;}
            [data-testid="stStatusWidget"] {display: none !important;}

            /* REMONTER LE CONTENU */
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 1rem !important;
            }

            /* LE TITRE */
            h1 {
                font-size: 2.5rem !important; /* Taille un peu plus grosse (14 approx) */
                margin-bottom: 0rem !important;
                line-height: 1.2 !important; /* Évite que les lignes se touchent trop si ça passe sur 2 lignes */
            }

            /* LA CITATION */
            h2 {
                font-size: 1.2rem !important; 
                font-weight: 400 !important;
                margin-top: 0.5rem !important;
            }
            
            /* AJUSTEMENT MARGES */
            .stMarkdown {
                margin-bottom: -10px;
            }
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
                "content": "Génère une citation courte, inspirante et philosophique pour commencer la journée. Une seule phrase. Pas de guillemets."
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

# --- 5. AFFICHAGE DU NOUVEAU TITRE ---
st.title(f"{coeur_du_jour} L'Écho de ton coeur")

if api_key:
    pensee = generer_pensee_du_jour(datetime.date.today(), api_key)
    st.header(f"✨ {pensee}")
else:
    st.subheader("Le miroir qui transforme ta journée.")

st.write("---") 

# --- 6. JOURNAL ---
user_input = st.text_area("Ton espace", height=120, placeholder="Comment te sens-tu aujourd'hui ? Écris-le ici...")

if st.button("💌 Recevoir ma réponse"):
    if not api_key:
        st.warning("Clé manquante...")
    elif not user_input:
        st.warning("J'ai besoin de mots pour t'aider.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('...'):
                prompt = f"""
                Agis comme un ami sage (L'Écho).
                L'utilisateur dit : "{user_input}"
                1. Analyse l'émotion.
                2. Choisis un emoji qui correspond.
                3. Commence ta réponse par cet emoji.
                4. Réponds avec bienveillance (3 phrases max).
                """
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.success(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Erreur : {e}")

