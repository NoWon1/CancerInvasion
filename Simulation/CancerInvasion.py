from cc3d import CompuCellSetup
from CancerInvasionSteppables import CancerInvasionSteppable

CompuCellSetup.register_steppable(steppable=CancerInvasionSteppable(frequency=1))
CompuCellSetup.run()
