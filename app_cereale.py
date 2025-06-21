import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import io
import xlsxwriter


# Configuration de la page
st.set_page_config(page_title="Analyse du Rendement Céréalier - Burkina Faso", layout="wide")

# Titre principal
st.title("🌾 Analyse Interactive du Rendement Céréalier au Burkina Faso (1996 - 2022)")



# Chargement des données
@st.cache_data
def load_data():
    return pd.read_excel('D:/Production/projetAGRI/base_finale.xlsx')

df = load_data()

# Aperçu
#st.subheader("Aperçu des données")
#st.dataframe(df.head())

# Filtres interactifs
st.sidebar.header("Filtres")

regions = df['Région'].unique()
cereales = df['Céréale'].unique()

regions_sel = st.sidebar.multiselect("Sélectionnez une ou plusieurs Régions", sorted(regions), default=sorted(regions)[:1])
cereales_sel = st.sidebar.multiselect("Sélectionnez une ou plusieurs Céréales", sorted(cereales), default=sorted(cereales)[:1])

# Choix de la variable de productivité
var_affiche1 = st.sidebar.selectbox("Variable de productivité", ['Production', 'Superficie', 'Rendement'])

# Choix de la variable de climatique
var_affiche2 = st.sidebar.selectbox("Variable climatique", ['Précipitation', 'Nombre_jour_Pluie', 'Température', 
                                                            'Humidité', 'Vitèsse_Vent', 'Durée_Ensoleillement'])

# Filtres sur les variables d'état

#Filtre sur régions uniquement
df_filtre1 = df[(df['Région'].isin(regions_sel))]

#Filtre sur céréales uniquement
df_filtre2 = df[df['Céréale'].isin(cereales_sel)]

#Filtre sur régions et céréales
df_filtre = df[(df['Région'].isin(regions_sel)) & (df['Céréale'].isin(cereales_sel))]

#Affichage de la table de données en fonction des variables d'état

if regions_sel and not cereales_sel:
    st.subheader(f"Table de données pour {', '.join(regions_sel)}")
    st.dataframe(df_filtre1)
    
elif cereales_sel and not regions_sel:
    st.subheader(f"Table de données pour {', '.join(cereales_sel)}")
    st.dataframe(df_filtre2)

elif regions_sel and cereales_sel:
    st.subheader(f"Table de données pour {', '.join(regions_sel)} et {', '.join(cereales_sel)}")
    st.dataframe(df_filtre)

else:
    st.subheader("Veuillez sélectionner au moins une Région ou une Céréale.")


# Export Excel
st.write("Télécharger les données filtrées")

# Créer un buffer Excel en mémoire
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    if regions_sel and not cereales_sel:
        df_filtre1.to_excel(writer, index=False, sheet_name='Données filtrées')
        data = output.getvalue()
    elif cereales_sel and not regions_sel:
        df_filtre2.to_excel(writer, index=False, sheet_name='Données filtrées')
        data = output.getvalue()
    elif regions_sel and cereales_sel:
        df_filtre.to_excel(writer, index=False, sheet_name='Données filtrées')
        data = output.getvalue()

