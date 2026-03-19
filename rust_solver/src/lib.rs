use pyo3::prelude::*;

mod casteljau;
mod solve;
pub mod midpoints;
pub use midpoints::*;

// 1. On définit les fonctions "pont" à l'extérieur pour la clarté
#[pyfunction]
fn casteljau_naive_py(v: Vec<f64>) -> (Vec<f64>, Vec<f64>) {
    crate::casteljau::casteljau_naive(&v)
}

#[pyfunction]
fn casteljau_py(v: Vec<f64>) -> (Vec<f64>, Vec<f64>) {
    crate::casteljau::casteljau(&v)
}

#[pyfunction]
fn solve_py(v: Vec<f64>, t_min: f64, t_max: f64, v_min: f64, v_max: f64, depth_start: usize) -> Vec<f64> {
    let mut tab = v; 
    let mut solutions = Vec::new();
    
    crate::solve::solve(
        &mut tab,
        t_min,
        t_max,
        v_min,
        v_max,
        &mut solutions,
        depth_start, // En général, on passe 0 ici depuis Python
    );

    solutions
}

#[pymodule]
fn rust_solver(m: &Bound<'_, PyModule>) -> PyResult<()> {

    m.add_function(wrap_pyfunction!(casteljau_naive_py, m)?)?;
    m.add_function(wrap_pyfunction!(casteljau_py, m)?)?;
    m.add_function(wrap_pyfunction!(solve_py, m)?)?;

    Ok(())
}