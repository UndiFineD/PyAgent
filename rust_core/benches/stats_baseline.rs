use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};

fn benchmark_stats_baseline(c: &mut Criterion) {
    let dataset: Vec<f64> = (0..1024).map(|x| x as f64).collect();
    let mut group = c.benchmark_group("stats/core");

    group.bench_with_input(BenchmarkId::new("sum/1k"), &dataset, |b, data| {
        b.iter(|| {
            let sum = data.iter().copied().sum::<f64>();
            black_box(sum)
        })
    });

    group.finish();
}

criterion_group!(benches, benchmark_stats_baseline);
criterion_main!(benches);
