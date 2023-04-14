import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from PIL import Image
import numpy as np
import mysql.connector
import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie

#page title
st.set_page_config(
    page_title="solaria daschbored",
    page_icon= "💰",
    layout="wide"
)

logo =  Image.open("C:/Users/ihebt/OneDrive/Bureau/daschbored solaria/logo.png")
st.sidebar.success("select a page    :arrow_up:")
st.sidebar.image(logo)

#---------------music app------------------------------

audio_file = open('music.mp3', 'rb')
audio_bytes = audio_file.read()

st.sidebar.audio(audio_bytes, format='audio/ogg')

sample_rate = 44100  # 44100 samples per second
seconds = 2  # Note duration of 2 seconds
frequency_la = 440  # Our played note will be 440 Hz
# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
t = np.linspace(0, seconds, seconds * sample_rate, False)
# Generate a 440 Hz sine wave
note_la = np.sin(frequency_la * t * 2 * np.pi)



st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 70px; text-align: center;'>💰controle revenu</h1>", unsafe_allow_html=True)
#data from excel
cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
query1 = "SELECT * FROM `data_cr`"
df_r1 = pd.read_sql(query1, con=cnx)


#les donnes et les representation graphigue
st.markdown(f"<h1 style='color: rgb(255, 195, 0) ; font-size: 50px;'>1-controle des revenues:</h1>", unsafe_allow_html=True)
st.write("---------")


fig0 = px.line(df_r1, y = ["Revenue Hébergement","Autres revenues","Revenue restaurations"],x="Date arrives",width=1200,title="🌟CA total")

fig01 =px.bar(df_r1, y = "CA totale",x="marche tourestique",width=600,title="🌟CA total par marche")








import plotly.express as px
df = px.data.gapminder().query("year == 2007")
fig = px.scatter_geo(df, locations="iso_alpha",
                     color="continent", # which column to use to set the color of markers
                     hover_name="country", # column added to hover information
                     size="pop", # size of markers
                     projection="natural earth",
                     title="🌟les payes cible")


left_column, right_column = st.columns(2)
with right_column:
    st.write(fig01)
with left_column:
    st.write(fig) 

st.write(fig0)

st.write("-------------------------")
st.markdown(f"<h1 style='color: rgb(255, 195, 0) ;'>2-comptable clients:</h1>", unsafe_allow_html=True)


cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
query1 = "SELECT * FROM `recouvrement`"
df1 = pd.read_sql(query1, con=cnx)
query2 = "SELECT * FROM `solde clients`"
df2 = pd.read_sql(query2, con=cnx)

query3 = "SELECT * FROM `data_caisse`"
df_caisse = pd.read_sql(query3, con=cnx)

query4 = "SELECT * FROM `data_bq`"
df_BQ = pd.read_sql(query4, con=cnx)
solde_compte = df_BQ["debit"]-df_BQ["credit"]
df_BQ["solde compte"] = solde_compte






fig1 = px.bar(df1,x="Date d'échéance",y="montant réglé",width=600,title="🌟reglement clients par date d'échéance")
fig2 = px.bar(df2,x="nom clients",y="solde clients",title="🌟solde clients",width=600)


left_column, right_column = st.columns(2)
with right_column:
    st.write(fig1)

with left_column:
    st.write(fig2)


fig4 = px.pie(df1, values='Montant', names='Statut', 
        hole=.6,width=550, title='🌟facteur en retared vs autre')
fig4.update_traces(textposition='inside', textinfo='percent+label')

# Créer un nouveau DataFrame pour stocker les données fusionnées
df_merged = pd.DataFrame()

# Ajouter la colonne "solde clients" de df2 à df_merged
df_merged["solde clients"] = df2["solde clients"]

# Calculer la somme des colonnes "Revenue Hébergement" et "Revenue Restaurations" de df_r1
revenue_sum = df_r1["Revenue Hébergement"] + df_r1["Revenue restaurations"]

# Ajouter la colonne "revenue_sum" à df_merged
df_merged["revenue_sum"] = revenue_sum
df_merged["Date départ"] = df_r1["Date départ"]
fig5= px.scatter(df_merged,x="revenue_sum",y= "solde clients",width=600,title="🌟corrélation entre les ventes d'un hôtel et les comptes clients ")

tabl_cor =df_merged[["revenue_sum","solde clients"]].corr()


left_column, right_column = st.columns(2)
with right_column:
    st.write(fig5)
 

with left_column:
    st.write(fig4)





# Load your data into DataFrames: df_BIAT, df_BNA, df_caisse

# Créer un nouveau DataFrame pour stocker les données fusionnées
df_treso = pd.DataFrame()

# Calculer la somme des colonnes "solde compte" des trois DataFrames
# Rename the columns in each DataFrame
df_BQ = df_BQ.rename(columns={'solde compte': 'solde_bq'})
df_caisse = df_caisse.rename(columns={'solde de fin jours': 'solde_compte_caisse'})

# Concatenate the DataFrames
df_treso = pd.concat([df_BQ['solde_bq'], df_caisse['solde_compte_caisse']], axis=1)

# Ajouter la colonne "trésorerie" à df_treso en faisant la somme des colonnes
df_treso['trésorerie'] = df_treso.sum(axis=1)
#st.write(df_treso)
treso = df_treso['trésorerie'].sum()
# Calculer la variation de la trésorerie en fonction de la valeur précédente
delta = df_treso['trésorerie'].diff().iloc[-1]



solde_BQ = df_treso['solde_bq'].sum()
delta_BQ = df_treso['solde_bq'].diff().iloc[-1]



solde_caisse = df_treso['solde_compte_caisse'].sum()
delta_caisse = df_treso['solde_compte_caisse'].diff().iloc[-1]

st.write ("-----------------------------------------------------")

st.markdown(f"<h1 style='color: rgb(255, 195, 0) ;'>3-suivie de Trésorerie</h1>", unsafe_allow_html=True)

# Afficher la trésorerie sous forme de métrique dans Streamlit avec la couleur du delta appropriée
col1, col2, col3 = st.columns(3)
col1.metric(label='💶Trésorerie', value= treso, delta=delta, delta_color="normal")
col2.metric("🏦banque",solde_BQ, delta=delta_BQ, delta_color="normal")
col3.metric("🧾caisse",solde_caisse, delta=delta_caisse, delta_color="normal" )



