import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Analisis Sentimen Exhuma", layout="wide")

# =========================
# CSS MAROON THEME
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1a0000, #000000);
    color: white;
}
.big-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #800000;
}
.card {
    background: rgba(50, 0, 0, 0.7);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
.number {
    font-size: 35px;
    font-weight: bold;
}
.label {
    color: #ccc;
}
input, textarea {
    background-color: #330000 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("labeled_data.csv")

# =========================
# DETECT KOLOM SENTIMEN
# =========================
kolom = None
for c in df.columns:
    if "sentimen" in c.lower() or "label" in c.lower():
        kolom = c
        break

df[kolom] = df[kolom].astype(str).str.lower().str.strip()

# =========================
# MAPPING
# =========================
mapping = {}
for val in df[kolom].unique():
    if "pos" in val or val == '2':
        mapping[val] = 'positif'
    elif "neg" in val or val == '0':
        mapping[val] = 'negatif'
    elif "net" in val or val == '1':
        mapping[val] = 'netral'

df['sentimen_fix'] = df[kolom].map(mapping)

# =========================
# HITUNG
# =========================
total = len(df)
positif = (df['sentimen_fix']=='positif').sum()
negatif = (df['sentimen_fix']=='negatif').sum()
netral = (df['sentimen_fix']=='netral').sum()

# =========================
# TITLE
# =========================
st.markdown("""
<div class="big-title">
Analisis Sentimen Komentar Penonton terhadap Film Exhuma di YouTube
</div>
""", unsafe_allow_html=True)

# =========================
# INPUT USER
# =========================
st.markdown("## ✍️ Coba Analisis Komentar")

user_input = st.text_area("Masukkan komentar kamu:")

if st.button("Analisis"):
    if user_input.strip() == "":
        st.warning("Masukkan komentar dulu!")
    else:
        # sederhana (dummy prediction kalau model belum dipakai)
        if "bagus" in user_input.lower() or "keren" in user_input.lower():
            hasil = "Positif"
        elif "jelek" in user_input.lower() or "buruk" in user_input.lower():
            hasil = "Negatif"
        else:
            hasil = "Netral"

        st.success(f"Hasil Sentimen: {hasil}")

# =========================
# CARDS
# =========================
c1,c2,c3,c4 = st.columns(4)

c1.markdown(f"<div class='card'><div class='number'>{total}</div><div class='label'>Total</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><div class='number'>{positif}</div><div class='label'>Positif</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><div class='number'>{negatif}</div><div class='label'>Negatif</div></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='card'><div class='number'>{netral}</div><div class='label'>Netral</div></div>", unsafe_allow_html=True)

# =========================
# CHART
# =========================
data_chart = pd.DataFrame({
    'Sentimen':['Positif','Negatif','Netral'],
    'Jumlah':[positif,negatif,netral]
})

col1,col2 = st.columns(2)

with col1:
    fig = px.bar(data_chart,x='Sentimen',y='Jumlah',color='Sentimen',template="plotly_dark")
    st.plotly_chart(fig,use_container_width=True)

with col2:
    fig2 = px.pie(data_chart,names='Sentimen',values='Jumlah',hole=0.5,template="plotly_dark")
    st.plotly_chart(fig2,use_container_width=True)

# =========================
# WORDCLOUD
# =========================
st.markdown("## ☁️ WordCloud")

kolom_teks = None
for c in df.columns:
    if "clean" in c.lower() or "komentar" in c.lower():
        kolom_teks = c
        break

if kolom_teks:
    df[kolom_teks] = df[kolom_teks].astype(str)

    pos_text = " ".join(df[df['sentimen_fix']=='positif'][kolom_teks])
    neg_text = " ".join(df[df['sentimen_fix']=='negatif'][kolom_teks])
    net_text = " ".join(df[df['sentimen_fix']=='netral'][kolom_teks])

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("🟢 Positif")
        wc = WordCloud(background_color="black",colormap="Greens").generate(pos_text)
        st.image(wc.to_array())

    with col2:
        st.markdown("🔴 Negatif")
        wc = WordCloud(background_color="black",colormap="Reds").generate(neg_text)
        st.image(wc.to_array())

    with col3:
        st.markdown("🔵 Netral")
        wc = WordCloud(background_color="black",colormap="Blues").generate(net_text)
        st.image(wc.to_array())