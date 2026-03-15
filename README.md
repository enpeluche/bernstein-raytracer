# Bernstein-Ray: Symbolic Raytracer for Algebraic Implicit Surfaces

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

<div align="center">
  <table style="margin-left: auto; margin-right: auto;">
    <tr>
      <td align="center">
        <img src="gallery/heart.gif" width="300"><br>
        <sub><b>Type:</b> Roman Surface (Z-axis rotation)<br><b>Camera:</b> Perspective</sub>
      </td>
    </tr>
  </table>
  
</div>

Bernstein-Ray is a research-oriented raytracer designed for rendering **algebraic implicit surfaces** defined by polynomial equations.

Instead of relying on numerical ray marching, the engine computes **exact ray–surface intersections** by transforming the implicit equation into a **univariate polynomial along the ray**, then solving it using **Bernstein basis subdivision (de Casteljau algorithm)**.

## News

📖 You can find a detailed article about the math and logic behind this project on my blog: 
👉 [Read the article here](https://enpeluche.github.io/blog/?post=2026-03-15-raytracing_00)

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
      <td align="center">
        <img src="gallery/csg_perspectivecamera.gif" width="200"><br>
        <sub><b>Type:</b> Roman Surface - Sphere (Z-axis rotation)<br><b>Camera:</b> Perspective</sub>
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
      <td align="center">
        <img src="gallery/cube_rota_xyz.gif" width="300"><br>
        <sub><b>Type:</b> Cube (CSG Animation)<br><b>Camera:</b> Perspective</sub>
      </td>
    </tr>
  </table>
</div>

<div align="center">
  <table style="margin-left: auto; margin-right: auto;">
    <tr>
      <td align="center">
        <img src="gallery/solar_system.png" width="200"><br>
        <sub><b>Type:</b> Solar System (CSG)<br><b>Camera:</b> Perspective</sub>
      </td>
      <td align="center">
        <img src="gallery/ouioui.gif" width="200"><br>
        <sub><b>Type:</b> CSG<br><b>Camera:</b> Perspective</sub>
      </td>
      <td align="center">
        <img src="gallery/render_beautiful.png" width="200"><br>
        <sub><b>Type:</b> CSG<br><b>Camera:</b> Perspective</sub>
      </td>
    </tr>
  </table>
</div>

## Tutorial: Implement Your Own Custom Surface

Want to render a surface that isn't in the library yet? Adding a new algebraic shape is as simple as defining its equation.

### Step 1: Find the Implicit Equation

Identify the equation where f(x,y,z)=0. For the Ding-Dong surface, the equation is:

$$x^2+y^2=(1−z)z^2 => x^2+y^2−(1−z)z^2=0$$

- **Degree**: 3 (Cubic)
- **Domain Analysis**: For the surface to exist ($x^2+y^2 \geq 0$), we need $(1−z)\geq 0$, meaning $z \in ]− \infty ,1]$.


### Step 2: Define the Primitive

Add the following function to py/shapes/cubics.py.

Note on AABB: Providing an Axis-Aligned Bounding Box (AABB) is optional but highly recommended. It significantly speeds up rendering by telling the raytracer exactly where to look for the surface.



```python
def dingdong(color=None, **kwargs) -> Primitive:
    # Define the symbolic expression
    expr = x**2 + y**2 - (1 - z) * z**2

    # Define the bounding box (Min_X, Min_Y, Min_Z, Max_X, Max_Y, Max_Z)
    # Even if Z goes to -infinity, we bound it for the render view.
    aabb = (-float("inf"), -float("inf"), -float("inf"), float("inf"), float("inf"), 1.0)

    return Primitive(
        implicit_function=expr, 
        color=color, 
        label="Ding-Dong", 
        aabb=aabb, 
        **kwargs
    )
```


### Step 3: Register the Surface

To make it accessible, update the __init__.py or the import section of your main script:


```python
from .cubics import cayley, whitney_umbrella, dingdong
```

### Step 4: Render!

Now you can use it in your scene just like any other shape:


```python
shape = dingdong(color=RED).rotate_x(DEG * 90)
```

# How it works
## Ray–Surface Intersection

Given an implicit surface

$$f(x,y,z) = 0$$

and a ray

$$r(t) = o + t d$$

we substitute the ray equation into the surface:

$$g(t) = f(o + t d)$$

For algebraic surfaces this produces a **polynomial in t**.

**Example:**

- Torus → degree 4 polynomial  
- Taubin heart → degree 6 polynomial

The roots of g(t) correspond to ray–surface intersections.

