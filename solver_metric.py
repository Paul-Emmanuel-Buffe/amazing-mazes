import csv
import os
import time
import psutil
from datetime import datetime

class SolverMetricsLogger:
    def __init__(self, csv_file="solver_metrics.csv"):
        self.csv_file = csv_file
        self.start_time = None
        self.initial_memory = None
        self.nodes_explored = 0
        self.path_length = 0
        self.current_metrics = {}

        # colonnes adaptées au solveur
        self.columns = [
            "timestamp","maze_name", "maze_size", "algorithm",
            "solve_time_ms", "ram_peak_mb", "file_size_bytes",
            "nodes_explored", "path_length"
        ]

        self._init_csv()

    def _init_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)

    def start(self, maze_name, maze_size, algorithm):
        self.start_time = time.perf_counter()
        try:
            self.initial_memory = psutil.Process().memory_info().rss / (1024 * 1024)
        except:
            self.initial_memory = 0

        self.nodes_explored = 0
        self.path_length = 0

        self.current_metrics = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "maze_name": maze_name,
            "maze_size": maze_size,
            "algorithm": algorithm
            
        }

    def increment_nodes(self):
        self.nodes_explored += 1

    def set_path_length(self, length):
        self.path_length = length

    def stop(self, filename):
        if self.start_time is None:
            raise RuntimeError("SolverMetricsLogger.stop() appelé avant start()")

        solve_time = (time.perf_counter() - self.start_time) * 1000  # en ms

        try:
            final_memory = psutil.Process().memory_info().rss / (1024 * 1024)
            peak_memory = max(self.initial_memory, final_memory)
        except:
            peak_memory = 0

        file_size = os.path.getsize(filename) if os.path.exists(filename) else 0

        self.current_metrics.update({
            "solve_time_ms": round(solve_time, 2),
            "ram_peak_mb": round(peak_memory, 2),
            "file_size_bytes": file_size,
            "nodes_explored": self.nodes_explored,
            "path_length": self.path_length
        })

        with open(self.csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            row = [self.current_metrics[col] for col in self.columns]
            writer.writerow(row)

        self.start_time = None

    def print_metrics(self):
        print("\n" + "="*30)
        print("RÉSUMÉ DES MÉTRIQUES SOLVEUR")
        print("="*30)
        for col in self.current_metrics:
            print(f"{col:>20}: {self.current_metrics[col]}")
        print("="*30 + "\n")