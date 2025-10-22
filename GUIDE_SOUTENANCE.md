# 🎤 Guide de Soutenance Intermédiaire
## SuperNutriScore - 24 Octobre 2025

---

## ⏱️ Timing : 15 minutes maximum

### Structure recommandée :
- Introduction : 1 minute
- Base de données : 2 minutes
- Algorithme Nutri-Score + Interface : 3 minutes
- ELECTRE TRI : 4 minutes
- Résultats et Comparaisons : 4 minutes
- Conclusion : 1 minute

---

## 📊 Points clés à présenter

### 1. BASE DE DONNÉES (Slide 3)

**Chiffres à retenir :**
- ✅ 289 produits (boissons)
- ✅ 8 catégories différentes
- ✅ Distribution Nutri-Score : A(28), B(65), C(85), D(50), E(61)
- ✅ 13.1% de produits BIO
- ✅ Toutes les classes représentées (≥20 produits par classe A-E)

**Points à mentionner :**
- Source : Open Food Facts
- Catégorie homogène (boissons) pour des comparaisons pertinentes
- Données nutritionnelles complètes pour les 7 critères
- Inclut également Green-Score et nombre d'additifs

### 2. ALGORITHME NUTRI-SCORE (Slide 4-5)

**Implémentation :**
- ✅ Algorithme officiel version Mars 2025
- ✅ Respect des tables de points
- ✅ Règle spéciale des protéines (score négatif ≥11 et fruits/légumes <80%)
- ✅ Classification en 5 classes (A à E)

**Interface graphique Streamlit :**
- ✅ Saisie interactive des 7 composantes
- ✅ Calcul instantané
- ✅ Affichage visuel avec couleurs officielles
- ✅ Détails du calcul (points positifs/négatifs)
- ✅ Graphiques de répartition

**DÉMONSTRATION LIVE si possible :**
```bash
streamlit run interface_streamlit.py
```
Tester avec un exemple (ex: Coca-Cola)

### 3. ELECTRE TRI (Slide 6)

