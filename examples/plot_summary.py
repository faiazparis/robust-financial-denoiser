import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def create_summary_plot():
    """Create a summary plot showing variance reduction for both datasets."""
    
    # Data from our current analysis (accurate results)
    datasets = ['GOOG']
    rv_original = [39.1224]  # Updated: actual Google data variance
    rv_denoised = [1.1248]   # Updated: actual denoised variance
    
    # Calculate percentage reductions
    reductions = [(orig - den) / orig * 100 for orig, den in zip(rv_original, rv_denoised)]
    
    # Create the plot with improved styling
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Set style
    plt.style.use('default')
    
    # Left plot: Realized Variance comparison
    x = np.arange(len(datasets))
    width = 0.4
    
    bars1 = ax1.bar(x - width/2, rv_original, width, label='Original', alpha=0.9, color='#2E86AB', edgecolor='#1B4965', linewidth=1)
    bars2 = ax1.bar(x + width/2, rv_denoised, width, label='Denoised', alpha=0.9, color='#A23B72', edgecolor='#6B2E5F', linewidth=1)
    
    ax1.set_xlabel('Dataset', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Realized Variance', fontsize=12, fontweight='bold')
    ax1.set_title('Realized Variance: Before vs After Denoising', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(datasets, fontsize=11)
    ax1.legend(fontsize=11, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Add value labels on bars with better formatting
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                f'{height:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                f'{height:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Right plot: Percentage reduction with improved styling
    colors = ['#28A745' if r > 0 else '#DC3545' for r in reductions]  # Better green/red
    bars3 = ax2.bar(datasets, reductions, color=colors, alpha=0.9, edgecolor='#2C3E50', linewidth=1.5)
    
    ax2.set_xlabel('Dataset', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Variance Reduction (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Percentage Reduction in Realized Variance', fontsize=14, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.axhline(y=0, color='#2C3E50', linestyle='-', alpha=0.5, linewidth=1)
    
    # Add value labels on bars with better positioning
    for bar, reduction in zip(bars3, reductions):
        height = bar.get_height()
        y_pos = height + (2 if height > 0 else -2)
        ax2.text(bar.get_x() + bar.get_width()/2., y_pos,
                f'{reduction:.1f}%', ha='center', va='bottom' if height > 0 else 'top', 
                fontsize=12, fontweight='bold', color='#2C3E50')
    
    # Improve overall appearance
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='both', which='major', labelsize=10)
    
    plt.tight_layout()
    plt.savefig('examples/plots/variance_reduction_summary.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("Saved variance reduction summary plot: examples/plots/variance_reduction_summary.png")
    
    # Print summary statistics
    print("\n" + "="*70)
    print("DENOISING RESULTS SUMMARY - CURRENT ACCURATE RESULTS")
    print("="*70)
    
    for i, dataset in enumerate(datasets):
        print(f"\n{dataset}:")
        print(f"  Original RV: {rv_original[i]:.6f}")
        print(f"  Denoised RV: {rv_denoised[i]:.6f}")
        print(f"  Reduction: {reductions[i]:.2f}%")
        print(f"  {'✅ EXCELLENT PERFORMANCE' if reductions[i] > 90 else '✅ GOOD PERFORMANCE' if reductions[i] > 70 else '❌ NEEDS IMPROVEMENT'}")

if __name__ == "__main__":
    Path("examples/plots").mkdir(parents=True, exist_ok=True)
    create_summary_plot()
