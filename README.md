# bernstein-raytracer

Sauf-ci mention contraire, nous travaillons dans l'espace vectoriel normé $\R^3$, muni du produit scalaire usuel, par exemple, on ne précisera pas que le point $c=(c_x, c_y, c_z)$ est un triplet de réel.

## Les fonctions utilitaires (util.py)

### -> normalise3

Pour un vecteur $v=(v_x, v_y, v_z)$, on a $ \|v\| = \sqrt{v_x^2 + v_y^2 + v_z^2}$, ainsi on peut créer le vecteur de norme $1$ :
$$n := \frac{v}{\|v\|} = \left(\frac{v_x}{\|v\|}, \frac{v_y}{\|v\|}, \frac{v_z}{\|v\|}\right)$$
Ce calcul est disponible via la fonction **normalise3**.

### -> clamp

"To clamp" signifie verouiller, si $x \in \R$, on peut forcer $x$ à appartenir à l'intervalle $[m, M]$.

$$clamp_{m, M}(x) := min(M, max(m, x))$$

Autrement dit, on a

$$
\text{clamp}_{m, M}(x) =
\begin{cases}
m & \text{si } x < m \\
x & \text{si } m \le x \le M \\
M & \text{si } x > M
\end{cases}
$$

### -> interpole

Admettons que l'on se balade sur un segment $[x_1, x_2]$, notons $x \in [x_1, x_2]$.

Si le segment maintenant se modifiait et devenait $[y_1, y_2]$, où se trouverait la nouvelle image de $x$ ?

Le problème peut se résumer par trouver un polynôme de degré minimal tel que $f(x1) = y1$ et $f(x2) = y2$, ainsi on pourrait calculer $f(x)$.

On se donne deux point $(x_0 y_0)$ et $(x_1, y_1)$ avec $x_0 \neq x_1$. On peut alors utiliser l 'interpolation de Lagrange (les hypothèses sont respectées), qui donnerait un unique polynôme de degré minimale, c'est-à-dire une droite, passant par ces deux points.

Le polynôme est le suivant :

$$L(x) = y_1\frac{x-x_0}{x_1-x_0} + y_0\frac{x-x_1}{x_0-x_1}$$

## Le rayon

Un rayon de source $s=(s_x, s_y, s_z)$ et de direction $d=(d_x, d_y, d_z)$ est défini par une équation paramétrique de la forme :
$$R_{s, d}(t) = (s_x + d_x \cdot t, s_y + d_y \cdot t, s_z + d_z \cdot t), \quad t \in \R$$

Le rayon sera modélisé par la classe Ray (fichier Ray.py) qui aura deux attributs: **origin** et **direction**, qui seront des points de $\R^3$.

## La caméra

Comment fonctionne le raytracing ?

Imaginons que l'on regarde ce qu'il se passe à travers une caméra. Cette caméra servira de pont entre ce que nous voyons à l'écran et ce qu'il se passe dans le monde mathématique.

La camera sera modélisée par la classe Camera disponible dans Cameras.py

Elle possède les attributs suivants:

- (elle possède une taille d'écran)
- (elle possède une taille de monde).
- Cette caméra a une position,
- elle regarde dans une direction.
- Elle possède un nom et sur la scène,
- on peut imaginer une source de lumière (afin de plus tard simuler des ombres).

Comment capte elle la lumière ? On va lui faire une méthode generate_ray. Là on a deux écoles :

Soit on fixe l'origine à l'origine de la caméra et on fait varier les rayons (qui donnera la classe Camera)

    world_x = interpole(0.0, 0.0, self.size_win, self.size_world, float(px))
        world_z = interpole(0.0, 0.0, self.size_win, self.size_world, float(pz))

        (cam_ox, cam_oy, cam_oz) = self.cam_o

return Ray(
origin=(
cam*ox + world_x * self.cam*dx[0] + world_z * self.cam*dz[0],
cam_oy + world_x * self.cam*dx[1] + world_z * self.cam*dz[1],
cam_oz + world_x * self.cam*dx[2] + world_z * self.cam_dz[2],
),
direction=self.oy,
)

soit on fixe la direction (direction oy de la caméra) et on déplace l'origine (qui donnera la classe camera perspective)
world_x = interpole(0.0, 0.0, self.size_win, self.size_world, float(px))
world_z = interpole(0.0, 0.0, self.size_win, self.size_world, float(pz))

        dx = (
            self.focale * self.cam_dy[0]
            + world_x * self.cam_dx[0]
            + world_z * self.cam_dz[0]
        )
        dy = (
            self.focale * self.cam_dy[1]
            + world_x * self.cam_dx[1]
            + world_z * self.cam_dz[1]
        )
        dz = (
            self.focale * self.cam_dy[2]
            + world_x * self.cam_dx[2]
            + world_z * self.cam_dz[2]
        )

        return Ray(origin=self.cam_o, direction=normalize3((dx, dy, dz)))

def **init**(
self, cam_o, cam_dx, cam_dy, cam_dz, size_world, size_win, light_dir, name
):

## La sphère

La sphère de centre $c=(c_x, c_y, c_z)$ et de rayon $r \in \R$ est définit par l'équation
$$(x-c_x)^2+(y-c_y)^2+(z-c_z)^2-r^2=0$$

$$
$$
