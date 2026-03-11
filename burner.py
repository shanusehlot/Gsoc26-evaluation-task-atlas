import time
import argparse
import os

def cpu_load(duration):
    start = time.time()
    while time.time() - start < duration:
        _ = [x**2 for x in range(1000)]

def mem_load(duration, size_mb):
    data = []
    chunk = " " * (1024 * 1024)
    for _ in range(size_mb):
        data.append(chunk)
    time.sleep(duration)
    del data

def io_load(duration, filename="temp_io.dat"):
    start = time.time()
    while time.time() - start < duration:
        with open(filename, "wb") as f:
            f.write(os.urandom(1024 * 1024))
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["cpu", "mem", "io"], required=True)
    parser.add_argument("--duration", type=int, default=10)
    parser.add_argument("--size", type=int, default=50)
    args = parser.parse_args()

    if args.mode == "cpu":
        cpu_load(args.duration)
    elif args.mode == "mem":
        mem_load(args.duration, args.size)
    elif args.mode == "io":
        io_load(args.duration)
