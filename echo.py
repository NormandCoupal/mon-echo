import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="L'Écho", page_icon="🧡")

st.title("🧡 L'Écho")
st.subheader("Le miroir qui transforme ta journée en force.")

# 1. On cherche la clé dans le coffre-fort (Secrets)
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    # Si on ne la trouve pas (ex: sur ton ordi), on la demande
    with st.sidebar:
        api_key = st.text_input("Clé API OpenAI", type="password")

st.write("Raconte-moi ta journée...")
user_input = st.text_area("Journal", height=150)

if st.button("✨ Recevoir ma dose d'amour"):
    if not api_key:
        st.warning("Je n'ai pas trouvé la Clé magique !")
    elif not user_input:
        st.warning("Écris quelque chose d'abord !")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('Analyse en cours...'):
                prompt = f"""
                Agis comme une IA bienveillante nommée L'Écho.
                Analyse ceci : "{user_input}"
                Transforme le négatif en positif. Valide les émotions.
                Réponds à la 2ème personne ("Tu..."). Sois bref et touchant.
                """
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.success(response.choices[0].message.content)
                st.balloons()
        except Exception as e:
            st.error(f"Erreur : {e}")
