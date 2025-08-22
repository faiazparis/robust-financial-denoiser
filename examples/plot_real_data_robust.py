#!/usr/bin/env python3
"""Generate Google stock before/after plot using the robust denoiser."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rpsd.denoise_robust import DenoiseConfig, wavelet_denoise, evaluate_guardrails

def create_robust_plot():
    """Create a comprehensive plot using the robust denoiser."""
    
    print("=== Google Stock Denoising with Robust Denoiser ===\n")
    
    # Load data
    try:
        df = pd.read_csv('examples/goog_1m.csv')
        print(f"✅ Loaded Google data: {len(df)} observations")
    except FileNotFoundError:
        print("❌ Google data not found. Please run 'python examples/download_data.py' first.")
        return
    
    # Extract prices and timestamps
    prices = df['price'].values
    timestamps = pd.to_datetime(df['timestamp'])
    
    print(f"📊 Data period: {timestamps.iloc[0]} to {timestamps.iloc[-1]}")
    print(f"💰 Price range: ${prices.min():.2f} - ${prices.max():.2f}")
    
    # Configure robust denoiser
    config = DenoiseConfig(
        wavelet='db4',
        max_level_reduction=2,
        alpha=1.0,
        vol_adaptive=True,
        vol_window=60,
        fir_apply=True,
        fir_cutoff_hz=0.01,
        fs_hz=1.0/60.0  # 1 minute bars
    )
    
    print(f"\n🔧 Denoiser configuration:")
    print(f"   Wavelet: {config.wavelet}")
    print(f"   Max level reduction: {config.max_level_reduction}")
    print(f"   Alpha: {config.alpha}")
    print(f"   FIR Filter: {config.fir_apply}")
    
    # Apply robust denoising
    print(f"\n🔄 Applying robust denoising...")
    denoised = wavelet_denoise(prices, config)
    
    # Evaluate results
    print(f"📈 Evaluating denoising quality...")
    report = evaluate_guardrails(prices, denoised, config)
    
    # Calculate essential metrics
    correlation = np.corrcoef(prices, denoised)[0, 1]
    rmse = np.sqrt(np.mean((prices - denoised) ** 2))
    
    # Print results
    print(f"\n📊 DENOISING RESULTS:")
    print(f"   Signal correlation: {correlation:.4f}")
    print(f"   RMSE: {rmse:.4f}")
    
    print(f"\n🛡️  GUARDRAIL ASSESSMENT:")
    print(f"   Correlation: {report.corr:.4f} (threshold: {config.min_correlation:.2f})")
    print(f"   RMSE: {report.rmse:.4f}")
    print(f"   Trend agreement: {report.trend_agreement:.2f} (threshold: {config.min_trend_agreement:.2f})")
    print(f"   Low-freq power: {report.lowfreq_preserve:.4f} (threshold: {config.min_lowfreq_power_preserve:.2f})")
    print(f"   Residual whiteness: {report.residual_white_pval:.4f} (threshold: 0.05)")
    
    # Guardrail compliance
    if report.corr >= config.min_correlation:
        print("✅ Good signal preservation")
    else:
        print("⚠️  Signal preservation below threshold")
    
    if report.rmse <= 0.5:  # Using reasonable RMSE threshold
        print("✅ Good tracking accuracy")
    else:
        print("⚠️  Tracking accuracy below threshold")
    
    if report.trend_agreement >= config.min_trend_agreement:
        print("✅ Good trend preservation")
    else:
        print("⚠️  Trend preservation below threshold")
    
    if report.lowfreq_preserve >= config.min_lowfreq_power_preserve:
        print("✅ Good structure preservation")
    else:
        print("⚠️  Structure preservation below threshold")
    
    if report.residual_white_pval >= 0.05:
        print("✅ Good residual properties")
    else:
        print("⚠️  Residual properties below threshold")
    
    # Calculate compliance score
    compliance_score = (
        min(report.corr / config.min_correlation, 1.0) * 40 +
        min(max(0, 1 - report.rmse / 0.5), 1.0) * 25 +
        min(report.trend_agreement / config.min_trend_agreement, 1.0) * 20 +
        min(report.lowfreq_preserve / config.min_lowfreq_power_preserve, 1.0) * 15
    )
    
    print(f"\n🎯 Overall Compliance Score: {compliance_score:.1f}/100")
    
    # Create visualization
    print(f"\n🎨 Creating robust denoising plot...")
    
    # Sample data for plotting (avoid overcrowding)
    max_points = 500
    if len(prices) > max_points:
        step = len(prices) // max_points
        plot_indices = np.arange(0, len(prices), step)
        plot_prices = prices[plot_indices]
        plot_denoised = denoised[plot_indices]
        plot_timestamps = timestamps.iloc[plot_indices]
    else:
        plot_prices = prices
        plot_denoised = denoised
        plot_timestamps = timestamps
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 1, figsize=(16, 12))
    fig.suptitle('Google Stock Denoising: Robust Wavelet Approach', 
                 fontsize=20, fontweight='bold', y=0.92, color='#2c3e50')
    
    # Top panel: Price series
    ax1 = axes[0]
    ax1.plot(plot_timestamps, plot_prices, label='Original', 
             color='#3498db', linewidth=2, alpha=0.9)
    ax1.plot(plot_timestamps, plot_denoised, label='Denoised', 
             color='#e74c3c', linewidth=2, alpha=0.9)
    ax1.set_title('Price Series', fontsize=16, fontweight='bold', 
                  color='#2c3e50', pad=25)
    ax1.set_ylabel('Price ($)', fontsize=14, fontweight='bold', color='#2c3e50')
    ax1.legend(fontsize=12, framealpha=0.9, loc='upper left')
    ax1.grid(True, alpha=0.2, linestyle='--')
    ax1.tick_params(axis='both', which='major', labelsize=11)
    
    # Bottom panel: Price changes (increments)
    ax2 = axes[1]
    original_changes = np.diff(plot_prices)
    denoised_changes = np.diff(plot_denoised)
    
    ax2.plot(plot_timestamps[1:], original_changes, label='Original Changes', 
             color='#3498db', linewidth=1.5, alpha=0.8)
    ax2.plot(plot_timestamps[1:], denoised_changes, label='Denoised Changes', 
             color='#e74c3c', linewidth=1.5, alpha=0.8)
    ax2.set_title('Price Changes (Increments)', fontsize=16, fontweight='bold', 
                  color='#2c3e50', pad=25)
    ax2.set_xlabel('Time', fontsize=14, fontweight='bold', color='#2c3e50')
    ax2.set_ylabel('Price Change ($)', fontsize=14, fontweight='bold', color='#2c3e50')
    ax2.legend(fontsize=12, framealpha=0.9, loc='upper left')
    ax2.grid(True, alpha=0.2, linestyle='--')
    ax2.tick_params(axis='both', which='major', labelsize=11)
    
    # Add performance summary text with better styling
    summary_text = f"""Performance Summary:
• Signal Correlation: {correlation:.3f}
• RMSE: {rmse:.3f}
• Compliance Score: {compliance_score:.1f}/100
• Trend Preservation: {report.trend_agreement:.1f}%"""
    
    # Position text box in top right with better styling
    ax1.text(0.98, 0.98, summary_text, transform=ax1.transAxes, 
             fontsize=11, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecf0f1', 
                      edgecolor='#bdc3c7', alpha=0.95),
             color='#2c3e50')
    
    plt.tight_layout()
    
    # Save plot
    output_path = 'examples/plots/goog_before_after_robust.png'
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Plot saved: {output_path}")
    print(f"📊 Shows: Original vs. denoised prices with performance metrics")

if __name__ == "__main__":
    create_robust_plot()
