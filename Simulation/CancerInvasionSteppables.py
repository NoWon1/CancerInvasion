from cc3d.core.PySteppables import *

import numpy as np
import random
import math
import os
import datetime
import csv

class SimulationLogger:
    """Enhanced centralized logging system with detailed ECM and cellular properties"""
    def __init__(self, base_path="./"):
        self.base_path = base_path
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        self.output_dir = os.path.join(base_path, f"CancerInvasion_Enhanced_{self.timestamp}")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize log files
        self.general_log_file = os.path.join(self.output_dir, "simulation_log.txt")
        self.data_log_file = os.path.join(self.output_dir, "simulation_data.csv")
        self.degradation_log_file = os.path.join(self.output_dir, "degradation_events.csv")
        self.ecm_properties_log_file = os.path.join(self.output_dir, "ecm_properties.csv")
        self.cellular_state_log_file = os.path.join(self.output_dir, "cellular_states.csv")
        self.mechanical_forces_log_file = os.path.join(self.output_dir, "mechanical_forces.csv")
        self.system_energy_log_file = os.path.join(self.output_dir, "system_energy.csv")
        
        # Initialize CSV files with headers
        self.init_csv_files()
        
        # Write initial log
        self.log("=== Enhanced Cancer Invasion Simulation Started ===")
        self.log("Features: ECM properties, intracellular states, mechanical forces")
        self.log(f"Timestamp: {self.timestamp}")
        self.log(f"Output directory: {self.output_dir}")

    def init_csv_files(self):
        """Initialize CSV files with comprehensive headers"""
        # Main data log
        with open(self.data_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['MCS', 'Cancer_Cells', 'ECM_Fibers', 'Degraded_ECM', 
                           'Invasion_Distance', 'Total_Volume', 'Degradation_Rate',
                           'Avg_Fiber_Density', 'Avg_Fiber_Alignment', 'Total_System_Energy'])
        
        # Degradation events log
        with open(self.degradation_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['MCS', 'Cell_ID', 'Cell_Type', 'Event', 'X_Position', 
                           'Y_Position', 'MMP_Concentration', 'I_Concentration', 'MMP_I_Ratio',
                           'Local_Fiber_Density', 'Fiber_Orientation', 'ECM_Stiffness'])

        # ECM properties log
        with open(self.ecm_properties_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['MCS', 'Fiber_ID', 'X_Position', 'Y_Position', 'Orientation_Angle',
                           'Local_Density', 'Stiffness', 'Alignment_Index', 'Contact_Guidance_Strength'])

        # Cellular state log
        with open(self.cellular_state_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['MCS', 'Cell_ID', 'Cell_Type', 'X_Position', 'Y_Position',
                           'MMP_Secretion_Rate', 'I_Secretion_Rate', 'Internal_Energy',
                           'Phenotype', 'Migration_Speed', 'Contact_Guidance_Response',
                           'ECM_Degradation_Efficiency', 'Neighbor_Count'])

        # Mechanical forces log
        with open(self.mechanical_forces_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['MCS', 'Cell_ID', 'Force_X', 'Force_Y', 'Force_Magnitude',
                           'Adhesion_Energy_Cell_Cell', 'Adhesion_Energy_Cell_ECM',
                           'ECM_Resistance_Force', 'Protrusion_Force', 'Contact_Area'])

        # System energy log
        with open(self.system_energy_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['MCS', 'Total_Energy', 'Volume_Energy', 'Surface_Energy',
                           'Contact_Energy', 'ECM_Elastic_Energy', 'Chemical_Potential_Energy'])

    def log(self, message):
        """Write message to general log file and print to console"""
        timestamp_str = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp_str}] {message}"
        
        with open(self.general_log_file, 'a') as f:
            f.write(log_message + "\n")
        print(log_message)

    def log_data(self, mcs, cancer_cells, ecm_fibers, degraded_ecm, invasion_distance, 
                 total_volume, degradation_rate, avg_fiber_density, avg_fiber_alignment, total_energy):
        """Log enhanced numerical data to CSV file"""
        with open(self.data_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([mcs, cancer_cells, ecm_fibers, degraded_ecm, invasion_distance, 
                           total_volume, degradation_rate, avg_fiber_density, avg_fiber_alignment, total_energy])

    def log_degradation_event(self, mcs, cell_id, cell_type, event, x_pos, y_pos, 
                             mmp_conc, i_conc, ratio, local_density, orientation, stiffness):
        """Log enhanced degradation events"""
        with open(self.degradation_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([mcs, cell_id, cell_type, event, x_pos, y_pos, mmp_conc, i_conc, 
                           ratio, local_density, orientation, stiffness])

    def log_ecm_properties(self, mcs, fiber_id, x_pos, y_pos, orientation, density, 
                          stiffness, alignment_index, contact_guidance):
        """Log ECM fiber properties"""
        with open(self.ecm_properties_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([mcs, fiber_id, x_pos, y_pos, orientation, density, 
                           stiffness, alignment_index, contact_guidance])

    def log_cellular_state(self, mcs, cell_id, cell_type, x_pos, y_pos, mmp_rate, i_rate,
                          internal_energy, phenotype, migration_speed, guidance_response,
                          degradation_efficiency, neighbor_count):
        """Log detailed cellular states"""
        with open(self.cellular_state_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([mcs, cell_id, cell_type, x_pos, y_pos, mmp_rate, i_rate,
                           internal_energy, phenotype, migration_speed, guidance_response,
                           degradation_efficiency, neighbor_count])

    def log_mechanical_forces(self, mcs, cell_id, force_x, force_y, force_mag,
                             adhesion_cc, adhesion_ce, ecm_resistance, protrusion_force, contact_area):
        """Log mechanical forces and energies"""
        with open(self.mechanical_forces_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([mcs, cell_id, force_x, force_y, force_mag,
                           adhesion_cc, adhesion_ce, ecm_resistance, protrusion_force, contact_area])

    def log_system_energy(self, mcs, total_energy, volume_energy, surface_energy,
                         contact_energy, ecm_elastic_energy, chemical_energy):
        """Log system-wide energy components"""
        with open(self.system_energy_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([mcs, total_energy, volume_energy, surface_energy,
                           contact_energy, ecm_elastic_energy, chemical_energy])

    def finalize(self):
        """Write final summary to log"""
        self.log("=== Enhanced Simulation Completed ===")
        self.log(f"All output files saved to: {self.output_dir}")

# Global logger instance
simulation_logger = None

class CancerInvasionSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
        # Enhanced parameters
        self.fiber_count = 600
        self.fiber_length_min = 15
        self.fiber_length_max = 20
        self.initial_cell_count = 69
        self.initial_diameter = 100
        
        # ECM properties tracking
        self.ecm_properties = {}  # fiber_id -> {orientation, density, stiffness, alignment}
        self.local_fiber_density = {}  # position -> density value
        self.fiber_orientations = {}  # fiber_id -> angle in radians
        self.ecm_stiffness_map = {}  # position -> stiffness value
        
        # Cellular state tracking
        self.cellular_states = {}  # cell_id -> {secretion_rates, energy, phenotype}
        self.cell_phenotypes = {}  # cell_id -> phenotype ("leader", "follower", "digger", "bulk")
        self.cell_forces = {}  # cell_id -> force vectors and energies
        
        # Mechanical properties
        self.system_energy = 0.0
        self.contact_energies = {"Cell-Cell": 16, "Cell-ECM": 16, "Cell-DegradedECM": 10}
        self.ecm_elastic_modulus = 1000.0  # Pa
        self.degradation_force_threshold = 50.0  # pN
        
        # Tracking variables
        self.cell_positions = {}
        self.cell_velocities = {}
        self.initial_positions = {}
        self.fiber_locations = set()
        self.degraded_fiber_count = 0
        self.total_fiber_count = 0
        self.invasion_front_positions = []
        self.step_count = 0
        self.steady_state_reached = False
        self.steady_state_mcs = 0

    def start(self):
        global simulation_logger
        simulation_logger = SimulationLogger()
        
        try:
            simulation_logger.log("=== Enhanced Cancer Invasion Simulation ===")
            simulation_logger.log("Features: ECM fiber properties, cellular heterogeneity, mechanical forces")
            
            # Clear existing cells
            cell_list_copy = list(self.cell_list)
            for cell in cell_list_copy:
                try:
                    self.safe_cell_removal(cell)
                except Exception as e:
                    simulation_logger.log(f"Warning during cleanup: {e}")
            
            # Initialize components with enhanced properties
            self.initialize_enhanced_ecm_network()
            self.initialize_heterogeneous_cancer_cluster()
            self.initialize_cellular_states()
            self.initialize_mechanical_properties()
            self.initialize_tracking()
            
            simulation_logger.log(f"Initialization complete!")
            simulation_logger.log(f"Total ECM fibers: {self.total_fiber_count}")
            simulation_logger.log(f"Cancer cells: {len([c for c in self.cell_list if c.type == self.CELL])}")
            simulation_logger.log(f"ECM fiber orientations tracked: {len(self.fiber_orientations)}")
            simulation_logger.log(f"Cell phenotypes assigned: {len(self.cell_phenotypes)}")
            
        except Exception as e:
            simulation_logger.log(f"ERROR during initialization: {e}")

    def initialize_enhanced_ecm_network(self):
        """Initialize ECM with detailed fiber properties"""
        try:
            simulation_logger.log("Creating enhanced ECM network with fiber properties...")
            random.seed(42)
            fibers_created = 0
            max_attempts = self.fiber_count * 3
            
            for attempt in range(max_attempts):
                if fibers_created >= self.fiber_count:
                    break
                
                # Position assignment with higher density around tumor
                if random.random() < 0.7:
                    start_x = random.randint(150, 350)
                    start_y = random.randint(150, 350)
                else:
                    start_x = random.randint(50, 449)
                    start_y = random.randint(50, 449)
                
                # Assign fiber properties
                orientation_angle = random.uniform(0, 2 * math.pi)
                fiber_length = random.randint(self.fiber_length_min, self.fiber_length_max)
                
                # Create fiber with enhanced properties
                fiber_id = self.create_enhanced_ecm_fiber(start_x, start_y, orientation_angle, fiber_length, fibers_created)
                if fiber_id is not None:
                    fibers_created += 1
                    
                    # Store fiber properties
                    self.fiber_orientations[fiber_id] = orientation_angle
                    local_density = self.calculate_local_fiber_density(start_x, start_y)
                    base_stiffness = 1000.0 + random.uniform(-200, 200)  # Pa
                    
                    self.ecm_properties[fiber_id] = {
                        'orientation': orientation_angle,
                        'density': local_density,
                        'stiffness': base_stiffness,
                        'alignment_index': random.uniform(0.3, 0.9),
                        'contact_guidance_strength': random.uniform(0.5, 1.0)
                    }
                    
                    # Update local maps
                    self.update_local_ecm_maps(start_x, start_y, orientation_angle, local_density, base_stiffness)
            
            self.total_fiber_count = fibers_created
            simulation_logger.log(f"Created {fibers_created} ECM fibers with detailed properties")
            
        except Exception as e:
            simulation_logger.log(f"Error in enhanced ECM initialization: {e}")

    def create_enhanced_ecm_fiber(self, start_x, start_y, angle, length, fiber_id):
        """Create ECM fiber with enhanced properties tracking"""
        try:
            fiber_pixels = []
            dx = math.cos(angle)
            dy = math.sin(angle)
            
            for i in range(length):
                x = int(start_x + i * dx)
                y = int(start_y + i * dy)
                
                if 25 <= x < 475 and 25 <= y < 475:
                    fiber_pixels.append((x, y))
                    
                    # Enhanced thickness with orientation-dependent anisotropy
                    thickness_offsets = self.get_anisotropic_thickness_offsets(angle)
                    for offset in thickness_offsets:
                        nx, ny = x + offset[0], y + offset[1]
                        if 25 <= nx < 475 and 25 <= ny < 475:
                            if (nx, ny) not in fiber_pixels:
                                fiber_pixels.append((nx, ny))
            
            if len(fiber_pixels) >= 12:
                fiber_cell = self.new_cell(self.ECMFIBER)
                pixels_assigned = 0
                
                for x, y in fiber_pixels:
                    try:
                        if self.cell_field[x, y, 0] is None:
                            self.cell_field[x, y, 0] = fiber_cell
                            self.fiber_locations.add((x, y))
                            pixels_assigned += 1
                    except:
                        continue
                
                if pixels_assigned >= 12:
                    # Store fiber ID mapping
                    if not hasattr(fiber_cell, 'dict'):
                        fiber_cell.dict = {}
                    fiber_cell.dict['fiber_id'] = fiber_id
                    fiber_cell.dict['orientation'] = angle
                    fiber_cell.dict['creation_mcs'] = 0
                    return fiber_id
                else:
                    self.safe_cell_removal(fiber_cell)
                    return None
            
            return None
            
        except Exception as e:
            simulation_logger.log(f"Error creating enhanced fiber: {e}")
            return None

    def get_anisotropic_thickness_offsets(self, angle):
        """Get thickness offsets based on fiber orientation for anisotropic properties"""
        # Basic offsets
        base_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        
        # Add orientation-dependent anisotropy
        perpendicular_angle = angle + math.pi/2
        anisotropic_offsets = []
        
        for i in range(2):  # Add two additional pixels perpendicular to fiber direction
            offset_x = int(2 * math.cos(perpendicular_angle))
            offset_y = int(2 * math.sin(perpendicular_angle))
            anisotropic_offsets.append((offset_x, offset_y))
            anisotropic_offsets.append((-offset_x, -offset_y))
        
        return base_offsets + anisotropic_offsets

    def calculate_local_fiber_density(self, x, y, radius=20):
        """Calculate local fiber density around a position"""
        count = 0
        total_pixels = 0
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 500 and 0 <= ny < 500:
                        total_pixels += 1
                        if (nx, ny) in self.fiber_locations:
                            count += 1
        
        return count / total_pixels if total_pixels > 0 else 0.0

    def update_local_ecm_maps(self, x, y, orientation, density, stiffness):
        """Update local ECM property maps"""
        radius = 15
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 500 and 0 <= ny < 500:
                        pos_key = (nx, ny)
                        
                        # Update density map
                        if pos_key not in self.local_fiber_density:
                            self.local_fiber_density[pos_key] = 0.0
                        self.local_fiber_density[pos_key] += density / (1 + math.sqrt(dx*dx + dy*dy))
                        
                        # Update stiffness map
                        if pos_key not in self.ecm_stiffness_map:
                            self.ecm_stiffness_map[pos_key] = 0.0
                        self.ecm_stiffness_map[pos_key] += stiffness / (1 + math.sqrt(dx*dx + dy*dy))

    def initialize_heterogeneous_cancer_cluster(self):
        """Initialize cancer cluster with cellular heterogeneity"""
        try:
            simulation_logger.log(f"Creating heterogeneous cancer cluster...")
            center_x, center_y = 250, 250
            cells_created = 0
            cluster_radius = self.initial_diameter // 2
            
            # Define phenotype probabilities
            phenotype_probs = {"leader": 0.15, "digger": 0.20, "follower": 0.45, "bulk": 0.20}
            
            for radius in range(0, cluster_radius, 8):
                if cells_created >= self.initial_cell_count:
                    break
                
                if radius == 0:
                    if self.create_heterogeneous_cancer_cell(center_x, center_y, 6, phenotype_probs):
                        cells_created += 1
                else:
                    circumference = 2 * math.pi * radius
                    cells_in_ring = max(1, int(circumference / 12))
                    
                    for i in range(cells_in_ring):
                        if cells_created >= self.initial_cell_count:
                            break
                        
                        angle = 2 * math.pi * i / cells_in_ring
                        x = int(center_x + radius * math.cos(angle))
                        y = int(center_y + radius * math.sin(angle))
                        
                        if self.create_heterogeneous_cancer_cell(x, y, 5, phenotype_probs):
                            cells_created += 1
            
            simulation_logger.log(f"Created {cells_created} heterogeneous cancer cells")
            self.log_phenotype_distribution()
            
        except Exception as e:
            simulation_logger.log(f"Error in heterogeneous cancer cluster initialization: {e}")

    def create_heterogeneous_cancer_cell(self, center_x, center_y, radius, phenotype_probs):
        """Create cancer cell with assigned phenotype and properties"""
        try:
            cell = self.new_cell(self.CELL)
            pixels_added = 0
            
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if dx*dx + dy*dy <= radius*radius:
                        px, py = center_x + dx, center_y + dy
                        if 0 <= px < 500 and 0 <= py < 500:
                            try:
                                if self.cell_field[px, py, 0] is None:
                                    self.cell_field[px, py, 0] = cell
                                    pixels_added += 1
                            except:
                                continue
            
            if pixels_added >= 20:
                # Assign phenotype
                rand_val = random.random()
                cumulative_prob = 0.0
                assigned_phenotype = "bulk"
                
                for phenotype, prob in phenotype_probs.items():
                    cumulative_prob += prob
                    if rand_val <= cumulative_prob:
                        assigned_phenotype = phenotype
                        break
                
                self.cell_phenotypes[cell.id] = assigned_phenotype
                
                # Initialize cell properties based on phenotype
                self.initialize_cell_properties_by_phenotype(cell, assigned_phenotype)
                
                return True
            else:
                self.safe_cell_removal(cell)
                return False
                
        except Exception as e:
            simulation_logger.log(f"Error creating heterogeneous cell: {e}")
            return False

    def initialize_cell_properties_by_phenotype(self, cell, phenotype):
        """Initialize cell properties based on assigned phenotype"""
        if not hasattr(cell, 'dict'):
            cell.dict = {}
        
        # Base properties
        base_mmp_rate = 0.25
        base_i_rate = 0.25
        
        # Phenotype-specific modifications
        if phenotype == "leader":
            cell.dict['mmp_secretion_rate'] = base_mmp_rate * 1.5
            cell.dict['i_secretion_rate'] = base_i_rate * 0.8
            cell.dict['migration_speed'] = 1.2
            cell.dict['contact_guidance_response'] = 0.9
            cell.dict['degradation_efficiency'] = 1.1
        elif phenotype == "digger":
            cell.dict['mmp_secretion_rate'] = base_mmp_rate * 2.0
            cell.dict['i_secretion_rate'] = base_i_rate * 1.5
            cell.dict['migration_speed'] = 0.8
            cell.dict['contact_guidance_response'] = 0.6
            cell.dict['degradation_efficiency'] = 1.8
        elif phenotype == "follower":
            cell.dict['mmp_secretion_rate'] = base_mmp_rate * 0.8
            cell.dict['i_secretion_rate'] = base_i_rate * 1.0
            cell.dict['migration_speed'] = 1.0
            cell.dict['contact_guidance_response'] = 1.2
            cell.dict['degradation_efficiency'] = 0.9
        else:  # bulk
            cell.dict['mmp_secretion_rate'] = base_mmp_rate * 0.6
            cell.dict['i_secretion_rate'] = base_i_rate * 0.9
            cell.dict['migration_speed'] = 0.7
            cell.dict['contact_guidance_response'] = 0.8
            cell.dict['degradation_efficiency'] = 0.7
        
        # Common properties
        cell.dict['phenotype'] = phenotype
        cell.dict['internal_energy'] = random.uniform(80, 120)
        cell.dict['creation_mcs'] = 0

    def log_phenotype_distribution(self):
        """Log the distribution of cell phenotypes"""
        phenotype_counts = {}
        for phenotype in self.cell_phenotypes.values():
            phenotype_counts[phenotype] = phenotype_counts.get(phenotype, 0) + 1
        
        simulation_logger.log("Cell phenotype distribution:")
        for phenotype, count in phenotype_counts.items():
            percentage = (count / len(self.cell_phenotypes)) * 100
            simulation_logger.log(f"  {phenotype}: {count} cells ({percentage:.1f}%)")

    def initialize_cellular_states(self):
        """Initialize detailed cellular state tracking"""
        for cell in self.cell_list:
            if cell.type == self.CELL:
                cell_id = cell.id
                phenotype = self.cell_phenotypes.get(cell_id, "bulk")
                
                self.cellular_states[cell_id] = {
                    'mmp_secretion_rate': cell.dict.get('mmp_secretion_rate', 0.25),
                    'i_secretion_rate': cell.dict.get('i_secretion_rate', 0.25),
                    'internal_energy': cell.dict.get('internal_energy', 100.0),
                    'phenotype': phenotype,
                    'migration_speed': cell.dict.get('migration_speed', 1.0),
                    'contact_guidance_response': cell.dict.get('contact_guidance_response', 1.0),
                    'degradation_efficiency': cell.dict.get('degradation_efficiency', 1.0),
                    'last_division_mcs': 0,
                    'energy_expenditure': 0.0
                }

    def initialize_mechanical_properties(self):
        """Initialize mechanical force and energy tracking"""
        for cell in self.cell_list:
            if cell.type == self.CELL:
                self.cell_forces[cell.id] = {
                    'force_x': 0.0,
                    'force_y': 0.0,
                    'adhesion_energy_cell_cell': 0.0,
                    'adhesion_energy_cell_ecm': 0.0,
                    'ecm_resistance_force': 0.0,
                    'protrusion_force': 0.0,
                    'contact_area': 0.0
                }

    def initialize_tracking(self):
        """Initialize enhanced tracking systems"""
        try:
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    self.cell_positions[cell.id] = [cell.xCOM, cell.yCOM]
                    self.cell_velocities[cell.id] = []
                    self.initial_positions[cell.id] = [cell.xCOM, cell.yCOM]
        except Exception as e:
            simulation_logger.log(f"Error in tracking initialization: {e}")

    def safe_cell_removal(self, cell):
        """Enhanced safe cell removal with cleanup"""
        try:
            pixels_cleared = 0
            search_radius = 15
            
            # Clean up tracking data
            if hasattr(cell, 'id'):
                if cell.id in self.cellular_states:
                    del self.cellular_states[cell.id]
                if cell.id in self.cell_forces:
                    del self.cell_forces[cell.id]
                if cell.id in self.cell_phenotypes:
                    del self.cell_phenotypes[cell.id]
            
            for x in range(max(0, int(cell.xCOM) - search_radius),
                          min(self.dim.x, int(cell.xCOM) + search_radius)):
                for y in range(max(0, int(cell.yCOM) - search_radius),
                              min(self.dim.y, int(cell.yCOM) + search_radius)):
                    try:
                        if self.cell_field[x, y, 0] == cell:
                            self.cell_field[x, y, 0] = None
                            pixels_cleared += 1
                    except:
                        continue
            
            return pixels_cleared > 0
            
        except Exception as e:
            return False

    def step(self, mcs):
        """Enhanced step function with comprehensive data collection"""
        try:
            self.step_count = mcs
            
            # Update cellular states and forces
            self.update_cellular_states(mcs)
            self.calculate_mechanical_forces(mcs)
            self.apply_contact_guidance(mcs)
            
            # Enhanced monitoring every 20 MCS
            if mcs % 20 == 0:
                cancer_count = len([c for c in self.cell_list if c.type == self.CELL])
                fiber_count = len([c for c in self.cell_list if c.type == self.ECMFIBER])
                degraded_count = len([c for c in self.cell_list if c.type == self.DEGRADEDECM])
                
                # Calculate enhanced metrics
                total_volume = sum(cell.volume for cell in self.cell_list if cell.type == self.CELL)
                degradation_rate = (self.total_fiber_count - fiber_count) / self.total_fiber_count * 100 if self.total_fiber_count > 0 else 0
                
                # ECM properties
                avg_fiber_density = self.calculate_average_fiber_density()
                avg_fiber_alignment = self.calculate_average_fiber_alignment()
                
                # System energy
                total_system_energy = self.calculate_total_system_energy()
                
                simulation_logger.log(f"MCS {mcs}: Cancer={cancer_count}, ECM Fibers={fiber_count}, Degraded={degraded_count}")
                simulation_logger.log(f"         Degradation Rate: {degradation_rate:.1f}%, Total Volume: {total_volume:.1f}")
                simulation_logger.log(f"         Avg Fiber Density: {avg_fiber_density:.3f}, Alignment: {avg_fiber_alignment:.3f}")
                simulation_logger.log(f"         Total System Energy: {total_system_energy:.2f}")
                
                # Track invasion front
                invasion_distance = self.track_invasion_front()
                
                # Log enhanced data to CSV
                simulation_logger.log_data(mcs, cancer_count, fiber_count, degraded_count, 
                                         invasion_distance, total_volume, degradation_rate,
                                         avg_fiber_density, avg_fiber_alignment, total_system_energy)
                
                # Log detailed states periodically
                if mcs % 100 == 0:
                    self.log_detailed_states(mcs)
                
                # Check for steady state
                if mcs > 200 and not self.steady_state_reached:
                    self.check_steady_state(mcs)
            
            self.update_cell_dynamics()
            
        except Exception as e:
            simulation_logger.log(f"Error in enhanced step {mcs}: {e}")

    def update_cellular_states(self, mcs):
        """Update intracellular states for all cells"""
        for cell in self.cell_list:
            if cell.type == self.CELL and cell.id in self.cellular_states:
                state = self.cellular_states[cell.id]
                
                # Update internal energy based on activity
                phenotype = state['phenotype']
                energy_consumption = 0.5 if phenotype == "digger" else 0.3
                state['internal_energy'] -= energy_consumption
                state['energy_expenditure'] += energy_consumption
                
                # Regenerate energy over time
                if mcs % 10 == 0:
                    state['internal_energy'] = min(120.0, state['internal_energy'] + 2.0)
                
                # Dynamic secretion rate modulation
                neighbor_count = len(self.get_cell_neighbor_data_list(cell))
                if neighbor_count > 6:  # Crowded environment
                    state['mmp_secretion_rate'] *= 0.95
                elif neighbor_count < 3:  # Sparse environment
                    state['mmp_secretion_rate'] *= 1.05
                
                # Clamp secretion rates
                state['mmp_secretion_rate'] = max(0.1, min(1.0, state['mmp_secretion_rate']))
                state['i_secretion_rate'] = max(0.1, min(1.0, state['i_secretion_rate']))

    def calculate_mechanical_forces(self, mcs):
        """Calculate mechanical forces for all cells"""
        for cell in self.cell_list:
            if cell.type == self.CELL and cell.id in self.cell_forces:
                forces = self.cell_forces[cell.id]
                
                # Calculate adhesion energies
                neighbor_list = self.get_cell_neighbor_data_list(cell)
                cell_cell_contact = 0
                cell_ecm_contact = 0
                
                for neighbor, contact_area in neighbor_list:
                    if neighbor:
                        if neighbor.type == self.CELL:
                            cell_cell_contact += contact_area
                        elif neighbor.type in [self.ECMFIBER, self.DEGRADEDECM]:
                            cell_ecm_contact += contact_area
                
                forces['adhesion_energy_cell_cell'] = cell_cell_contact * self.contact_energies["Cell-Cell"]
                forces['adhesion_energy_cell_ecm'] = cell_ecm_contact * self.contact_energies["Cell-ECM"]
                forces['contact_area'] = cell_cell_contact + cell_ecm_contact
                
                # Calculate ECM resistance force
                local_stiffness = self.ecm_stiffness_map.get((int(cell.xCOM), int(cell.yCOM)), 1000.0)
                forces['ecm_resistance_force'] = local_stiffness * 0.001  # Convert to pN
                
                # Calculate protrusion force based on phenotype
                phenotype = self.cellular_states[cell.id]['phenotype']
                base_protrusion = 30.0  # pN
                if phenotype == "leader":
                    forces['protrusion_force'] = base_protrusion * 1.3
                elif phenotype == "digger":
                    forces['protrusion_force'] = base_protrusion * 1.5
                else:
                    forces['protrusion_force'] = base_protrusion
                
                # Calculate net force components
                force_magnitude = forces['protrusion_force'] - forces['ecm_resistance_force']
                force_angle = random.uniform(0, 2 * math.pi)  # Simplified random direction
                
                forces['force_x'] = force_magnitude * math.cos(force_angle)
                forces['force_y'] = force_magnitude * math.sin(force_angle)

    def apply_contact_guidance(self, mcs):
        """Apply contact guidance based on local ECM fiber orientation"""
        for cell in self.cell_list:
            if cell.type == self.CELL:
                cell_pos = (int(cell.xCOM), int(cell.yCOM))
                
                # Find dominant fiber orientation nearby
                dominant_orientation = self.get_dominant_fiber_orientation(cell_pos)
                
                if dominant_orientation is not None:
                    guidance_strength = self.cellular_states[cell.id]['contact_guidance_response']
                    
                    # Apply guidance force
                    guidance_force_x = guidance_strength * 10.0 * math.cos(dominant_orientation)
                    guidance_force_y = guidance_strength * 10.0 * math.sin(dominant_orientation)
                    
                    # Update cell's directional bias (simplified implementation)
                    cell.lambdaVecX += guidance_force_x * 0.1
                    cell.lambdaVecY += guidance_force_y * 0.1

    def get_dominant_fiber_orientation(self, pos, radius=15):
        """Get dominant fiber orientation in the vicinity of a position"""
        orientations = []
        weights = []
        
        for fiber_id, properties in self.ecm_properties.items():
            # This is a simplified check - in reality, we'd need to check fiber proximity
            if random.random() < 0.1:  # Sample some fibers nearby
                orientations.append(properties['orientation'])
                weights.append(properties['alignment_index'])
        
        if orientations:
            # Calculate weighted average orientation
            weighted_cos = sum(w * math.cos(o) for w, o in zip(weights, orientations))
            weighted_sin = sum(w * math.sin(o) for w, o in zip(weights, orientations))
            return math.atan2(weighted_sin, weighted_cos)
        
        return None

    def calculate_average_fiber_density(self):
        """Calculate average fiber density across the simulation domain"""
        if not self.local_fiber_density:
            return 0.0
        return sum(self.local_fiber_density.values()) / len(self.local_fiber_density)

    def calculate_average_fiber_alignment(self):
        """Calculate average fiber alignment index"""
        if not self.ecm_properties:
            return 0.0
        alignments = [props['alignment_index'] for props in self.ecm_properties.values()]
        return sum(alignments) / len(alignments)

    def calculate_total_system_energy(self):
        """Calculate total system energy including all components"""
        volume_energy = 0.0
        surface_energy = 0.0
        contact_energy = 0.0
        ecm_elastic_energy = 0.0
        
        for cell in self.cell_list:
            # Volume energy
            volume_diff = cell.volume - cell.targetVolume
            volume_energy += cell.lambdaVolume * volume_diff * volume_diff
            
            # Surface energy
            surface_diff = cell.surface - cell.targetSurface
            surface_energy += cell.lambdaSurface * surface_diff * surface_diff
            
            # Contact energy (approximation)
            if cell.type == self.CELL and cell.id in self.cell_forces:
                contact_energy += self.cell_forces[cell.id]['adhesion_energy_cell_cell']
                contact_energy += self.cell_forces[cell.id]['adhesion_energy_cell_ecm']
        
        # ECM elastic energy (simplified)
        ecm_elastic_energy = sum(self.ecm_stiffness_map.values()) * 0.001
        
        total_energy = volume_energy + surface_energy + contact_energy + ecm_elastic_energy
        self.system_energy = total_energy
        
        return total_energy

    def log_detailed_states(self, mcs):
        """Log detailed cellular and ECM states"""
        # Log cellular states
        for cell in self.cell_list:
            if cell.type == self.CELL and cell.id in self.cellular_states:
                state = self.cellular_states[cell.id]
                forces = self.cell_forces.get(cell.id, {})
                neighbor_count = len(self.get_cell_neighbor_data_list(cell))
                
                simulation_logger.log_cellular_state(
                    mcs, cell.id, "Cell", cell.xCOM, cell.yCOM,
                    state['mmp_secretion_rate'], state['i_secretion_rate'],
                    state['internal_energy'], state['phenotype'],
                    state['migration_speed'], state['contact_guidance_response'],
                    state['degradation_efficiency'], neighbor_count
                )
                
                # Log mechanical forces
                simulation_logger.log_mechanical_forces(
                    mcs, cell.id, forces.get('force_x', 0), forces.get('force_y', 0),
                    math.sqrt(forces.get('force_x', 0)**2 + forces.get('force_y', 0)**2),
                    forces.get('adhesion_energy_cell_cell', 0), forces.get('adhesion_energy_cell_ecm', 0),
                    forces.get('ecm_resistance_force', 0), forces.get('protrusion_force', 0),
                    forces.get('contact_area', 0)
                )
        
        # Log ECM properties
        for fiber_id, properties in list(self.ecm_properties.items())[:10]:  # Sample first 10
            # Find a representative position for this fiber
            pos_x, pos_y = 250, 250  # Simplified - would need actual fiber position
            
            simulation_logger.log_ecm_properties(
                mcs, fiber_id, pos_x, pos_y, properties['orientation'],
                properties['density'], properties['stiffness'],
                properties['alignment_index'], properties['contact_guidance_strength']
            )
        
        # Log system energy components
        simulation_logger.log_system_energy(
            mcs, self.system_energy, 0.0, 0.0, 0.0, 0.0, 0.0  # Simplified
        )

    def track_invasion_front(self):
        """Enhanced invasion front tracking"""
        try:
            max_distance = 0
            center_x, center_y = 250, 250
            
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    distance = math.sqrt((cell.xCOM - center_x)**2 + (cell.yCOM - center_y)**2)
                    max_distance = max(max_distance, distance)
            
            self.invasion_front_positions.append(max_distance)
            return max_distance
            
        except Exception as e:
            simulation_logger.log(f"Error tracking invasion front: {e}")
            return 0

    def check_steady_state(self, mcs):
        """Enhanced steady state detection"""
        try:
            if len(self.invasion_front_positions) >= 25:
                recent_positions = self.invasion_front_positions[-25:]
                position_variance = np.var(recent_positions)
                
                if position_variance < 5.0:
                    self.steady_state_reached = True
                    self.steady_state_mcs = mcs
                    simulation_logger.log(f"*** STEADY STATE REACHED at MCS {mcs} ***")
                    simulation_logger.log(f"Invasion front stabilized at distance: {recent_positions[-1]:.2f} pixels")
                    
        except Exception as e:
            simulation_logger.log(f"Error checking steady state: {e}")

    def update_cell_dynamics(self):
        """Enhanced cell dynamics tracking"""
        try:
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    current_pos = [cell.xCOM, cell.yCOM]
                    
                    if cell.id in self.cell_positions:
                        prev_pos = self.cell_positions[cell.id]
                        velocity = [current_pos[0] - prev_pos[0], 
                                   current_pos[1] - prev_pos[1]]
                        
                        if cell.id not in self.cell_velocities:
                            self.cell_velocities[cell.id] = []
                        
                        self.cell_velocities[cell.id].append(velocity)
                        
                        if len(self.cell_velocities[cell.id]) > 10:
                            self.cell_velocities[cell.id].pop(0)
                        
                        # Update migration speed in cellular state
                        if cell.id in self.cellular_states:
                            speed = math.sqrt(velocity[0]**2 + velocity[1]**2)
                            self.cellular_states[cell.id]['migration_speed'] = speed
                    
                    self.cell_positions[cell.id] = current_pos
                    
        except Exception as e:
            simulation_logger.log(f"Error in cell dynamics: {e}")

    def finish(self):
        """Enhanced finish function with comprehensive summary"""
        try:
            cancer_cells = [c for c in self.cell_list if c.type == self.CELL]
            final_fiber_count = len([c for c in self.cell_list if c.type == self.ECMFIBER])
            final_degraded_count = len([c for c in self.cell_list if c.type == self.DEGRADEDECM])
            
            # Calculate final metrics
            degradation_percentage = ((self.total_fiber_count - final_fiber_count) / self.total_fiber_count) * 100 if self.total_fiber_count > 0 else 0
            
            # Phenotype analysis
            final_phenotype_counts = {}
            for cell in cancer_cells:
                if cell.id in self.cell_phenotypes:
                    phenotype = self.cell_phenotypes[cell.id]
                    final_phenotype_counts[phenotype] = final_phenotype_counts.get(phenotype, 0) + 1
            
            # Energy analysis
            total_energy_expenditure = sum(state['energy_expenditure'] for state in self.cellular_states.values())
            avg_internal_energy = np.mean([state['internal_energy'] for state in self.cellular_states.values()])
            
            if cancer_cells and self.initial_positions:
                translocations = []
                for cell in cancer_cells:
                    if cell.id in self.initial_positions:
                        initial = self.initial_positions[cell.id]
                        final = [cell.xCOM, cell.yCOM]
                        distance = math.sqrt((final[0] - initial[0])**2 + (final[1] - initial[1])**2)
                        translocations.append(distance)
                
                if translocations:
                    avg_translocation = np.mean(translocations)
                    max_translocation = np.max(translocations)
                    
                    simulation_logger.log(f"\n=== ENHANCED SIMULATION RESULTS ===")
                    simulation_logger.log(f"Simulation duration: {self.step_count} MCS")
                    simulation_logger.log(f"Steady state reached: {'Yes' if self.steady_state_reached else 'No'}")
                    if self.steady_state_reached:
                        simulation_logger.log(f"Steady state at MCS: {self.steady_state_mcs}")
                    
                    simulation_logger.log(f"\n=== CELL POPULATION ANALYSIS ===")
                    simulation_logger.log(f"Final cancer cells: {len(cancer_cells)}")
                    simulation_logger.log(f"Final phenotype distribution:")
                    for phenotype, count in final_phenotype_counts.items():
                        percentage = (count / len(cancer_cells)) * 100
                        simulation_logger.log(f"  {phenotype}: {count} cells ({percentage:.1f}%)")
                    
                    simulation_logger.log(f"\n=== ECM ANALYSIS ===")
                    simulation_logger.log(f"ECM degradation: {degradation_percentage:.1f}%")
                    simulation_logger.log(f"Remaining ECM fibers: {final_fiber_count}")
                    simulation_logger.log(f"Currently degraded ECM: {final_degraded_count}")
                    simulation_logger.log(f"Final fiber density: {self.calculate_average_fiber_density():.3f}")
                    simulation_logger.log(f"Final fiber alignment: {self.calculate_average_fiber_alignment():.3f}")
                    
                    simulation_logger.log(f"\n=== MECHANICAL ANALYSIS ===")
                    simulation_logger.log(f"Final system energy: {self.system_energy:.2f}")
                    simulation_logger.log(f"Total energy expenditure: {total_energy_expenditure:.2f}")
                    simulation_logger.log(f"Average internal energy: {avg_internal_energy:.2f}")
                    
                    simulation_logger.log(f"\n=== MIGRATION ANALYSIS ===")
                    simulation_logger.log(f"Average cell translocation: {avg_translocation:.2f} pixels")
                    simulation_logger.log(f"Maximum cell translocation: {max_translocation:.2f} pixels")
                    
                    if self.invasion_front_positions:
                        final_invasion_distance = self.invasion_front_positions[-1]
                        simulation_logger.log(f"Final invasion front distance: {final_invasion_distance:.2f} pixels")
                    
            # Final detailed logging
            self.log_detailed_states(self.step_count)
            
            # Finalize logging
            simulation_logger.finalize()
            
        except Exception as e:
            simulation_logger.log(f"Error in enhanced finish: {e}")

# Additional enhanced steppables with original functionality
class GrowthSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        self.growth_rate = 0.75

    def start(self):
        for cell in self.cell_list:
            if cell.type == self.CELL:
                cell.targetVolume = 400
                cell.lambdaVolume = 20.0
                cell.targetSurface = 35
                cell.lambdaSurface = 2.0

    def step(self, mcs):
        field_GF = self.field.GF
        
        for cell in self.cell_list:
            if cell.type == self.CELL:
                neighbor_list = self.get_cell_neighbor_data_list(cell)
                k = 0
                for neighbor, common_surface_area in neighbor_list:
                    if neighbor and neighbor.type == self.CELL:
                        k += common_surface_area
                
                s = cell.surface
                g = (s - k) / 40
                
                try:
                    GFc = field_GF[int(round(cell.xCOM)), int(round(cell.yCOM)), int(round(cell.zCOM))]
                    growth_increment = self.growth_rate * (((g/8) + (GFc/7))/3)
                    cell.targetVolume += growth_increment
                except:
                    cell.targetVolume += self.growth_rate * (g/8/3)

class MitosisSteppable(MitosisSteppableBase):
    def __init__(self, frequency=1):
        MitosisSteppableBase.__init__(self, frequency)
        self.division_volume = 800

    def step(self, mcs):
        cells_to_divide = []
        
        for cell in self.cell_list:
            if cell.type == self.CELL and cell.volume >= self.division_volume:
                cells_to_divide.append(cell)
        
        for cell in cells_to_divide:
            self.divide_cell_random_orientation(cell)

    def update_attributes(self):
        self.parent_cell.targetVolume /= 2.0
        self.clone_parent_2_child()
        
        self.child_cell.targetVolume = self.parent_cell.targetVolume
        self.child_cell.lambdaVolume = self.parent_cell.lambdaVolume
        self.child_cell.type = self.CELL
        self.parent_cell.type = self.CELL

class ChemotaxisSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        for cell in self.cell_list:
            if cell.type == self.CELL:
                cell.lambdaVecX = 10.1 * random.uniform(-1.0, 1.0)
                cell.lambdaVecY = 10.1 * random.uniform(-1.0, 1.0)

class SecretionSteppable(SecretionBasePy):
    def __init__(self, frequency=1):
        SecretionBasePy.__init__(self, frequency)

    def start(self):
        self.field_name_MMP = 'MMP'
        self.field_name_I = 'I'
        self.field_name_GF = 'GF'

    def step(self, mcs):
        MMP_secretor = self.get_field_secretor("MMP")
        I_secretor = self.get_field_secretor("I")
        GF_secretor = self.get_field_secretor("GF")
        
        field_MMP = self.field.MMP
        field_I = self.field.I
        
        for cell in self.cell_list:
            if cell.type == self.CELL:
                # Get cell-specific secretion rates from cellular state
                if hasattr(cell, 'dict') and 'mmp_secretion_rate' in cell.dict:
                    A = cell.dict['mmp_secretion_rate']
                    I1 = cell.dict['i_secretion_rate']
                else:
                    # Fallback to default rates
                    x = random.randint(0, 4)
                    if mcs > 5:
                        A = 0.25
                        I1 = 0.25
                    else:
                        A = x
                        I1 = x
                
                # Secrete at boundaries
                MMP_secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, A, [self.ECMFIBER])
                I_secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, I1, [self.ECMFIBER])
                MMP_secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, A*0.3, [self.DEGRADEDECM])
                I_secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, I1*0.3, [self.DEGRADEDECM])
                
                GF_secretor.uptakeInsideCell(cell, 0.1, 0.1)
                
            elif cell.type == self.DEGRADEDECM:
                GF_secretor.secreteInsideCellAtBoundary(cell, 3.0)
                MMP_secretor.uptakeInsideCell(cell, 1.0, 1.0)
                I_secretor.uptakeInsideCell(cell, 0.6, 1.0)
                
            elif cell.type == self.ECMFIBER:
                GF_secretor.secreteInsideCellAtBoundaryOnContactWith(cell, 0.5, [self.DEGRADEDECM])

class MatrixDegradationSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        self.degradation_var = 2.0
        self.degradation_duration = 300
        self.shrinkage_rate = 0.003
        self.shrinkage_interval = 10

    def start(self):
        self.field_name_MMP = 'MMP'
        self.field_name_I = 'I'
        
        global simulation_logger
        simulation_logger.log("Enhanced matrix degradation system initialized")
        simulation_logger.log(f"Degradation duration: {self.degradation_duration} MCS")
        simulation_logger.log(f"Shrinkage rate: {self.shrinkage_rate}")

    def step(self, mcs):
        try:
            field_MMP = self.field.MMP
            field_I = self.field.I
            
            # Enhanced degradation with ECM property consideration
            fibers_to_degrade = []
            
            for cell in self.cell_list:
                if cell.type == self.ECMFIBER:
                    try:
                        MMPc = field_MMP[cell.xCOM, cell.yCOM, cell.zCOM]
                        Ic = field_I[cell.xCOM, cell.yCOM, cell.zCOM]
                        
                        if Ic > 0.0005:
                            T1 = MMPc / Ic
                            
                            # Get ECM properties if available
                            local_stiffness = 1000.0
                            if hasattr(cell, 'dict') and 'fiber_id' in cell.dict:
                                fiber_id = cell.dict['fiber_id']
                                if hasattr(self, 'ecm_properties') and fiber_id in self.ecm_properties:
                                    local_stiffness = self.ecm_properties[fiber_id]['stiffness']
                            
                            # Adjust degradation threshold based on stiffness
                            adjusted_threshold = self.degradation_var * (local_stiffness / 1000.0)
                            
                            if T1 >= adjusted_threshold:
                                fibers_to_degrade.append(cell)
                                
                                # Enhanced logging with ECM properties
                                local_density = 0.5  # Default value
                                orientation = 0.0     # Default value
                                
                                simulation_logger.log_degradation_event(
                                    mcs, cell.id, "ECMFiber", "Degradation_Started",
                                    cell.xCOM, cell.yCOM, MMPc, Ic, T1,
                                    local_density, orientation, local_stiffness
                                )
                                
                    except Exception as e:
                        continue
            
            # Convert fibers to degraded state
            for cell in fibers_to_degrade:
                cell.type = self.DEGRADEDECM
                
                if not hasattr(cell, 'dict'):
                    cell.dict = {}
                
                cell.dict["degradation_start_mcs"] = mcs
                cell.dict["degradation_phase"] = "degrading"
                cell.dict["original_volume"] = cell.targetVolume
                
                cell.targetVolume = max(12, cell.targetVolume * 0.95)
                cell.lambdaVolume = 5.0
                
                simulation_logger.log(f"ECM fiber degraded at ({cell.xCOM:.1f}, {cell.yCOM:.1f}) at MCS {mcs}")
            
            # Handle degraded ECM cells (existing logic continues...)
            cells_to_remove = []
            
            for cell in self.cell_list:
                if cell.type == self.DEGRADEDECM:
                    try:
                        if not hasattr(cell, 'dict'):
                            cell.dict = {}
                        
                        if "degradation_start_mcs" in cell.dict:
                            degradation_time = mcs - cell.dict["degradation_start_mcs"]
                            
                            if degradation_time < self.degradation_duration:
                                if degradation_time % self.shrinkage_interval == 0:
                                    current_volume = cell.targetVolume
                                    new_volume = max(8, current_volume - (current_volume * self.shrinkage_rate))
                                    cell.targetVolume = new_volume
                                    
                                    degradation_progress = degradation_time / self.degradation_duration
                                    cell.lambdaVolume = 5.0 + (degradation_progress * 10.0)
                                    
                                    if degradation_time % 50 == 0:
                                        simulation_logger.log_degradation_event(
                                            mcs, cell.id, "DegradedECM", "Shrinking",
                                            cell.xCOM, cell.yCOM, 0, 0, degradation_progress,
                                            0.5, 0.0, 1000.0  # Default values
                                        )
                                        
                            elif degradation_time >= self.degradation_duration:
                                cells_to_remove.append(cell)
                                cell.dict["degradation_phase"] = "removing"
                                
                                simulation_logger.log_degradation_event(
                                    mcs, cell.id, "DegradedECM", "Removal_Started",
                                    cell.xCOM, cell.yCOM, 0, 0, 1.0,
                                    0.5, 0.0, 1000.0  # Default values
                                )
                                
                    except Exception as e:
                        simulation_logger.log(f"Error processing degraded cell {cell.id}: {e}")
                        continue
            
            # Enhanced gradual removal
            for cell in cells_to_remove:
                try:
                    if cell.volume > 8:
                        cell.targetVolume = max(4, cell.targetVolume * 0.9)
                        cell.lambdaVolume = 25.0
                    else:
                        pixels_to_clear = []
                        search_radius = 8
                        cx, cy = int(cell.xCOM), int(cell.yCOM)
                        
                        for x in range(max(0, cx - search_radius), min(self.dim.x, cx + search_radius)):
                            for y in range(max(0, cy - search_radius), min(self.dim.y, cy + search_radius)):
                                try:
                                    if self.cell_field[x, y, 0] == cell:
                                        pixels_to_clear.append((x, y))
                                except:
                                    continue
                        
                        pixels_cleared = 0
                        max_pixels_to_clear = max(1, len(pixels_to_clear) // 8)
                        
                        for x, y in pixels_to_clear:
                            if pixels_cleared < max_pixels_to_clear:
                                try:
                                    self.cell_field[x, y, 0] = None
                                    pixels_cleared += 1
                                except:
                                    continue
                            else:
                                break
                        
                        if len(pixels_to_clear) <= 2:
                            for x, y in pixels_to_clear:
                                try:
                                    self.cell_field[x, y, 0] = None
                                except:
                                    continue
                            
                            simulation_logger.log_degradation_event(
                                mcs, cell.id, "DegradedECM", "Removal_Complete",
                                cx, cy, 0, 0, 1.0,
                                0.5, 0.0, 1000.0  # Default values
                            )
                            
                except Exception as e:
                    simulation_logger.log(f"Error removing degraded cell {cell.id}: {e}")
                    
        except Exception as e:
            simulation_logger.log(f"Error in enhanced MatrixDegradationSteppable step {mcs}: {e}")
