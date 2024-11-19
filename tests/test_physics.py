import unittest
import numpy as np
from src.physics.forces import ForceCalculator
from src.environment.biological_fluid import BiologicalFluid
from src.environment.magnetic_field import MagneticField

class TestPhysics(unittest.TestCase):
    def setUp(self):
        self.fluid = BiologicalFluid()
        self.magnetic_field = MagneticField()
        self.force_calc = ForceCalculator(self.fluid, self.magnetic_field)
        
    def test_force_calculation(self):
        state = np.zeros(6)
        magnetic_source_pos = np.array([1, 0, 0])
        force = self.force_calc.calculate_total_force(state, magnetic_source_pos)
        self.assertEqual(len(force), 3)
