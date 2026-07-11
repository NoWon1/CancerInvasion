import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')

class CC3DViolin:
    """
    Class to analyze CC3D simulation data and generate violin plots
    for collective migration analysis
    """
    
    def __init__(self):
        self.data = None
        self.results = {}
        
    def load_simulation_data(self, data_path=None, simulation_data=None):
        """
        Load CC3D simulation results
        
        Parameters:
        -----------
        data_path : str, optional
            Path to CSV file containing simulation results
        simulation_data : dict, optional
            Dictionary containing simulation results
        """
        if data_path:
            self.data = pd.read_csv(data_path)
        elif simulation_data:
            self.data = pd.DataFrame(simulation_data)
        else:
            # Generate sample data for demonstration
            self.data = self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate sample data matching the experimental setup"""
        np.random.seed(42)
        
        # Parameters for different adhesion strengths
        conditions = {
            'Cell-cell adhesion halved': {
                'area_mean': 25000, 'area_std': 3000,
                'clusters_mean': 4.5, 'clusters_std': 0.8
            },
            'Model cell-cell adhesion': {
                'area_mean': 18000, 'area_std': 2000,
                'clusters_mean': 3.2, 'clusters_std': 0.6
            },
            'Cell-cell adhesion doubled': {
                'area_mean': 14000, 'area_std': 1500,
                'clusters_mean': 1.8, 'clusters_std': 0.4
            }
        }
        
        # Generate data for 50 simulations per condition
        data_list = []
        for condition, params in conditions.items():
            for sim in range(50):
                area = np.random.normal(params['area_mean'], params['area_std'])
                clusters = np.random.normal(params['clusters_mean'], params['clusters_std'])
                clusters = max(1, int(clusters))  # Ensure at least 1 cluster
                
                data_list.append({
                    'condition': condition,
                    'simulation_id': sim,
                    'area_largest_cluster': max(0, area),
                    'num_disconnected_clusters': clusters,
                    'adhesion_type': 'cell-cell'
                })
        
        # Add cell-ECM adhesion data
        ecm_conditions = {
            'Cell-ECM adhesion halved': {
                'area_mean': 15000, 'area_std': 2500,
                'clusters_mean': 3.8, 'clusters_std': 0.7
            },
            'Model cell-ECM adhesion': {
                'area_mean': 18000, 'area_std': 2200,
                'clusters_mean': 2.8, 'clusters_std': 0.5
            },
            'Cell-ECM adhesion doubled': {
                'area_mean': 28000, 'area_std': 3500,
                'clusters_mean': 1.2, 'clusters_std': 0.3
            }
        }
        
        for condition, params in ecm_conditions.items():
            for sim in range(50):
                area = np.random.normal(params['area_mean'], params['area_std'])
                clusters = np.random.normal(params['clusters_mean'], params['clusters_std'])
                clusters = max(1, int(clusters))
                
                data_list.append({
                    'condition': condition,
                    'simulation_id': sim,
                    'area_largest_cluster': max(0, area),
                    'num_disconnected_clusters': clusters,
                    'adhesion_type': 'cell-ECM'
                })
        
        return pd.DataFrame(data_list)
    
    def perform_statistical_analysis(self, metric, adhesion_type):
        """
        Perform one-way ANOVA with Tukey post-hoc analysis
        
        Parameters:
        -----------
        metric : str
            'area_largest_cluster' or 'num_disconnected_clusters'
        adhesion_type : str
            'cell-cell' or 'cell-ECM'
        """
        # Filter data for specific adhesion type
        filtered_data = self.data[self.data['adhesion_type'] == adhesion_type]
        
        # Group data by condition
        groups = []
        group_names = []
        for condition in filtered_data['condition'].unique():
            group_data = filtered_data[filtered_data['condition'] == condition][metric]
            groups.append(group_data)
            group_names.append(condition)
        
        # Perform one-way ANOVA
        f_stat, p_value = f_oneway(*groups)
        
        # Perform Tukey post-hoc test
        tukey_results = pairwise_tukeyhsd(
            filtered_data[metric], 
            filtered_data['condition'], 
            alpha=0.05
        )
        
        return {
            'f_stat': f_stat,
            'p_value': p_value,
            'tukey_results': tukey_results,
            'group_names': group_names
        }
    
    def create_violin_plot(self, adhesion_type, figsize=(12, 8)):
        """
        Create violin plots for both metrics
        
        Parameters:
        -----------
        adhesion_type : str
            'cell-cell' or 'cell-ECM'
        figsize : tuple
            Figure size
        """
        # Filter data
        plot_data = self.data[self.data['adhesion_type'] == adhesion_type].copy()
        
        # Create figure with subplots
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Define order for conditions
        if adhesion_type == 'cell-cell':
            order = ['Cell-cell adhesion halved', 'Model cell-cell adhesion', 'Cell-cell adhesion doubled']
        else:
            order = ['Cell-ECM adhesion halved', 'Model cell-ECM adhesion', 'Cell-ECM adhesion doubled']
        
        # Plot 1: Area of largest cluster
        sns.violinplot(
            data=plot_data,
            x='condition',
            y='area_largest_cluster',
            order=order,
            ax=axes[0],
            palette=['lightblue', 'lightgreen', 'lightcoral'],
            inner='box'
        )
        axes[0].set_title('Area of largest cell cluster', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Area of largest cell cluster', fontsize=12)
        axes[0].set_xlabel('')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Add statistical significance
        stats_area = self.perform_statistical_analysis('area_largest_cluster', adhesion_type)
        self._add_significance_bars(axes[0], stats_area, plot_data, 'area_largest_cluster', order)
        
        # Plot 2: Number of disconnected clusters
        sns.violinplot(
            data=plot_data,
            x='condition',
            y='num_disconnected_clusters',
            order=order,
            ax=axes[1],
            palette=['lightblue', 'lightgreen', 'lightcoral'],
            inner='box'
        )
        axes[1].set_title('Number of disconnected cell clusters', fontsize=14, fontweight='bold')
        axes[1].set_ylabel('Number of disconnected cell clusters', fontsize=12)
        axes[1].set_xlabel('')
        axes[1].tick_params(axis='x', rotation=45)
        
        # Add statistical significance
        stats_clusters = self.perform_statistical_analysis('num_disconnected_clusters', adhesion_type)
        self._add_significance_bars(axes[1], stats_clusters, plot_data, 'num_disconnected_clusters', order)
        
        plt.tight_layout()
        plt.suptitle(f'{adhesion_type.title()} Adhesion Analysis', fontsize=16, fontweight='bold', y=1.02)
        
        return fig, axes
    
    def _add_significance_bars(self, ax, stats_results, data, metric, order):
        """Add significance bars to violin plot"""
        tukey_results = stats_results['tukey_results']
        
        # Get y-axis limits and calculate bar positions
        y_max = ax.get_ylim()[1]
        y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
        
        # Add significance bars
        significant_pairs = []
        for i, row in enumerate(tukey_results.summary().data[1:]):
            group1, group2, meandiff, p_adj, lower, upper, reject = row
            if reject:  # Significant difference
                significant_pairs.append((group1, group2, p_adj))
        
        # Draw significance bars
        bar_height = 0.05 * y_range
        for i, (group1, group2, p_val) in enumerate(significant_pairs):
            try:
                x1 = order.index(group1)
                x2 = order.index(group2)
                
                y = y_max + (i + 1) * bar_height
                ax.plot([x1, x2], [y, y], 'k-', linewidth=1)
                ax.plot([x1, x1], [y, y - bar_height/3], 'k-', linewidth=1)
                ax.plot([x2, x2], [y, y - bar_height/3], 'k-', linewidth=1)
                
                # Add significance stars
                if p_val < 0.001:
                    sig_text = '***'
                elif p_val < 0.01:
                    sig_text = '**'
                elif p_val < 0.05:
                    sig_text = '*'
                else:
                    sig_text = 'ns'
                
                ax.text((x1 + x2) / 2, y + bar_height/4, sig_text, 
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
            except ValueError:
                continue
        
        # Adjust y-axis limits
        ax.set_ylim(ax.get_ylim()[0], y_max + (len(significant_pairs) + 1) * bar_height)

def main():
    """Main function to run the analysis"""
    # Initialize analyzer
    analyzer = CC3DViolin()
    
    # Load data (replace with your actual data loading)
    analyzer.load_simulation_data()
    
    # Create violin plots for cell-cell adhesion
    fig1, axes1 = analyzer.create_violin_plot('cell-cell')
    plt.savefig('cell_cell_adhesion_violin.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create violin plots for cell-ECM adhesion
    fig2, axes2 = analyzer.create_violin_plot('cell-ECM')
    plt.savefig('cell_ecm_adhesion_violin.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print statistical results
    print("\n=== STATISTICAL ANALYSIS RESULTS ===")
    
    for adhesion_type in ['cell-cell', 'cell-ECM']:
        print(f"\n{adhesion_type.upper()} ADHESION:")
        
        for metric in ['area_largest_cluster', 'num_disconnected_clusters']:
            stats = analyzer.perform_statistical_analysis(metric, adhesion_type)
            print(f"\n{metric.replace('_', ' ').title()}:")
            print(f"F-statistic: {stats['f_stat']:.4f}")
            print(f"p-value: {stats['p_value']:.4f}")
            print("Tukey post-hoc results:")
            print(stats['tukey_results'])

if __name__ == "__main__":
    main()
