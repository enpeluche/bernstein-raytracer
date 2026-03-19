use criterion::{black_box, criterion_group, criterion_main, Criterion};
use rand::Rng;
use rust_solver::*;



fn generate_data(n: usize) -> Vec<f64> {
    let mut rng = rand::thread_rng();
    (0..n).map(|_| rng.r#gen::<f64>()).collect()
}

fn bench_midpoints(c: &mut Criterion) {

    let sizes = [100, 1_000, 10_000, 1_000_000];

    for &size in &sizes {
        let data = generate_data(size);

        let mut group = c.benchmark_group(format!("midpoints n={}", size));

        group.bench_function("naive", |b| {
            b.iter(|| midpoints_naive(black_box(&data)))
        });

        group.bench_function("iter_zip", |b| {
            b.iter(|| midpoints_iter_zip(black_box(&data)))
        });

        group.bench_function("windows", |b| {
            b.iter(|| midpoints_iter_windows(black_box(&data)))
        });

        group.bench_function("auto_vectorized", |b| {
            b.iter(|| midpoints_auto_vectorized(black_box(&data)))
        });

        group.bench_function("simd", |b| {
            b.iter(|| midpoints_simd(black_box(&data)))
        });

        group.finish();
    }
}

criterion_group!(benches, bench_midpoints);
criterion_main!(benches);