# ATLAS Performance Monitoring & Anomaly Detection

This project satisfies the GSoC 2026 evaluation task for the CERN-HSF ATLAS Automated Software Performance Monitoring project. It provides a native performance monitoring pipeline optimized for macOS (Apple Silicon).

## Project Overview

The system consists of three main components:
1. A process monitor that captures time-series resource usage (CPU, Memory, I/O).
2. A burner tool that generates configurable workloads to simulate typical ATLAS job behaviors.
3. An anomaly detection script that identifies performance deviations using machine learning.

## How to Run

Install the required dependencies:
```bash
pip install psutil pandas scikit-learn matplotlib
```

Run the automated pipeline (generates data and performs analysis):
```bash
python3 atlas_monitor/prmon_native.py --cmd "python3 atlas_monitor/burner.py --mode mem --duration 12 --size 20" --out atlas_monitor/data/normal_mem.csv
python3 atlas_monitor/prmon_native.py --cmd "python3 atlas_monitor/burner.py --mode mem --duration 12 --size 80" --out atlas_monitor/data/anomaly_mem.csv
python3 atlas_monitor/anomaly_detection.py
```

## Approach and Implementation

Since the standard `prmon` tool is Linux-specific (relying on /proc), this implementation uses a native Python monitor built on `psutil`. This allows for accurate tracking of Proportional Set Size (RSS) and CPU cycles on macOS arm64.

The anomaly detection uses an Isolation Forest algorithm. I chose this approach because it is highly effective at identifying outliers in time-series data without needing to define complex statistical thresholds manually. It treats the performance metrics as a multi-dimensional space and isolates points that are "few and far between."

## Analysis of Results

The generated plots show the memory footprint of a process under normal versus high-load conditions. The red markers indicate points where the memory usage deviated significantly from the "normal" baseline observed in the first half of the dataset.

Trade-offs:
- Using Python provides high portability and quick iteration but introduces slightly more overhead than the C++ original.
- The monitoring interval is set to 0.5s to balance resolution with system stability on the M1 Pro.

## AI Disclosure

I used Claude (via Antigravity) to assist with the code structure, dependency management on macOS, and documentation design. The core logic and monitoring strategy were developed through iterative prompt engineering to meet the specific CERN-HSF requirements.
