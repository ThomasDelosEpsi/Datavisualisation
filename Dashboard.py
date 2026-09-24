import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth

# Charger les données des résultats d'élections (fichier CSV)
data = pd.read_csv('communes_votes.csv')  # Assurez-vous que votre fichier contient les colonnes appropriées

# Afficher les colonnes du CSV pour vérifier les noms
print(data.columns)

# Charger les données géographiques (fichier shapefile ou GeoJSON)
geo_data = gpd.read_file('communes-20220101.shp')  # Remplacez par votre fichier shapefile ou GeoJSON

# Afficher les colonnes du shapefile pour vérifier le nom de la commune
print(geo_data.columns)

# Supposons que le shapefile contient une colonne 'nom_commune', qui est l'identifiant des communes
# Assurez-vous que les noms des communes dans le fichier CSV et shapefile correspondent

# Fusionner les données géographiques avec les résultats des élections
# Remplacez 'nom_commune' par le nom correct de la colonne dans votre shapefile

merged = geo_data.set_index('nom_commune').join(data.set_index('Commune'))

# Création de la carte centrée sur la région Savoie et Haute-Savoie
m = folium.Map(location=[45.9, 6.5], zoom_start=10)

# Créer une couche choroplèthe pour afficher les résultats en couleur
choropleth = Choropleth(
    geo_data=geo_data,
    data=merged,
    columns=['Commune', 'Macron PCT'],  # Remplacez 'Macron PCT' par la colonne que vous voulez visualiser
    key_on='feature.properties.nom_commune',  # Assurez-vous que le nom de la colonne dans le shapefile est correct
    fill_color='YlGnBu',  # Palette de couleurs
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Pourcentage de vote"
).add_to(m)

# Ajouter des marqueurs avec le nom des communes et les pourcentages de vote
for _, row in merged.iterrows():
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],  # Centrer les markers dans chaque commune
        popup=f"{row['Commune']}<br>Macron: {row['Macron PCT']}%",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Enregistrer la carte dans un fichier HTML
m.save('carte_elections_savoie.html')
