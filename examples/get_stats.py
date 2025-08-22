import pandas as pd

def print_stats(filename, symbol):
    df = pd.read_csv(filename)
    print(f"\n{symbol}:")
    print(f"  Price range: ${df.price.min():.2f} - ${df.price.max():.2f}")
    print(f"  Mean price: ${df.price.mean():.2f}")
    print(f"  Std dev: ${df.price.std():.2f}")
    print(f"  Total return: {((df.price.iloc[-1]/df.price.iloc[0])-1)*100:.2f}%")
    print(f"  Data points: {len(df)}")

print("=== DATASET STATISTICS ===")
print_stats("examples/goog_1m.csv", "GOOG")
