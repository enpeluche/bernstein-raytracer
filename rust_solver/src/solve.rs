pub fn solve(
    tab: &mut [f64],        // Les coeffs actuels
    t1: f64,
    t2: f64,
    v_min: f64,
    v_max: f64,
    solutions: &mut Vec<f64>,
    depth: usize,
) {
    // 1. Test enveloppe convexe (Rapide et sans copie)
    let mut min_val = tab[0];
    let mut max_val = tab[0];
    for &x in tab.iter() {
        if x < min_val { min_val = x; }
        if x > max_val { max_val = x; }
    }
    if min_val > 0.0 || max_val < 0.0 { return; }

    // 2. Précision / Limite
    let dt = t2 - t1;
    if dt < 1e-6 || depth > 20 {
        solutions.push(0.5 * (t1 + t2));
        return;
    }

    // 3. Subdivision IN-PLACE (La magie de Casteljau)
    let n = tab.len();
    let tm = 0.5 * (t1 + t2);

    // On crée deux buffers temporaires pour la descente
    // Rust est si rapide qu'on peut se permettre ces deux-là si on ne peut pas faire autrement,
    // mais l'idéal est de travailler sur des portions du tableau original.
    let mut left = vec![0.0; n];
    let mut right = vec![0.0; n];

    // Algorithme de Casteljau qui remplit left et right
    let mut temp = tab.to_vec();
    left[0] = temp[0];
    right[n-1] = temp[n-1];
    for i in 1..n {
        for k in 0..(n - i) {
            temp[k] = 0.5 * (temp[k] + temp[k + 1]);
        }
        left[i] = temp[0];
        right[n - 1 - i] = temp[n - 1];
    }

    // 4. Appels récursifs
    solve(&mut left, t1, tm, v_min, v_max, solutions, depth + 1);
    solve(&mut right, tm, t2, v_min, v_max, solutions, depth + 1);
}