import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from PIL import Image
import numpy as np
from streamlit_lottie import st_lottie
import pandas as pd
from datetime import datetime, date
import mysql.connector
import time
import requests
import psycopg2




st.set_page_config(
    page_title="solaria daschbored",
    page_icon= "📦",
    layout="wide"
)


logo =  Image.open("logo.png")
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


#-----------------------------------------data from my postgredatabase---------------------------------------------------------------------------

cnx = psycopg2.connect("postgres://iheb:3oO6ZpxwsB3iKuwe1oqO2YaHIzMI9vyt@dpg-chgh7ou7avjbbjpn4h50-a.oregon-postgres.render.com/solaria")

# Query 1: data controle achats
query1 = "SELECT * FROM \"data controle achats\""
df_controle_achats = pd.read_sql(query1, con=cnx)

# Query 2: budget achats
query2 = "SELECT * FROM \"budget achats\""
df_controle_achats_budget = pd.read_sql(query2, con=cnx)

# Query 3: data compt fres
query3 = "SELECT * FROM \"data compt fres\""
df_compt_fres = pd.read_sql(query3, con=cnx)

# Query 4: charge personnel
query4 = "SELECT * FROM \"charge personnel\""
df_charge_personnel = pd.read_sql(query4, con=cnx)

# Query 5: budget charge personnel
query5 = "SELECT * FROM \"budget charge personnel\""
df_budget_charge_personnel = pd.read_sql(query5, con=cnx)

cnx.close()




#--------------------------------------------------------filtre les donnes----------------------------------------------------------

st.sidebar.write("--------------------")
st.sidebar.title("📆 donnes liee au controle achats")
df_controle_achats['date'] = pd.to_datetime(df_controle_achats['date'])
# Extract months and create a new column 'month_column'
df_controle_achats['month_column'] = df_controle_achats['date'].dt.month
df_controle_achats['years_column'] = df_controle_achats['date'].dt.year
years_df_controle_achats= st.sidebar.multiselect(
    "Select Year(s) for KPI",
    options=df_controle_achats["years_column"].unique(),  # Update column name here
    default=df_controle_achats["years_column"].unique(),
    key="years_df_achats")  # Update column name here
mois_df_controle_achats = st.sidebar.multiselect(
    "Select Month(s) for KPI",
    options=df_controle_achats["month_column"].unique(),
    default=df_controle_achats["month_column"].unique(),
    key="mois_df_achats")

# Apply filters to the DataFrame
df_controle_achats_filtres = df_controle_achats[(df_controle_achats["month_column"].isin(mois_df_controle_achats)) & (df_controle_achats["years_column"].isin(years_df_controle_achats))]  


st.sidebar.write("--------------------")
st.sidebar.title("📆 donnes liee au budget achats")
mois_controle_achats_budget = st.sidebar.multiselect(
    "choisire les mois pour les budget ",
    options=df_controle_achats_budget["Mois"].unique(),  # Update column name here
    default=df_controle_achats_budget["Mois"].unique(),
    key = "mois_df_controle achats budget")  # Update column name here


# Apply filters to the DataFrame
df_controle_achats_budget_filtre = df_controle_achats_budget[(df_controle_achats_budget["Mois"].isin(mois_controle_achats_budget))]


st.sidebar.write("--------------------")
st.sidebar.title("📆 donnes liee au charge personnel")

yeras_df_charge_personnel = st.sidebar.multiselect(
    "Select Year(s) for KPI",
    options = df_charge_personnel["Année"].unique(),  # Update column name here
    default=df_charge_personnel["Année"].unique(),
    key="years_df_charge personnel")  # Update column name here
mois_df_charge_personnel = st.sidebar.multiselect(
    "Select Month(s) for KPI",
    options=df_charge_personnel["Mois"].unique(),
    default=df_charge_personnel["Mois"].unique(),
    key="mois_df_vharge personnel")

# Apply filters to the DataFrame
df_charge_personnel_filtres = df_charge_personnel[(df_charge_personnel["Mois"].isin(mois_df_charge_personnel)) & (df_charge_personnel["Année"].isin(yeras_df_charge_personnel))]  # Update column name here


st.sidebar.write("--------------------")
st.sidebar.title("📆 donnes liee au budget de charge personnel")
mois_df_budget_charge_personnel = st.sidebar.multiselect(
    "choisire les mois pour les budget ",
    options=df_budget_charge_personnel["Mois"].unique(),  # Update column name here
    default=df_budget_charge_personnel["Mois"].unique(),
    key = "mois_df_budget_charge_personnel")  # Update column name here

