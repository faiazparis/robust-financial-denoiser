#!/usr/bin/env python3
"""Simple script to create variance reduction plot with current accurate data."""

import matplotlib
matplotlib.use('Agg')  # Force non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def main():
    # Current accurate results
    original_variance = 39.1224
    denoised_variance = 1.1248
    reduction_percent = 97.12
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Variance comparison
    labels = ['Original', 'Denoised']
    values = [original_variance, denoised_variance]
    colors = ['#2E86AB', '#A23B72']
    
    bars1 = ax1.bar(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    ax1.set_title('Realized Variance Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Variance', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, value in zip(bars1, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Right: Reduction percentage
    ax2.bar(['GOOG'], [reduction_percent], color='#28A745', alpha=0.8, edgecolor='black', linewidth=1)
    ax2.set_title('Variance Reduction', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Reduction (%)', fontsize=12)
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    
    # Add percentage label
    ax2.text(0, reduction_percent + 1, f'{reduction_percent:.1f}%', 
             ha='center', va='bottom', fontweight='bold', fontsize=14)
    
    # Overall title
    fig.suptitle('Google Stock Denoising Results: 97.12% Variance Reduction', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    
    # Save with high quality
    output_path = 'examples/plots/variance_reduction_summary.png'
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Plot saved: {output_path}")
    print(f"📊 Shows: {original_variance:.2f} → {denoised_variance:.2f} = {reduction_percent:.1f}% reduction")

if __name__ == "__main__":
    main()
