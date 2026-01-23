# bernstein-raytracer

Sauf-ci mention contraire, nous travaillons dans l'espace vectoriel $\R^3$, par exemple, on ne précisera pas que le point $c=(c_x, c_y, c_z)$ est un triplet de réel.

## Le rayon

Un rayon de source $s=(s_x, s_y, s_z)$ et de direction $d=(d_x, d_y, d_z)$ est défini par une équation paramétrique de la forme :
$$R_{s, d}(t) = (s_x + d_x \cdot t, s_y + d_y \cdot t, s_z + d_z \cdot t), \quad t \in \R$$

Le rayon sera modélisé par la classe Rayon (fichier Rayon.py) qui aura deux attributs: **source** et **direction**, qui seront des points de $\R^3$.

## La sphère

La sphère de centre $c=(c_x, c_y, c_z)$ et de rayon $r \in \R$ est définit par l'équation
$$(x-c_x)^2+(y-c_y)^2+(z-c_z)^2-r^2=0$$
