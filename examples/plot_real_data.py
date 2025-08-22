import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def create_comparison_plot(original_file: str, denoised_file: str, title: str, output_file: str, max_points: int = 1000):
    """Create a before/after comparison plot for real financial data."""
    
    # Load data
    df_orig = pd.read_csv(original_file)
    df_den = pd.read_csv(denoised_file)
    
    # Merge on timestamp
    merged = df_orig.merge(df_den, on='timestamp', suffixes=('_orig', '_den'))
    
    # Limit points for visualization
    N = min(max_points, len(merged))
    data = merged.head(N)
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Top plot: Price series
    ax1.plot(data['timestamp'], data['price_orig'], alpha=0.7, label='Original', linewidth=1)
    ax1.plot(data['timestamp'], data['price_den'], alpha=0.9, label='Denoised', linewidth=1.5)
    ax1.set_ylabel('Price')
    ax1.set_title(f'{title} - Price Series Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Bottom plot: Price differences (increments)
    price_diff_orig = np.diff(data['price_orig'])
    price_diff_den = np.diff(data['price_den'])
    timestamps_diff = data['timestamp'].iloc[1:].values
    
    ax2.plot(timestamps_diff, price_diff_orig, alpha=0.7, label='Original increments', linewidth=1)
    ax2.plot(timestamps_diff, price_diff_den, alpha=0.9, label='Denoised increments', linewidth=1.5)
    ax2.set_ylabel('Price Increments')
    ax2.set_xlabel('Time')
    ax2.set_title('Price Increments Comparison')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved plot: {output_file}")
    
    # Print statistics
    rv_orig = np.sum(price_diff_orig**2)
    rv_den = np.sum(price_diff_den**2)
    reduction = (rv_orig - rv_den) / rv_orig * 100
    
    print(f"Realized Variance - Original: {rv_orig:.6f}")
    print(f"Realized Variance - Denoised: {rv_den:.6f}")
    print(f"Reduction: {reduction:.2f}%")

if __name__ == "__main__":
    # Create plots directory
    Path("examples/plots").mkdir(parents=True, exist_ok=True)
    
    # Plot Google data
    print("Creating Google (GOOG) comparison plot...")
    create_comparison_plot(
        "examples/goog_1m.csv",
        "out/goog_denoised.csv", 
        "Google (GOOG) - 1 Minute Data",
        "examples/plots/goog_before_after.png"
    )
    
    print("\n" + "="*50 + "\n")
    
    print("\nAll plots generated successfully!")
