import csv
import os
import time
import psutil # enregistrement de l'empreinte mémoire
from datetime import datetime

class MetricsLogger:
# centralise l'écriture des métriques
# garde l'empreinte temporaire entre start et stop

    def __init__(self, csv_file="kruskal_strict.csv"):
        self.csv_file = csv_file
        self.start_time  = None
        self.initial_memory = None
        self .backtrack_count = 0
        self.edges_processed = 0
        self.current_metrics = {} # disctionnaire temporaire 
                                # servant de dépot avant record to csv

        # noms des colonnes 
        self.columns = [
            "timestamp", "filename", "maze_size", "seed", "algorithm",
            "generation_time_ms", "ram_peak_mb", "file_size_bytes",
            "backtrack_count", "edges_processed"
        ]

        self._init_csv() 

    def _init_csv(self): # création de l'en-tête si fichier non existant
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns) # prends la valeur de la liste de la variable self.columns

    # Début de la prise des métriques
    def start(self, maze_size, algorithm, seed=None):
        self.start_time = time.perf_counter() # lancement du chrono
        try:
            self.initial_memory = psutil.Process().memory_info().rss / (1024 * 1024) # quantité de RAM occupé au moment précis
                                                                                     # où on appelle cette methode
                                                                                     # ex : 50 mo => rss =  50 x 1024 x 1024 = 52428800
                                                                                     # on divise par (1024 x 1024) pour une mailleure lecture
        except:
            self.initial_memory = 0

        self .backtrack_count = 0
        self.edges_processed = 0

        self.current_metrics = {
            "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "maze_size" : maze_size,
            "algorithm" : algorithm,
            "seed" : seed if seed is not None else ""
        }


    def increment_edge(self):
        self.edges_processed += 1

    def increment_backtrack(self):
        self.backtrack_count += 1


