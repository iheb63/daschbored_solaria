import streamlit as st
import pandas as pd 
import plotly.express as px
import PIL
from PIL import Image
import numpy as np 
import mysql.connector
import time
import requests
import streamlit as st
from streamlit_lottie import st_lottie

import psycopg2


st.set_page_config(
    page_title="solaria daschbored",
    page_icon= "🏩",
    layout="wide"
)



st.markdown("<h1 style=' color: rgb(0, 255, 255); font-size: 100px; text-align: center;'>-🌞solaria KPI-</h1>", unsafe_allow_html=True)

logo =  Image.open("logo.png")
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


#-----------------------------------------data from my sql---------------------------------------------------------------------------
#data-control revenues
# data CR
#cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
#query = "SELECT * FROM Data_CR"
#df0 = pd.read_sql(query, con=cnx)
#cnx.close()

# data CR postgre
# Establish a connection to PostgreSQL
cnx = psycopg2.connect("postgres://iheb:3oO6ZpxwsB3iKuwe1oqO2YaHIzMI9vyt@dpg-chgh7ou7avjbbjpn4h50-a.oregon-postgres.render.com/solaria")
cursor = cnx.cursor()
query = "SELECT * FROM Data_CR"
cursor.execute(query)
rows = cursor.fetchall()
df0 = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
cursor.close()
cnx.close()


# data prevision revenue
#cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
#query_p_r = "SELECT * FROM prevision_revenue"
#df0_revznue_prev = pd.read_sql(query_p_r, con=cnx)
#cnx.close()

cnx = psycopg2.connect("postgres://iheb:3oO6ZpxwsB3iKuwe1oqO2YaHIzMI9vyt@dpg-chgh7ou7avjbbjpn4h50-a.oregon-postgres.render.com/solaria")
cursor = cnx.cursor()
query_p_r = "SELECT * FROM prevision_revenue"
cursor.execute(query_p_r)
rows = cursor.fetchall()
df0_revznue_prev = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
cursor.close()
cnx.close()


# data GRH
#cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
#query_personnel = "SELECT * FROM `charge personnel`"
#df_personnel = pd.read_sql(query_personnel, con=cnx)
#cnx.close()

cnx = psycopg2.connect("postgres://iheb:3oO6ZpxwsB3iKuwe1oqO2YaHIzMI9vyt@dpg-chgh7ou7avjbbjpn4h50-a.oregon-postgres.render.com/solaria")
cursor = cnx.cursor()
query_personnel = "SELECT * FROM \"charge personnel\""
cursor.execute(query_personnel)
rows = cursor.fetchall()
df_personnel = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
cursor.close()
cnx.close()

# data control couts
#cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
#query_couts_s = "SELECT * FROM `controle achats sortie`"
#df_couts_s = pd.read_sql(query_couts_s, con=cnx)
#cnx.close()

cnx = psycopg2.connect("postgres://iheb:3oO6ZpxwsB3iKuwe1oqO2YaHIzMI9vyt@dpg-chgh7ou7avjbbjpn4h50-a.oregon-postgres.render.com/solaria")
cursor = cnx.cursor()
query_couts_s = "SELECT * FROM \"controle achats sortie\""
cursor.execute(query_couts_s)
rows = cursor.fetchall()
df_couts_s = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
cursor.close()
cnx.close()

# data revenue restauration 
#cnx = mysql.connector.connect(user='root', host='localhost', database='solaria')
#query_r_restauration = "SELECT * FROM `data revenue restauration`"
#df_r_restauration = pd.read_sql(query_r_restauration, con=cnx)
#cnx.close()

cnx = psycopg2.connect("postgres://iheb:3oO6ZpxwsB3iKuwe1oqO2YaHIzMI9vyt@dpg-chgh7ou7avjbbjpn4h50-a.oregon-postgres.render.com/solaria")
cursor = cnx.cursor()
query_r_restauration = "SELECT * FROM \"data revenue restauration\""
cursor.execute(query_r_restauration)
rows = cursor.fetchall()
df_r_restauration = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
cursor.close()
cnx.close()

