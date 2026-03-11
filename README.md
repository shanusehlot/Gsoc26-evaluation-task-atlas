# ATLAS Software Performance Monitoring – GSoC 2026 Evaluation

This is my submission for the warm-up exercise for the CERN-HSF GSoC 2026 project on automated software performance monitoring for the ATLAS experiment.

The task was to generate real process-level time-series data using a monitoring tool, inject anomalies, and apply an automated method to detect them.

---

## Structure

```
atlas_monitor/
├── burner.py
├── prmon_native.py
├── anomaly_detection.py
├── data/
│   ├── normal_mem.csv
│   └── anomaly_mem.csv
└── plots/
    └── anomaly_detection.png
```

`burner.py` generates a controlled memory workload. Pass it a size and duration and it allocates that memory and holds it for the run.

`prmon_native.py` monitors a subprocess and records RSS memory, CPU, and I/O at 0.5-second intervals. Standard `prmon` relies on `/proc` and does not run on macOS, so this script uses `psutil` instead, which gives the same metrics on Apple Silicon.

`anomaly_detection.py` loads the two CSVs, combines them into a single labeled time series, runs Isolation Forest on the RSS column, and saves the result to `plots/`.

---

## How to run

```
pip install psutil pandas scikit-learn matplotlib
```

```
python3 atlas_monitor/prmon_native.py \
  --cmd "python3 atlas_monitor/burner.py --mode mem --duration 12 --size 20" \
  --out atlas_monitor/data/normal_mem.csv

python3 atlas_monitor/prmon_native.py \
  --cmd "python3 atlas_monitor/burner.py --mode mem --duration 12 --size 80" \
  --out atlas_monitor/data/anomaly_mem.csv

python3 atlas_monitor/anomaly_detection.py
```

---

## Results

Both runs lasted 12 seconds, sampled every 0.5 seconds, giving 24 data points each and 48 total.

The 20MB run forms a flat baseline. The 80MB run sits clearly above it. Isolation Forest was set with a contamination rate of 0.1, meaning it was told to expect about 10% of points to be anomalous.

It flagged 4 points, all from the 80MB run. Precision was 100% — no false alarms. Recall was 16.6% — it caught the most extreme part of the spike but not the whole block.

Overall accuracy across all 48 samples was around 58%. That number looks low, but it reflects a deliberate choice: the algorithm was configured for a scenario where anomalies are rare. In a real monitoring system, true anomalies are infrequent, so a contamination of 0.1 is a reasonable starting point. Raising it improves recall but introduces false alarms.

---

## Why Isolation Forest

Isolation Forest partitions data randomly and measures how quickly each point gets isolated. Points far from the main cluster get isolated in fewer splits, so they score as anomalies. It does not assume any particular distribution, which matters because memory usage patterns in ATLAS pipelines are not guaranteed to be Gaussian.

The alternative I considered was a Z-score threshold. For a simple two-regime dataset like this one, Z-score would likely catch the entire 80MB block since it sits several standard deviations above the mean. The trade-off is that Z-score is fragile when the baseline drifts or when anomalies appear gradually rather than as a sharp spike. Isolation Forest handles those cases better, at the cost of being harder to interpret and tune.

For a production ATLAS monitoring system, you would want to tune the contamination parameter against real incident history, or use an adaptive threshold that adjusts as the baseline evolves over time.

---

## AI disclosure

I used Claude (Anthropic) for code generation and script structure. The choice of algorithm, parameter values, and interpretation of results are my own. All code was reviewed and tested before inclusion.
