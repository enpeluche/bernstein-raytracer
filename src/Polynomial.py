from .Casteljau import *

from .BernsteinSolver import solve, has_root
from math import sqrt, comb

from .constants import EPSILON

from .DAG import Number


# vérifier que c'est int ou float pour roots et to_bernstein_basis


def unique_with_epsilon(values):
    values = sorted(values)
    result = []
    for v in values:
        if not result or abs(v - result[-1]) > 1e-5:
            result.append(v)
    return result


class Polynomial:
    __slots__ = ("coefficients", "len")
    _mul_cache = {}
    _BERNSTEIN_CACHE = {}

    r"""
    Représente un polynôme réel en base canonique (puissances de x).
    
    Cette classe est le cœur algébrique du moteur de rendu. Elle gère les 
    opérations arithmétiques standard, l'évaluation optimisée par la méthode 
    de Horner, et la recherche de racines par subdivision de Bernstein.
    
    Modèle mathématique :
    $P(x) = a_0 + a_1x + a_2x^2 + \dots + a_nx^n$
    
    Caractéristiques techniques :
    - Immuabilité : Les coefficients sont stockés dans un tuple pour éviter les effets de bord.
    - Performance : Utilise `__slots__` pour minimiser l'empreinte mémoire et accélérer 
      l'accès aux attributs sous PyPy.
    - Robustesse : Nettoyage automatique des coefficients de haut degré proches de zéro (EPS).
    - Polyvalence : Capacité de conversion vers la base de Bernstein pour le solveur géométrique.

    Attributes:
        coefficients (tuple[float, ...]): Les coefficients $a_i$ par ordre de puissance croissante.
        len (int): Le nombre de coefficients (degré + 1).
    """

    def __init__(self, coefficients: tuple) -> None:
        """
        Create a Polynomial object (where c[0] is the constant term).

        Args:
            c (tuple): coefficients of polynomial in ascending order of power.
        """

        coefficients = list(coefficients)

        while len(coefficients) > 1:
            last = coefficients[-1]

            # Cas A : Un nombre ou un flottant.
            if isinstance(last, (int, float)):
                if abs(last) < EPSILON:
                    coefficients.pop()
                else:
                    break

            # Cas B : Un Number
            elif isinstance(last, Number):
                if abs(last.value) < EPSILON:
                    coefficients.pop()
                else:
                    break

            # Cas C : Autre
            else:
                break

        self.coefficients = tuple(coefficients)

        self.len = len(self.coefficients)

    def get_coefficients(self) -> tuple[float]:
        """
        Accesseur pour les coefficients du polynôme.

        Les coefficients sont retournés sous forme de tuple immuable, classés par
        ordre de puissance croissante : (a_0, a_1, ..., a_n) où P(x) = sum(a_i * x^i).
        L'utilisation d'un tuple garantit que la structure interne du polynôme
        ne peut pas être modifiée de l'extérieur.

        Returns:
            tuple[float, ...]: La séquence des coefficients (le premier terme est la constante).
        """
        return self.coefficients

    def __call__(self, x):
        r"""
        Évalue le polynôme pour une valeur réelle donnée via la méthode de Horner.

        Plutôt que de calculer chaque puissance de x individuellement ($a_i \cdot x^i$),
        cet algorithme réorganise le polynôme sous forme de multiplications imbriquées :
        $P(x) = (...((a_n \cdot x + a_{n-1}) \cdot x + a_{n-2}) \cdot x + ... + a_0)$.

        Avantages :
        - Complexité temporelle optimale : $O(n)$.
        - Stabilité numérique accrue : réduit les erreurs d'arrondi liées aux grandes puissances.
        - Efficacité : seulement $n$ multiplications et $n$ additions.

        Args:
            x : La valeur (souvent le paramètre de distance $t$) à évaluer.

        Returns:
            Le résultat de l'évaluation $P(x)$.
        """

        n = self.len

        value = self.coefficients[n - 1]

        for i in range(n - 2, -1, -1):
            value = value * x + self.coefficients[i]

        return value

    def __add__(self, Q: "Polynomial") -> "Polynomial":
        """
        Calcule la somme de deux polynômes (addition binaire).

        L'opération additionne les coefficients de P et Q ($P + Q$) terme à terme.
        Cette implémentation est optimisée pour gérer efficacement les polynômes
        de degrés différents :
        - Identifie le polynôme de plus haut degré pour servir de base.
        - Additionne les coefficients du plus petit polynôme sur une copie du plus grand.
        - Garantit que l'alignement se fait sur les constantes ($a_0$).

        Cette méthode implémente l'opérateur binaire `+` (ex: R = P + Q).

        Args:
            Q (Polynomial): Le polynôme à ajouter.

        Returns:
            Polynomial: Un nouveau polynôme représentant la somme.
        """

        if self.len > Q.len:
            grand, petit = self, Q
        else:
            grand, petit = Q, self

        Z = list(grand.coefficients)

        for i in range(petit.len):
            Z[i] += petit.coefficients[i]

        return Polynomial(Z)

    def __mul__(self, Q: "Polynomial") -> "Polynomial":

        r"""
        Calcule le produit de deux polynômes (produit de Cauchy).

        L'opération réalise la convolution discrète des coefficients de P et Q.
        Le degré du polynôme résultant est la somme des degrés des opérandes :
        $deg(P \cdot Q) = deg(P) + deg(Q)$.

        Optimisation :
        - Pré-allocation de la liste de coefficients pour éviter les redimensionnements.
        - Saut des itérations pour les coefficients nuls afin d'accélérer les
          calculs sur les polynômes creux (sparse).

        Cette méthode implémente l'opérateur binaire `*` (ex: R = P * Q).

        Args:
            Q (Polynomial): Le polynôme multiplicateur.

        Returns:
            Polynomial: Un nouveau polynôme représentant le produit.
        """
        if Q is POLY_ONE:
            return self
        if Q is POLY_ZERO:
            return POLY_ZERO

        key = (id(self), id(Q))

        if key in Polynomial._mul_cache:
            return Polynomial._mul_cache[key]

        len_self = self.len
        len_Q = Q.len

        mul_coeffs = [0] * (len_self + len_Q - 1)

        for i in range(len_self):
            c1 = self.coefficients[i]

            if isinstance(c1, (int, float)) and c1 == 0:
                continue

            if isinstance(c1, Number) and c1.value == 0:
                continue

            for j in range(len_Q):
                mul_coeffs[i + j] += c1 * Q.coefficients[j]

        Polynomial._mul_cache[key] = Polynomial(mul_coeffs)

        return Polynomial(mul_coeffs)

    def __sub__(self, Q: "Polynomial") -> "Polynomial":
        r"""
        Calcule la différence entre deux polynômes (soustraction binaire).

        L'opération soustrait les coefficients de Q de ceux de P ($P - Q$) terme à terme.
        Cette implémentation gère explicitement les polynômes de degrés différents :
        - Si $deg(P) \geq deg(Q)$, on soustrait simplement les coefficients existants.
        - Si $deg(Q) > deg(P)$, on complète les termes de plus haut degré par les
          opposés de ceux de Q.

        Cette méthode implémente l'opérateur binaire `-` (ex: R = P - Q).

        Args:
            Q (Polynomial): Le polynôme à soustraire.

        Returns:
            Polynomial: Un nouveau polynôme représentant la différence.
        """

        if self.len >= Q.len:
            Z = list(self.coefficients)

            for i in range(Q.len):
                Z[i] -= Q.coefficients[i]

        else:
            Z = list(self.coefficients)

            for i in range(self.len):
                Z[i] -= Q.coefficients[i]

            for i in range(self.len, Q.len):
                Z.append(-Q.coefficients[i])

        return Polynomial(Z)

    def __neg__(self) -> "Polynomial":
        """
        Calcule l'opposé du polynôme (inverse additif).

        Chaque coefficient a_i est remplacé par -a_i. Graphiquement, cela
        correspond à une réflexion du polynôme par rapport à l'axe des abscisses.
        Cette méthode est appelée par l'opérateur unaire `-` (ex: Q = -P).

        Returns:
            Polynomial: Un nouveau polynôme dont tous les coefficients sont nuls ou inversés.
        """

        return Polynomial([-c for c in self.coefficients])

    def reverse(self) -> "Polynomial":
        """
        Génère le polynôme réciproque (reciprocal polynomial).

        Mathématiquement, si P(t) est de degré n, alors P_reverse(t) = t^n * P(1/t).
        Cette transformation inverse l'ordre des coefficients et est cruciale pour
        trouver les racines du polynôme sur l'intervalle [1, +inf[ en les ramenant
        sur l'intervalle [0, 1].

        Returns:
            Polynomial: Un nouveau polynôme avec les coefficients inversés.
        """

        return Polynomial(self.coefficients[::-1])

    def roots(
        self, t_min: float = -float("inf"), t_max: float = float("inf")
    ) -> list[float]:
        """
        Calcule les racines réelles du polynôme sur l'intervalle [0, +inf[.

        Cette méthode utilise une stratégie hybride pour maximiser la performance :
        1. Cas analytiques (Fast-path) : Résolution directe pour les degrés 1 et 2.
        2. Cas numérique (Artillerie lourde) : Pour les degrés > 2, utilise le solveur
           de Bernstein par subdivision sur [0, 1].
        3. Extension à l'infini : Utilise le polynôme réciproque (reverse) pour
           trouver les racines au-delà de t = 1.

        Returns:
            list[float]: Une liste de racines réelles, triées et sans doublons (EPS).
        """

        P = self

        if not P.coefficients:
            return []

        # --- GESTION DE LA RACINE À L'ORIGINE (t = 0) ---

        # Si le terme constant (a_0) est nul, alors P(0) = 0.
        # Mathématiquement, on factorise par 't' : P(t) = t * Q(t).
        # On ajoute 0.0 aux solutions et on cherche les racines restantes dans Q(t).
        if len(P.coefficients) > 1 and abs(P.coefficients[0]) < EPSILON:
            # On crée le polynôme quotient Q(t) en décalant les coefficients
            other_roots = Polynomial(P.coefficients[1:]).roots(t_min, t_max)

            # On combine 0.0 avec les autres racines en garantissant l'unicité
            return unique_with_epsilon(other_roots)

        # --- CAS ANALYTIQUES (Optimisation pour les formes de base) ---

        # Degré 0 : Polynôme constant.
        # Soit P(t) = c (pas de solution), soit P(t) = 0 (infinité, ignoré ici).

        if P.len == 1:
            return []

        # Degré 1 : Équation linéaire a*t + b = 0.
        # t = -b / a. Représente l'intersection avec un plan.

        if P.len == 2:
            root = -P.coefficients[0] / P.coefficients[1]
            return [root] if t_min <= root <= t_max else []

        # Degré 2 : Équation quadratique a*t² + b*t + c = 0.
        # Utilise le discriminant (Delta) pour les sphères, cylindres, etc.

        if P.len == 3:
            c = P.coefficients[0]
            b = P.coefficients[1]
            a = P.coefficients[2]

            if abs(a) < EPSILON:
                if abs(b) < EPSILON:
                    return []
                root = -c / b
                return [root] if t_min <= root <= t_max else []

            delta = b * b - 4 * a * c

            if abs(delta) < EPSILON:
                root = -b / (2 * a)
                return [root] if t_min <= root <= t_max else []

            if delta < 0:
                return []

            sqrt_delta = sqrt(delta)

            t1 = (-b - sqrt_delta) / (2 * a)
            t2 = (-b + sqrt_delta) / (2 * a)

            return [t for t in sorted([t1, t2]) if t_min <= t <= t_max]

        # --- CAS NUMÉRIQUES (Artillerie lourde : Bernstein & Subdivision) ---

        solutions = []

        if t_min <= 1.0:
            # 1. Recherche sur l'intervalle local [0, 1]
            # On convertit en base de Bernstein pour profiter de la propriété de
            # l'enveloppe convexe (élimination rapide des segments sans racines).

            roots_near = solve(
                P.to_bernstein_basis(), 0, 1.0, t_min, min(t_max, 1.0), []
            )
            solutions.extend(roots_near)

        if t_max > 1.0:
            # 2. Recherche sur l'intervalle lointain [1, +inf[
            # Astuce mathématique : on utilise le polynôme réciproque P_reverse(u).
            # Les racines 'u' de P_reverse sur [0, 1] correspondent aux racines 't'
            # de P sur [1, +inf[ via la relation t = 1/u.

            # u_min et u_max basés sur t_max et t_min
            u_min = 1.0 / t_max if t_max != float("inf") else 0.0
            u_max = 1.0 / max(1.0, t_min)

            roots_far_inv = solve(
                P.reverse().to_bernstein_basis(), 0, 1.0, u_min, u_max, []
            )

            roots_far = []
            for u in roots_far_inv:
                if abs(u) > EPSILON:  # Évite la division par zéro (racine à l'infini)
                    t = 1.0 / u

                    if t > 1.0 + EPSILON and t_min <= t <= t_max:
                        roots_far.append(t)

            solutions.extend(sorted(roots_far))

        # --- FINALISATION ---

        if not solutions:
            return []

        return unique_with_epsilon(solutions)

    def has_any_root(self, t_min: float, t_max: float) -> bool:
        """Détermine si au moins une racine existe dans [t_min, t_max]."""
        P = self
        if not P.coefficients:
            return False

        # --- GESTION ORIGINE ---
        if len(P.coefficients) > 1 and abs(P.coefficients[0]) < EPSILON:
            if t_min <= 0.0 <= t_max:
                return True
            # Sinon on cherche dans le reste
            return Polynomial(P.coefficients[1:]).has_any_root(t_min, t_max)

        # --- CAS ANALYTIQUES (Rapides) ---
        if P.len == 1:
            return False

        if P.len == 2:
            root = -P.coefficients[0] / P.coefficients[1]
            return t_min <= root <= t_max

        if P.len == 3:
            c, b, a = P.coefficients[0], P.coefficients[1], P.coefficients[2]
            if abs(a) < EPSILON:
                if abs(b) < EPSILON:
                    return False
                return t_min <= (-c / b) <= t_max

            delta = b * b - 4 * a * c
            if delta < 0:
                return False

            if abs(delta) < EPSILON:
                return t_min <= (-b / (2 * a)) <= t_max

            sqrt_delta = delta ** 0.5
            t1 = (-b - sqrt_delta) / (2 * a)
            if t_min <= t1 <= t_max:
                return True  # Arrêt précoce

            t2 = (-b + sqrt_delta) / (2 * a)
            return t_min <= t2 <= t_max

        # --- CAS NUMÉRIQUES (Bernstein court-circuité) ---
        if t_min <= 1.0:
            if has_root(P.to_bernstein_basis(), 0.0, 1.0, t_min, min(t_max, 1.0)):
                return True

        if t_max > 1.0:
            u_min = 1.0 / t_max if t_max != float("inf") else 0.0
            u_max = 1.0 / max(1.0, t_min)
            # Dès que la première racine lointaine est validée, ça remonte et sort !
            if has_root(P.reverse().to_bernstein_basis(), 0.0, 1.0, u_min, u_max):
                return True

        return False

    @classmethod
    def _get_bernstein_matrix(cls, n):
        """Méthode de classe pour gérer le cache des matrices de passage."""
        if n not in cls._BERNSTEIN_CACHE:
            # On génère la matrice triangulaire inférieure
            matrix = []
            for k in range(n + 1):
                row = [comb(k, i) / comb(n, i) for i in range(k + 1)]
                matrix.append(row)
            cls._BERNSTEIN_CACHE[n] = matrix

        return cls._BERNSTEIN_CACHE[n]

    def to_bernstein_basis(self) -> list[float]:
        r"""
        Convertit le polynôme de la base canonique (puissances de t) vers la base de Bernstein.

        Cette transformation est indispensable pour le solveur géométrique. En base de Bernstein,
        les coefficients (appelés points de contrôle) possèdent une propriété capitale :
        l'enveloppe convexe. Le polynôme est entièrement contenu dans l'intervalle défini par
        ses points de contrôle sur [0, 1], ce qui permet une recherche de racines par subdivision.

        Mathématiquement, pour un degré n, on calcule les coefficients $b_k$ tels que :
        $P(t) = \sum_{k=0}^n b_k \cdot \binom{n}{k} t^k (1-t)^{n-k}$

        Formule de conversion utilisée :
        $b_k = \sum_{i=0}^k a_i \cdot \frac{\binom{k}{i}}{\binom{n}{i}}$ où $a_i$ sont les coefficients canoniques.

        Returns:
            list[float]: Les points de contrôle de la courbe de Bézier équivalente sur [0, 1].
        """
        n = self.len - 1
        if n < 0:
            return []

        matrix = self._get_bernstein_matrix(n)

        bernstein_coeffs = [0.0] * self.len

        for k, row in enumerate(matrix):
            s = 0.0
            for i, matrix_val in enumerate(row):
                s += self.coefficients[i] * matrix_val
            bernstein_coeffs[k] = s

        return bernstein_coeffs

    def __str__(self):
        return f"Polynomial([{', '.join(str(c) for c in self.coefficients)}])"


POLY_ZERO = Polynomial([0.0])
POLY_ONE = Polynomial([1.0])
