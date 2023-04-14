import streamlit as st
import pandas as pd 
import plotly_express as px
from PIL import Image
import numpy as np 
import mysql.connector
import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie


st.set_page_config(
    page_title="solaria daschbored",
    page_icon= "🏩",
    layout="wide"
)

#https://assets10.lottiefiles.com/packages/lf20_yKGuIT.json

st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 100px; text-align: center;'>-🌞solaria KPI-</h1>", unsafe_allow_html=True)

logo =  Image.open("C:/Users/ihebt/OneDrive/Bureau/daschbored solaria/logo.png")
st.sidebar.success("select a page    :arrow_up:")

st.sidebar.image(logo)
#____________music-app___________________

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


#data from my sql
cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
query = "SELECT * FROM Data_CR"
df0 = pd.read_sql(query, con=cnx)


cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
query_p_r = "SELECT * FROM prevision_revenue"
df0_revznue_prev = pd.read_sql(query_p_r, con=cnx)


# Convert 'date_column' to datetime type
df0['Date arrives'] = pd.to_datetime(df0['Date arrives'])

# Extract months and create a new column 'month_column'
df0['month_column'] = df0['Date arrives'].dt.month
df0['years_column'] = df0['Date arrives'].dt.year



years = st.sidebar.multiselect(
    "Select Year(s) for KPI",
    options=df0["years_column"].unique(),  # Update column name here
    default=df0["years_column"].unique())  # Update column name here



mois = st.sidebar.multiselect(
    "Select Month(s) for KPI",
    options=df0["month_column"].unique(),
    default=df0["month_column"].unique())

# Apply filters to the DataFrame
df = df0[(df0["month_column"].isin(mois)) & (df0["years_column"].isin(years))]  # Update column name here



#---------------------------------------
st.markdown("<h1 style=' color: rgb(255, 195, 0); font-size: 50px; text-align: center;'>📊 les indicateur de performance de l'hôtellerie</h1>", unsafe_allow_html=True)

st.write("-----------------")
st.markdown("<h1 style=' font-size: 40px;color:rgb(255,69,0);'>🛌 l'activite hebergement</h1>", unsafe_allow_html=True)




# Calcul du taux d'occupation
NBch = df['Chambre réservée'].sum()
NBch_dispo = 239
taux_docupation = (NBch/NBch_dispo)*100
taux_docupation = round(taux_docupation, 2) # Arrondir à 2 décimales

df["taux d'ocupation"] = taux_docupation


fig = px.line(df, x='Date arrives', y="taux d'ocupation", symbol="taux d'ocupation",width=600,title="🎯taux d'ocupation")

revenu_moyen_chambre = df["CA totale"]/df["Chambre réservée"]
df["revenu moyen chambre"] = revenu_moyen_chambre
fig11 = px.bar(df, y="revenu moyen chambre", x="Date arrives", title="🎯revenu moyen chambre")



left_column, right_column = st.columns(2)
with right_column:
    st.write(fig)
    with st.expander("🔑explexation"):
         st.write("""

    """)
with left_column:
    st.write(fig11)

    with st.expander("🔑explexation"):
       st.write("""
. 
    """)


fig4 = px.area(df, y = "CA totale",x="Date arrives",width=1100,title="🎯CA total")

st.write(fig4)
with st.expander("🔑explexation"):
       st.write("""
 
    """)




REVPAR = df["Revenue Hébergement"]/239
df["REVPAR"] = REVPAR

LADR = df["Revenue Hébergement"]/df["Chambre réservée"]
df["L'ADR"]= LADR

fig2 = px.bar(df, y=["REVPAR", "L'ADR", "CA totale"], x="Date arrives",barmode='group', title="🎯REVPAR L'ADR  CA totale")




# Génération du diagramme en anneau
fig3 = px.pie(df, values='CA totale', names='manier de reservation', 
        hole=.6,width=600 ,title='🌟source de reservation')





left_column, right_column = st.columns(2)
with right_column:
    st.write(fig3)
    with st.expander("🔑explexation"):
         st.write("""

    """)
with left_column:
    st.write(fig2)

    with st.expander("🔑explexation"):
       st.write("""

    """)


nb_arrives = df['nombre de voyageurs'].sum()
nb_nuites = df['Nombre nuits'].sum()
duree_moyenne = round(nb_nuites/nb_arrives,3)






left_column, right_column,col3= st.columns(3)
with left_column:
        st.markdown("<h1 style=' font-size: 30px;'>🎯duree moyenne de se jour:</h1>", unsafe_allow_html=True)
        st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{duree_moyenne}</h1>", unsafe_allow_html=True)
        with st.expander("🔑explexation"):
         st.write("""

    """)
  
