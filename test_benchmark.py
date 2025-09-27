from benchmarking.benchmark_runner import BenchmarkRunner

runner = BenchmarkRunner()
results = runner.run_comparative_benchmark([
    {'requests': 50, 'concurrent': 5, 'name': 'Test Load'}
])
print(results)
