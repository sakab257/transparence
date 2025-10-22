"""
Interface graphique pour le SuperNutriScore
Application Streamlit pour calculer et comparer Nutri-Score et ELECTRE TRI
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from supernutriscore import (
    NutriScore, ElectreTri, AnalyseResultats,
    creer_profils_limites, definir_poids_criteres
)

# Configuration de la page
st.set_page_config(
    page_title="SuperNutriScore",
    page_icon="🥗",
    layout="wide"
)

# Titre principal
st.title("🥗 SuperNutriScore")
st.markdown("### Évaluation transparente des aliments : Nutri-Score & ELECTRE TRI")

# Sidebar pour la navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Accueil", "🧮 Calculateur Nutri-Score", 
     "📊 ELECTRE TRI", "📈 Analyse Comparative"]
)

# Chargement de la base de données
@st.cache_data
def charger_donnees():
    """Charge la base de données des boissons"""
    try:
        df = pd.read_csv('base_donnees_boissons.csv', encoding='utf-8')
        # Nettoyer les colonnes
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return None

df = charger_donnees()

# ============================================================================
# PAGE ACCUEIL
# ============================================================================
if page == "🏠 Accueil":
    st.markdown("""
    ## Bienvenue dans SuperNutriScore !
    
    Cette application vous permet de :
    
    ### 🧮 Calculer le Nutri-Score
    - Entrez les valeurs nutritionnelles d'un produit
    - Obtenez instantanément le score et le label (A à E)
    - Visualisez les détails du calcul
    
    ### 📊 Appliquer ELECTRE TRI
    - Classifiez les produits avec la méthode ELECTRE TRI
    - Procédures pessimiste et optimiste
    - Paramètres personnalisables (poids, seuils)
    
    ### 📈 Comparer les méthodes
    - Matrices de confusion
    - Métriques de performance
    - Statistiques descriptives
    
    ---
    
    ### 📋 Base de données
    """)
    
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Nombre de produits", len(df))
        
        with col2:
            n_categories = df['Label_Nutriscore'].nunique()
            st.metric("Catégories Nutri-Score", n_categories)
        
        with col3:
            n_marques = df['Marque'].nunique()
            st.metric("Nombre de marques", n_marques)
        
        with col4:
            pct_bio = (df['Label_Bio'] == 'OUI').sum() / len(df) * 100
            st.metric("% Bio", f"{pct_bio:.1f}%")
        
        # Distribution des labels
        st.markdown("#### Distribution des labels Nutri-Score")
        
        labels_count = df['Label_Nutriscore'].value_counts().sort_index()
        
        fig = px.bar(
            x=labels_count.index,
            y=labels_count.values,
            labels={'x': 'Label Nutri-Score', 'y': 'Nombre de produits'},
            color=labels_count.index,
            color_discrete_map={
                'A': '#038141',
                'B': '#85BB2F',
                'C': '#FECB02',
                'D': '#EE8100',
                'E': '#E63E11'
            }
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Aperçu des données
        st.markdown("#### Aperçu de la base de données")
        st.dataframe(df.head(50), use_container_width=True)

# ============================================================================
# PAGE CALCULATEUR NUTRI-SCORE
# ============================================================================
elif page == "🧮 Calculateur Nutri-Score":
    st.markdown("## 🧮 Calculateur Nutri-Score")
    st.markdown("Entrez les informations nutritionnelles pour 100g/100ml de produit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Composantes à limiter")
        energie_kj = st.number_input(
            "Énergie (kJ)", 
            min_value=0.0, 
            max_value=5000.0, 
            value=180.0,
            help="Valeur énergétique en kilojoules"
        )
        
        acides_gras = st.number_input(
            "Acides gras saturés (g)", 
            min_value=0.0, 
            max_value=50.0, 
            value=0.0,
            help="Quantité d'acides gras saturés"
        )
        
        sucres = st.number_input(
            "Sucres (g)", 
            min_value=0.0, 
            max_value=100.0, 
            value=10.6,
            help="Quantité de sucres"
        )
        
        sodium = st.number_input(
            "Sodium (mg)", 
            min_value=0.0, 
            max_value=5000.0, 
            value=0.0,
            help="Quantité de sodium"
        )
    
    with col2:
        st.markdown("### 🟢 Composantes à favoriser")
        proteines = st.number_input(
            "Protéines (g)", 
            min_value=0.0, 
            max_value=50.0, 
            value=0.0,
            help="Quantité de protéines"
        )
        
        fibres = st.number_input(
            "Fibres (g)", 
            min_value=0.0, 
            max_value=50.0, 
            value=0.0,
            help="Quantité de fibres"
        )
        
        fruits_legumes = st.number_input(
            "Fruits/Légumes/Noix (%)", 
            min_value=0, 
            max_value=100, 
            value=0,
            help="Pourcentage de fruits, légumes, légumineuses et noix"
        )
    
    # Bouton de calcul
    if st.button("🧮 Calculer le Nutri-Score", type="primary"):
        resultat = NutriScore.calculer_score_nutritionnel(
            energie_kj, acides_gras, sucres, sodium,
            proteines, fibres, fruits_legumes
        )
        
        # Affichage du résultat
        st.markdown("---")
        st.markdown("## 🎯 Résultat")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f"### Score: **{resultat['score']}**")
        
        with col2:
            # Affichage du label avec couleur
            couleurs = {
                'A': '#038141',
                'B': '#85BB2F',
                'C': '#FECB02',
                'D': '#EE8100',
                'E': '#E63E11'
            }
            label = resultat['label']
            st.markdown(
                f"<div style='background-color: {couleurs[label]}; "
                f"padding: 30px; border-radius: 10px; text-align: center;'>"
                f"<h1 style='color: white; margin: 0;'>Label: {label}</h1>"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col3:
            if label in ['A', 'B']:
                st.success("✅ Bonne qualité nutritionnelle")
            elif label == 'C':
                st.warning("⚠️ Qualité nutritionnelle moyenne")
            else:
                st.error("❌ À consommer avec modération")
        
        # Détails du calcul
        st.markdown("### 📊 Détails du calcul")
        
        details = resultat['details']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔴 Points négatifs")
            st.write(f"- Énergie: **{details['points_energie']}** points")
            st.write(f"- Acides gras saturés: **{details['points_acides_gras_satures']}** points")
            st.write(f"- Sucres: **{details['points_sucres']}** points")
            st.write(f"- Sodium: **{details['points_sodium']}** points")
            st.write(f"**Total négatif: {details['score_negatif']} points**")
        
        with col2:
            st.markdown("#### 🟢 Points positifs")
            if details['proteines_comptees']:
                st.write(f"- Protéines: **{details['points_proteines']}** points")
            else:
                st.write(f"- Protéines: ~~{details['points_proteines']}~~ **0** points (non comptées)")
            st.write(f"- Fibres: **{details['points_fibres']}** points")
            st.write(f"- Fruits/Légumes: **{details['points_fruits_legumes']}** points")
            st.write(f"**Total positif: {details['score_positif']} points**")
        
        # Graphique de répartition
        fig = go.Figure(data=[
            go.Bar(
                name='Négatif',
                x=['Énergie', 'AG Saturés', 'Sucres', 'Sodium'],
                y=[details['points_energie'], details['points_acides_gras_satures'],
                   details['points_sucres'], details['points_sodium']],
                marker_color='#E63E11'
            ),
            go.Bar(
                name='Positif',
                x=['Protéines', 'Fibres', 'Fruits/Légumes'],
                y=[details['points_proteines'], details['points_fibres'],
                   details['points_fruits_legumes']],
                marker_color='#038141'
            )
        ])
        
        fig.update_layout(
            title="Répartition des points",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE ELECTRE TRI
# ============================================================================
elif page == "📊 ELECTRE TRI":
    st.markdown("## 📊 Classification ELECTRE TRI")
    
    if df is None:
        st.error("Impossible de charger la base de données")
    else:
        # Paramètres
        st.sidebar.markdown("### ⚙️ Paramètres ELECTRE TRI")
        
        lambda_seuil = st.sidebar.slider(
            "Seuil de majorité (λ)",
            min_value=0.5,
            max_value=1.0,
            value=0.6,
            step=0.05,
            help="Seuil de concordance pour le surclassement"
        )
        
        methode = st.sidebar.radio(
            "Procédure d'affectation",
            ["Pessimiste", "Optimiste"],
            help="Pessimiste: plus conservateur, Optimiste: plus favorable"
        )
        
        # Définir les poids
        st.sidebar.markdown("#### Poids des critères")
        
        poids = {}
        criteres_noms = {
            'Energie_kJ': 'Énergie',
            'Acides_Gras_Satures_g': 'Acides gras saturés',
            'Sucres_g': 'Sucres',
            'Sodium_mg': 'Sodium',
            'Proteines_g': 'Protéines',
            'Fibres_g': 'Fibres',
            'Fruits_Legumes_Pct': 'Fruits/Légumes',
            'Nombre_Additifs': 'Additifs'
        }
        
        poids_default = definir_poids_criteres()
        
        for crit, nom in criteres_noms.items():
            poids[crit] = st.sidebar.slider(
                nom,
                min_value=0.0,
                max_value=1.0,
                value=poids_default[crit],
                step=0.05
            )
        
        # Normaliser les poids
        somme_poids = sum(poids.values())
        if somme_poids > 0:
            poids = {k: v/somme_poids for k, v in poids.items()}
        
        st.sidebar.info(f"Somme des poids normalisés: {sum(poids.values()):.2f}")
        
        # Bouton pour lancer la classification
        if st.button("🚀 Lancer la classification ELECTRE TRI", type="primary"):
            with st.spinner("Classification en cours..."):
                # Créer les profils
                profils = creer_profils_limites(df)
                
                # Afficher les profils
                st.markdown("### 📋 Profils limites")
                st.dataframe(profils.T, use_container_width=True)
                
                # Classifier
                electre = ElectreTri(poids, profils, lambda_seuil)
                
                methode_str = methode.lower()
                df_resultat = electre.classifier_base_donnees(df, methode_str)
                
                colonne_classe = f'Classe_ELECTRE_{methode}'
                
                # Afficher les résultats
                st.markdown(f"### 🎯 Résultats - Procédure {methode}")
                
                # Distribution des classes
                classes_count = df_resultat[colonne_classe].value_counts().sort_index()
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(
                        x=classes_count.index,
                        y=classes_count.values,
                        labels={'x': 'Classe ELECTRE TRI', 'y': 'Nombre de produits'},
                        title=f"Distribution des classes - {methode}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### Statistiques")
                    for classe in classes_count.index:
                        pct = classes_count[classe] / len(df) * 100
                        st.write(f"**{classe}**: {classes_count[classe]} ({pct:.1f}%)")
                
                # Comparaison avec Nutri-Score
                st.markdown("### 📊 Comparaison avec Nutri-Score")
                
                # Préparer les données pour la comparaison
                df_comp = df_resultat.copy()
                df_comp['Classe_ELECTRE_Clean'] = df_comp[colonne_classe].str.replace("'", "")
                
                # Matrice de confusion
                matrice = AnalyseResultats.matrice_confusion(
                    df_comp['Label_Nutriscore'],
                    df_comp['Classe_ELECTRE_Clean']
                )
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### Matrice de confusion")
                    st.dataframe(matrice, use_container_width=True)
                    
                    # Heatmap
                    fig = px.imshow(
                        matrice.values,
                        labels=dict(x="ELECTRE TRI", y="Nutri-Score", color="Nombre"),
                        x=matrice.columns,
                        y=matrice.index,
                        color_continuous_scale='Blues',
                        text_auto=True
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Métriques
                    metriques = AnalyseResultats.calculer_metriques(matrice)
                    
                    st.markdown("#### Métriques globales")
                    st.metric("Accuracy", f"{metriques['accuracy']:.2%}")
                    
                    st.markdown("#### Par classe")
                    for classe, metrics in metriques['par_classe'].items():
                        with st.expander(f"Classe {classe}"):
                            st.write(f"Précision: **{metrics['precision']:.2%}**")
                            st.write(f"Rappel: **{metrics['rappel']:.2%}**")
                            st.write(f"F1-Score: **{metrics['f1_score']:.2%}**")
                
                # Tableau des résultats
                st.markdown("### 📋 Tableau des résultats")
                colonnes_affichage = [
                    'Nom_Produit', 'Marque', 'Label_Nutriscore',
                    colonne_classe, 'Score_Nutriscore', 'Nombre_Additifs'
                ]
                st.dataframe(
                    df_resultat[colonnes_affichage].head(20),
                    use_container_width=True
                )
                
                # Téléchargement
                csv = df_resultat.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="📥 Télécharger les résultats (CSV)",
                    data=csv,
                    file_name=f"resultats_electre_{methode.lower()}_{lambda_seuil}.csv",
                    mime="text/csv"
                )

# ============================================================================
# PAGE ANALYSE COMPARATIVE
# ============================================================================
elif page == "📈 Analyse Comparative":
    st.markdown("## 📈 Analyse Comparative Approfondie")
    
    if df is None:
        st.error("Impossible de charger la base de données")
    else:
        st.markdown("""
        Cette page permet de comparer en détail les résultats du Nutri-Score 
        avec ceux d'ELECTRE TRI pour différents paramètres.
        """)
        
        # Comparaison des deux procédures avec λ=0.6 et λ=0.7
        st.markdown("### 🔬 Test avec différents seuils")
        
        col1, col2 = st.columns(2)
        
        resultats_comparaison = []
        
        for lambda_val in [0.6, 0.7]:
            for methode in ['pessimiste', 'optimiste']:
                # Créer les profils
                profils = creer_profils_limites(df)
                poids = definir_poids_criteres()
                
                # Classifier
                electre = ElectreTri(poids, profils, lambda_val)
                df_temp = electre.classifier_base_donnees(df, methode)
                
                colonne = f'Classe_ELECTRE_{methode.capitalize()}'
                df_temp['Classe_Clean'] = df_temp[colonne].str.replace("'", "")
                
                # Calculer accuracy
                matrice = AnalyseResultats.matrice_confusion(
                    df_temp['Label_Nutriscore'],
                    df_temp['Classe_Clean']
                )
                metriques = AnalyseResultats.calculer_metriques(matrice)
                
                resultats_comparaison.append({
                    'Lambda': lambda_val,
                    'Méthode': methode.capitalize(),
                    'Accuracy': metriques['accuracy']
                })
        
        df_comp = pd.DataFrame(resultats_comparaison)
        
        # Graphique de comparaison
        fig = px.bar(
            df_comp,
            x='Méthode',
            y='Accuracy',
            color='Lambda',
            barmode='group',
            title="Accuracy selon le seuil λ et la méthode",
            labels={'Accuracy': 'Taux de concordance', 'Lambda': 'Seuil λ'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau des résultats
        st.dataframe(df_comp, use_container_width=True)
        
        # Analyse par catégorie
        st.markdown("### 📊 Analyse par catégorie de produits")
        
        if 'Categorie' in df.columns:
            categories = df['Categorie'].value_counts().head(5)
            
            for categorie in categories.index:
                with st.expander(f"📂 {categorie} ({categories[categorie]} produits)"):
                    df_cat = df[df['Categorie'] == categorie]
                    
                    # Statistiques
                    stats = df_cat[['Energie_kcal', 'Sucres_g', 'Proteines_g', 
                                   'Nombre_Additifs']].describe()
                    st.dataframe(stats.T, use_container_width=True)
                    
                    # Distribution Nutri-Score
                    labels_dist = df_cat['Label_Nutriscore'].value_counts()
                    fig = px.pie(
                        values=labels_dist.values,
                        names=labels_dist.index,
                        title=f"Distribution Nutri-Score - {categorie}"
                    )
                    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>SuperNutriScore - Projet M2 ID-SITN - Année 2025/2026</p>
    <p>Méthodes d'Aide Multicritère à la Décision</p>
</div>
""", unsafe_allow_html=True)
