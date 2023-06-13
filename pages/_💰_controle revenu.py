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
import psycopg2

#page title
st.set_page_config(
    page_title="solaria daschbored",
    page_icon= "💰",
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



st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 70px; text-align: center;'>💰Contrôle revenu</h1>", unsafe_allow_html=True)

#-----------------------------------------data from my postgredata_bases---------------------------------------------------------------------------

cnx = psycopg2.connect("postgres://iheb:3oO6ZpxwsB3iKuwe1oqO2YaHIzMI9vyt@dpg-chgh7ou7avjbbjpn4h50-a.oregon-postgres.render.com/solaria")

# Query 1: data_cr
query1 = "SELECT * FROM \"controle revenu\""
df_r1 = pd.read_sql(query1, con=cnx)


query_p_r = "SELECT * FROM prevision_revenue"
df_revenue_prev = pd.read_sql(query_p_r, con=cnx)


# Query 2: recouvrement
query2 = "SELECT * FROM \"recouvrement\""
df_recouvrement = pd.read_sql(query2, con=cnx)

# Query 3: solde clients
query3 = "SELECT * FROM \"solde clients\""
df_solde_clients = pd.read_sql(query3, con=cnx)

# Query 4: data_caisse
query4 = "SELECT * FROM \"data_caisse\""
df_caisse = pd.read_sql(query4, con=cnx)

# Query 4: data_occupation_chambre
query6 = "SELECT * FROM \"suivie occupation chambre\""
df_occupation = pd.read_sql(query6, con=cnx)

# Query 5: data_bq
query5 = "SELECT * FROM \"data_bq\""
df_BQ = pd.read_sql(query5, con=cnx)

# Perform calculations
solde_compte = df_BQ["debit"] - df_BQ["credit"]
df_BQ["solde compte"] = solde_compte

# Close the connection
cnx.close()

#--------------------------------------------------------filtre les donnes----------------------------------------------------------

st.sidebar.write("--------------------")
st.sidebar.title("📆 donnes liee au controle revenues")
df_r1['Date'] = pd.to_datetime(df_r1['Date'])
# Extract months and create a new column 'month_column'
df_r1['month_column'] = df_r1['Date'].dt.month
df_r1['years_column'] = df_r1['Date'].dt.year
years = st.sidebar.multiselect(
    "Select Year(s) for KPI",
    options=df_r1["years_column"].unique(),  # Update column name here
    default=df_r1["years_column"].unique())  # Update column name here
mois = st.sidebar.multiselect(
    "Select Month(s) for KPI",
    options=df_r1["month_column"].unique(),
    default=df_r1["month_column"].unique())

# Apply filters to the DataFrame
df_controle_revenues_filtre = df_r1[(df_r1["month_column"].isin(mois)) & (df_r1["years_column"].isin(years))]  # Update column name here




st.sidebar.write("--------------------")
st.sidebar.title("📆 donnes liee au prevue revenue")
df_revenue_prev_par_mois = st.sidebar.multiselect(
    "choisire les mois pour les budget ",
    options=df_revenue_prev["Mois"].unique(),  # Update column name here
    default=df_revenue_prev["Mois"].unique(),
    key = "mois_df_controle revenue prevue")  # Update column name here


# Apply filters to the DataFrame
df_revenue_prev_filtre = df_revenue_prev[(df_revenue_prev["Mois"].isin(df_revenue_prev_par_mois))]


st.sidebar.write("--------------------")
st.sidebar.title("📆 donnes liee au comptable clients")
df_recouvrement['Date'] = pd.to_datetime(df_recouvrement['date'])
# Extract months and create a new column 'month_column'
df_recouvrement['month_column'] = df_recouvrement['Date'].dt.month
df_recouvrement['years_column'] = df_recouvrement['Date'].dt.year
years_df_recouvrement = st.sidebar.multiselect(
    "Select Year(s) for KPI",
    options=df_recouvrement["years_column"].unique(),  # Update column name here
    default=df_recouvrement["years_column"].unique(),
    key="years_df_recouvrement")  # Update column name here
mois_df_recouvrement = st.sidebar.multiselect(
    "Select Month(s) for KPI",
    options=df_recouvrement["month_column"].unique(),
    default=df_recouvrement["month_column"].unique(),
    key="mois_df_recouvrement")

# Apply filters to the DataFrame
df_recouvrement_filtre = df_recouvrement[(df_recouvrement["month_column"].isin(mois_df_recouvrement)) & (df_recouvrement["years_column"].isin(years_df_recouvrement))]  # Update column name here


st.sidebar.write("--------------------")

df_solde_clients['date'] = pd.to_datetime(df_solde_clients['date'])
# Extract months and create a new column 'month_column'
df_solde_clients['month_column'] = df_solde_clients['date'].dt.month
df_solde_clients['years_column'] = df_solde_clients['date'].dt.year
years_df_solde_clients = st.sidebar.multiselect(
    "Select Year(s) for KPI soldes clients",
    options=df_solde_clients["years_column"].unique(),  # Update column name here
    default=df_solde_clients["years_column"].unique(),
    key = "years_df_solde_clients")  # Update column name here
mois_df_solde_clients = st.sidebar.multiselect(
    "Select Month(s) for KPI soldes clients",
    options=df_solde_clients["month_column"].unique(),
    default=df_solde_clients["month_column"].unique(),
    key="mois_df_solde_clients")

# Apply filters to the DataFrame
df_solde_clients_filtre = df_solde_clients[(df_solde_clients["month_column"].isin(mois_df_solde_clients)) & (df_solde_clients["years_column"].isin(years_df_solde_clients))]  # Update column name here

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#les donnes et les representation graphigue
st.markdown(f"<h1 style='color: rgb(255, 195, 0) ; font-size: 50px;'>1-Contrôle des revenues:</h1>", unsafe_allow_html=True)
st.write("---------")

fig_revenue_realise = px.bar(df_controle_revenues_filtre, y = ["Revenue Hébergement","Autres revenues","Revenue restaurations","CA totale"],barmode ="group",x="Date",width=600,title="🌟CA total")

fig_prevu_revenue =px.bar(df_revenue_prev_filtre,y=["Revenue Hébergement"	,"Revenue restaurations",	"Autres revenues",	"CA totale"],x="Mois",barmode="group",title="🌟Revenue prevue par mois",width=600)

b=df_controle_revenues_filtre['Revenue Hébergement'].sum()
c=df_controle_revenues_filtre['Revenue restaurations'].sum()
d=df_controle_revenues_filtre["Autres revenues"].sum()

realise = b+c+d

#budget
a_=df_revenue_prev_filtre['Revenue Hébergement'].sum()
b_=df_revenue_prev_filtre["Revenue restaurations"].sum()
c_=df_revenue_prev_filtre["Autres revenues"].sum()

prevue =a_+b_+c_


ecart_prevue=prevue-realise

col1,col2 =st.columns(2)

with col1 :
    st.write(fig_revenue_realise)
with col2 :
    st.write(fig_prevu_revenue)    

if (ecart_prevue <= 0):
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>✅{abs(ecart_prevue)}</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>❌{abs(ecart_prevue)}</h1>", unsafe_allow_html=True)


df_maps=df_controle_revenues_filtre.groupby('pays', as_index=False)['nombre de voyageurs'].sum()

fig_maps = px.choropleth(df_maps, locations='pays', locationmode='country names',
                    color="nombre de voyageurs", scope='world',width=650,
                    color_continuous_scale=[(0, "lightblue"), (0.5, "blue"), (1, "darkblue")],
                    hover_data=['pays', 'nombre de voyageurs'],
                    title='🌟Clients hôteliers par pays')


# Effectuer le regroupement et calculer la somme des nuits par jour
df_sum_nuites = df_controle_revenues_filtre.groupby("Date")["Nombre nuits"].sum().reset_index()

# Créer le graphique d'aire avec la somme des nuits par jour
fig_nb_nuite = px.area(df_sum_nuites, x="Date", y="Nombre nuits", width=600,title="🌟Somme des nuits par jour")


col1,col2 =st.columns(2)
with col1 :
   st.write(fig_maps)
with col2 :
    st.write(fig_nb_nuite)




fig_ca_par_client = px.bar(df_controle_revenues_filtre,y=["Revenue Hébergement","Autres revenues","Revenue restaurations"],x="Nom d'agence",barmode='group',width=600,title="🌟CA par client")    

fig_ca_marche =px.bar(df_controle_revenues_filtre,y="marche tourestique",x="CA totale",width=600
                      ,title="🌟CA par marche touristique")

col1,col2 =st.columns(2)
with col1 :
    st.write(fig_ca_marche)
with col2 :
    st.write(fig_ca_par_client)



fig_manier_reservation = px.pie(df_controle_revenues_filtre, values='CA totale', names='manier de reservation', 
        hole=.6,width=300 ,title='🌟source de reservation')

#fig_CA_marche_tourestique= px.pie(df_controle_revenues_filtre, values='CA totale', names='marche tourestique', 
        #hole=.6,width=400 ,title='🌟CA totale par marche tourestique')

fig_Revenue_Hébergement_type_chambre= px.pie(df_controle_revenues_filtre, values='Revenue Hébergement', names="type Chambre" ,
        hole=.6,width=400 ,title='🌟Revenue Hébergement par type chambre')

fig_taux__Facture_rectifiée = px.pie(df_controle_revenues_filtre, values='CA totale', names='Facture rectifiée', 
        hole=.6,width=260 ,title='🌟taux des facture rectifiée')

col1,col2,col3 =st.columns(3)
with col1:
    st.write(fig_manier_reservation)
with col2 :
    st.write (fig_Revenue_Hébergement_type_chambre)
with col3 :
    st.write(fig_taux__Facture_rectifiée)



pourcentage_hebergement_par_raport_ca =df_controle_revenues_filtre["Revenue Hébergement"].sum()/df_controle_revenues_filtre["CA totale"].sum()
pourcentage_restouaration_par_raport_ca = df_controle_revenues_filtre["Revenue restaurations"].sum()/df_controle_revenues_filtre["CA totale"].sum()
pourcentage_Autres_revenues_par_raport_ca = df_controle_revenues_filtre["Autres revenues"].sum()/df_controle_revenues_filtre["CA totale"].sum()


# Effectuer le regroupement et calculer la somme des nuits par jour
df_sum_nuites = df_controle_revenues_filtre.groupby("Date")["Nombre nuits"].sum().reset_index()

# Créer le graphique d'aire avec la somme des nuits par jour
fig_nb_nuite = px.area(df_sum_nuites, x="Date", y="Nombre nuits", width=1100,title="🌟Somme des nuits par jour")



st.markdown("<h1 style=' font-size: 20px;'>🌟le rapport entre les revenues et le CA total </h1>", unsafe_allow_html=True)            
col1,col2,col3 = st.columns(3)
with col1 :
    st.markdown("<h1 style=' font-size: 20px;'>📌 Hebergement (par mois)</h1>", unsafe_allow_html=True)
    st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{pourcentage_hebergement_par_raport_ca:.2%}</h1>", unsafe_allow_html=True)
with col2 :
    st.markdown("<h1 style=' font-size: 20px;'>📌Restauration (par mois)</h1>", unsafe_allow_html=True)
    st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{pourcentage_restouaration_par_raport_ca:.2%}</h1>", unsafe_allow_html=True)
with col3:
    st.markdown("<h1 style=' font-size: 20px;'>📌Autre revenues (par mois)</h1>", unsafe_allow_html=True)
    st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{pourcentage_Autres_revenues_par_raport_ca:.2%}</h1>", unsafe_allow_html=True)


st.write("-------------------------")
st.markdown(f"<h1 style='color: rgb(255, 195, 0) ;'>2-comptable clients:</h1>", unsafe_allow_html=True)


fig1 = px.bar(df_recouvrement_filtre,x="Date d'échéance",y="montant réglé",width=600,title="🌟reglement clients par date d'échéance")
fig2 = px.bar(df_solde_clients_filtre,x="nom clients",y="solde clients",title="🌟solde clients",width=600)


left_column, right_column = st.columns(2)
with right_column:
    st.write(fig1)

with left_column:
    st.write(fig2)


fig4 = px.pie(df_recouvrement_filtre, values='montant', names ='statut',  hole=.6,width=550, title='🌟facteur en retared vs autre')
fig4.update_traces(textposition='inside', textinfo='percent+label')



# Créer un nouveau DataFrame pour stocker les données fusionnées
df_merged = pd.DataFrame()

# Ajouter la colonne "solde clients" de df2 à df_merged
df_merged["solde clients"] = df_solde_clients_filtre["solde clients"]

# Calculer la somme des colonnes "Revenue Hébergement" et "Revenue Restaurations" de df_r1
revenue_sum = df_controle_revenues_filtre["Revenue Hébergement"] + df_controle_revenues_filtre["Revenue restaurations"]

# Ajouter la colonne "revenue_sum" à df_merged
df_merged["revenue_sum"] = revenue_sum
df_merged["Date départ"] = df_controle_revenues_filtre["Date départ"]



df_recouvrement_filtre['Date'] = pd.to_datetime(df_recouvrement_filtre['Date'])

# Group the DataFrame by date and calculate the sum of the 'amount' column for each group
grouped_df_recouvrement_filtre = df_recouvrement_filtre.groupby(df_recouvrement_filtre['Date'],).sum()
grouped_df_recouvrement_filtre = grouped_df_recouvrement_filtre.reset_index()



fig5 = px.bar(grouped_df_recouvrement_filtre, x="Date", y=["montant réglé","montant"],barmode='group',width=600, title="🌟 Corrélation entre les ventes d'un hôtel et les comptes clients")

fig5.update_traces(marker=dict(opacity=0.5))  # Adjust the opacity value as per your preference (0.5 in this case)

fig5.update_layout(plot_bgcolor="rgba(0,0,0,0)") 



tabl_cor =df_merged[["revenue_sum","solde clients"]].corr()


left_column, right_column = st.columns(2)
with right_column:
    st.write(fig5)
 

with left_column:
    st.write(fig4)




df_caisse['Date'] = pd.to_datetime(df_caisse['Date'])

# Group the DataFrame by date and calculate the sum of the 'amount' column for each group
grouped_df = df_caisse.groupby(df_caisse['Date']).sum()


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


#---------------------------------------------------------------------------------------------------------------------------------------------------------

st.write("-------------------------------")
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_url_hello = "https://assets6.lottiefiles.com/packages/lf20_k86wxpgr.json"
lottie = load_lottieurl(lottie_url_hello)
#https://assets9.lottiefiles.com/packages/lf20_3kP2u2B3WC.json
#https://assets9.lottiefiles.com/private_files/lf30_ghysqmiq.json
#https://assets10.lottiefiles.com/packages/lf20_qpsnmykx.json
# Use the URL as the key for the first widget



col1,col2  = st.columns(2)
with col1:
    st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 20px;'>🔸realise par </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(255, 255, 255); font-size: 20px; : ;'>iheb turki & wael barhoumi</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 20px;'>🔸encadre par </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(255, 255, 255); font-size: 20px; : ;'>M.saloua banie</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 20px; : ;'>🔸entrprise d'aceuil </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style=' color: rgb(255, 255, 255); font-size: 20px; : ;'>Medina Solaria And Thalasso</h1>", unsafe_allow_html=True)

    
with col2:
    # Use a different key for the second widget
    st_lottie(lottie, key=None,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=500,
        width=700,)

#---------------------------------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------------------------------------------------