**Principe :**
- Classification par comparaison à des profils limites (b1 à b6)
- 8 critères (7 du Nutri-Score + nombre d'additifs)
- Transparence : tous les paramètres sont explicites

**8 Critères utilisés :**

À MINIMISER :
1. Énergie (kJ)
2. Acides gras saturés (g)
3. Sucres (g)
4. Sodium (mg)
5. Nombre d'additifs

À MAXIMISER :
6. Protéines (g)
7. Fibres (g)
8. Fruits/Légumes/Noix (%)

**Profils limites :**
- b1 à b6 : définis par quantiles de la base
- b6 = meilleur profil, b1 = moins bon profil
- Permet de séparer les 5 classes (A' à E')

**Poids des critères (à justifier) :**
```
Énergie : 15%          (impact santé important)
Sucres : 15%           (problème de santé publique)
Sodium : 15%           (maladies cardiovasculaires)
Fruits/Légumes : 15%   (composante nutritionnelle positive)
AG saturés : 10%       (facteur de risque)
Protéines : 10%        (apport bénéfique)
Fibres : 10%           (santé digestive)
Additifs : 10%         (naturalité du produit)
```

**Seuils de majorité testés :**
- λ = 0.6 (60% des critères doivent être favorables)
- λ = 0.7 (70% des critères doivent être favorables)

**Deux procédures :**
- **Pessimiste** : descend de b6 vers b1
  → Plus conservative, tend vers des classes moins bonnes
- **Optimiste** : monte de b1 vers b6
  → Plus favorable, tend vers des classes meilleures

### 4. RÉSULTATS (Slide 7)

**Taux de concordance avec Nutri-Score :**

| Méthode | λ=0.6 | λ=0.7 |
|---------|-------|-------|
| Pessimiste | **32.5%** | 31.1% |
| Optimiste | 24.2% | 22.1% |

**Analyse des résultats :**

✅ **Ce qui fonctionne bien :**
- La procédure pessimiste est plus cohérente avec le Nutri-Score
- λ=0.6 donne de meilleurs résultats que λ=0.7
- Les deux méthodes classifient correctement les extrêmes (A et E)

⚠️ **Explications de l'accuracy modérée :**
1. **Philosophies différentes :**
   - Nutri-Score = formule arithmétique simple
   - ELECTRE TRI = approche multicritère avec compensation limitée

2. **Différence dans l'importance des critères :**
   - Nutri-Score : poids implicites dans les tables de points
   - ELECTRE TRI : poids explicites et paramètrables

3. **Nombre d'additifs :**
   - Absent du Nutri-Score
   - Pris en compte dans ELECTRE TRI → classifications différentes

4. **C'est POSITIF pour la suite :**
   - Montre que les deux approches sont complémentaires
   - Justifie le SuperNutri-Score qui les combinera

**Matrices de confusion :**
- Disponibles dans les fichiers générés
- Montrent où les désaccords se situent
- Classe C : zone de transition, classifications variables

### 5. DÉMONSTRATIONS POSSIBLES

**Si temps disponible, montrer :**

1. **Fichier Excel des résultats** (`resultats_complets.xlsx`)
   - Comparaison côte à côte des classifications
   - Exemples de produits classés différemment

2. **Graphiques générés** :
   - Distribution Nutri-Score
   - Matrice de confusion (heatmap)
   - Comparaison des accuracies

3. **Interface Streamlit** (page ELECTRE TRI)
   - Lancer une classification avec différents paramètres
   - Montrer l'impact du changement de λ

---

## 🎯 Messages clés à faire passer

### Accomplissements

1. ✅ **Base de données complète** (289 produits, toutes classes représentées)

2. ✅ **Nutri-Score implémenté** avec interface graphique fonctionnelle

3. ✅ **ELECTRE TRI opérationnel** avec deux procédures testées

4. ✅ **Comparaisons effectuées** avec différents paramètres (λ=0.6 et 0.7)

5. ✅ **Résultats documentés** avec matrices de confusion et métriques

### Points de discussion

**Question attendue : "Pourquoi l'accuracy n'est que de 32% ?"**

**Réponse structurée :**
1. C'est attendu et même souhaitable ! Les deux méthodes ont des philosophies différentes.
2. Nutri-Score = formule fixe, ELECTRE TRI = approche multicritère paramétrable
3. ELECTRE TRI intègre les additifs (absents du Nutri-Score)
4. L'objectif du SuperNutri-Score est justement de combiner les forces des deux approches
5. Une accuracy de 100% signifierait qu'ELECTRE TRI n'apporte rien de nouveau

**Question possible : "Comment avez-vous choisi les poids ?"**

**Réponse :**
1. Première approche : équilibrage entre critères négatifs et positifs
2. Importance relative basée sur impacts santé connus
3. Énergie, Sucres, Sodium, Fruits/Légumes = 15% (critères majeurs)
4. Autres critères = 10% (importants mais secondaires)
5. Pour la soutenance finale : optimisation possible via tests de sensibilité

**Question possible : "Comment avez-vous défini les profils ?"**

**Réponse :**
1. Méthode statistique : quantiles de la base de données
2. b6 = valeurs extrêmes favorables (10% du min pour critères à minimiser)
3. b2, b3, b4, b5 = quantiles 20%, 40%, 60%, 80%
4. b1 = valeurs extrêmes défavorables (150% du max pour critères à minimiser)
5. Garantit une répartition cohérente avec la distribution observée

---

## 🔮 Prochaines étapes (Slide 8)

### Pour la soutenance finale :

1. **SuperNutri-Score** (modèle combiné)
   - Intégration Green-Score (impact environnemental)
   - Intégration label BIO
   - Règles d'association transparentes

2. **Interface complète**
   - Paramètres ELECTRE TRI modifiables
   - Visualisation des 3 scores côte à côte
   - Recommandations personnalisées

3. **Analyses approfondies**
   - Tests sur autres bases de données
   - Validation croisée
   - Optimisation des paramètres

---

## 💡 Conseils pour la présentation

### À FAIRE :
✅ Montrer les fichiers et résultats concrets
✅ Utiliser les graphiques générés
✅ Être précis sur les chiffres
✅ Expliquer les choix méthodologiques
✅ Anticiper les questions sur l'accuracy
✅ Montrer l'interface en live si possible

### À ÉVITER :
❌ S'excuser pour l'accuracy "faible"
❌ Entrer dans trop de détails techniques
❌ Lire les slides mot pour mot
❌ Dépasser 15 minutes
❌ Oublier de conclure sur la suite

---

## 📋 Checklist avant la soutenance

- [ ] Tester l'interface Streamlit (vérifier qu'elle se lance)
- [ ] Avoir les fichiers de résultats accessibles
- [ ] Préparer 1-2 exemples de produits à montrer
- [ ] Répéter le timing (max 15 min)
- [ ] Anticiper 3-4 questions probables
- [ ] Avoir la présentation PowerPoint ouverte
- [ ] Vérifier que tous les graphiques s'affichent

---

## 🎬 Ouverture suggérée

"Bonjour à tous. Nous allons vous présenter SuperNutriScore, un système d'évaluation 
transparent des aliments. Notre objectif est de proposer une alternative au Nutri-Score 
en utilisant ELECTRE TRI, une méthode d'aide multicritère à la décision qui permet 
d'expliciter tous les paramètres de classification.

Aujourd'hui, nous vous présenterons notre base de données de 289 boissons, l'implémentation 
du Nutri-Score avec son interface graphique, la méthode ELECTRE TRI que nous avons 
développée, et enfin une comparaison détaillée des résultats obtenus."

---

## 🏁 Conclusion suggérée

"En conclusion, nous avons :
1. Constitué une base de données complète de 289 boissons
2. Implémenté l'algorithme officiel du Nutri-Score avec une interface graphique
3. Développé et testé ELECTRE TRI avec différents paramètres
4. Comparé les deux approches, montrant qu'elles sont complémentaires

Les résultats montrent que les deux méthodes ont des philosophies différentes, ce qui 
justifie notre objectif de les combiner dans le SuperNutri-Score. D'ici la soutenance 
finale, nous intégrerons le Green-Score et le label BIO pour créer un modèle d'évaluation 
complet et transparent.

Merci pour votre attention. Avez-vous des questions ?"

---

## 📞 Support technique

**Si problème avec Streamlit :**
```bash
cd /chemin/vers/projet
streamlit run interface_streamlit.py
```

**Si problème de dépendances :**
```bash
pip install pandas numpy matplotlib seaborn plotly streamlit openpyxl
```

**Fichiers essentiels à avoir :**
- supernutriscore.py
- interface_streamlit.py
- base_donnees_boissons.csv
- Presentation_SuperNutriScore.pptx

---

**Bonne soutenance ! 🚀**