#--------------------------------------------------------filtre les donnes----------------------------------------------------------


# ***************filtre pour les dataframe control revenue
st.sidebar.title("📊KPI revenues")
st.sidebar.write("--------------------")
st.sidebar.title("📆KPI l'activite hebergement")
df0['Date arrives'] = pd.to_datetime(df0['Date arrives'])
# Extract months and create a new column 'month_column'
df0['month_column'] = df0['Date arrives'].dt.month
df0['years_column'] = df0['Date arrives'].dt.year
years = st.sidebar.multiselect(
    "Select Year(s) for KPI",
    options=df0["years_column"].unique(),  # Update column name here
    default=df0["years_column"].unique(),  # Update column name here
    key="years_r")  # Add a unique key argument

mois = st.sidebar.multiselect(
    "Select Month(s) for KPI",
    options=df0["month_column"].unique(),
    default=df0["month_column"].unique(),
    key="mois_r")

# Apply filters to the DataFrame
df = df0[(df0["month_column"].isin(mois)) & (df0["years_column"].isin(years))]  # Update column name here

# ***************filtre pour les dataframe control revenue(restauration)


st.sidebar.title("📆KPI l'activite restauration")
df_r_restauration['Date'] = pd.to_datetime(df_r_restauration['Date'])
# Extract months and create a new column 'month_column'
df_r_restauration['month_column'] = df_r_restauration['Date'].dt.month
df_r_restauration['years_column'] = df_r_restauration['Date'].dt.year

years_r_restauration = st.sidebar.multiselect(
    "Select Year(s) for KPI",
    options=df_r_restauration["years_column"].unique(),
    default=df_r_restauration["years_column"].unique(),
    key="years_r_restauration")  # Add a unique key argument

mois_r_restauration = st.sidebar.multiselect(
    "Select Month(s) for KPI",
    options=df_r_restauration["month_column"].unique(),
    default=df_r_restauration["month_column"].unique(),
    key="mois_r_restauration")  # Add a unique key argument

df_r_restauration_filtre = df_r_restauration[(df_r_restauration["month_column"].isin(mois_r_restauration)) & (df_r_restauration["years_column"].isin(years_r_restauration))]  # Update column name here


#****************filtre pour les dataframe GRH
st.sidebar.title("📊les KPI couts")
st.sidebar.write("--------------------")
st.sidebar.title("📆les KPI l'activite hebergement")
years_GRH = st.sidebar.multiselect(
    "Select Year(s) pour les donnes liee a la GRH",
    options=df_personnel["Année"].unique(),  # Update column name here
    default=df_personnel["Année"].unique(),
    key="years_GRH")  
mois_GRH = st.sidebar.multiselect(
    "Select Year(s) pour les donnes liee a la GRH",
    options=df_personnel["Mois"].unique(),  # Update column name here
    default=df_personnel["Mois"].unique(),
    key="mois_GRH")  

df_personnel_filtre = df_personnel[(df_personnel["Mois"].isin(mois_GRH)) & (df_personnel["Année"].isin(years_GRH))]  # Update column name here

#****************filtre pour les dataframe controle couts sortie 

st.sidebar.title("📆les KPI l'activite restauration")
df_couts_s['date'] = pd.to_datetime(df_couts_s['date'])
# Extract months and create a new column 'month_column'
df_couts_s['month_column'] = df_couts_s['date'].dt.month
df_couts_s['years_column'] = df_couts_s['date'].dt.year

years_df_couts_s = st.sidebar.multiselect(
    "Select Year(s) pour les donnes liee a les sorties",
    options=df_couts_s["years_column"].unique(),
    default=df_couts_s["years_column"].unique(),
    key="years_df_couts_s")  # Add a unique key argument

