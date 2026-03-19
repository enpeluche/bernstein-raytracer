pub fn midpoints_naive(points: &[f64]) -> Vec<f64>{
    let mut mid: Vec<f64> = Vec::with_capacity(points.len()-1);

    for i in 0..points.len()-1 {
        mid.push((points[i] + points[i + 1]) * 0.5);
    }
    mid
}

pub fn midpoints_iter_zip(points: &[f64]) -> Vec<f64>{
    points.iter()
          .zip(points[1..].iter())
          .map(|(a, b)| (a+b)*0.5)
          .collect()
}

pub fn midpoints_iter_windows(points: &[f64]) -> Vec<f64>{
    points.windows(2)
          .map(|w| (w[0]+w[1])*0.5)
          .collect()
}

#[inline(always)]
pub fn midpoints_auto_vectorized(points: &[f64]) -> Vec<f64>{
    let mut mid = vec![0.0;points.len()-1];

    for i in 0..points.len()-1 {
        mid[i] = (points[i] + points[i+1])*0.5;
    }
    mid
}

#[cfg(target_arch = "x86_64")]
use core::arch::x86_64::*;
pub fn midpoints_simd(points: &[f64]) -> Vec<f64>{
    let mut mid = vec![0.0;points.len()-1];
    let mut i = 0;
    let n = points.len()-1;
    let p_ptr = points.as_ptr();
    let m_ptr = mid.as_mut_ptr();

    unsafe {
        let c = _mm256_set1_pd(0.5);
        while i+4 <= n {
            let a = _mm256_loadu_pd(p_ptr.add(i));
            let b = _mm256_loadu_pd(p_ptr.add(i + 1));

            let sum = _mm256_add_pd(a, b);
            
            let result = _mm256_mul_pd(sum, c);
            
            _mm256_storeu_pd(m_ptr.add(i), result);

            i+=4;
        }
    }
        for j in i..n {
            mid[j] = (points[j] + points[j+1])*0.5;
        }
        mid
        
    
}

pub fn midpoints_const<const IN: usize, const OUT: usize>(points: &[f64; IN]) -> [f64; OUT] {
    debug_assert!(OUT == IN - 1); 
    let mut mid = [0.0; OUT];

    for i in 0..OUT {
        mid[i] = (points[i] + points[i+1])*0.5;
    }
    mid
}