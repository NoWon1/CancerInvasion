import numpy as np
import pandas as pd
from pathlib import Path
import re

class CC3DDataProcessor:
    """
    Process CC3D simulation output files to extract metrics
    for violin plot analysis
    """
    
    def __init__(self, simulation_dir):
        self.simulation_dir = Path(simulation_dir)
        self.processed_data = []
    
    def extract_cluster_metrics(self, screenshot_dir):
        """
        Extract cluster metrics from CC3D simulation screenshots/output
        
        This is a template function - adapt based on your actual CC3D output format
        """
        # This function should be customized based on your CC3D output format
        # Example implementation for processing simulation results
        
        metrics = {
            'area_largest_cluster': 0,
            'num_disconnected_clusters': 0
        }
        
        # Example: Read from CC3D output files
        # You would adapt this based on your actual file structure
        try:
            # Look for output files (adapt path patterns to your setup)
            output_files = list(screenshot_dir.glob('*.txt'))
            
            if output_files:
                # Process the latest output file
                latest_file = max(output_files, key=lambda x: x.stat().st_mtime)
                
                with open(latest_file, 'r') as f:
                    content = f.read()
                    
                    # Extract metrics using regex (adapt to your format)
                    area_match = re.search(r'largest_cluster_area:\s*(\d+)', content)
                    if area_match:
                        metrics['area_largest_cluster'] = int(area_match.group(1))
                    
                    clusters_match = re.search(r'num_clusters:\s*(\d+)', content)
                    if clusters_match:
                        metrics['num_disconnected_clusters'] = int(clusters_match.group(1))
        
        except Exception as e:
            print(f"Error processing {screenshot_dir}: {e}")
        
        return metrics
    
    def process_simulation_batch(self, condition_name, adhesion_type, num_simulations=50):
        """
        Process a batch of simulations for a given condition
        
        Parameters:
        -----------
        condition_name : str
            Name of the experimental condition
        adhesion_type : str
            'cell-cell' or 'cell-ECM'
        num_simulations : int
            Number of simulations to process
        """
        for sim_id in range(num_simulations):
            sim_dir = self.simulation_dir / f"{condition_name}_sim_{sim_id}"
            
            if sim_dir.exists():
                metrics = self.extract_cluster_metrics(sim_dir)
                
                self.processed_data.append({
                    'condition': condition_name,
                    'simulation_id': sim_id,
                    'area_largest_cluster': metrics['area_largest_cluster'],
                    'num_disconnected_clusters': metrics['num_disconnected_clusters'],
                    'adhesion_type': adhesion_type
                })
            else:
                print(f"Warning: Simulation directory {sim_dir} not found")
    
    def save_processed_data(self, output_file):
        """Save processed data to CSV file"""
        df = pd.DataFrame(self.processed_data)
        df.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
        return df

# Example usage
def process_all_simulations():
    """
    Process all CC3D simulation results
    """
    # Initialize processor
    processor = CC3DDataProcessor("/path/to/your/cc3d/simulations")
    
    # Process cell-cell adhesion conditions
    conditions_cell_cell = [
        "Cell-cell adhesion halved",
        "Model cell-cell adhesion", 
        "Cell-cell adhesion doubled"
    ]
    
    for condition in conditions_cell_cell:
        processor.process_simulation_batch(condition, "cell-cell")
    
    # Process cell-ECM adhesion conditions
    conditions_cell_ecm = [
        "Cell-ECM adhesion halved",
        "Model cell-ECM adhesion",
        "Cell-ECM adhesion doubled"
    ]
    
    for condition in conditions_cell_ecm:
        processor.process_simulation_batch(condition, "cell-ECM")
    
    # Save processed data
    df = processor.save_processed_data("cc3d_simulation_results.csv")
    
    return df