mois_df_couts_s = st.sidebar.multiselect(
    "Select Month(s) pour les donnes liee a les sorties",
    options=df_couts_s["month_column"].unique(),
    default=df_couts_s["month_column"].unique(),
    key="mois_df_couts_s")  # Add a unique key argument

df_couts_s_filtre = df_couts_s[(df_couts_s["month_column"].isin(mois_df_couts_s)) & (df_couts_s["years_column"].isin(years_df_couts_s))]  # Update column name here



#---------------------------------------les indicateur performance ---------------------------------------------------------------------------------
st.markdown("<h1 style=' color: rgb(255, 195, 0); font-size: 50px; text-align: center;'>📊 les indicateur de performance de l'hôtel</h1>", unsafe_allow_html=True)

st.write("-----------------")
st.markdown("<h1 style=' font-size: 40px;color:rgb(255,69,0);'>🛌 l'activite hebergement</h1>", unsafe_allow_html=True)

# Calcul du taux d'occupation

NBch = df['Chambre réservée']
NBch_dispo = 239
taux_docupation = (NBch/NBch_dispo)*100
taux_docupation = round(taux_docupation, 2) # Arrondir à 2 décimales
df["taux d'ocupation"] = taux_docupation

fig = px.area(df, x='Date arrives', y="taux d'ocupation",text="taux d'ocupation",width=600,title="🎯taux d'ocupation")

#revenu_moyen_chambre
revenu_moyen_chambre = df["CA totale"]/df["Chambre réservée"]
df["revenu moyen chambre"] = revenu_moyen_chambre
fig11 = px.bar(df, y="revenu moyen chambre", x="Date arrives", title="🎯revenu moyen chambre")


left_column, right_column = st.columns(2)
with right_column:
    st.write(fig)
    with st.expander("🔑explexation"):
         st.write("""
Intérêt :         
Il permet de traduire le nombre de chambres louées en % par rapport à la
capacité totale en chambres offertes. Autrement formulé, et d’une manière
statique, c’est répondre à la question suivante : Combien avons-nous loué de
chambres ?
Sur le plan dynamique, le taux d’occupation nous renseigne sur la capacité
commerciale de la brigade de réception et celle de l’équipe de la force de vente
(L’agressivité commerciale). On peut le calculer pour une journée, une décade,
un mois... 
    """)
with left_column:
    st.write(fig11)
    with st.expander("🔑explexation"):
         st.write("""
Intérêt :       
Il permet de mesurer l’effet de la variation combinée de l’occupation des
chambres et du prix moyen par chambre louée, réalisant ainsi une synthèse de la
performance commerciale de l’établissement. Pour beaucoup de responsables
hôteliers, le « Yield » est aujourd’hui le principal indicateur de performance de
l’hôtel.
    """)



REVPAR = df["Revenue Hébergement"]/239
df["REVPAR"] = REVPAR

LADR = df["Revenue Hébergement"]/df["Chambre réservée"]
df["L'ADR"]= LADR

fig2 = px.bar(df, y=["REVPAR", "L'ADR", "CA totale"], x="Date arrives",barmode='group', title="🎯REVPAR L'ADR  CA totale")


nb_arrives = df['nombre de voyageurs']
nb_nuites = df['Nombre nuits']
duree_moyenne = nb_nuites/nb_arrives
df["duree_moyenne"]= duree_moyenne


fig_duree_moyenne = px.area(df, y = "duree_moyenne",x="Date arrives",width=600,title="🎯duree moyenne de se jour")




left_column, right_column = st.columns(2)
with right_column:
        st.write(fig_duree_moyenne)
        with st.expander("🔑explexation"):
         st.write("""
Formule :
NBRE DE NUITEES/NBRE DES ARRIVEES

Intérêt :
D’une part, il nous renseigne sur le type de clientèle (de passage, de séjour),
d’autre part, il permet de juger la capacité de l’hôtel à retenir et à prolonger la
durée de la présence du client. Son calcul s·effectue sur une période
déterminée : une semaine, un mois,         



    """)