Bernstein-Ray isolates roots using **Bernstein polynomial subdivision**
based on the **de Casteljau algorithm**, which provides robust root finding
without requiring explicit polynomial solving.


## Benchmarks

Resolution of 1000^2, Orthographic camera, Pypy 3 (3.10.14), 30 runs

| Shape (Degree) | Mean   | Std Dev | Var    | RSD     | min    | max    | time/px |
|:--------------:|:------:|:-------:|:------:|:-------:|:------:|:------:|:-------:|
| Sphere (2)     | 4.29s  | 0.159s  | 0.025s²| ± 3.69% | 4.085s | 4.626s | 4.29µs  |
| Lens(0.7,0.2)  | 2.61s  | 0.077s  | 0.006s²| ± 2.53% | 2.499s | 2.919s | 2.61µs  |
| Ding-Dong (3)  | 11.91s | 0.421s  | 0.177s²| ± 3.53% | 10.847s| 12.197s| 11.9µs  |
| Roman (4)      | 6.2s   | 0.064s  | 0.004s²| ± 1.02% | 6.134s | 6.357s | 6.2µs   |
| Taubin (6)     | 26.04s | 0.553s  | 0.306s²| ± 2.13% | 24.45s | 26.927s| 26µs    |



| Shape (Degree) | Mean   | Std Dev | Var    | RSD     | min    | max    | time/px |
|:--------------:|:------:|:-------:|:------:|:-------:|:------:|:------:|:-------:|
| Sphere (2)     | 4.29s  | 0.159s  | 0.025s²| ± 3.69% | 4.085s | 4.626s | 4.29µs  |
| S_4 (4)        | 20.833s| 0.529s  | 0.279s²| ± 2.54% | 19.181s|22.368s | 20.83µs |
| S_6 (6)        | 34.755s| 0.275s  | 0.076s²| ± 0.79% | 33.812s|35.217s | 34.75µs |
| S_8 (8)        | 37.700s| 0.706s  | 0.498s²| ± 1.87% | 35.290s|38.427s | 37.70µs |
| S_10 (10)      | 40.863s| 0.588s  | 0.345s²| ± 1.44% | 38.580s|41.841s | 40.86µs |


### Key Takeaways
* **Degree is not everything:** The mathematical degree is not always the dominant performance bottleneck (e.g., the degree 4 Roman surface renders faster than the degree 3 Ding-Dong). The shape's topology and gradient play a massive role in root-finding speed.
* **AABB Filtering is critical:** The CSG Lens performs remarkably fast, proving that aggressive bounding box culling successfully skips heavy polynomial evaluations.
* **DAG Optimization:** Simplifying the Directed Acyclic Graph (DAG) by minimizing transformations and CSG nesting is crucial for maintaining low render times.



## Future Work & Known Limitations

Building a robust symbolic raytracer is an ongoing mathematical challenge. While the core Bernstein solver is highly stable, there are several edge cases and optimizations planned for future releases:

* **Open vs. Closed Surface Topology:**
    * *The Issue:* Currently, open surfaces (like the Hyperbolic Cylinder or Hyperbolic Paraboloid) struggle to render correctly. The engine's interval logic assumes all objects enclose a solid volume ($f < 0$ means "inside"). This breaks down for non-manifold, infinitely open sheets.
    * *The Fix:* Introduce an explicit `is_closed` flag in the `Primitive` class to branch the rendering logic, allowing for both "solid CSG" objects and "thin-shell" open surfaces.

* **Granular Artifacts on Odd-Degree Surfaces:**
    * Surfaces defined by odd-degree polynomials occasionally exhibit grainy or stippled artifacts. This requires refining the root-finding precision and interval merging logic when polynomial tails go to positive/negative infinity.

* **Camera Projection Clipping (The "Half-Cube" Bug):**
    * There is a known issue where CSG-based objects (like a Box made of 6 Half-spaces) only render halfway under certain camera projections (Orthographic / Perspective). This requires a deep dive into how ray origins interact with AABB boundaries and `t_min` clamping.

* **Optimization: Descartes' Rule of Signs:**
    * *The Goal:* Upgrade the early-exit `has_root()` method. By analyzing the coefficient sign changes using **Descartes' Rule of Signs**, the engine will be able to instantly detect if a segment has zero roots, bypassing the heavy Bernstein subdivision entirely for massive performance gains.

* **Make an Animation Class:**
    * *The Goal:* Build a dedicated module to render time-based sequences directly from the engine, outputting ready-to-use frame sequences.
    * *Features:* Support for keyframe interpolation on camera paths, object transformations (translation/rotation), and dynamic algebraic coefficients (e.g., morphing a shape's defining equation over time).