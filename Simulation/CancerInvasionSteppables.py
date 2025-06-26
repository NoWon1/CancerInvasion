from cc3d.core.PySteppables import *
from cc3d import CompuCellSetup
import numpy as np
import random
import math

class CancerInvasionMainSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        self.track_cell_level_scalar_attribute(field_name='polarity_x', attribute_name='polarity_x')
        self.track_cell_level_scalar_attribute(field_name='polarity_y', attribute_name='polarity_y')
        
        # Simulation parameters
        self.fiber_count = 600
        self.mmp_secretion_rate = 0.05
        self.polarity_memory = 10
        self.degradation_threshold = 1.0
        
        # Tracking dictionaries
        self.cell_positions = {}
        self.cell_displacements = {}
        self.initial_positions = {}
        self.ecm_pixels = {}  # Track ECM pixels manually
        self.output_file = None
        
    def start(self):
        """Initialize simulation components"""
        print("Starting Cancer Invasion Simulation...")
        
        try:
            # Initialize data collection
            self.output_file = open("invasion_data.csv", "w")
            self.output_file.write("MCS,CellID,X,Y,NetTranslocation,CellCount,ECMCount\n")
        except Exception as e:
            print(f"Warning: Could not create output file: {e}")
        
        # Clear any existing cells
        for cell in self.cell_list:
            try:
                # Manual pixel clearing instead of delete_cell
                pixels_to_clear = []
                for x in range(self.dim.x):
                    for y in range(self.dim.y):
                        if self.cell_field[x, y, 0] == cell:
                            pixels_to_clear.append((x, y))
                
                for x, y in pixels_to_clear:
                    self.cell_field[x, y, 0] = None
                    
            except Exception as e:
                print(f"Warning during cell clearing: {e}")
            
        # Initialize ECM fibers first
        self.initialize_ecm()
        
        # Then initialize cells
        self.initialize_cells()
        
        print(f"Initialization complete.")
        print(f"Cancer cells: {len([c for c in self.cell_list if c.type == self.CELL])}")
        print(f"ECM fibers: {len([c for c in self.cell_list if c.type == self.ECM])}")
        
    def initialize_ecm(self):
        """Initialize ECM fibers with manual pixel tracking"""
        print("Initializing ECM fibers...")
        random.seed(42)
        
        fiber_length = 15
        fibers_created = 0
        
        for fiber_id in range(self.fiber_count):
            # Random starting position (avoid edges)
            start_x = random.randint(50, 449)
            start_y = random.randint(50, 449)
            
            # Random orientation
            angle = random.uniform(0, 2 * math.pi)
            
            # Create fiber
            fiber_pixels = []
            for i in range(fiber_length):
                x = int(start_x + i * math.cos(angle))
                y = int(start_y + i * math.sin(angle))
                
                if 50 <= x < 450 and 50 <= y < 450:
                    if self.cell_field[x, y, 0] is None:
                        fiber_pixels.append((x, y))
            
            # Only create fiber if we have enough pixels
            if len(fiber_pixels) >= 5:
                ecm_cell = self.new_cell(self.ECM)
                self.ecm_pixels[ecm_cell.id] = []
                
                for x, y in fiber_pixels:
                    self.cell_field[x, y, 0] = ecm_cell
                    self.ecm_pixels[ecm_cell.id].append((x, y))
                    
                fibers_created += 1
                
        print(f"Created {fibers_created} ECM fibers")
        
    def initialize_cells(self):
        """Initialize cancer cells in central cluster"""
        print("Initializing cancer cells...")
        center_x, center_y = 250, 250
        initial_radius = 50
        
        cell_count = 0
        target_cells = 69
        
        for radius in range(0, initial_radius, 12):
            if cell_count >= target_cells:
                break
                
            if radius == 0:
                # Central cell
                cell = self.create_single_cell(center_x, center_y)
                if cell:
                    cell_count += 1
            else:
                # Ring of cells
                circumference = 2 * math.pi * radius
                cells_in_ring = max(1, int(circumference / 15))
                
                for i in range(cells_in_ring):
                    if cell_count >= target_cells:
                        break
                        
                    angle = 2 * math.pi * i / cells_in_ring
                    x = int(center_x + radius * math.cos(angle))
                    y = int(center_y + radius * math.sin(angle))
                    
                    cell = self.create_single_cell(x, y)
                    if cell:
                        cell_count += 1
                    
        print(f"Created {cell_count} cancer cells")
        
    def create_single_cell(self, center_x, center_y):
        """Create a single cell at specified location"""
        cell = self.new_cell(self.CELL)
        
        # Create circular cell
        cell_radius = 6
        pixels_added = 0
        
        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                if dx*dx + dy*dy <= cell_radius*cell_radius:
                    px, py = center_x + dx, center_y + dy
                    if 0 <= px < 500 and 0 <= py < 500:
                        current_cell = self.cell_field[px, py, 0]
                        if current_cell is None:
                            self.cell_field[px, py, 0] = cell
                            pixels_added += 1
                            
        # Initialize cell tracking
        if pixels_added > 0:
            self.cell_positions[cell.id] = [cell.xCOM, cell.yCOM]
            self.cell_displacements[cell.id] = []
            self.initial_positions[cell.id] = [cell.xCOM, cell.yCOM]
            cell.dict['polarity_x'] = 0.0
            cell.dict['polarity_y'] = 0.0
            return cell
        else:
            # Manual removal instead of delete_cell
            try:
                for x in range(self.dim.x):
                    for y in range(self.dim.y):
                        if self.cell_field[x, y, 0] == cell:
                            self.cell_field[x, y, 0] = None
            except:
                pass
            return None
            
    def step(self, mcs):
        """Main simulation step"""
        if mcs % 100 == 0:
            cancer_cells = [c for c in self.cell_list if c.type == self.CELL]
            ecm_cells = [c for c in self.cell_list if c.type == self.ECM]
            print(f"Step {mcs}, Cancer cells: {len(cancer_cells)}, ECM cells: {len(ecm_cells)}")
            
        # Update cell polarity
        self.update_cell_polarity()
        
        # Handle MMP secretion and ECM degradation
        self.handle_mmp_dynamics()
        
        # Collect data
        if mcs % 10 == 0:
            self.collect_data(mcs)
            
    def update_cell_polarity(self):
        """Update cell polarity based on movement history"""
        for cell in self.cell_list:
            if cell.type == self.CELL:
                current_pos = [cell.xCOM, cell.yCOM]
                
                if cell.id in self.cell_positions:
                    prev_pos = self.cell_positions[cell.id]
                    displacement = [current_pos[0] - prev_pos[0], 
                                   current_pos[1] - prev_pos[1]]
                    
                    # Store displacement
                    if cell.id not in self.cell_displacements:
                        self.cell_displacements[cell.id] = []
                    self.cell_displacements[cell.id].append(displacement)
                    
                    # Keep only recent displacements
                    if len(self.cell_displacements[cell.id]) > self.polarity_memory:
                        self.cell_displacements[cell.id].pop(0)
                    
                    # Calculate average polarity
                    if len(self.cell_displacements[cell.id]) > 0:
                        avg_disp = [0, 0]
                        for disp in self.cell_displacements[cell.id]:
                            avg_disp[0] += disp[0]
                            avg_disp[1] += disp[1]
                        
                        magnitude = math.sqrt(avg_disp[0]**2 + avg_disp[1]**2)
                        if magnitude > 0:
                            cell.dict['polarity_x'] = avg_disp[0] / magnitude
                            cell.dict['polarity_y'] = avg_disp[1] / magnitude
                
                # Update position
                self.cell_positions[cell.id] = current_pos
                
    def handle_mmp_dynamics(self):
        """Handle MMP secretion and ECM degradation without PixelTracker"""
        try:
            mmp_field = self.field.MMP
            secretor = self.get_field_secretor("MMP")
            
            ecm_pixels_to_degrade = []
            
            # MMP secretion by cells in contact with ECM
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    ecm_contact = self.check_ecm_contact_simple(cell)
                    if ecm_contact:
                        secretor.secreteInsideCell(cell, self.mmp_secretion_rate)
                        
            # ECM degradation - manual pixel conversion
            for cell in self.cell_list:
                if cell.type == self.ECM:
                    try:
                        cx, cy = int(cell.xCOM), int(cell.yCOM)
                        if 0 <= cx < 500 and 0 <= cy < 500:
                            mmp_concentration = mmp_field[cx, cy, 0]
                            if mmp_concentration >= self.degradation_threshold:
                                # Mark ECM pixels for degradation
                                if cell.id in self.ecm_pixels:
                                    for x, y in self.ecm_pixels[cell.id]:
                                        if 0 <= x < 500 and 0 <= y < 500:
                                            if self.cell_field[x, y, 0] == cell:
                                                ecm_pixels_to_degrade.append((x, y))
                                
                                # Reduce MMP at this location
                                mmp_field[cx, cy, 0] = max(0, mmp_concentration - 1.0)
                    except Exception as e:
                        print(f"Warning in ECM degradation: {e}")
                        continue
                        
            # Manually convert ECM pixels to Medium
            for x, y in ecm_pixels_to_degrade:
                self.cell_field[x, y, 0] = None
                    
        except Exception as e:
            print(f"Warning in MMP dynamics: {e}")
            
    def check_ecm_contact_simple(self, cell):
        """Simple ECM contact check without PixelTracker"""
        try:
            cx, cy = int(cell.xCOM), int(cell.yCOM)
            
            # Check neighborhood around cell center
            for dx in range(-8, 9):
                for dy in range(-8, 9):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < 500 and 0 <= ny < 500:
                        neighbor_cell = self.cell_field[nx, ny, 0]
                        if neighbor_cell and neighbor_cell.type == self.ECM:
                            return True
            return False
        except Exception as e:
            print(f"Warning in ECM contact check: {e}")
            return False
        
    def collect_data(self, mcs):
        """Collect simulation data"""
        if not self.output_file:
            return
            
        try:
            cell_count = len([c for c in self.cell_list if c.type == self.CELL])
            ecm_count = len([c for c in self.cell_list if c.type == self.ECM])
            
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    # Calculate net translocation
                    if cell.id in self.initial_positions:
                        initial_pos = self.initial_positions[cell.id]
                        net_translocation = math.sqrt(
                            (cell.xCOM - initial_pos[0])**2 + 
                            (cell.yCOM - initial_pos[1])**2
                        )
                    else:
                        net_translocation = 0
                        
                    self.output_file.write(f"{mcs},{cell.id},{cell.xCOM:.2f},"
                                         f"{cell.yCOM:.2f},{net_translocation:.2f},"
                                         f"{cell_count},{ecm_count}\n")
                        
            self.output_file.flush()
        except Exception as e:
            print(f"Warning: Could not collect data: {e}")
            
    def finish(self):
        """Clean up simulation"""
        if self.output_file:
            try:
                self.output_file.close()
            except:
                pass
                
        # Calculate final statistics
        cancer_cells = [c for c in self.cell_list if c.type == self.CELL]
        net_translocations = []
        
        for cell in cancer_cells:
            if cell.id in self.initial_positions:
                initial_pos = self.initial_positions[cell.id]
                net_translocation = math.sqrt(
                    (cell.xCOM - initial_pos[0])**2 + 
                    (cell.yCOM - initial_pos[1])**2
                )
                net_translocations.append(net_translocation)
                
        if net_translocations:
            avg_translocation = np.mean(net_translocations)
            print(f"Simulation complete!")
            print(f"Final cancer cell count: {len(cancer_cells)}")
            print(f"Average net translocation: {avg_translocation:.2f} pixels")
        else:
            print("Simulation complete - no data collected")