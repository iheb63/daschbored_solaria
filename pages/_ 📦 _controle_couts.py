import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from PIL import Image
import numpy as np
import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="solaria daschbored",
    page_icon= "📦",
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









# Load the data from Excel
df_controle_achats = pd.read_excel("C:/Users/ihebt/OneDrive/Bureau/data/data controle achats/Data_CA.xlsx")
# Define the variables to plot
variables = ['totale COUTS F&B', 'Cout energie', 'Produits de nettoyage', "Produits d'acceuil", 'Fourniture de bureau','achats techniques','consomation personnel ']

# Melt the data to create a long format
df_melt = pd.melt(df_controle_achats, id_vars='date', value_vars=variables, var_name='variable')

# Add a filter for the variables 
selected_months = st.sidebar.multiselect('Selectionnez les mois pour les charges d\'achats :', sorted(df_controle_achats['date'].dt.month.unique()))

# Filter the data to include only the selected variables and months
df_selected = df_melt[df_melt['date'].dt.month.isin(selected_months)]
total_chargeA = df_selected['value'].sum()
# Create the line plot
fig = px.bar(df_selected, x='date', y='value', color=('variable'), barmode='group',title="🌟les charge d'achats par mois:      "    + str(total_chargeA),)




#histograme budget 
df_controle_achats_B = pd.read_excel("C:/Users/ihebt/OneDrive/Bureau/data/data controle achats/Data_CA.xlsx",
                                   sheet_name="Sheet2")


# Create the line plot
fig2 = px.bar(df_controle_achats_B, x='Mois', y=['budget f&b'	,'budget energie'	,'budge nettoyage'	,"budget d'acceuil",	"budget FB",
"consomation personnel "], barmode='group',title="🌟les budgets des achats")


left_column, right_column , = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)


if (total_chargeA>= 0):
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>✅{total_chargeA}</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>❌{total_chargeA}</h1>", unsafe_allow_html=True)
#----totale depense d'achats ____________________________________________________
#total_charge = df_selected["value"].sum()
#st.title("Total charge département achats", className="title")
#st.markdown(f"<h1 style='text-align: center; color: rgb(253, 254, 254);'>Total charge département achats:</h1>", unsafe_allow_html=True)
#st.markdown(f"<h1 style='text-align: center; color : rgb(0, 255, 255) ;'>{total_charge}</h1>", unsafe_allow_html=True)
# ecatrs entre budget

fig00 =px.line(df_controle_achats,x="date",y=["achats techniques","Boisson","Nourriture","Water","Electricity","Fuel & Gas"],title="🌟suivie les charge les plus important",width=1200)
st.write(fig00)



#-----------------------------------GRH-----------------------------------------------


st.write("-----------------------------------------------------------------------------------")
st.markdown(f"<h1 style=' color: rgb(255, 195, 0) ;'>2-suivie des charges personnels :</h1>", unsafe_allow_html=True)
# read the data
df_GRH = pd.read_excel("C:/Users/ihebt/OneDrive/Bureau/data/data GRH/Data_RH.xlsx") 
df_GRHB = pd.read_excel("C:/Users/ihebt/OneDrive/Bureau/data/data GRH/Data_RH.xlsx",
                        sheet_name="budget")

# create the month filter
mois = st.sidebar.multiselect(
    "selectione le Mois pour les KPI RH",
    options=df_GRH["Mois"].unique(),
    default=df_GRH["Mois"].unique()
)

# filter the dataframe based on the selected months
df_selection_RH = df_GRH[df_GRH["Mois"].isin(mois)]
df_selection_RHB = df_GRHB[df_GRHB["Mois"].isin(mois)]
# histigrame couts salaires
total_chargeS = df_selection_RH['salaires net'].sum()

fig = px.bar(df_selection_RH, x="Mois", y='salaires net',
             color='Département', barmode='group',title="🌟charge personnel:        "+str(total_chargeS))

#histograme budget 
df_GRHB = pd.read_excel("C:/Users/ihebt/OneDrive/Bureau/data/data GRH/Data_RH.xlsx",
                        sheet_name="budget")

fig0 = px.bar(df_GRHB, x="Mois", y='budget salaires globael ',
             barmode='group',title="🌟budget charge personnel",
             height=400)

fig3 = px.pie(df_GRH, values='salaires net', names='Type de contrat', 
        hole=.6, title='🌟type de contrat ')
fig3.update_traces(textposition='inside', textinfo='percent+label')

fig4 = px.bar(df_GRH, x="Sexe", y='salaires net',
             barmode='group',title="🌟charge personnel par sexe",color="Sexe",
             height=400)

left_column, right_column , = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig0, use_container_width=True)
#ecatrs budget et realisation
total__budget_s  = df_selection_RHB['budget salaires globael '].sum()
ECART_RH = round(total__budget_s - total_chargeS,3)
st.title("🌟Ecarts entre realisatiion et budget:")

if (ECART_RH >= 0):
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>✅{ECART_RH}</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>❌{ECART_RH}</h1>", unsafe_allow_html=True)

left_column, right_column , = st.columns(2)
left_column.plotly_chart(fig3, use_container_width=True)
right_column.plotly_chart(fig4, use_container_width=True)

HD = df_selection_RH["jours dus "].sum()
HT = df_selection_RH["jours travaile"].sum()
taux_dabsence = 1-(HT/HD)
#st.title("Taux d'absentéisme par mois:")
#st.markdown(f"<h1 style='text-align: center; color: rgb(0, 255, 255);'>{taux_dabsence:.2%}</h1>", unsafe_allow_html=True)

EFFECTIF =  df_selection_RH["Matricule"].count()
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
df_comptable_fres = pd.read_excel("C:/Users/ihebt/OneDrive/Bureau/data/data compt fres/Data_CF.xlsx")

fig5 = px.bar(df_comptable_fres,x="Nom du fournisseur",y="reste du  dettes",height=600,title="🌟solde par fres")

fig6 = px.line(df_comptable_fres,x="Échéance",y="reste du  dettes",height=450,title="🌟solde par date ")


left_column, right_column , = st.columns(2)
left_column.plotly_chart(fig5, use_container_width=True)
right_column.plotly_chart(fig6, use_container_width=True)

fig7 = px.pie(df_comptable_fres, values='reste du  dettes', names='etat de facture ', 
        hole=.6,width=550, title='🌟facteur en retared vs autre')
fig7.update_traces(textposition='inside', textinfo='percent+label')

import pandas as pd
from datetime import datetime, date

# convert date object to datetime object
today = datetime.combine(date.today(), datetime.min.time())

# convert string column to datetime object
df_comptable_fres['Échéance'] = pd.to_datetime(df_comptable_fres['Échéance']) 

# filter rows based on date comparison
prochaines_P = df_comptable_fres[(df_comptable_fres['Échéance'] >= today)&(df_comptable_fres['reste du  dettes']>0)]

# select columns "Numéro de facture" and "Nom du fournisseur"
prochaines_P_subset = prochaines_P[["Échéance", "Nom du fournisseur","reste du  dettes"]]
prochaines_P_subset.sort_values(["reste du  dettes"], inplace=True , ascending=False)


left_column, right_column = st.columns(2)
with left_column:
        st.markdown(f"<h1 style=' color: rgb(255, 255, 255); font-size: 15px;'>🌟les 10 prochaine reglement</h1>", unsafe_allow_html=True)
        st.write(prochaines_P_subset.head(10))
with right_column:
    st.write(fig7)

st.write("----------------------")


