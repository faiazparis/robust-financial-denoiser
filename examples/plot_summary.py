import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def create_summary_plot():
    """Create a summary plot showing variance reduction for both datasets."""
    
    # Data from our analysis
    datasets = ['GOOG']
    rv_original = [39.122448]
    rv_denoised = [11.703872]
    
    # Calculate percentage reductions
    reductions = [(orig - den) / orig * 100 for orig, den in zip(rv_original, rv_denoised)]
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Left plot: Realized Variance comparison
    x = np.arange(len(datasets))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, rv_original, width, label='Original', alpha=0.8, color='skyblue')
    bars2 = ax1.bar(x + width/2, rv_denoised, width, label='Denoised', alpha=0.8, color='lightcoral')
    
    ax1.set_xlabel('Dataset')
    ax1.set_ylabel('Realized Variance')
    ax1.set_title('Realized Variance: Before vs After Denoising')
    ax1.set_xticks(x)
    ax1.set_xticklabels(datasets)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{height:.2f}', ha='center', va='bottom', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{height:.2f}', ha='center', va='bottom', fontsize=9)
    
    # Right plot: Percentage reduction
    colors = ['green' if r > 0 else 'red' for r in reductions]
    bars3 = ax2.bar(datasets, reductions, color=colors, alpha=0.8)
    
    ax2.set_xlabel('Dataset')
    ax2.set_ylabel('Variance Reduction (%)')
    ax2.set_title('Percentage Reduction in Realized Variance')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Add value labels on bars
    for bar, reduction in zip(bars3, reductions):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + (1 if height > 0 else -1),
                f'{reduction:.1f}%', ha='center', va='bottom' if height > 0 else 'top', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('examples/plots/variance_reduction_summary.png', dpi=150, bbox_inches='tight')
    print("Saved variance reduction summary plot: examples/plots/variance_reduction_summary.png")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("DENOISING RESULTS SUMMARY")
    print("="*60)
    
    for i, dataset in enumerate(datasets):
        print(f"\n{dataset}:")
        print(f"  Original RV: {rv_original[i]:.6f}")
        print(f"  Denoised RV: {rv_denoised[i]:.6f}")
        print(f"  Reduction: {reductions[i]:.2f}%")
        print(f"  {'✅ SUCCESS' if reductions[i] > 0 else '❌ INCREASE'}")

if __name__ == "__main__":
    Path("examples/plots").mkdir(parents=True, exist_ok=True)
    create_summary_plot()
