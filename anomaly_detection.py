import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import numpy as np
import os

def detect_anomalies():
    normal = pd.read_csv("atlas_monitor/data/normal_mem.csv")
    anomaly = pd.read_csv("atlas_monitor/data/anomaly_mem.csv")
    
    normal["Label"] = 1
    anomaly["Label"] = -1
    
    df = pd.concat([normal, anomaly]).reset_index(drop=True)
    
    model = IsolationForest(contamination=0.1, random_state=42)
    df["Prediction"] = model.fit_predict(df[["RSS"]])
    
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["RSS"] / (1024*1024), label="Memory Usage (MB)", color="blue")
    
    anomalies = df[df["Prediction"] == -1]
    plt.scatter(anomalies.index, anomalies["RSS"] / (1024*1024), color="red", label="Detected Anomaly", s=10)
    
    plt.title("Performance Monitoring: Memory Usage with Anomaly Detection")
    plt.xlabel("Step")
    plt.ylabel("RSS (MB)")
    plt.legend()
    plt.grid(True)
    plt.savefig("atlas_monitor/plots/anomaly_detection.png")
    
    print("\nEvaluation Summary")
    print("-" * 20)
    print(f"Total samples analyzed: {len(df)}")
    print(f"Injected anomalies: {len(anomaly)}")
    print(f"Detected anomalies: {len(anomalies)}")
    print(f"Plot saved to: atlas_monitor/plots/anomaly_detection.png")

if __name__ == "__main__":
    detect_anomalies()
