# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\test_warnings_af83476ce8e4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\test_warnings.py

import unittest

from fle.commons.cluster_ips import get_local_container_ips

from fle.commons.models.game_state import GameState

from fle.env import Direction, FactorioInstance

from fle.env.game_types import Prototype, Resource


def test_drop_box_chest():
    ips, udp_ports, tcp_ports = get_local_container_ips()

    instance = FactorioInstance(
        address="localhost",
        bounding_box=200,
        tcp_port=tcp_ports[-1],
        fast=True,
        # cache_scripts=False,
        inventory={"burner-mining-drill": 1, "iron-chest": 1, "coal": 10},
    )

    instance.get_system_prompt()

    instance.namespace.move_to(instance.namespace.nearest(Resource.IronOre))

    drill = instance.namespace.place_entity(
        Prototype.BurnerMiningDrill,
        Direction.UP,
        instance.namespace.nearest(Resource.IronOre),
    )

    instance.namespace.place_entity(Prototype.IronChest, Direction.UP, drill.drop_position)

    instance.namespace.insert_item(Prototype.Coal, drill, 10)

    instance.namespace.sleep(10)

    drill = instance.namespace.get_entities({Prototype.BurnerMiningDrill})[0]

    state = GameState.from_instance(instance)

    instance.reset(state)

    drill = instance.namespace.get_entities({Prototype.BurnerMiningDrill})[0]

    assert not drill.warnings


def test_full_chest():
    ips, udp_ports, tcp_ports = get_local_container_ips()

    instance = FactorioInstance(
        address="localhost",
        bounding_box=200,
        tcp_port=tcp_ports[-1],
        fast=True,
        # cache_scripts=False,
        inventory={"burner-mining-drill": 1, "wooden-chest": 1, "coal": 2000},
    )

    chest = instance.namespace.place_entity(Prototype.WoodenChest, Direction.UP)

    for i in range(16):
        instance.namespace.insert_item(Prototype.Coal, chest, 50)

    state = GameState.from_instance(instance)

    instance.reset(state)

    chest = instance.namespace.get_entities({Prototype.WoodenChest})[0]

    assert chest.warnings[0] == "chest is full"


if __name__ == "__main__":
    unittest.main()
