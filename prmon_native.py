import psutil
import time
import csv
import argparse
import subprocess
import os

def monitor(command, interval, output_file):
    process = subprocess.Popen(command, shell=True)
    ps_proc = psutil.Process(process.pid)
    
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "CPU", "RSS", "VMS", "IO_Read", "IO_Write"])
        
        start_time = time.time()
        try:
            while process.poll() is None:
                try:
                    stats = ps_proc.memory_info()
                    cpu = ps_proc.cpu_percent(interval=None)
                    io = ps_proc.io_counters() if hasattr(ps_proc, "io_counters") else None
                    
                    writer.writerow([
                        round(time.time() - start_time, 2),
                        cpu,
                        stats.rss,
                        stats.vms,
                        io.read_bytes if io else 0,
                        io.write_bytes if io else 0
                    ])
                    f.flush()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                time.sleep(interval)
        except KeyboardInterrupt:
            process.terminate()
        
    process.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--interval", type=float, default=0.5)
    args = parser.parse_args()
    
    monitor(args.cmd, args.interval, args.out)