with left_column:
    st.write(fig2)
    with st.expander("🔑explexation"):
       st.write("""
L’ADR (average daily rate) est le prix moyen quotidien de vos chambres

Intérêt :
Le REVPAR (revenue per available room) représente le revenu par chambre disponible. Ceci signifie qu’une chambre en particulier peut être louée pendant la période observée. Cet indicateur métrique est calculé en multipliant l’ADR par le taux d’occupation. Il sert à déterminer le prix moyen affiché pour les chambres disponibles. Prenons un exemple sur un mois. 
le chiffre d'affaire d'une entreprise correspond à la somme des ventes effectuées par celle-ci. Il peut être dit HT (hors taxes) ou peut inclure la TVA (Taxe sur la Valeur Ajoutée), auquel cas on parle de chiffre d'affaires TTC (toutes charges comprises).          
 
       """)




prevue_financiere = df0_revznue_prev["Revenue Hébergement"].sum()
realisation_financiere =df0["Revenue Hébergement"].sum()

taux_realisation_financiere = (realisation_financiere/prevue_financiere)*100



# Création d'un DataFrame fictif pour les données
df_taux_realisation_financiere = pd.DataFrame({'Catégories': ['Prévue', 'Réalisée'],
                   'Valeurs': [prevue_financiere, realisation_financiere]})

# Calcul du taux de réalisation financière en pourcentage
taux_realisation = (realisation_financiere / prevue_financiere) * 100

# Création du graphique de barre de progression
fig_taux_realisation = px.bar(df_taux_realisation_financiere, y='Catégories', x='Valeurs', text='Valeurs',width=1100)

# Personnalisation du graphique
fig_taux_realisation.update_traces(marker_color=['lightgray', 'limegreen'], # Couleurs des barres
                  hoverinfo='none', # Désactivation des informations au survol
                  texttemplate='%{y:,.0f}', # Format du texte affiché sur les barres
                  textposition='inside') # Position du texte à l'intérieur des barres

# Ajout d'une annotation pour afficher le taux de réalisation
fig_taux_realisation.add_annotation(y='Réalisée', x=realisation_financiere, 
                   text=f'{taux_realisation:.2f}%', showarrow=False)

# Mise en forme du titre et des axes
fig_taux_realisation.update_layout(
                  xaxis_title_text='Catégories',
                  yaxis_title_text='Valeurs')

# Affichage du graphique
st.markdown("<h1 style=' font-size: 30px;'>🎯Taux de la realisation financiere revenue hebergement</h1>", unsafe_allow_html=True)            
st.write(fig_taux_realisation)
with st.expander("🔑explexation"):
       st.write("""
Formule :
C.A. TOTAL REALISE EN LOCATION/C.A. POTENTIEL 

Intérêt:
 Il permet de connaître le manque à gagner de la sous-location et donc,
d’engager les actions nécessaires.

    """)
    
st.markdown("<h1 style=' font-size: 40px;color:rgb(255,69,0);'>🍴  l'activite restauration</h1>", unsafe_allow_html=True)

st.write("---------------------")


nombre_de_repas = df_r_restauration_filtre["Nombre repas servie"].sum()
taux_remplissage = nombre_de_repas/(300*3*360)


ca_restauration = df_r_restauration_filtre["Revenue restaurations"].sum()
nombre_de_couvert_servis = df_r_restauration_filtre["Nombre de couvert servis"].sum()
ticket_moyen = ca_restauration/nombre_de_couvert_servis


nb_chaise = 300 
nombre_de_couvert_servis_columns = df_r_restauration_filtre["Nombre de couvert servis"]
taux_occupation_chaise = nombre_de_couvert_servis_columns/nb_chaise
df_r_restauration_filtre["taux_occupation_chaise"]=taux_occupation_chaise

fig_taux_occupation_chaise = px.line(df_r_restauration_filtre, x='Date', y="taux_occupation_chaise",width=600)




prevue_financiere_restauration = df0_revznue_prev["Revenue restaurations"].sum()
realisation_financiere_restauration =df0["Revenue restaurations"].sum()




