# Amazing Mazes

A comprehensive maze generation and solving system implementing multiple algorithms for performance comparison and analysis. This project explores the legendary labyrinth of Crete through modern algorithmic approaches, from Daedalus' original design to automated generation and intelligent pathfinding.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Architecture](#architecture)
7. [Performance Analysis](#performance-analysis)
8. [Documentation](#documentation)
9. [Roadmap](#roadmap)
10. [Contributors](#contributors)
11. [License](#license)

---

## Overview

Amazing Mazes is a Python-based project that generates and solves perfect mazes using different algorithmic approaches. Inspired by the Greek mythology of Theseus and the Minotaur, this system implements both classical and modern algorithms to create unique maze experiences and analyze their computational complexity.

The project focuses on perfect mazes where there exists exactly one unique path between any two empty spaces. Multiple generation and solving algorithms are implemented to provide comprehensive performance comparisons across different maze sizes.

**Technologies used:**
- Python 3.10
- DuckDB for data analysis
- Pandas & NumPy for data manipulation
- Matplotlib & Seaborn for visualization
- SciPy & Statsmodels for statistical analysis

---

## Features

- **Multiple Generation Algorithms:**
  - Recursive Backtracking for simple, efficient maze creation
  - Kruskal's Algorithm for more complex maze structures

- **Advanced Solving Capabilities:**
  - Recursive Backtracking solver for basic pathfinding
  - A* (AStar) algorithm for optimal path discovery

- **Performance Analysis:**
  - Comprehensive metrics collection and analysis
  - Statistical comparison between algorithms
  - Performance testing on large-scale mazes (1K, 10K, 100K cells)

- **Visual Output:**
  - ASCII representation with clear symbols (# for walls, . for paths)
  - Solution visualization (o for solution path, * for explored areas)
  - Image conversion capabilities for better visualization

- **Perfect Maze Generation:**
  - Ensures unique paths between any two points
  - Configurable maze sizes with consistent entry/exit points
  - Top-left entrance, bottom-right exit positioning

---

## Prerequisites

- **Python 3.10 or higher**
- **Required Libraries:**
  - duckdb
  - pandas
  - matplotlib
  - seaborn
  - numpy
  - scipy
  - statsmodels

- **System Requirements:**
  - Windows/Linux/MacOS
  - Sufficient RAM for large maze processing (recommended 8GB+ for 100K cell mazes)

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/username/amazing-mazes.git
cd amazing-mazes
pip install -r requirements.txt
```

**Manual installation of dependencies:**
```bash
pip install duckdb pandas matplotlib seaborn numpy scipy statsmodels
```

---

## Usage

### Maze Generation

**Recursive Backtracking Generator:**
```bash
python backtrack_constructor.py
# Follow prompts for maze size and output filename
```

**Kruskal Algorithm Generator:**
```bash
python kruskal_strict.py
# Follow prompts for maze size and output filename
```

### Maze Solving

**Solve generated mazes:**
```bash
python mazes_solvers.py
# Follow prompts for input maze file and desired solver algorithm
```

### Performance Analysis

**Run metrics collection:**
```bash
python metrics_record.py
python solver_metric.py
```

**View detailed analysis:**
```bash
jupyter notebook amazing_mazes_report.ipynb
```

### Input/Output Format

- **Input:** Integer value for maze size (n x n grid)
- **Output:** Text files (.txt) with ASCII representation
  - `#` - Walls
  - `.` - Empty paths
  - `o` - Solution path
  - `*` - Explored but not part of final solution

---

## Architecture

```
amazing-mazes/
├── README.md                    # Project documentation
├── __pycache__/                 # Python cache files
├── amazing_mazes_report.ipynb   # Interactive analysis notebook
├── amazing_mazes_report.pdf     # Complete performance analysis report
├── anaconda_projects/           # Anaconda environment configurations
├── backtrack_constructor.py     # Recursive backtracking maze generator
├── constructors_metrics.csv     # Generation algorithm performance data
├── kruskal_grids/              # Generated mazes using Kruskal algorithm
├── kruskal_strict.py           # Kruskal algorithm maze generator
├── mazes_solvers.py            # Unified maze solving system
├── metrics_record.py           # Performance metrics collection
├── pictures/                   # Visual outputs and maze images
├── recursive_grids/            # Generated mazes using recursive backtrack
├── solver_metric.py            # Solver performance analysis
└── solver_metrics.csv          # Solving algorithm performance data
```

**Core Components:**
- **Generation Module:** Creates perfect mazes using different algorithms
- **Solving Module:** Implements pathfinding with performance tracking
- **Metrics Module:** Collects and analyzes algorithmic performance
- **Analysis Module:** Statistical comparison and visualization

---

## Performance Analysis

The project includes comprehensive performance analysis comparing:

- **Generation Algorithms:** Recursive Backtracking vs Kruskal
- **Solving Algorithms:** Recursive Backtracking vs A*
- **Scalability:** Performance across maze sizes (1K to 100K cells)
- **Complexity Analysis:** Time and space complexity measurements

Key findings and detailed statistical analysis are available in both the interactive notebook (`amazing_mazes_report.ipynb`) and the complete PDF report (`amazing_mazes_report.pdf`).

---

## Documentation

The project includes comprehensive documentation in multiple formats:

### Interactive Analysis
- **`amazing_mazes_report.ipynb`** - Jupyter notebook with executable code, interactive visualizations, and detailed analysis
  - Real-time code execution
  - Interactive plots and charts
  - Step-by-step methodology explanation

### Complete Report
- **`amazing_mazes_report.pdf`** - Comprehensive performance analysis report
  - Executive summary of findings
  - Detailed algorithmic comparisons
  - Statistical analysis and conclusions
  - Performance benchmarks and recommendations
  - Visual representations of all key metrics

**Accessing the Documentation:**
```bash
# View interactive notebook
jupyter notebook amazing_mazes_report.ipynb

# View PDF report (requires PDF viewer)
open amazing_mazes_report.pdf
# or
xdg-open amazing_mazes_report.pdf  # Linux
# or
start amazing_mazes_report.pdf     # Windows
```

---

## Roadmap

### Completed
- Basic maze generation (Recursive Backtracking)
- Advanced maze generation (Kruskal)
- Multiple solving algorithms
- Performance metrics collection
- Statistical analysis framework
- Comprehensive documentation (notebook + PDF report)

### Future Enhancements
- Additional generation algorithms (Prim's, Wilson's)
- Interactive maze visualization
- Web-based interface
- 3D maze generation capabilities
- Multi-threading for large maze processing

---

## Contributors

- **Khady Ndiaye** - Algorithm implementation and performance analysis
- **Paul-Emmanuel Buffe** - System architecture and statistical modeling

---

## License

This project is part of an academic assignment exploring algorithmic complexity and maze generation techniques. All code is provided for educational purposes.