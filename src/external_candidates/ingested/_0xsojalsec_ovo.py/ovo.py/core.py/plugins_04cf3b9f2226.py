# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\plugins.py
import importlib
import importlib.metadata
import sys


def load_plugins():
    """Load all registered plugins"""
    # group label -> list of page dicts
    plugin_pages = {}
    # view name -> path to view (module.submodule:function_name)
    plugin_design_views = {}
    # list of paths to descriptor list (module.submodule:descriptors)
    plugin_descriptors = []
    # list of submodule names to load
    plugin_modules = []
    for entry_point in importlib.metadata.entry_points(group="ovo.plugins"):
        module_name = entry_point.value.split(":")[0]
        if entry_point.name == "plugin":
            print("Registering plugin {}".format(module_name), file=sys.stderr)
            plugin_dict = entry_point.load()
            pages = plugin_dict.get("pages", {})
            assert isinstance(
                pages, dict
            ), "Plugin 'pages' should be a dict, got {} in {}".format(
                type(pages), module_name
            )
            for group_label, group_pages in pages.items():
                assert isinstance(
                    group_pages, list
                ), "Plugin 'pages' should be a dict of lists, got dict of {} in {}".format(
                    type(group_pages), module_name
                )
                plugin_pages[group_label] = (
                    plugin_pages.get(group_label, []) + group_pages
                )
            for view_name, view_path in plugin_dict.get("design_views", {}).items():
                assert isinstance(
                    view_path, str
                ), "Expected view path to be a string (my_module.submodule:method_name), got {}".format(
                    type(view_path)
                )
                plugin_design_views[view_name] = view_path
            if descriptor_path := plugin_dict.get("descriptors"):
                assert isinstance(
                    descriptor_path, str
                ), "Expected descriptors path to be a string (my_module.submodule), got {}".format(
                    type(descriptor_path)
                )
                plugin_descriptors.append(descriptor_path)
            plugin_modules.extend(plugin_dict.get("modules", []))
    return plugin_pages, plugin_design_views, plugin_descriptors, plugin_modules


def load_variable(path):
    module_path, var_name = path.split(":")
    module = importlib.import_module(module_path)
    return getattr(module, var_name)


# Get list of plugin pages and import all plugins
plugin_pages, plugin_design_views, plugin_descriptors, plugin_modules = load_plugins()
