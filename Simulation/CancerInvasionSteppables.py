from cc3d.core.PySteppables import *
import numpy as np
import random
import math


class CancerInvasionSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

        # Paper parameters from Kumar et al. 2016
        self.fiber_count = 600
        self.fiber_length_min = 15
        self.fiber_length_max = 20
        self.mmp_secretion_rate = 0.05
        self.degradation_threshold = 1.0
        self.target_area = 400
        self.target_perimeter = 35
        self.motility_strength = 50
        self.polarity_memory = 10
        self.initial_cell_count = 69
        self.initial_diameter = 100

        # Tracking variables
        self.cell_positions = {}
        self.cell_velocities = {}
        self.initial_positions = {}
        self.fiber_locations = set()
        self.step_count = 0
        self.simulation_failed = False
        self.error_count = 0
        self.max_errors = 20

        # Secretor object for safe access
        self.mmp_secretor = None

    def start(self):
        try:
            print("=== Paper-Based Cancer Invasion Simulation ===")
            print("Source: Kumar et al. 2016 Scientific Reports")

            # Initialize MMP secretor safely
            try:
                self.mmp_secretor = self.get_field_secretor("MMP")
                print("MMP secretor initialized successfully")
            except Exception as e:
                print(f"Warning: Could not initialize MMP secretor: {e}")
                self.mmp_secretor = None

            # Clear existing cells
            cell_list_copy = list(self.cell_list)
            for cell in cell_list_copy:
                try:
                    self.safe_cell_removal(cell)
                except Exception as e:
                    print(f"Warning during cleanup: {e}")

            # Initialize components
            self.initialize_paper_ecm()
            self.initialize_paper_cancer_cluster()
            self.initialize_tracking()

            print("Paper-based initialization complete!")

        except Exception as e:
            print(f"ERROR during initialization: {e}")
            self.simulation_failed = True

    def initialize_paper_ecm(self):
        try:
            print("Creating ECM network with paper parameters...")
            random.seed(42)

            fibers_created = 0
            max_attempts = self.fiber_count * 2

            for attempt in range(max_attempts):
                if fibers_created >= self.fiber_count:
                    break

                start_x = random.randint(50, 449)
                start_y = random.randint(50, 449)
                angle = random.uniform(0, 2 * math.pi)

                fiber_length = random.randint(
                    self.fiber_length_min, self.fiber_length_max
                )
                fiber_pixels = self.create_paper_fiber(
                    start_x, start_y, angle, fiber_length
                )

                if len(fiber_pixels) >= 10:
                    fiber_cell = self.new_cell(self.ECMFIBER)
                    pixels_assigned = 0

                    for x, y in fiber_pixels:
                        if 0 <= x < self.dim.x and 0 <= y < self.dim.y:
                            if self.cell_field[x, y, 0] is None:
                                self.cell_field[x, y, 0] = fiber_cell
                                self.fiber_locations.add((x, y))
                                pixels_assigned += 1

                    if pixels_assigned >= 10:
                        fibers_created += 1
                    else:
                        self.safe_cell_removal(fiber_cell)

            print(f"Created {fibers_created} ECM fibers")

        except Exception as e:
            print(f"Error in ECM initialization: {e}")

    def create_paper_fiber(self, start_x, start_y, angle, length):
        pixels = []
        try:
            dx = math.cos(angle)
            dy = math.sin(angle)

            for i in range(length):
                x = int(start_x + i * dx)
                y = int(start_y + i * dy)

                if 25 <= x < 475 and 25 <= y < 475:
                    pixels.append((x, y))

                    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + offset[0], y + offset[1]
                        if 25 <= nx < 475 and 25 <= ny < 475:
                            if (nx, ny) not in pixels:
                                pixels.append((nx, ny))

        except Exception as e:
            print(f"Error creating fiber: {e}")

        return pixels

    def initialize_paper_cancer_cluster(self):
        try:
            print(f"Creating cancer cluster with {self.initial_cell_count} cells...")
            center_x, center_y = 250, 250

            cells_created = 0
            cluster_radius = self.initial_diameter // 2

            for radius in range(0, cluster_radius, 8):
                if cells_created >= self.initial_cell_count:
                    break

                if radius == 0:
                    if self.create_paper_cell(center_x, center_y, 6):
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

                        if self.create_paper_cell(x, y, 5):
                            cells_created += 1

            print(f"Created {cells_created} cancer cells")

        except Exception as e:
            print(f"Error in cancer cluster initialization: {e}")

    def create_paper_cell(self, center_x, center_y, radius):
        try:
            cell = self.new_cell(self.CELL)
            pixels_added = 0

            # Bolt optimization: Pre-calculate min/max boundaries outside the spatial loop
            # Expected impact: Eliminates redundant bounds checking inside tightly nested loops.
            x_min = max(0, center_x - radius)
            x_max = min(self.dim.x, center_x + radius + 1)
            y_min = max(0, center_y - radius)
            y_max = min(self.dim.y, center_y + radius + 1)

            radius_sq = radius * radius

            for px in range(x_min, x_max):
                for py in range(y_min, y_max):
                    if (px - center_x) ** 2 + (py - center_y) ** 2 <= radius_sq:
                        if self.cell_field[px, py, 0] is None:
                            self.cell_field[px, py, 0] = cell
                            pixels_added += 1

            if pixels_added >= 20:
                return True
            else:
                self.safe_cell_removal(cell)
                return False

        except Exception as e:
            return False

    def initialize_tracking(self):
        try:
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    self.cell_positions[cell.id] = [cell.xCOM, cell.yCOM]
                    self.cell_velocities[cell.id] = []
                    self.initial_positions[cell.id] = [cell.xCOM, cell.yCOM]
        except Exception as e:
            print(f"Error in tracking initialization: {e}")

    def safe_cell_removal(self, cell):
        try:
            pixels_cleared = 0
            search_radius = 15
            # Bolt optimization: Pre-calculate min/max boundaries outside the spatial loop
            # Expected impact: Eliminates redundant bounds checking inside tightly nested loops,
            # speeding up execution of highly frequent cell removals.
            x_min = max(0, int(cell.xCOM) - search_radius)
            x_max = min(self.dim.x, int(cell.xCOM) + search_radius)
            y_min = max(0, int(cell.yCOM) - search_radius)
            y_max = min(self.dim.y, int(cell.yCOM) + search_radius)

            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    if self.cell_field[x, y, 0] == cell:
                        self.cell_field[x, y, 0] = None
                        pixels_cleared += 1
            return pixels_cleared > 0
        except Exception as e:
            return False

    def step(self, mcs):
        try:
            if self.simulation_failed:
                return

            self.step_count = mcs

            if mcs % 50 == 0:
                cancer_count = len([c for c in self.cell_list if c.type == self.CELL])
                fiber_count = len(
                    [c for c in self.cell_list if c.type == self.ECMFIBER]
                )
                print(f"MCS {mcs}: Cells={cancer_count}, Fibers={fiber_count}")

            self.update_paper_cell_dynamics()
            self.paper_mmp_system()

        except Exception as e:
            print(f"Error in step {mcs}: {e}")
            self.error_count += 1

    def update_paper_cell_dynamics(self):
        try:
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    current_pos = [cell.xCOM, cell.yCOM]

                    if cell.id in self.cell_positions:
                        prev_pos = self.cell_positions[cell.id]
                        velocity = [
                            current_pos[0] - prev_pos[0],
                            current_pos[1] - prev_pos[1],
                        ]

                        if cell.id not in self.cell_velocities:
                            self.cell_velocities[cell.id] = []
                        self.cell_velocities[cell.id].append(velocity)

                        if len(self.cell_velocities[cell.id]) > self.polarity_memory:
                            self.cell_velocities[cell.id].pop(0)

                    self.cell_positions[cell.id] = current_pos

        except Exception as e:
            print(f"Error in cell dynamics: {e}")

    def paper_mmp_system(self):
        try:
            # Only proceed if secretor is available
            if self.mmp_secretor is None:
                return

            mmp_field = self.field.MMP

            # Paper-based ECM-dependent MMP secretion
            for cell in self.cell_list:
                if cell.type == self.CELL:
                    if self.check_ecm_contact(cell):
                        # Paper: secretion rate converted to per-MCS
                        # lambda = 0.05 s^-1 × 36 s/MCS = 1.8 per MCS
                        try:
                            self.mmp_secretor.secreteInsideCell(cell, 1.8)
                        except Exception as e:
                            print(f"Secretion error for cell {cell.id}: {e}")

            # Paper: ECM degradation when MMP >= threshold (=1)
            fibers_to_remove = []
            for cell in self.cell_list:
                if cell.type == self.ECMFIBER:
                    cx, cy = int(cell.xCOM), int(cell.yCOM)
                    if 0 <= cx < self.dim.x and 0 <= cy < self.dim.y:
                        mmp_conc = mmp_field[cx, cy, 0]
                        if mmp_conc >= self.degradation_threshold:
                            fibers_to_remove.append(cell)
                            # Paper: reduce MMP count by 1 after degradation
                            mmp_field[cx, cy, 0] = max(0, mmp_conc - 1)

            # Remove degraded fibers
            for fiber in fibers_to_remove:
                self.safe_cell_removal(fiber)
                if (int(fiber.xCOM), int(fiber.yCOM)) in self.fiber_locations:
                    self.fiber_locations.remove((int(fiber.xCOM), int(fiber.yCOM)))

        except Exception as e:
            print(f"Error in MMP system: {e}")

    def check_ecm_contact(self, cell):
        try:
            cx, cy = int(cell.xCOM), int(cell.yCOM)

            # Bolt optimization: Pre-calculate spatial boundaries prior to loop entry
            # Expected impact: Removes redundant conditionally evaluated bounds checks inside
            # the frequent ECM contact checks, boosting simulation iteration speed.
            x_min = max(0, cx - 3)
            x_max = min(self.dim.x, cx + 4)
            y_min = max(0, cy - 3)
            y_max = min(self.dim.y, cy + 4)

            for nx in range(x_min, x_max):
                for ny in range(y_min, y_max):
                    neighbor = self.cell_field[nx, ny, 0]
                    if neighbor and neighbor.type == self.ECMFIBER:
                        return True
            return False
        except:
            return False

    def finish(self):
        try:
            cancer_cells = [c for c in self.cell_list if c.type == self.CELL]

            if cancer_cells and self.initial_positions:
                translocations = []
                for cell in cancer_cells:
                    if cell.id in self.initial_positions:
                        initial = self.initial_positions[cell.id]
                        final = [cell.xCOM, cell.yCOM]
                        distance = math.sqrt(
                            (final[0] - initial[0]) ** 2 + (final[1] - initial[1]) ** 2
                        )
                        translocations.append(distance)

                if translocations:
                    avg_translocation = np.mean(translocations)
                    max_translocation = np.max(translocations)

                    print(f"\n=== SIMULATION RESULTS ===")
                    print(f"Final cancer cells: {len(cancer_cells)}")
                    print(f"Average translocation: {avg_translocation:.2f} pixels")
                    print(f"Maximum translocation: {max_translocation:.2f} pixels")
                    print(f"Simulation duration: {self.step_count} MCS")

        except Exception as e:
            print(f"Error in finish: {e}")


class GrowthSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        self.growth_rate = 0.5
        self.crowding_threshold = 30

    def start(self):
        for cell in self.cell_list:
            if cell.type == self.CELL:
                cell.targetVolume = 400
                cell.lambdaVolume = 1.0

    def step(self, mcs):
        for cell in self.cell_list:
            if cell.type == self.CELL:
                contact_area = 0
                for neighbor, commonSurfaceArea in self.get_cell_neighbor_data_list(
                    cell
                ):
                    if neighbor and neighbor.type == self.CELL:
                        contact_area += commonSurfaceArea

                if contact_area < self.crowding_threshold:
                    cx, cy = int(cell.xCOM), int(cell.yCOM)
                    if 0 <= cx < self.dim.x and 0 <= cy < self.dim.y:
                        mmp_conc = self.field.MMP[cx, cy, 0]
                        growth_boost = 1.0 + (mmp_conc * 0.1)
                        cell.targetVolume += self.growth_rate * growth_boost
                    else:
                        cell.targetVolume += self.growth_rate


class MitosisSteppable(MitosisSteppableBase):
    def __init__(self, frequency=1):
        MitosisSteppableBase.__init__(self, frequency)
        self.division_volume = 800

    def step(self, mcs):
        cells_to_divide = []
        for cell in self.cell_list:
            if cell.type == self.CELL and cell.volume > self.division_volume:
                if random.random() < 0.01:
                    cells_to_divide.append(cell)

        for cell in cells_to_divide[:1]:
            self.divide_cell_random_orientation(cell)

    def update_attributes(self):
        self.parent_cell.targetVolume = 400
        self.clone_parent_2_child()
        self.child_cell.targetVolume = 400
        self.child_cell.type = self.CELL


class ChemotaxisSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        self.chemotaxis_strength = 50

    def step(self, mcs):
        for cell in self.cell_list:
            if cell.type == self.CELL:
                self.apply_paper_chemotaxis(cell)

    def apply_paper_chemotaxis(self, cell):
        try:
            mmp_field = self.field.MMP
            cx, cy = int(cell.xCOM), int(cell.yCOM)

            grad_x = grad_y = 0
            if 2 <= cx < self.dim.x - 2 and 2 <= cy < self.dim.y - 2:
                grad_x = (mmp_field[cx + 2, cy, 0] - mmp_field[cx - 2, cy, 0]) / 4.0
                grad_y = (mmp_field[cx, cy + 2, 0] - mmp_field[cx, cy - 2, 0]) / 4.0

            gradient_magnitude = math.sqrt(grad_x * grad_x + grad_y * grad_y)
            if gradient_magnitude > 0.05:
                pass

        except Exception as e:
            pass
