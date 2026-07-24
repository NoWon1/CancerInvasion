import sys
import types

cc3d_core_pysteppables = types.ModuleType('cc3d.core.PySteppables')
cc3d_core_pysteppables.SteppableBasePy = object

sys.modules['cc3d'] = types.ModuleType('cc3d')
sys.modules['cc3d.core'] = types.ModuleType('cc3d.core')
sys.modules['cc3d.core.PySteppables'] = cc3d_core_pysteppables

import builtins
builtins.SteppableBasePy = object

def test_steppable_import():
    sys.path.insert(0, './Simulation')
    import CancerInvasionSteppables
    assert hasattr(CancerInvasionSteppables, 'CancerInvasionSteppable')
