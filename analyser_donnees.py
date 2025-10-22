"""
Script principal pour générer les résultats et préparer la soutenance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from supernutriscore import (
    NutriScore, ElectreTri, AnalyseResultats,
    creer_profils_limites, definir_poids_criteres
)

def main():
    print("=" * 80)
    print("SUPERNUTRISCORE - Analyse complète")
    print("=" * 80)
    print()
    
    # 1. Chargement des données
    print("📂 Chargement de la base de données...")
    df = pd.read_csv('base_donnees_boissons.csv', encoding='utf-8')
    df.columns = df.columns.str.strip()
    print(f"✓ {len(df)} produits chargés")
    print()
    
    # 2. Statistiques descriptives
    print("📊 Statistiques descriptives de la base de données")
    print("-" * 80)
    print(f"Nombre total de produits: {len(df)}")
    print(f"\nDistribution des labels Nutri-Score:")
    print(df['Label_Nutriscore'].value_counts().sort_index())
    print(f"\nNombre de catégories: {df['Categorie'].nunique()}")
    print(f"Produits BIO: {(df['Label_Bio'] == 'OUI').sum()} ({(df['Label_Bio'] == 'OUI').sum()/len(df)*100:.1f}%)")
    print()
    
    # 3. Vérification du calcul Nutri-Score
    print("🧮 Vérification du calcul Nutri-Score")
    print("-" * 80)
    
    # Test avec un produit de la base
    produit_test = df.iloc[6]  # Coca Cola
    print(f"Produit test: {produit_test['Nom_Produit']}")
    print(f"Marque: {produit_test['Marque']}")
    
    resultat = NutriScore.calculer_score_nutritionnel(
        produit_test['Energie_kJ'],
        produit_test['Acides_Gras_Satures_g'],
        produit_test['Sucres_g'],
        produit_test['Sodium_mg'],
        produit_test['Proteines_g'],
        produit_test['Fibres_g'],
        produit_test['Fruits_Legumes_Pct']
    )
    
    print(f"\nRésultats:")
    print(f"  Score calculé: {resultat['score']}")
    print(f"  Label calculé: {resultat['label']}")
    print(f"  Score base de données: {produit_test['Score_Nutriscore']}")
    print(f"  Label base de données: {produit_test['Label_Nutriscore']}")
    print(f"  ✓ Concordance: {resultat['label'] == produit_test['Label_Nutriscore']}")
    print()
    
    # 4. Création des profils ELECTRE TRI
    print("📋 Création des profils limites ELECTRE TRI")
    print("-" * 80)
    profils = creer_profils_limites(df)
    print("Profils créés (valeurs pour chaque critère):")
    print(profils)
    print()
    
    # 5. Classification ELECTRE TRI avec λ=0.6
    print("🔬 Classification ELECTRE TRI (λ=0.6)")
    print("-" * 80)
    
    poids = definir_poids_criteres()
    print("Poids des critères:")
    for crit, poids_val in poids.items():
        print(f"  {crit}: {poids_val:.2f}")
    print()
    
    # Procédure pessimiste
    print("Procédure PESSIMISTE:")
    electre_pess = ElectreTri(poids, profils, lambda_seuil=0.6)
    df_pess_06 = electre_pess.classifier_base_donnees(df, 'pessimiste')
    
    print("Distribution des classes:")
    print(df_pess_06['Classe_ELECTRE_Pessimiste'].value_counts().sort_index())
    
    # Matrice de confusion
    df_pess_06['Classe_Clean'] = df_pess_06['Classe_ELECTRE_Pessimiste'].str.replace("'", "")
    matrice_pess_06 = AnalyseResultats.matrice_confusion(
        df_pess_06['Label_Nutriscore'],
        df_pess_06['Classe_Clean']
    )
    
    print("\nMatrice de confusion (Nutri-Score vs ELECTRE TRI Pessimiste):")
    print(matrice_pess_06)
    
    metriques_pess_06 = AnalyseResultats.calculer_metriques(matrice_pess_06)
    print(f"\nAccuracy: {metriques_pess_06['accuracy']:.2%}")
    print()
    
    # Procédure optimiste
    print("Procédure OPTIMISTE:")
    electre_opt = ElectreTri(poids, profils, lambda_seuil=0.6)
    df_opt_06 = electre_opt.classifier_base_donnees(df, 'optimiste')
    
    print("Distribution des classes:")
    print(df_opt_06['Classe_ELECTRE_Optimiste'].value_counts().sort_index())
    
    df_opt_06['Classe_Clean'] = df_opt_06['Classe_ELECTRE_Optimiste'].str.replace("'", "")
    matrice_opt_06 = AnalyseResultats.matrice_confusion(
        df_opt_06['Label_Nutriscore'],
        df_opt_06['Classe_Clean']
    )
    
    print("\nMatrice de confusion (Nutri-Score vs ELECTRE TRI Optimiste):")
    print(matrice_opt_06)
    
    metriques_opt_06 = AnalyseResultats.calculer_metriques(matrice_opt_06)
    print(f"\nAccuracy: {metriques_opt_06['accuracy']:.2%}")
    print()
    
    # 6. Classification ELECTRE TRI avec λ=0.7
    print("🔬 Classification ELECTRE TRI (λ=0.7)")
    print("-" * 80)
    
    # Procédure pessimiste
    print("Procédure PESSIMISTE:")
    electre_pess_07 = ElectreTri(poids, profils, lambda_seuil=0.7)
    df_pess_07 = electre_pess_07.classifier_base_donnees(df, 'pessimiste')
    
    print("Distribution des classes:")
    print(df_pess_07['Classe_ELECTRE_Pessimiste'].value_counts().sort_index())
    
    df_pess_07['Classe_Clean'] = df_pess_07['Classe_ELECTRE_Pessimiste'].str.replace("'", "")
    matrice_pess_07 = AnalyseResultats.matrice_confusion(
        df_pess_07['Label_Nutriscore'],
        df_pess_07['Classe_Clean']
    )
    
    metriques_pess_07 = AnalyseResultats.calculer_metriques(matrice_pess_07)
    print(f"\nAccuracy: {metriques_pess_07['accuracy']:.2%}")
    print()
    
    # Procédure optimiste
    print("Procédure OPTIMISTE:")
    electre_opt_07 = ElectreTri(poids, profils, lambda_seuil=0.7)
    df_opt_07 = electre_opt_07.classifier_base_donnees(df, 'optimiste')
    
    print("Distribution des classes:")
    print(df_opt_07['Classe_ELECTRE_Optimiste'].value_counts().sort_index())
    
    df_opt_07['Classe_Clean'] = df_opt_07['Classe_ELECTRE_Optimiste'].str.replace("'", "")
    matrice_opt_07 = AnalyseResultats.matrice_confusion(
        df_opt_07['Label_Nutriscore'],
        df_opt_07['Classe_Clean']
    )
    
    metriques_opt_07 = AnalyseResultats.calculer_metriques(matrice_opt_07)
    print(f"\nAccuracy: {metriques_opt_07['accuracy']:.2%}")
    print()
    
    # 7. Comparaison des méthodes
    print("📊 Comparaison des méthodes")
    print("-" * 80)
    
    comparaison = pd.DataFrame({
        'Méthode': [
            'ELECTRE TRI Pessimiste (λ=0.6)',
            'ELECTRE TRI Optimiste (λ=0.6)',
            'ELECTRE TRI Pessimiste (λ=0.7)',
            'ELECTRE TRI Optimiste (λ=0.7)'
        ],
        'Accuracy': [
            metriques_pess_06['accuracy'],
            metriques_opt_06['accuracy'],
            metriques_pess_07['accuracy'],
            metriques_opt_07['accuracy']
        ]
    })
    
    print(comparaison.to_string(index=False))
    print()
    
    # 8. Sauvegarde des résultats
    print("💾 Sauvegarde des résultats")
    print("-" * 80)
    
    # Ajouter toutes les colonnes de classification au DataFrame original
    df_final = df.copy()
    df_final['Classe_ELECTRE_Pessimiste_06'] = df_pess_06['Classe_ELECTRE_Pessimiste']
    df_final['Classe_ELECTRE_Optimiste_06'] = df_opt_06['Classe_ELECTRE_Optimiste']
    df_final['Classe_ELECTRE_Pessimiste_07'] = df_pess_07['Classe_ELECTRE_Pessimiste']
    df_final['Classe_ELECTRE_Optimiste_07'] = df_opt_07['Classe_ELECTRE_Optimiste']
    
    # Sauvegarder
    output_file = 'resultats_complets.xlsx'
    df_final.to_excel(output_file, index=False)
    print(f"✓ Résultats sauvegardés dans: {output_file}")
    
    # Sauvegarder les profils
    profils_file = 'profils_limites.csv'
    profils.to_csv(profils_file)
    print(f"✓ Profils limites sauvegardés dans: {profils_file}")
    
    # Sauvegarder les matrices de confusion
    matrices_file = 'matrices_confusion.xlsx'
    with pd.ExcelWriter(matrices_file) as writer:
        matrice_pess_06.to_excel(writer, sheet_name='Pessimiste_06')
        matrice_opt_06.to_excel(writer, sheet_name='Optimiste_06')
        matrice_pess_07.to_excel(writer, sheet_name='Pessimiste_07')
        matrice_opt_07.to_excel(writer, sheet_name='Optimiste_07')
    print(f"✓ Matrices de confusion sauvegardées dans: {matrices_file}")
    
    # Sauvegarder le tableau de comparaison
    comparaison_file = 'comparaison_methodes.csv'
    comparaison.to_csv(comparaison_file, index=False)
    print(f"✓ Comparaison sauvegardée dans: {comparaison_file}")
    print()
    
    # 9. Génération de visualisations
    print("📈 Génération des visualisations")
    print("-" * 80)
    
    # Figure 1: Distribution des labels Nutri-Score
    fig, ax = plt.subplots(figsize=(10, 6))
    labels_count = df['Label_Nutriscore'].value_counts().sort_index()
    colors = ['#038141', '#85BB2F', '#FECB02', '#EE8100', '#E63E11']
    labels_count.plot(kind='bar', ax=ax, color=colors)
    ax.set_title('Distribution des labels Nutri-Score', fontsize=14, fontweight='bold')
    ax.set_xlabel('Label', fontsize=12)
    ax.set_ylabel('Nombre de produits', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig('distribution_nutriscore.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique 1 sauvegardé: distribution_nutriscore.png")
    plt.close()
    
    # Figure 2: Heatmap matrice de confusion (Pessimiste λ=0.6)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(matrice_pess_06, annot=True, fmt='d', cmap='Blues', ax=ax, cbar_kws={'label': 'Nombre de produits'})
    ax.set_title('Matrice de confusion - ELECTRE TRI Pessimiste (λ=0.6)', fontsize=14, fontweight='bold')
    ax.set_xlabel('ELECTRE TRI', fontsize=12)
    ax.set_ylabel('Nutri-Score', fontsize=12)
    plt.tight_layout()
    plt.savefig('matrice_confusion_pessimiste_06.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique 2 sauvegardé: matrice_confusion_pessimiste_06.png")
    plt.close()
    
    # Figure 3: Comparaison des accuracies
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(comparaison))
    bars = ax.bar(x, comparaison['Accuracy'], color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Comparaison des méthodes ELECTRE TRI', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(comparaison['Méthode'], rotation=15, ha='right')
    ax.set_ylim(0, 1)
    ax.grid(axis='y', alpha=0.3)
    
    # Ajouter les valeurs sur les barres
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{comparaison["Accuracy"].iloc[i]:.1%}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('comparaison_accuracies.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique 3 sauvegardé: comparaison_accuracies.png")
    plt.close()
    
    print()
    print("=" * 80)
    print("✅ ANALYSE TERMINÉE AVEC SUCCÈS")
    print("=" * 80)
    print()
    print("📁 Fichiers générés:")
    print("  - resultats_complets.xlsx")
    print("  - profils_limites.csv")
    print("  - matrices_confusion.xlsx")
    print("  - comparaison_methodes.csv")
    print("  - distribution_nutriscore.png")
    print("  - matrice_confusion_pessimiste_06.png")
    print("  - comparaison_accuracies.png")
    print()
    print("🚀 Pour lancer l'interface graphique, exécutez:")
    print("   streamlit run interface_streamlit.py")
    print()

if __name__ == "__main__":
    main()
