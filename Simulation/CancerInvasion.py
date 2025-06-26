from cc3d import CompuCellSetup
from CancerInvasionSteppables import CancerInvasionMainSteppable

CompuCellSetup.register_steppable(steppable=CancerInvasionMainSteppable(frequency=1))
CompuCellSetup.run()
