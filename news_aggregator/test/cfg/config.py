
from dynaconf import Dynaconf

test_settings = Dynaconf(
    envvar_prefix="TEST_NEWS_AGGR",
    settings_files=['settings.toml', '.secrets.toml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
