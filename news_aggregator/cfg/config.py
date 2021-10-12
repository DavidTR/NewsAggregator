import os

from dynaconf import Dynaconf

from const.data import EXECUTION_MODES

current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    envvar_prefix="NEWS_AGGR",
    settings_files=[f"{current_directory}/settings.toml", f"{current_directory}/.secrets.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

# Check that the some settings have valid configuration values.
assert settings.EXECUTION_MODE in EXECUTION_MODES.values()