with right_column:
        st.markdown("<h1 style=' font-size: 30px;'>🎯Taux de la realisation financiere</h1>", unsafe_allow_html=True)
        #st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{realisation_financiere}</h1>", unsafe_allow_html=True)

with col3:
     st.markdown("<h1 style=' font-size: 30px;'>🎯le taux de reduction</h1>", unsafe_allow_html=True)


  
     
    
st.write("---------------------")

st.markdown("<h1 style=' font-size: 40px;color:rgb(255,69,0);'>🍴  l'activite restauration</h1>", unsafe_allow_html=True)



#data from my sql
cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
query_r_restauration = "SELECT * FROM `data revenue restauration`"
df_r_restauration = pd.read_sql(query_r_restauration, con=cnx)



nombre_de_repas = df_r_restauration["Nombre repas servie"].sum()
taux_remplissage = nombre_de_repas/(300*3*360)


ca_restauration = df_r_restauration["Revenue restaurations"].sum()
nombre_de_couvert_servis = df_r_restauration["Nombre de couvert servis"].sum()
ticket_moyen = ca_restauration/nombre_de_couvert_servis


nb_chaise = 300 
taux_occupation_chaise = nombre_de_couvert_servis/nb_chaise




col1,col2,col3 =st.columns(3)
with col1:
     st.markdown("<h1 style=' font-size: 30px;'>🎯le taux de remplissage</h1>", unsafe_allow_html=True) 
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{taux_remplissage:.2%}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)


with col2:
     st.markdown("<h1 style=' font-size: 30px;'>🎯le ticket moyen</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{ticket_moyen:.2%}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)

with col3:
     st.markdown("<h1 style=' font-size: 30px;'>🎯le taux d'occupation de la chaise par jour</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{taux_occupation_chaise:.2%}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)










st.markdown("<h1 style='  color: rgb(255, 195, 0); font-size: 50px; text-align: center;'>📊 les indicateur de performance liee aux couts</h1>", unsafe_allow_html=True)
st.write("------------------")
st.markdown("<h1 style=' font-size: 40px;color:rgb(255,69,0);'>🛌 l'activite hebergement</h1>", unsafe_allow_html=True)



cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
query_personnel = "SELECT * FROM `charge personnel`"
df_personnel = pd.read_sql(query_personnel, con=cnx)

nb_salaries = df_personnel["Matricule"].count()
rendement_employe= round(NBch/nb_salaries,3)

df_salaries_etage = df_personnel[df_personnel.Département=="Etage"]
nb_salaries_etage = df_salaries_etage["Département"].count()

Rendement_etage = NBch / nb_salaries_etage

col1,col2 =st.columns(2)
with col1:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Rendement par employe</h1>", unsafe_allow_html=True) 
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{rendement_employe}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)

with col2:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Rendement au service etage</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{Rendement_etage}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)







st.markdown("<h1 style=' font-size: 40px;color:rgb(255,69,0);'>🍴  l'activite restauration</h1>", unsafe_allow_html=True)









col1,col2 =st.columns(2)
with col1:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Le cout nourriture</h1>", unsafe_allow_html=True) 
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{rendement_employe}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)

with col2:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Le cout boisson</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{Rendement_etage}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)
       


col1,col2 =st.columns(2)
with col1:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Le cout matiere</h1>", unsafe_allow_html=True) 
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{rendement_employe}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)

with col2:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Efficacite du personnel</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{Rendement_etage}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""

    """)      











st.write("--------------------------")
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_url_hello = "https://assets6.lottiefiles.com/packages/lf20_yjrdpceb.json"
lottie = load_lottieurl(lottie_url_hello)
#https://assets9.lottiefiles.com/packages/lf20_3kP2u2B3WC.json
#https://assets9.lottiefiles.com/private_files/lf30_ghysqmiq.json
#https://assets10.lottiefiles.com/packages/lf20_qpsnmykx.json
# Use the URL as the key for the first widget




left_column, right_column = st.columns(2)
with left_column:
    st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 20px;'>🔸realise par :</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(255, 255, 255); font-size: 20px; : ;'>iheb turki & wael barhoumi</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 20px;'>🔸encadre par :</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(255, 255, 255); font-size: 20px; : ;'>M.saloua banie</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 20px; : ;'>🔸entrprise d'aceuil </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(255, 255, 255); font-size: 20px; : ;'>Medina Solaria And Thalasso</h1>", unsafe_allow_html=True)

    
with right_column:
    # Use a different key for the second widget
    st_lottie(lottie, key=None,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=400,
        width=700,
    )