# Création d'un DataFrame fictif pour les données
df_taux_realisation_financiere_r = pd.DataFrame({'Catégories': ['Prévue', 'Réalisée'],
                   'Valeurs': [prevue_financiere_restauration, realisation_financiere_restauration]})

# Calcul du taux de réalisation financière en pourcentage
taux_realisation_financiere_r = (realisation_financiere_restauration/prevue_financiere_restauration)*100


# Création du graphique de barre de progression
fig_taux_realisation_r = px.bar(df_taux_realisation_financiere_r, y='Catégories', x='Valeurs', text='Valeurs',width=1100)

# Personnalisation du graphique
fig_taux_realisation_r.update_traces(marker_color=['lightgray', 'limegreen'], # Couleurs des barres
                  hoverinfo='none', # Désactivation des informations au survol
                  texttemplate='%{y:,.0f}', # Format du texte affiché sur les barres
                  textposition='inside') # Position du texte à l'intérieur des barres

# Ajout d'une annotation pour afficher le taux de réalisation
fig_taux_realisation_r.add_annotation(y='Réalisée', x=realisation_financiere_restauration, 
                   text=f'{taux_realisation_financiere_r:.2f}%', showarrow=False)

# Mise en forme du titre et des axes
fig_taux_realisation_r.update_layout(
                  xaxis_title_text='Catégories',
                  yaxis_title_text='Valeurs')


col1,col2 =st.columns(2)
with col1:
     st.markdown("<h1 style=' font-size: 30px;'>🎯le taux de remplissage</h1>", unsafe_allow_html=True) 
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{taux_remplissage:.2%}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""formule:
(Nombre de repas servis/ (nombre de place disponible*nombre de service*nombre de jours d’exploitations*100

Intérêt :
C’est l’équivalent du taux d’occupation en hébergement, il nous renseigne sur le
nombre de repas que le restaurant a vendu.

    """)
     st.markdown("<h1 style=' font-size: 30px;'>🎯le ticket moyen</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{ticket_moyen:.2%}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""
        Formule :
CA d’une période/Nb total de couverts servis sur la même période

Intérêt :
Il nous permet de connaitre la dépense moyenne consentie par les clients.

    """)


with col2:
     st.markdown("<h1 style=' font-size: 30px;'>🎯le taux d'occupation de la chaise par jour</h1>", unsafe_allow_html=True)
     st.write(fig_taux_occupation_chaise)
     with st.expander("🔑explexation"):
       st.write("""
Formule :
Nombre de couverts servis/Nombre de chaises

Intérêt :
Il permet de nous indiquer le taux de rotation de la chaise
    """)
       
st.markdown("<h1 style=' font-size: 30px;'>🎯Taux de la realisation financiere Revenue restaurations</h1>", unsafe_allow_html=True)
st.write(fig_taux_realisation_r)  
with st.expander("🔑explexation"):
       st.write("""
Formule :
(C.A realise en restauration /C.A. POTENTIEL)*100

Intérêt :
Il permet de connaître le manque à gagner de la rsetauration et donc,
d’engager les actions nécessaires.
       """)


#---------------------------------------les indicateur  couts ---------------------------------------------------------------------------------


st.markdown("<h1 style='  color: rgb(255, 195, 0); font-size: 50px; text-align: center;'>📊 les indicateur de performance liee aux couts</h1>", unsafe_allow_html=True)
st.markdown("<h1 style=' font-size: 40px;color:rgb(255,69,0);'>🛌 l'activite hebergement</h1>", unsafe_allow_html=True)
st.write("------------------")

nb_salaries = df_personnel_filtre["Matricule"].count()
nombre_chambre_de_periode = df['Chambre réservée'].sum()
rendement_employe= round(nombre_chambre_de_periode/nb_salaries,3)

df_salaries_etage = df_personnel_filtre[df_personnel_filtre.Département=="Etage"]
nb_salaries_etage = df_salaries_etage["Département"].count()

Rendement_etage = nombre_chambre_de_periode / nb_salaries_etage

col1,col2 =st.columns(2)
with col1:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Rendement par employe (par mois)</h1>", unsafe_allow_html=True) 
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{rendement_employe}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""
Formule :
(NBRE DE CHAMBRES DISPONIBLES OU DE CHAMBRES LOUEES)/(NBRE DE SALARIES)

Intérêt :
Ce ratio indique l’effectif moyen par chambre disponible ou louée. Il est calculé
pour l’ensemble de l’établissement de l’établissement ou pour un service donné.
Il dépend de la catégorie de l’établissement et permet des comparaisons avec les
statistiques professionnelles
    """)

with col2:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Rendement au service etage (par mois)</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{Rendement_etage}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""
Formule :
(NBRE DE CHAMBRES LOUEES)/ (NBRE D’HEURES DU PERSONNEL ETAGE)

Intérêt :
Il nous indique sur le rendement du service des étages. Il est très utilisé dans
tous les établissements hôteliers qui ne sous traitent pas cette activité
    """)

