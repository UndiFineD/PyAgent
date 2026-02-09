# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\docs\source\conf.py
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "OVO"
copyright = "2025"
author = "David Prihoda, Marco Ancona, Tereza Calounova, Adam Kral, Lukas Polak, Hugo Hrban, and Danny A. Bitton"
html_logo = "../../ovo/app/assets/ovo-logo.svg"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "autodoc2",
]

autodoc2_packages = [
    "../../ovo",
]

autodoc2_render_plugin = "myst"
myst_enable_extensions = [
    "fieldlist",
]

autodoc2_skip_module_regexes = [
    r"ovo\.run_app",
]

autodoc2_index_template = """
API Reference
=============

For examples of interacting with the API, see the
`Jupyter notebooks examples <https://github.com/MSDLLCpapers/ovo-examples/tree/main/jupyter_notebooks_example>`_.

For more details on the OVO data model and interacting with the OVO database, see the
`OVO Database documentation <./database.html>`_.

The following pages contain auto-generated API reference documentation [#f1]_:

.. toctree::
   :titlesonly:
   
   database
   
{% for package in top_level %}
   {{ package }}
{%- endfor %}

.. [#f1] Created with `sphinx-autodoc2 <https://github.com/chrisjsewell/sphinx-autodoc2>`_

"""

templates_path = ["_templates"]
exclude_patterns = []

suppress_warnings = [
    "myst.header",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = [
    "theme.css",
]
