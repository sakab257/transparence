"""
SuperNutriScore - Projet M2 ID-SITN
Implémentation du Nutri-score et ELECTRE TRI pour l'évaluation des aliments
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List


class NutriScore:
    """Classe pour calculer le Nutri-Score selon la méthodologie officielle"""
    
    # Tables de points pour les composantes négatives
    ENERGIE_POINTS = [
        (335, 0), (670, 1), (1005, 2), (1340, 3), (1675, 4),
        (2010, 5), (2345, 6), (2680, 7), (3015, 8), (3350, 9), (float('inf'), 10)
    ]
    
    ACIDES_GRAS_SATURES_POINTS = [
        (1, 0), (2, 1), (3, 2), (4, 3), (5, 4),
        (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (float('inf'), 10)
    ]
    
    SUCRES_POINTS = [
        (3.4, 0), (6.8, 1), (10, 2), (14, 3), (17, 4), (20, 5),
        (24, 6), (27, 7), (31, 8), (34, 9), (37, 10), (41, 11),
        (44, 12), (48, 13), (51, 14), (float('inf'), 15)
    ]
    
    SODIUM_POINTS = [
        (90, 0), (180, 1), (270, 2), (360, 3), (450, 4), (540, 5),
        (630, 6), (720, 7), (810, 8), (900, 9), (990, 10), (1080, 11),
        (1170, 12), (1260, 13), (1350, 14), (1440, 15), (1530, 16),
        (1620, 17), (1710, 18), (1800, 19), (float('inf'), 20)
    ]
    
    # Tables de points pour les composantes positives
    PROTEINES_POINTS = [
        (2.4, 0), (4.8, 1), (7.2, 2), (9.6, 3), (12, 4),
        (14, 5), (17, 6), (float('inf'), 7)
    ]
    
    FIBRES_POINTS = [
        (3.0, 0), (4.1, 1), (5.2, 2), (6.3, 3), (7.4, 4), (float('inf'), 5)
    ]
    
    FRUITS_LEGUMES_POINTS = [
        (40, 0), (60, 1), (80, 2), (float('inf'), 5)
    ]
    
    # Seuils pour les classes
    CLASSES = [
        (-float('inf'), 0, 'A', 'Vert foncé'),
        (0, 2, 'B', 'Vert clair'),
        (3, 10, 'C', 'Jaune'),
        (11, 18, 'D', 'Orange clair'),
        (19, float('inf'), 'E', 'Orange foncé')
    ]
    
    @staticmethod
    def get_points(valeur: float, table: List[Tuple]) -> int:
        """Retourne les points selon la table donnée"""
        for seuil, points in table:
            if valeur < seuil:
                return points
        return table[-1][1]
    
    @classmethod
    def calculer_score_nutritionnel(cls, 
                                   energie_kj: float,
                                   acides_gras_satures: float,
                                   sucres: float,
                                   sodium: float,
                                   proteines: float,
                                   fibres: float,
                                   fruits_legumes: float) -> Dict:
        """
        Calcule le score nutritionnel selon la méthodologie Nutri-Score
        
        Returns:
            Dict contenant le score, le label et les détails de calcul
        """
        # Calcul des points négatifs
        points_energie = cls.get_points(energie_kj, cls.ENERGIE_POINTS)
        points_ag_sat = cls.get_points(acides_gras_satures, cls.ACIDES_GRAS_SATURES_POINTS)
        points_sucres = cls.get_points(sucres, cls.SUCRES_POINTS)
        points_sodium = cls.get_points(sodium, cls.SODIUM_POINTS)
        
        score_negatif = points_energie + points_ag_sat + points_sucres + points_sodium
        
        # Calcul des points positifs
        points_proteines = cls.get_points(proteines, cls.PROTEINES_POINTS)
        points_fibres = cls.get_points(fibres, cls.FIBRES_POINTS)
        points_fruits_legumes = cls.get_points(fruits_legumes, cls.FRUITS_LEGUMES_POINTS)
        
        # Règle spéciale : si score négatif >= 11 et fruits/légumes < 80%,
        # les protéines ne comptent pas
        if score_negatif >= 11 and fruits_legumes < 80:
            score_positif = points_fibres + points_fruits_legumes
            proteines_comptees = False
        else:
            score_positif = points_proteines + points_fibres + points_fruits_legumes
            proteines_comptees = True
        
        # Score final
        score_final = score_negatif - score_positif
        
        # Détermination de la classe
        label = 'E'  # Par défaut
        for min_val, max_val, classe, couleur in cls.CLASSES:
            if min_val <= score_final <= max_val:
                label = classe
                break
        
        return {
            'score': score_final,
            'label': label,
            'details': {
                'score_negatif': score_negatif,
                'score_positif': score_positif,
                'points_energie': points_energie,
                'points_acides_gras_satures': points_ag_sat,
                'points_sucres': points_sucres,
                'points_sodium': points_sodium,
                'points_proteines': points_proteines if proteines_comptees else 0,
                'points_fibres': points_fibres,
                'points_fruits_legumes': points_fruits_legumes,
                'proteines_comptees': proteines_comptees
            }
        }
    
    @classmethod
    def get_label_from_score(cls, score: int) -> str:
        """Retourne le label correspondant à un score"""
        for min_val, max_val, classe, couleur in cls.CLASSES:
            if min_val <= score <= max_val:
                return classe
        return 'E'


class ElectreTri:
    """Classe pour implémenter la méthode ELECTRE TRI"""
    
    def __init__(self, poids: Dict[str, float], profils: pd.DataFrame, 
                 lambda_seuil: float = 0.6):
        """
        Initialise ELECTRE TRI
        
        Args:
            poids: Dictionnaire des poids pour chaque critère
            profils: DataFrame contenant les 6 profils (b1 à b6)
            lambda_seuil: Seuil de majorité (entre 0 et 1)
        """
        self.poids = poids
        self.profils = profils
        self.lambda_seuil = lambda_seuil
        self.criteres_a_minimiser = ['Energie_kJ', 'Acides_Gras_Satures_g', 
                                     'Sucres_g', 'Sodium_mg', 'Nombre_Additifs']
        self.criteres_a_maximiser = ['Proteines_g', 'Fibres_g', 'Fruits_Legumes_Pct']
    
    def concordance_partielle(self, aliment: pd.Series, profil: pd.Series, 
                             critere: str) -> Tuple[float, float]:
        """
        Calcule les indices de concordance partiels c(a,b) et c(b,a)
        
        Returns:
            Tuple (c(aliment, profil), c(profil, aliment))
        """
        val_aliment = aliment[critere]
        val_profil = profil[critere]
        
        if critere in self.criteres_a_maximiser:
            # Critère à maximiser
            c_ab = 1.0 if val_aliment >= val_profil else 0.0
            c_ba = 1.0 if val_profil >= val_aliment else 0.0
        else:
            # Critère à minimiser
            c_ab = 1.0 if val_profil >= val_aliment else 0.0
            c_ba = 1.0 if val_aliment >= val_profil else 0.0
        
        return c_ab, c_ba
    
    def concordance_globale(self, aliment: pd.Series, profil: pd.Series) -> Tuple[float, float]:
        """
        Calcule les indices de concordance globaux C(a,b) et C(b,a)
        
        Returns:
            Tuple (C(aliment, profil), C(profil, aliment))
        """
        somme_poids = sum(self.poids.values())
        
        C_ab = 0.0
        C_ba = 0.0
        
        for critere, poids in self.poids.items():
            c_ab, c_ba = self.concordance_partielle(aliment, profil, critere)
            C_ab += poids * c_ab
            C_ba += poids * c_ba
        
        C_ab /= somme_poids
        C_ba /= somme_poids
        
        return C_ab, C_ba
    
    def surclassement(self, aliment: pd.Series, profil: pd.Series) -> Tuple[bool, bool]:
        """
        Détermine les relations de surclassement
        
        Returns:
            Tuple (a_S_b, b_S_a) où S signifie "surclasse"
        """
        C_ab, C_ba = self.concordance_globale(aliment, profil)
        
        a_S_b = C_ab >= self.lambda_seuil
        b_S_a = C_ba >= self.lambda_seuil
        
        return a_S_b, b_S_a
    
    def affectation_pessimiste(self, aliment: pd.Series) -> str:
        """
        Procédure d'affectation pessimiste
        
        Returns:
            Classe affectée (A', B', C', D', E')
        """
        # Les profils sont ordonnés de b6 à b1
        # Classes: A' (meilleure) à E' (moins bonne)
        classes = ["A'", "B'", "C'", "D'", "E'"]
        
        # Comparer successivement à b6, b5, b4, b3, b2, b1
        # b6 sépare A' de B', b5 sépare B' de C', etc.
        for i in range(6, 0, -1):  # De b6 à b1
            profil_name = f'b{i}'
            profil = self.profils.loc[profil_name]
            
            a_S_b, b_S_a = self.surclassement(aliment, profil)
            
            # Si l'aliment surclasse le profil bi, il est affecté à la classe Ci
            if a_S_b:
                # b6 -> A', b5 -> B', b4 -> C', b3 -> D', b2 -> E', b1 -> E'
                if i == 6:
                    return "A'"
                elif i == 5:
                    return "B'"
                elif i == 4:
                    return "C'"
                elif i == 3:
                    return "D'"
                else:
                    return "E'"
        
        # Si aucun surclassement, affecter à la classe la plus basse
        return "E'"
    
    def affectation_optimiste(self, aliment: pd.Series) -> str:
        """
        Procédure d'affectation optimiste
        
        Returns:
            Classe affectée (A', B', C', D', E')
        """
        # Comparer successivement à b1, b2, b3, b4, b5, b6
        for i in range(1, 7):  # De b1 à b6
            profil_name = f'b{i}'
            profil = self.profils.loc[profil_name]
            
            a_S_b, b_S_a = self.surclassement(aliment, profil)
            
            # Si le profil surclasse l'aliment ET l'aliment ne surclasse pas le profil
            if b_S_a and not a_S_b:
                # b1 -> E', b2 -> D', b3 -> C', b4 -> B', b5 -> A', b6 -> A'
                if i == 1:
                    return "E'"
                elif i == 2:
                    return "D'"
                elif i == 3:
                    return "C'"
                elif i == 4:
                    return "B'"
                else:
                    return "A'"
        
        # Si aucune condition remplie, affecter à la classe la plus haute
        return "A'"
    
    def classifier_base_donnees(self, df: pd.DataFrame, 
                               methode: str = 'pessimiste') -> pd.DataFrame:
        """
        Classifie tous les produits d'une base de données
        
        Args:
            df: DataFrame contenant les produits
            methode: 'pessimiste' ou 'optimiste'
        
        Returns:
            DataFrame avec une nouvelle colonne contenant la classe affectée
        """
        resultats = []
        
        for idx, aliment in df.iterrows():
            if methode == 'pessimiste':
                classe = self.affectation_pessimiste(aliment)
            else:
                classe = self.affectation_optimiste(aliment)
            
            resultats.append(classe)
        
        df_resultat = df.copy()
        colonne_nom = f'Classe_ELECTRE_{methode.capitalize()}'
        df_resultat[colonne_nom] = resultats
        
        return df_resultat


class AnalyseResultats:
    """Classe pour analyser et comparer les résultats"""
    
    @staticmethod
    def matrice_confusion(vraies_classes: pd.Series, 
                         classes_predites: pd.Series) -> pd.DataFrame:
        """Calcule la matrice de confusion"""
        classes = ['A', 'B', 'C', 'D', 'E']
        
        # Créer la matrice de confusion
        matrice = pd.DataFrame(0, index=classes, columns=classes)
        
        for vrai, pred in zip(vraies_classes, classes_predites):
            # Enlever les apostrophes si présentes
            vrai_clean = str(vrai).replace("'", "")
            pred_clean = str(pred).replace("'", "")
            
            if vrai_clean in classes and pred_clean in classes:
                matrice.loc[vrai_clean, pred_clean] += 1
        
        return matrice
    
    @staticmethod
    def calculer_metriques(matrice: pd.DataFrame) -> Dict:
        """Calcule les métriques de performance à partir de la matrice de confusion"""
        total = matrice.sum().sum()
        correct = np.trace(matrice)
        
        accuracy = correct / total if total > 0 else 0
        
        # Calcul par classe
        metriques_par_classe = {}
        for classe in matrice.index:
            tp = matrice.loc[classe, classe]
            fp = matrice[classe].sum() - tp
            fn = matrice.loc[classe].sum() - tp
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            rappel = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * rappel) / (precision + rappel) if (precision + rappel) > 0 else 0
            
            metriques_par_classe[classe] = {
                'precision': precision,
                'rappel': rappel,
                'f1_score': f1
            }
        
        return {
            'accuracy': accuracy,
            'par_classe': metriques_par_classe
        }
    
    @staticmethod
    def statistiques_descriptives(df: pd.DataFrame, colonne_classe: str) -> pd.DataFrame:
        """Calcule des statistiques descriptives par classe"""
        stats = df.groupby(colonne_classe).agg({
            'Energie_kcal': ['mean', 'std', 'min', 'max'],
            'Sucres_g': ['mean', 'std', 'min', 'max'],
            'Proteines_g': ['mean', 'std', 'min', 'max'],
            'Nombre_Additifs': ['mean', 'std', 'min', 'max']
        }).round(2)
        
        return stats


def creer_profils_limites(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée les 6 profils limites (b1 à b6) basés sur les quantiles de la base de données
    
    Args:
        df: DataFrame contenant les produits
    
    Returns:
        DataFrame contenant les 6 profils
    """
    criteres = ['Energie_kJ', 'Acides_Gras_Satures_g', 'Sucres_g', 'Sodium_mg',
                'Proteines_g', 'Fibres_g', 'Fruits_Legumes_Pct', 'Nombre_Additifs']
    
    profils = pd.DataFrame(index=['b1', 'b2', 'b3', 'b4', 'b5', 'b6'], 
                          columns=criteres)
    
    # Pour les critères à minimiser, b6 (meilleur) = valeur minimale
    # Pour les critères à maximiser, b6 (meilleur) = valeur maximale
    
    criteres_minimiser = ['Energie_kJ', 'Acides_Gras_Satures_g', 'Sucres_g', 
                         'Sodium_mg', 'Nombre_Additifs']
    criteres_maximiser = ['Proteines_g', 'Fibres_g', 'Fruits_Legumes_Pct']
    
    # b1 : borne inférieure (pire)
    # b6 : borne supérieure (meilleur)
    
    for critere in criteres:
        if critere in criteres_minimiser:
            # Pour minimiser : b6 = min, b1 = max + marge
            profils.loc['b6', critere] = df[critere].min() * 0.1  # 10% du min
            profils.loc['b5', critere] = df[critere].quantile(0.20)
            profils.loc['b4', critere] = df[critere].quantile(0.40)
            profils.loc['b3', critere] = df[critere].quantile(0.60)
            profils.loc['b2', critere] = df[critere].quantile(0.80)
            profils.loc['b1', critere] = df[critere].max() * 1.5  # 150% du max
        else:
            # Pour maximiser : b6 = max, b1 = min - marge
            profils.loc['b6', critere] = df[critere].max() * 1.5  # 150% du max
            profils.loc['b5', critere] = df[critere].quantile(0.80)
            profils.loc['b4', critere] = df[critere].quantile(0.60)
            profils.loc['b3', critere] = df[critere].quantile(0.40)
            profils.loc['b2', critere] = df[critere].quantile(0.20)
            profils.loc['b1', critere] = df[critere].min() * 0.1  # 10% du min
    
    return profils.astype(float)


def definir_poids_criteres() -> Dict[str, float]:
    """
    Définit les poids pour chaque critère
    
    Returns:
        Dictionnaire avec les poids
    """
    poids = {
        'Energie_kJ': 0.15,
        'Acides_Gras_Satures_g': 0.10,
        'Sucres_g': 0.15,
        'Sodium_mg': 0.15,
        'Proteines_g': 0.10,
        'Fibres_g': 0.10,
        'Fruits_Legumes_Pct': 0.15,
        'Nombre_Additifs': 0.10
    }
    
    return poids


if __name__ == "__main__":
    print("SuperNutriScore - Implémentation Nutri-Score et ELECTRE TRI")
    print("=" * 70)
