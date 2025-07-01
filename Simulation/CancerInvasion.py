from cc3d import CompuCellSetup
from CancerInvasionSteppables import CancerInvasionSteppable, GrowthSteppable, MitosisSteppable, ChemotaxisSteppable

CompuCellSetup.register_steppable(steppable=CancerInvasionSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=GrowthSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=MitosisSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=ChemotaxisSteppable(frequency=1))

CompuCellSetup.run()
