# Bernstein-Ray: Symbolic Raytracer for Algebraic Implicit Surfaces

<div align="center">
  <table style="margin-left: auto; margin-right: auto;">
    <tr>
      <td align="center">
        <img src="gallery/0001.png" width="200"><br>
        <sub><b>Type:</b> Roman Surface (Z-axis rotation)<br><b>Camera:</b> Perspective</sub>
      </td>
    </tr>
  </table>
  
</div>

Bernstein-Ray is a research-oriented raytracer designed for rendering **algebraic implicit surfaces** defined by polynomial equations.

Instead of relying on numerical ray marching, the engine computes **exact ray–surface intersections** by transforming the implicit equation into a **univariate polynomial along the ray**, then solving it using **Bernstein basis subdivision (de Casteljau algorithm)**.

This approach allows robust rendering of complex algebraic surfaces such as:

- Steiner surfaces
- Roman surfaces
- Torii
- Taubin hearts
- Quartic algebraic surfaces


## Key Features

- Symbolic construction of ray–surface intersection polynomials
- Root isolation using Bernstein basis subdivision
- Support for arbitrary algebraic implicit surfaces
- Constructive Solid Geometry (CSG)
- Multiple camera models:
  - Perspective
  - Orthographic
  - Fisheye
  - Thin lens (depth of field)
  - Cylindrical
- Automatic transformation of rays into object space

<div align="center">
  <table style="margin-left: auto; margin-right: auto;">
    <tr>
      <td align="center">
        <img src="gallery/roman_rotation_z.gif" width="200"><br>
        <sub><b>Type:</b> Roman Surface (Z-axis rotation)<br><b>Camera:</b> Perspective</sub>
      </td>
    </tr>
  </table>
  
</div>

## Implicit Surfaces Gallery

### Degree 2 Algebraic Surfaces: Quadrics

<div align="center">
  <table style="margin-left: auto; margin-right: auto;">
    <tr>
      <td align="center">
        <img src="gallery/ellipsoid_orthographiccamera.png" width="200"><br>
        <sub><b>Type:</b> Ellipsoid<br><b>Camera:</b> Orthographic</sub>
      </td>
      <td align="center">
        <img src="gallery/elliptic_cone_fovperspectivecamera.png" width="200"><br>
        <sub><b>Type:</b> Elliptic Cone<br><b>Camera:</b> FOV Perspective</sub>
      </td>
      <td align="center">
        <img src="gallery/elliptic_cylinder_fisheyecamera.png" width="200"><br>
        <sub><b>Type:</b> Elliptic Cylinder<br><b>Camera:</b> Fisheye</sub>
      </td>
    </tr>
  </table>
  <table style="margin-left: auto; margin-right: auto;">
    <tr>
      <td align="center">
        <img src="gallery/hyperbolic_cylinder_thinLenscamera.png" width="300"><br>
        <sub><b>Type:</b> Hyperbolic Cylinder<br><b>Camera:</b> Thin Lens (DOF)</sub>
      </td>
      <td align="center">
        <img src="gallery/hyperboloid_of_two_sheets_cylindricalcamera.png" width="300"><br>
        <sub><b>Type:</b> Hyperboloid (2 Sheets)<br><b>Camera:</b> Cylindrical</sub>
      </td>
    </tr>
  </table>
</div>


### Degree 4 Algebraic Surfaces: Quartics

<div align="center">
  <table style="margin-left: auto; margin-right: auto;">
    <tr>
      <td align="center">
        <img src="gallery/steiner2_cylindricalcamera.png" width="200"><br>
        <sub><b>Type:</b> Steiner Surface (Type 2)<br><b>Camera:</b> Cylindrical</sub>
      </td>
      <td align="center">
        <img src="gallery/steiner4_thinLenscamera.png" width="200"><br>
        <sub><b>Type:</b> Steiner Surface (Type 4)<br><b>Camera:</b> Thin Lens (DOF)</sub>
      </td>
      <td align="center">
        <img src="gallery/torus_fisheyecamera.png" width="200"><br>
        <sub><b>Type:</b> Torus<br><b>Camera:</b> Fisheye</sub>
      </td>
    </tr>
  </table>
</div>

## A Glimpse into CSG (Constructive Solid Geometry)

<div align="center">
  <table style="margin-left: auto; margin-right: auto;">
    <tr>
      <td align="center">
        <img src="gallery/barillet_anim.gif" width="300"><br>
        <sub><b>Type:</b> Revolver Cylinder (CSG Animation)<br><b>Camera:</b> Orthographic</sub>
      </td>
    </tr>
  </table>
</div>

## Tutorial: Implement Your Own Custom Surface

Want to render a surface that isn't in the library yet? Adding a new algebraic shape is as simple as defining its equation.

### Step 1: Find the Implicit Equation

Identify the equation where f(x,y,z)=0. For the Ding-Dong surface, the equation is:

x2+y2=(1−z)z2⟹x2+y2−(1−z)z2=0

Degree: 3 (Cubic)

Domain Analysis: For the surface to exist (x2+y2≥0), we need (1−z)≥0, meaning z∈[−∞,1].


Step 2: Define the Primitive

Add the following function to py/shapes/cubics.py.

    Note on AABB: Providing an Axis-Aligned Bounding Box (AABB) is optional but highly recommended. It significantly speeds up rendering by telling the raytracer exactly where to look for the surface.


on doit avoir (1-z) z^2 > 0 donc 1-z >0 donc z in -infini, 1

on peut donc englober d'une AABB

-infini, -infini, -infini
infini, infini, 1

```
def dingdong(color=None, **kwargs) -> Primitive:
    # Define the symbolic expression
    expr = x**2 + y**2 - (1 - z) * z**2

    # Define the bounding box (Min_X, Min_Y, Min_Z, Max_X, Max_Y, Max_Z)
    # Even if Z goes to -infinity, we bound it for the render view.
    aabb = (-1.5, -1.5, -1.0, 1.5, 1.5, 1.0)

    return Primitive(
        implicit_function=expr, 
        color=color, 
        label="Ding-Dong", 
        aabb=aabb, 
        **kwargs
    )
```


Step 3: Register the Surface

To make it accessible, update the __init__.py or the import section of your main script:


from .cubics import cayley, whitney_umbrella

devient

from .cubics import cayley, whitney_umbrella, dingdong

Step 4: Render!

Now you can use it in your scene just like any other shape:



shape = dingdong(color=RED).rotate_x(DEG * 90)

# How it works
## Ray–Surface Intersection

Given an implicit surface

f(x,y,z) = 0

and a ray

r(t) = o + t d

we substitute the ray equation into the surface:

g(t) = f(o + t d)

For algebraic surfaces this produces a **polynomial in t**.

Example:

Torus → degree 4 polynomial  
Taubin heart → degree 6 polynomial

The roots of g(t) correspond to ray–surface intersections.

Bernstein-Ray isolates roots using **Bernstein polynomial subdivision**
based on the **de Casteljau algorithm**, which provides robust root finding
without requiring explicit polynomial solving.