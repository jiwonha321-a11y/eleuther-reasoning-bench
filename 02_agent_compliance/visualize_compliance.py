import os
import matplotlib.pyplot as plt
import seaborn as sns

def generate_compliance_chart(output_path="02_agent_compliance/agent_compliance_chart.png"):
    """
    Generates a high-resolution bar chart demonstrating the programmatic suppression
    of deceptive compliance rates before and after implementing hierarchical auditing protocols.
    """
    # Ensure the target directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set professional presentation styling
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'figure.titlesize': 16
    })

    # Experimental configuration data mapping
    configurations = [
        'Native Unmonitored\n(Baseline Configuration)', 
        'Hierarchical Auditing\n(Layered Guard Protocols)'
    ]
    deceptive_rates = [88.5, 12.0] # Quantified suppression metrics from the framework profile
    colors = ['#DE5D4E', '#2A9D8F'] # High-contrast structural alerting vs. safe-state color palette

    # Initialize figures and dimensions
    fig, ax = plt.subplots(figsize=(7, 5.5))
    
    # Render operational bars
    bars = ax.bar(configurations, deceptive_rates, color=colors, width=0.5, edgecolor='#333333', linewidth=1.2)

    # Inscribe numerical precision values atop each structural vector
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', 
                    fontweight='bold', color='#222222')

    # Y-axis boundaries alignment
    ax.set_ylim(0, 100)
    ax.set_ylabel('Deceptive Compliance / Shortcut Rate (%)', fontweight='bold', labelpad=10)
    ax.set_title('Deceptive Compliance Suppression Profile under Adversarial Stress', fontweight='bold', pad=20)

    # Refine layout and purge axis chart redundancy
    plt.tight_layout()
    sns.despine(left=True, bottom=False)

    # Programmatic asset write execution
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Security analysis chart programmatically generated and saved to: {output_path}")

if __name__ == "__main__":
    generate_compliance_chart()