# Apply filters to the DataFrame
df_budget_charge_personnel_filtre = df_budget_charge_personnel[(df_budget_charge_personnel["Mois"].isin(mois_controle_achats_budget))]



st.sidebar.write("--------------------")
st.sidebar.title("📆 comptable fournisseurs")
df_compt_fres['Date'] = pd.to_datetime(df_compt_fres['Date'])
# Extract months and create a new column 'month_column'
df_compt_fres['month_column'] = df_compt_fres['Date'].dt.month
df_compt_fres['years_column'] = df_compt_fres['Date'].dt.year
years = st.sidebar.multiselect(
    "Select Year(s) for KPI",
    options=df_compt_fres["years_column"].unique(),  # Update column name here
    default=df_compt_fres["years_column"].unique())  # Update column name here
mois = st.sidebar.multiselect(
    "Select Month(s) for KPI",
    options=df_compt_fres["month_column"].unique(),
    default=df_compt_fres["month_column"].unique())

# Apply filters to the DataFrame
df_compt_fres_filtres= df_compt_fres[(df_compt_fres["month_column"].isin(mois)) & (df_compt_fres["years_column"].isin(years))]  # Update column name here

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 70px; text-align: center;'> 📦controle couts </h1>", unsafe_allow_html=True)

#---------------------suivie d'achats---------------------------------------------
st.markdown(
    """
    <style>
    .title {
        color: rgb(255, 195, 0);
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>1-suivie d'achats</h1>", unsafe_allow_html=True)

st.markdown("----------------------------------------------------------------")

# Create the line plot
fig_les_achats = px.bar(df_controle_achats_filtres, x='date', y=['totale COUTS F&B', 'Cout energie', 'Produits de nettoyage', "Produits d'acceuil", 'Fourniture de bureau','achats techniques','consomation personnel'],width=600,barmode='group',title="🌟les charge d'achats par mois")

fig_les_budget_achats = px.bar(df_controle_achats_budget_filtre, x='Mois', y=["budget food & beverage","budget energie","budge nettoyage","budget d'acceuil","budget fourniture de bureau","budget achats techniques","budget personnel"], barmode='group',width=600,title="🌟les charge d'achats par mois")

col1,col2=st.columns(2)
with col1 :
     st.write(fig_les_achats)
with col2 :
     st.write(fig_les_budget_achats)


cols_to_sum1 = ['totale COUTS F&B', 'Cout energie', 'Produits de nettoyage', "Produits d'acceuil", 'Fourniture de bureau', 'achats techniques', 'consomation personnel']
df_controle_achats_filtres['total_charge'] = df_controle_achats_filtres[cols_to_sum1].sum(axis=1)
#st.write(df_controle_achats_filtres)

cols_to_sum2 = ["budget food & beverage","budget energie","budge nettoyage","budget d'acceuil","budget fourniture de bureau","budget achats techniques","budget personnel"]
df_controle_achats_budget_filtre['total_budget_charge_achats'] = df_controle_achats_budget_filtre[cols_to_sum2].sum(axis=1)

#st.write(df_controle_achats_budget_filtre)


df_merged = pd.DataFrame()
df_merged["total_charge_achats"] = df_controle_achats_filtres["total_charge"]
df_merged["total_budget_charge_achats"] = df_controle_achats_budget_filtre["total_budget_charge_achats"]
df_merged["ecarts"]=df_merged["total_budget_charge_achats"]-df_merged["total_charge_achats"]
#st.write(df_merged)

ECART_achats = df_merged["ecarts"].sum()
st.title("🌟Ecarts entre realisatiion et budget:")

if (ECART_achats <= 0):
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>✅{abs(ECART_achats)}</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>❌{abs(ECART_achats)}</h1>", unsafe_allow_html=True)

fig_charge_important =px.line(df_controle_achats_filtres,x="date",y=["achats techniques","Boisson","Nourriture","Water","Electricity","Fuel & Gas"],title="🌟suivie les charge les plus important",width=1200)
st.write(fig_charge_important)



#-----------------------------------GRH----------------------------------------------------------------------------------------------------------------

st.write("-----------------------------------------------------------------------------------")
st.markdown(f"<h1 style=' color: rgb(255, 195, 0) ;'>2-suivie des charges personnels :</h1>", unsafe_allow_html=True)

# histigrame couts salaires
total_charge_salarial_personnel = df_charge_personnel_filtres['salaires net'].sum()

fig = px.bar(df_charge_personnel_filtres, x="Mois", y='salaires net',
             color='Département', barmode='group',title="🌟charge personnel")

#histograme budget 

fig0 = px.bar(df_budget_charge_personnel_filtre, x="Mois", y='salaires net',
             barmode='group',title="🌟budget charge personnel",
             height=400)

fig3 = px.pie(df_charge_personnel_filtres, values='salaires net', names='Type de contrat', 
        hole=.6, title='🌟type de contrat ')
fig3.update_traces(textposition='inside', textinfo='percent+label')

fig4 = px.bar(df_charge_personnel_filtres, x="Sexe", y='salaires net',
             barmode='group',title="🌟charge personnel par sexe",color="Sexe",color_discrete_sequence=px.colors.qualitative.Dark2,
             height=400)

left_column, right_column , = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig0, use_container_width=True)
#ecatrs budget et realisation
total__budget_salarial_personnel  = df_budget_charge_personnel_filtre['salaires net'].sum()
ECART_RH = round(total__budget_salarial_personnel - total_charge_salarial_personnel,3)
st.title("🌟Ecarts entre realisatiion et budget:")

if (ECART_RH >= 0):
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>✅{abs(ECART_RH)}</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>❌{abs(ECART_RH)}</h1>", unsafe_allow_html=True)

left_column, right_column , = st.columns(2)
left_column.plotly_chart(fig3, use_container_width=True)
right_column.plotly_chart(fig4, use_container_width=True)

HD = df_charge_personnel_filtres["jours dus"].sum()
HT = df_charge_personnel_filtres["jours travaile"].sum()
taux_dabsence = 1-(HT/HD)
#st.title("Taux d'absentéisme par mois:")
#st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{taux_dabsence:.2%}</h1>", unsafe_allow_html=True)

EFFECTIF =  df_charge_personnel_filtres["Matricule"].count()
#st.title("effectif RH par mois:")
#st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{EFFECTIF}</h1>", unsafe_allow_html=True)

left_column, right_column = st.columns(2)
with left_column:
        st.title("🌟Effectif RH par Mois :")
        st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{EFFECTIF}</h1>", unsafe_allow_html=True)
with right_column:
    st.title("🌟Taux d'absentéisme :")
    st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'> {taux_dabsence:.2%}</h1>", unsafe_allow_html=True)

#-------------------------compt fres---------------------------------------------------------------------------------------

st.write("-----------------------------------------------------------------------------------")
st.markdown(f"<h1 style=' color: rgb(255, 195, 0) ;'>3-Suivi règlement des fournisseurs :</h1>", unsafe_allow_html=True)


fig5 = px.bar(df_compt_fres_filtres,x="Nom du fournisseur",y="reste du dettes",height=600,title="🌟solde par fres")

fig6 = px.line(df_compt_fres_filtres,x="Échéance",y="reste du dettes",height=450,title="🌟solde par date ")


left_column, right_column , = st.columns(2)
left_column.plotly_chart(fig5, use_container_width=True)
right_column.plotly_chart(fig6, use_container_width=True)

fig7 = px.pie(df_compt_fres_filtres, values='reste du dettes', names='etat de facture', 
        hole=.6,width=550, title='🌟facteur en retared vs autre')
fig7.update_traces(textposition='inside', textinfo='percent+label')



# convert date object to datetime object
today = datetime.combine(date.today(), datetime.min.time())

# convert string column to datetime object
df_compt_fres_filtres['Échéance'] = pd.to_datetime(df_compt_fres_filtres['Échéance']) 

# filter rows based on date comparison
prochaines_P = df_compt_fres_filtres[(df_compt_fres_filtres['Échéance'] >= today)&(df_compt_fres_filtres['reste du dettes']>0)]

# select columns "Numéro de facture" and "Nom du fournisseur"
prochaines_P_subset = prochaines_P[["Échéance", "Nom du fournisseur","reste du dettes"]]
prochaines_P_subset.sort_values(["reste du dettes"], inplace=True , ascending=False)


left_column, right_column = st.columns(2)
with left_column:
        st.markdown(f"<h1 style=' color: rgb(255, 255, 255); font-size: 15px;'>🌟les 10 prochaine reglement</h1>", unsafe_allow_html=True)
        st.write(prochaines_P_subset.head(10))
with right_column:
    st.write(fig7)

st.write("----------------------")


