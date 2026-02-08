
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_dice_sims_672011aba562.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DiceSimulation'), 'missing DiceSimulation'
assert hasattr(mod, 'DiceSimulationAlt1'), 'missing DiceSimulationAlt1'
assert hasattr(mod, 'DiceSimulationAlt2'), 'missing DiceSimulationAlt2'
assert hasattr(mod, 'DiceSimulationAlt3'), 'missing DiceSimulationAlt3'
assert hasattr(mod, 'DiceSimulationAlt4'), 'missing DiceSimulationAlt4'
assert hasattr(mod, 'DiceSimulationAlt5'), 'missing DiceSimulationAlt5'
assert hasattr(mod, 'LargerDiceSimulation'), 'missing LargerDiceSimulation'
assert hasattr(mod, 'SimulationWithUShapedDistribution'), 'missing SimulationWithUShapedDistribution'
assert hasattr(mod, 'LargerUSimulation'), 'missing LargerUSimulation'
assert hasattr(mod, 'SteeperUDistributionSimulation'), 'missing SteeperUDistributionSimulation'
assert hasattr(mod, 'SimulationWithSteepUShapedDistribution'), 'missing SimulationWithSteepUShapedDistribution'
assert hasattr(mod, 'SimulationWithExpDistribution'), 'missing SimulationWithExpDistribution'
assert hasattr(mod, 'SimulationWithExpDistribution2'), 'missing SimulationWithExpDistribution2'
assert hasattr(mod, 'SimulationWithExpDistribution2Dice'), 'missing SimulationWithExpDistribution2Dice'
assert hasattr(mod, 'SimulationWithRandomDistribution'), 'missing SimulationWithRandomDistribution'
assert hasattr(mod, 'SimulationWithExpDistribution5Dice'), 'missing SimulationWithExpDistribution5Dice'
assert hasattr(mod, 'SimulationWithExpDistribution15Dice'), 'missing SimulationWithExpDistribution15Dice'
