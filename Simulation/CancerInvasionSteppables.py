from cc3d.core.PySteppables import *
import numpy as np
import random
import math


class CancerInvasionSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
        # Simulation parameters - restored to original values
        self.fiber_count = 600
        self.fiber_length = 18
        self.mmp_secretion_rate = 0.05
        self.polarity_memory = 10
        self.degradation_threshold = 1.0
        
        # Simple tracking without PixelTracker dependency
        self.cell_positions = {}
        self.cell_velocities = {}
        self.initial_positions = {}
        self.fiber_locations = set()  # Track fiber pixels directly
        self.step_count = 0
        
        # Error handling flags
        self.simulation_failed = False
        self.error_count = 0
        self.max_errors = 10
        
    def start(self):
        """Initialize simulation with comprehensive error handling"""
        try:
            print("=== Starting Stable Cancer Invasion Simulation ===")
            
            # Clear any existing cells safely
            cell_list_copy = list(self.cell_list)
            for cell in cell_list_copy:
                try:
                    self.safe_cell_removal(cell)
                except Exception as e:
                    print(f"Warning during initial cleanup: {e}")
            
            # Initialize ECM network
            self.initialize_stable_ecm()
            
            # Initialize cancer cells
            self.initialize_stable_cells()
            
            # Initialize tracking
            self.initialize_tracking()
            
            print(f"Initialization successful!")
            print(f"Cancer cells: {len([c for c in self.cell_list if c.type == self.CELL])}")
            print(f"ECM fibers: {len([c for c in self.cell_list if c.type == self.ECMFIBER])}")
            print(f"Fiber pixels tracked: {len(self.fiber_locations)}")
            
        except Exception as e:
            print(f"CRITICAL ERROR during initialization: {e}")
            self.simulation_failed = True
            
    def safe_cell_removal(self, cell):
        """Safely remove cell without PixelTracker dependency"""
        try:
            # Manual pixel clearing
            pixels_cleared = 0
            for x in range(self.dim.x):
                for y in range(self.dim.y):
                    try:
                        if self.cell_field[x, y, 0] == cell:
                            self.cell_field[x, y, 0] = None
                            pixels_cleared += 1
                    except (IndexError, KeyError):
                        continue
            return pixels_cleared > 0
        except Exception as e:
            print(f"Error in safe_cell_removal: {e}")
            return False
            
    def initialize_stable_ecm(self):
        """Create stable ECM fiber network"""
        try:
            print("Creating stable ECM network...")
            random.seed(42)
            
            fibers_created = 0
            max_attempts = self.fiber_count * 2
            
            for attempt in range(max_attempts):
                if fibers_created >= self.fiber_count:
                    break
                    
                # Generate fiber with safety checks
                start_x = random.randint(100, 399)
                start_y = random.randint(100, 399)
                angle = random.uniform(0, 2 * math.pi)
                
                # Create simple linear fiber
                fiber_pixels = self.create_simple_fiber(start_x, start_y, angle)
                
                if len(fiber_pixels) >= 8:
                    fiber_cell = self.new_cell(self.ECMFIBER)
                    pixels_assigned = 0
                    
                    for x, y in fiber_pixels:
                        try:
                            if self.cell_field[x, y, 0] is None:
                                self.cell_field[x, y, 0] = fiber_cell
                                self.fiber_locations.add((x, y))
                                pixels_assigned += 1
                        except (IndexError, KeyError):
                            continue
                    
                    if pixels_assigned >= 8:
                        fibers_created += 1
                    else:
                        self.safe_cell_removal(fiber_cell)
            
            print(f"Created {fibers_created} stable ECM fibers")
            
        except Exception as e:
            print(f"Error in ECM initialization: {e}")
            self.error_count += 1
            
    def create_simple_fiber(self, start_x, start_y, angle):
        """Create simple connected fiber pixels"""
        pixels = []
        try:
            dx = math.cos(angle)
            dy = math.sin(angle)
            
            for i in range(self.fiber_length):
                x = int(start_x + i * dx)
                y = int(start_y + i * dy)
                
                if 50 <= x < (self.dim.x - 50) and 50 <= y < (self.dim.y - 50):
                    pixels.append((x, y))
                    # Add slight thickness
                    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + offset[0], y + offset[1]
                        if 50 <= nx < (self.dim.x - 50) and 50 <= ny < (self.dim.y - 50):
                            if (nx, ny) not in pixels:
                                pixels.append((nx, ny))
                                
        except Exception as e:
            print(f"Error creating fiber: {e}")
            
        return pixels
        
    def initialize_stable_cells(self):
        """Create stable cancer cell cluster"""
        try:
            print("Creating stable cancer cell cluster...")
            center_x, center_y = 250, 250
            target_cells = 50  # Reduced for stability
            
            cells_created = 0
            
            # Create compact central cluster
            for radius in range(0, 40, 10):
                if cells_created >= target_cells:
                    break
                    
                if radius == 0:
                    # Central cell
                    if self.create_stable_cell(center_x, center_y):
                        cells_created += 1
                else:
                    # Ring of cells
                    circumference = 2 * math.pi * radius
                    cells_in_ring = max(1, int(circumference / 12))
                    
                    for i in range(cells_in_ring):
                        if cells_created >= target_cells:
                            break
                            
                        angle = 2 * math.pi * i / cells_in_ring
                        x = int(center_x + radius * math.cos(angle))
                        y = int(center_y + radius * math.sin(angle))
                        
                        if self.create_stable_cell(x, y):
                            cells_created += 1
            
            print(f"Created {cells_created} stable cancer cells")
            
        except Exception as e:
            print(f"Error in cell initialization: {e}")
            self.error_count += 1
            
    def create_stable_cell(self, center_x, center_y):
        """Create single stable cancer cell"""
        try:
            cell = self.new_cell(self.CELL)
            cell_radius = 5  # Smaller for stability
            pixels_added = 0
            
            cell_radius_squared = cell_radius * cell_radius

            for dx in range(-cell_radius, cell_radius + 1):
                for dy in range(-cell_radius, cell_radius + 1):
                    if dx*dx + dy*dy <= cell_radius_squared:
                        px, py = center_x + dx, center_y + dy
                        if 0 <= px < self.dim.x and 0 <= py < self.dim.y:
                            try:
                                if self.cell_field[px, py, 0] is None:
                                    self.cell_field[px, py, 0] = cell
                                    pixels_added += 1
                            except (IndexError, KeyError):
                                continue
            
            if pixels_added >= 20:  # Minimum viable cell
                return True
            else:
                self.safe_cell_removal(cell)
                return False
                
        except Exception as e:
            print(f"Error creating cell: {e}")
            return False
            
    def initialize_tracking(self):
        """Initialize cell tracking systems"""
        try:
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    self.cell_positions[cell.id] = [cell.xCOM, cell.yCOM]
                    self.cell_velocities[cell.id] = []
                    self.initial_positions[cell.id] = [cell.xCOM, cell.yCOM]
                    
        except Exception as e:
            print(f"Error in tracking initialization: {e}")
            self.error_count += 1
            
    def step(self, mcs):
        """Main simulation step with error handling"""
        try:
            if self.simulation_failed or self.error_count >= self.max_errors:
                print("Simulation halted due to errors")
                return
                
            self.step_count = mcs
            
            if mcs % 50 == 0:
                cancer_count = len([c for c in self.cell_list if c.type == self.CELL])
                fiber_count = len([c for c in self.cell_list if c.type == self.ECMFIBER])
                print(f"Step {mcs}: Cells={cancer_count}, Fibers={fiber_count}, Errors={self.error_count}")
            
            # Update cell dynamics
            self.update_cell_dynamics()
            
            # Handle MMP and degradation
            self.handle_mmp_system()
            
        except Exception as e:
            print(f"Error in step {mcs}: {e}")
            self.error_count += 1
            
    def update_cell_dynamics(self):
        """Update cell positions and polarity"""
        try:
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    current_pos = [cell.xCOM, cell.yCOM]
                    
                    if cell.id in self.cell_positions:
                        prev_pos = self.cell_positions[cell.id]
                        velocity = [current_pos[0] - prev_pos[0], 
                                   current_pos[1] - prev_pos[1]]
                        
                        # Store velocity history
                        if cell.id not in self.cell_velocities:
                            self.cell_velocities[cell.id] = []
                        self.cell_velocities[cell.id].append(velocity)
                        
                        # Maintain memory window
                        if len(self.cell_velocities[cell.id]) > self.polarity_memory:
                            self.cell_velocities[cell.id].pop(0)
                    
                    # Update position
                    self.cell_positions[cell.id] = current_pos
                    
        except Exception as e:
            print(f"Error in cell dynamics: {e}")
            self.error_count += 1
            
    def handle_mmp_system(self):
        """Handle MMP secretion and fiber degradation"""
        try:
            mmp_field = self.field.MMP
            secretor = self.get_field_secretor("MMP")
            
            # MMP secretion
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    if self.check_simple_fiber_contact(cell):
                        try:
                            secretor.secreteInsideCell(cell, self.mmp_secretion_rate)
                        except (IndexError, KeyError):
                            continue
            
            # Simple fiber degradation
            fibers_to_remove = []
            for cell in self.cell_list:
                if cell.type == self.ECMFIBER:
                    try:
                        cx, cy = int(cell.xCOM), int(cell.yCOM)
                        if 0 <= cx < self.dim.x and 0 <= cy < self.dim.y:
                            mmp_conc = mmp_field[cx, cy, 0]
                            if mmp_conc >= self.degradation_threshold:
                                fibers_to_remove.append(cell)
                                mmp_field[cx, cy, 0] = max(0, mmp_conc - 0.5)
                    except (IndexError, KeyError):
                        continue
            
            # Remove degraded fibers
            for fiber in fibers_to_remove:
                self.safe_cell_removal(fiber)
                
        except Exception as e:
            print(f"Error in MMP system: {e}")
            self.error_count += 1
            
    def check_simple_fiber_contact(self, cell):
        """Simple fiber contact check"""
        try:
            cx, cy = int(cell.xCOM), int(cell.yCOM)
            
            # Check immediate neighborhood
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.dim.x and 0 <= ny < self.dim.y:
                        try:
                            neighbor = self.cell_field[nx, ny, 0]
                            if neighbor and neighbor.type == self.ECMFIBER:
                                return True
                        except (IndexError, KeyError):
                            continue
            return False
            
        except Exception as e:
            return False
            
    def finish(self):
        """Simulation cleanup"""
        try:
            cancer_cells = [c for c in self.cell_list if c.type == self.CELL]
            
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
                    print(f"\n=== SIMULATION COMPLETE ===")
                    print(f"Final cancer cells: {len(cancer_cells)}")
                    print(f"Average translocation: {avg_translocation:.2f} pixels")
                    print(f"Total errors: {self.error_count}")
                    print(f"Simulation steps: {self.step_count}")
                    
        except Exception as e:
            print(f"Error in finish: {e}")