st.markdown("<h1 style=' font-size: 40px;color:rgb(255,69,0);'>🍴  l'activite restauration</h1>", unsafe_allow_html=True)

cout_nourriture_vendues  = df_couts_s_filtre["Nourriture"].sum()
totale_vendue_nourriture = df_r_restauration_filtre["Nombre repas servie"].sum()
cout_nourriture = (cout_nourriture_vendues/totale_vendue_nourriture)*100


cout_boisson_vendues = df_couts_s_filtre["Boisson"].sum()
totale_vendue_boisson = df_r_restauration_filtre["ventes boissons"].sum()
cout_boisson = (cout_boisson_vendues/totale_vendue_boisson)*100

cout_fb = df_couts_s_filtre["totale COUTS F&B"].sum()
Revenue_restaurations= df_r_restauration_filtre["Revenue restaurations"].sum()
cout_matiere = (cout_fb/Revenue_restaurations)*100


total_couvert_servie =df_r_restauration_filtre["Nombre de couvert servis"].sum()
jour_travaille_personnel = df_personnel_filtre["jours travaile"].sum()
heure_travaille = jour_travaille_personnel*8
efficacite_personnel = heure_travaille/total_couvert_servie



col1,col2 =st.columns(2)
with col1:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Le cout nourriture(par mois)</h1>", unsafe_allow_html=True) 
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{cout_nourriture}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""
Formule :
Coûts nourriture vendue d’une période11/total ventes nourriture de la période
x100

Intérêt :
Il permet de mesurer le coût des denrées utilisées dans la confection des plats.
    """)

with col2:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Le cout boisson(par mois)</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{cout_boisson}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""
 Formule :
Coûts boissons vendues d’une période/total ventes boissons de la période x100

Intérêt :
Il permet de refléter l’ensemble des coûts boissons et nourritures comprise dans
les boissons

    """)
       

col1,col2 =st.columns(2)
with col1:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Le cout matiere(par mois)</h1>", unsafe_allow_html=True) 
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{cout_matiere}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""
 Formule :
Coûts F&B d’une période/total ventes de la période x100

Intérêt :
 Coût nourriture vendue=stock début de période +chats de matières premières –stock
fin de période-repas personnel-offerts
Il permet à l’entreprise de mieux suivre le premier de ses coûts principaux

    """)

with col2:
     st.markdown("<h1 style=' font-size: 30px;'>🎯Efficacite du personnel(par mois)</h1>", unsafe_allow_html=True)
     st.write(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{efficacite_personnel}</h1>", unsafe_allow_html=True)
     with st.expander("🔑explexation"):
       st.write("""
 Formule :
Total d’heures travaillées sur une période/total de couverts sur la même période

Intérêt :
Il détermine le coût, en temps, de chaque couvert
    """)      




#---------------------------------------------------------------------------------------------------------------------------------------------------------

st.write("-------------------------------")
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