st.download_button(
    label="Télécharger en Excel",
    data=data,
    file_name='donnees_filtrees.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)


# Graphique et statistiques des variables productivité en fonction des régions  
st.subheader(" Graphique et Statistiques de productivité en fonction de la région ")
if not df_filtre1.empty:
    st.write(f" 1. Evolution de {var_affiche1} (1996 - 2022) pour {', '.join(regions_sel)} ")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=df_filtre1,
        x='Année',
        y=var_affiche1,
        hue='Région',
        markers=True,
        dashes=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.ylabel(var_affiche1)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write(f" 2. Statistiques Descriptives de {var_affiche1} pour {', '.join(regions_sel)} ")
    stats = df_filtre1.groupby(['Région'])[var_affiche1].describe().reset_index()
    st.dataframe(stats)
else:
    st.warning("Aucune donnée disponible pour les sélections actuelles.")


    
    
# Graphique et statistiques des variables productivité en fonction des céréales
st.subheader(" Graphique et Statistiques de productivité en fonction de la céréale ")
if not df_filtre2.empty:
    st.write(f" 1. Evolution de {var_affiche1} (1996 - 2022) pour {', '.join(cereales_sel)} ")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=df_filtre2,
        x='Année',
        y=var_affiche1,
        hue='Céréale',
        markers=True,
        dashes=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.ylabel(var_affiche1)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write(f" 2. Statistiques Descriptives de {var_affiche1} pour {', '.join(cereales_sel)} ")
    stats = df_filtre2.groupby(['Céréale'])[var_affiche1].describe().reset_index()
    st.dataframe(stats)
else:
    st.warning("Aucune donnée disponible pour les sélections actuelles.")


# Graphique et statistiques des variables productivité en fonction des régions et des céréales
st.subheader(" Graphique et Statistiques de productivité en fonction de la région et de la céréale ")
if not df_filtre.empty:
    st.write(f" 1. Evolution de {var_affiche1} (1996 - 2022) pour {', '.join(regions_sel)} et {', '.join(cereales_sel)}")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=df_filtre,
        x='Année',
        y=var_affiche1,
        hue='Région',
        style='Céréale',
        markers=True,
        dashes=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.ylabel(var_affiche1)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write(f" 2. Statistiques Descriptives de {var_affiche1} pour {', '.join(regions_sel)} et {', '.join(cereales_sel)} ")
    stats = df_filtre.groupby(['Région', 'Céréale'])[var_affiche1].describe().reset_index()
    st.dataframe(stats)
else:
    st.warning("Aucune donnée disponible pour les sélections actuelles.")
    

# Graphique et statistiques des variables climatiques en fonction des régions  
st.subheader(" Graphique et Statistiques de climat en fonction de la région ")
if not df_filtre1.empty:
    st.write(f" 1. Evolution de {var_affiche2} (1996 - 2022) pour {', '.join(regions_sel)} ")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=df_filtre1,
        x='Année',
        y=var_affiche2,
        hue='Région',
        markers=True,
        dashes=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.ylabel(var_affiche2)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write(f" 2. Statistiques Descriptives de {var_affiche2} pour {', '.join(regions_sel)} ")
    stats = df_filtre1.groupby(['Région'])[var_affiche2].describe().reset_index()
    st.dataframe(stats)
else:
    st.warning("Aucune donnée disponible pour les sélections actuelles.")



#####################################################################################

# Filtrage interactif
st.sidebar.header("🔍 Filtres")

regions_1 = st.sidebar.multiselect("Sélectionnez les régions :", sorted(df['Région'].unique()), default=df['Région'].unique())
cereales_1 = st.sidebar.multiselect("Sélectionnez les types de céréales :", sorted(df['Céréale'].unique()), default=df['Céréale'].unique())
annees_1 = st.sidebar.slider("Sélectionnez la plage d'années :", int(df['Année'].min()), int(df['Année'].max()), (1996, 2022))

# Application des filtres
df_filtre_3 = df[
    (df['Région'].isin(regions_1)) &
    (df['Céréale'].isin(cereales_1)) &
    (df['Année'] >= annees_1[0]) &
    (df['Année'] <= annees_1[1])
]

# Graphique de tendance de la production
st.subheader("📈 Évolution de la Production par Année")

fig_prod = px.line(
    df_filtre.groupby(['Année', 'Céréale'])['Production'].mean().reset_index(),
    x='Année',
    y='Production',
    color='Céréale',
    title='Production moyenne par type de céréale',
    markers=True
)
st.plotly_chart(fig_prod, use_container_width=True)

# Heatmap de corrélation
st.subheader("🔍 Corrélation entre les variables climatiques et la Production")

cols_corr = ['Production', 'Température', 'Précipitation', 'Humidité', 'Vitèsse_Vent', 'Durée_Ensoleillement', 'Nombre_Jour_Pluie']
corr = df_filtre_3[cols_corr].corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

# Analyse par région
st.subheader("🌍 Carte de Production Moyenne par Région")

moyenne_region = df_filtre_3.groupby('Région')['Production'].mean().reset_index()

fig_region = px.bar(
    moyenne_region,
    x='Région',
    y='Production',
    title="Production moyenne (tonne/ha) par région",
    color='Production',
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_region, use_container_width=True)

# Analyse climat vs production
st.subheader("🌦 Impact des facteurs climatiques sur la Production")

# Sélection de la variable
var_x = st.selectbox("Choisissez une variable climatique :", [
    'Température', 'Précipitation', 'Humidité', 'Vitèsse_Vent',
    'Durée_Ensoleillement', 'Nombre_Jour_Pluie'
])


# Bouton pour afficher le graphique
if st.button("📊 Cliquez ici pour afficher le graphique"):
    fig_scatter = px.scatter(
        df_filtre_3,
        x=var_x,
        y='Production',
        color='Céréale',
        size='Superficie',
        hover_data=['Région', 'Année'],
        trendline="ols",
        title=f"Relation entre {var_x} et la Production"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


###################################### MODELISATION ##################################


# Charger le pipeline et les sélections
reduced_pipeline = joblib.load("model_rendement.pkl")  # Assure-toi que ce fichier existe
selected_cat = ['Région', 'Céréale', 'Année']
selected_num = ['Superficie', 'Température', 'Précipitation', 'Nombre_Jour_Pluie', 'Humidité', 'Vitèsse_Vent', 'Durée_Ensoleillement']


st.title("🌾 Prédiction de la Production Céréalière au Burkina Faso")

# Interface utilisateur
with st.form("prediction_form"):
    st.subheader("Entrez les caractéristiques pour la prédiction")
    
    region = st.selectbox("Région du Burkina Faso", ['Sahel', 'Centre', 'Boucle du Mouhoun', 'Centre-Sud', 
                                                     'Centre-Nord', 'Hauts-Bassins', 'Cascades', 'Plateau Centrale', 
                                                     'Est', 'Centre-Ouest', 'Nord', 'Sud-Ouest'])
    
    cereale = st.selectbox("Type de Céréale", ['Arachide', 'Coton', 'Maïs', 'Mil', 'Nebié', 'Riz', 'Sorgho'])
    annee = st.number_input("Année", min_value=2000, max_value=2030, value=2023)

    superficie = st.number_input("Superficie (ha)", min_value=0.0, value=5500.0)
    temperature = st.number_input("Température Moyenne (°C)", value=30.0)
    precipitation = st.number_input("Précipitation (mm)", value=200.0)
    nb_jours_pluie = st.number_input("Nombre de Jours de Pluie dans l'année", value=7)
    humidite = st.number_input("Humidité Moyenne annuelle (%)", value=65.0)
    vent = st.number_input("Vitesse du Vent (km/h)", value=22.0)
    ensoleillement = st.number_input("Durée d'Ensoleillement (h)", value=6.0)

    submitted = st.form_submit_button("Prédire")

if submitted:
    # Préparer les données
    new_data = pd.DataFrame({
        'Région': [region],
        'Céréale': [cereale],
        'Année': [annee],
        'Superficie': [superficie],
        'Température': [temperature],
        'Précipitation': [precipitation],
        'Nombre_Jour_Pluie': [nb_jours_pluie],
        'Humidité': [humidite],
        'Vitèsse_Vent': [vent],
        'Durée_Ensoleillement': [ensoleillement]
    })

    new_data_selected = new_data[selected_cat + selected_num]

    # Prédiction
    prediction = reduced_pipeline.predict(new_data_selected)

    st.success(f"🌟 La production prédite est de : **{prediction[0]:.2f} tonne/ha**")



# Footer
st.markdown("---")
st.markdown("📍 Données issues de la source de Base de données du Burkina Faso. © 2025")