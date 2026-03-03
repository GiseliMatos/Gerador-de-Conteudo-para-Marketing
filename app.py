#py -m pip install langchain langchain-community langchain-groq
#py -m pip install streamlit
#py -m pip install python-dotenvpy 
# py -m pip install streamlit

#python -m streamlit run app.py

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

id_model = "llama-3.3-70b-versatile"
llm = ChatGroq(
    model=id_model,
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def llm_generate(llm, prompt):
  template = ChatPromptTemplate.from_messages([
      ("system", "Você é um especialista em marketing digital com foco em SEO e escrita persuasiva."),
      ("human", "{prompt}"),
  ])

  chain = template | llm | StrOutputParser()

  res = chain.invoke({"prompt": prompt})
  return res

st.set_page_config(page_title = "Gerador de conteúdo 🤖", page_icon="🤖")
st.title("Gerador de conteúdo")

topic = st.text_input("Tema:", placeholder="Ex: saúde mental, alimentação saudável, prevenção, etc.")
platform = st.selectbox("Plataforma:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Tom:", ['Normal', 'Informativo', 'Inspirador', 'Urgente', 'Informal'])
length = st.selectbox("Tamanho:", ['Curto', 'Médio', 'Longo'])
audience = st.selectbox("Público-alvo:", ['Geral', 'Jovens adultos', 'Famílias', 'Idosos', 'Adolescentes'])
cta = st.text_input("Chamada para Ação (CTA):", placeholder="Ex: Clique para aproveitar a promoção!")
hashtags = st.checkbox("Retornar Hashtags")
keywords = st.text_area("Palavras-chave (SEO):", placeholder="Ex: bem-estar, medicina preventiva...")

if st.button("Gerar conteúdo"):
  prompt = f"""
  Escreva um texto com SEO otimizado sobre o tema '{topic}'.
  Retorne em sua resposta apenas o texto final e não inclua ela dentro de aspas.
  - Onde será publicado: {platform}.
  - Tom: {tone}.
  - Público-alvo: {audience}.
  - Comprimento: {length}.
  - {"Inclua ao final do texto esta chamada para ação:" + cta if cta else "Não inclua chamada para ação"}
  - {"Retorne ao final do texto hashtags relevantes." if hashtags else "Não inclua hashtags."}
  {"- Palavras-chave que devem estar presentes nesse texto (para SEO): " + keywords if keywords else ""}
  """
  try:
      res = llm_generate(llm, prompt)
      st.markdown(res)
  except Exception as e:
      st.error(f"Erro: {e}")