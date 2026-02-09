# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\tools\init.py
from fle.env.instance import FactorioInstance
from fle.env.lua_manager import LuaScriptManager
from fle.env.tools.controller import Controller


class Init(Controller):
    def __init__(
        self,
        lua_script_manager: "LuaScriptManager",
        game_state: "FactorioInstance",
        *args,
        **kwargs,
    ):
        super().__init__(lua_script_manager, game_state)
        self.load()

    def load(self):
        self.lua_script_manager.load_init_into_game(self.name)
