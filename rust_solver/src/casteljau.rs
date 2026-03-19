

pub fn old_casteljau(){
    todo!()
}



























pub fn casteljau_naive(v: &[f64]) -> (Vec<f64>, Vec<f64>) {
    let n = v.len();

    match n {
        // Degré 2
        3 => {
            let p0 = v[0];
            let p1 = v[1];
            let p2 = v[2];

            let m0 = 0.5 * (p0 + p1);
            let m1 = 0.5 * (p1 + p2);
            let s  = 0.5 * (m0 + m1);

            (vec![p0, m0, s], vec![s, m1, p2])
        }

        // Degré 3
        4 => {
            let p0 = v[0];
            let p1 = v[1];
            let p2 = v[2];
            let p3 = v[3];

            let m0 = 0.5 * (p0 + p1);
            let m1 = 0.5 * (p1 + p2);
            let m2 = 0.5 * (p2 + p3);

            let n0 = 0.5 * (m0 + m1);
            let n1 = 0.5 * (m1 + m2);

            let s = 0.5 * (n0 + n1);

            (vec![p0, m0, n0, s], vec![s, n1, m2, p3])
        }

        // Degré 4
        5 => {
            let c0 = v[0];
            let c1 = v[1];
            let c2 = v[2];
            let c3 = v[3];
            let c4 = v[4];

            let m0 = 0.5 * (c0 + c1);
            let m1 = 0.5 * (c1 + c2);
            let m2 = 0.5 * (c2 + c3);
            let m3 = 0.5 * (c3 + c4);

            let m01 = 0.5 * (m0 + m1);
            let m12 = 0.5 * (m1 + m2);
            let m23 = 0.5 * (m2 + m3);

            let m012 = 0.5 * (m01 + m12);
            let m123 = 0.5 * (m12 + m23);

            let s = 0.5 * (m012 + m123);

            (
                vec![c0, m0, m01, m012, s],
                vec![s, m123, m23, m3, c4],
            )
        }

        // Cas général
        _ => {
            let mut temp = v.to_vec();

            let mut left = Vec::with_capacity(n);
            let mut right = Vec::with_capacity(n);

            left.push(temp[0]);
            right.push(temp[n - 1]);

            for i in 1..n {
                for k in 0..(n - i) {
                    temp[k] = 0.5 * (temp[k] + temp[k + 1]);
                }

                left.push(temp[0]);
                right.push(temp[n - 1 - i]);
            }

            right.reverse();

            (left, right)
        }
    }
}

#[inline(always)]
pub fn casteljau_inplace(
    input: &[f64],
    left: &mut [f64],
    right: &mut [f64],
    scratch: &mut [f64],
) {
    let n = input.len();

    debug_assert!(left.len() == n);
    debug_assert!(right.len() == n);
    debug_assert!(scratch.len() == n);

    // copie initiale dans scratch
    scratch[..n].copy_from_slice(input);

    left[0] = scratch[0];
    right[0] = scratch[n - 1];

    for i in 1..n {
        // cœur du Casteljau
        for k in 0..(n - i) {
            scratch[k] = 0.5 * (scratch[k] + scratch[k + 1]);
        }

        left[i] = scratch[0];
        right[i] = scratch[n - 1 - i];
    }

    // inversion de right
    right[..n].reverse();
}

#[inline(always)]
pub fn casteljau_small<const N: usize>(
    input: &[f64; N],
    left: &mut [f64; N],
    right: &mut [f64; N],
) {
    let mut scratch = *input;

    left[0] = scratch[0];
    right[0] = scratch[N - 1];

    for i in 1..N {
        for k in 0..(N - i) {
            scratch[k] = 0.5 * (scratch[k] + scratch[k + 1]);
        }

        left[i] = scratch[0];
        right[i] = scratch[N - 1 - i];
    }

    right.reverse();
}

pub fn casteljau(v: &[f64]) -> (Vec<f64>, Vec<f64>) {
    let n = v.len();

    let mut left = vec![0.0; n];
    let mut right = vec![0.0; n];
    let mut scratch = vec![0.0; n];

    casteljau_inplace(v, &mut left, &mut right, &mut scratch);

    (left, right)
}