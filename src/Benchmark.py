import json
import datetime
import platform
import timeit
import os


class Benchmark:
    def __init__(self, context, filename, name, loops, values):
        self.filename = filename
        self.context = context
        self.loops = loops
        self.metadata = {
            "name": name,
            "date": str(datetime.datetime.now()),
            "loops": loops,
            "node": platform.node(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
            "python_version": platform.python_version(),
            "python_impl": platform.python_implementation(),
            "python_compiler": platform.python_compiler(),
        }
        self.benchmarks = []
        self.values = values

    def run_test(self, config, name):

        print(f"run test for {name}")
        setup_template = config.get("setup", "pass")
        stmt = config["stmt"]

        results = []

        for k in self.values:
            print(k)
            current_context = self.context.copy()
            current_context["k"] = k

            try:
                timer = timeit.Timer(
                    stmt=stmt, setup=setup_template, globals=current_context
                )

                total_time = timer.timeit(number=self.loops)

                avg_time = total_time / self.loops * 1_000_000

                results.append({"k": k, "duration": avg_time})

            except Exception as e:
                print(f"Crash pour k={k} dans le benchmark {name}")

        self.benchmarks.append({"name": name, "results": results})

    def save(self):
        folder = "benchmarks/" + self.filename

        if not os.path.exists(folder):
            os.makedirs(folder)

        full_path = os.path.join(folder, "benchmark.json")

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(
                {"metadata": self.metadata, "benchmarks": self.benchmarks}, f, indent=2
            )

    def plot(self, output_image="benchmark_plot.png"):

        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 7))

        colors = ["#e74c3c", "#2ecc71", "#3498db", "#f1c40f", "#9b59b6"]
        markers = ["o", "s", "^", "D", "*"]

        for i, benchmark in enumerate(self.benchmarks):

            test_name = benchmark.get("name", f"Test #{i}")
            results = benchmark.get("results", [])

            degrees = [r["k"] for r in results]
            times = [r["duration"] for r in results]

            color = colors[i % len(colors)]
            marker = markers[i % len(markers)]
            plt.plot(
                degrees,
                times,
                label=test_name,
                marker=marker,
                linestyle="-",
                linewidth=2,
                color=color,
                alpha=0.8,
            )

        run_name = self.metadata.get("name", "Benchmark")
        plt.title(f"Résultats : {run_name}", fontsize=16, fontweight="bold")

        plt.xlabel("Taille (k)", fontsize=12)
        plt.ylabel("Temps moyen (µs)", fontsize=12)
        plt.grid(True, linestyle=":", alpha=0.6)

        plt.legend(fontsize=11, loc="best", frameon=True, shadow=True)

        plt.tight_layout()
        folder = "benchmarks/" + self.filename
        if not os.path.exists(folder):
            os.makedirs(folder)

        full_path = os.path.join(folder, "plot.png")

        plt.savefig(full_path, dpi=300)

        plt.show()
