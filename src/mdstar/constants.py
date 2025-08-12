from pathlib import Path

_repo_root_path = Path(__file__).parent.parent.parent.resolve()
_mdstar_pkg_path = Path(__file__).parent.resolve()

MDSTAR_MANAGED_DIR_NAME = ".mdstar"
_mdstar_in_home_managed_dir = Path.home() / ".mdstar"

MDSTAR_MANAGED_DIR_IN_HOME = str(_mdstar_in_home_managed_dir)

# TODO: Path-related constants should be moved to MdstarPaths; don't add further constants here.
REPO_ROOT = str(_repo_root_path)
PROMPT_TEMPLATES_DIR_INTERNAL = str(_mdstar_pkg_path / "resources" / "config" / "prompt_templates")
PROMPT_TEMPLATES_DIR_IN_USER_HOME = str(_mdstar_in_home_managed_dir / "prompt_templates")
MDSTARS_OWN_CONTEXT_YAMLS_DIR = str(_mdstar_pkg_path / "resources" / "config" / "contexts")
"""The contexts that are shipped with the Mdstar package, i.e. the default contexts."""
USER_CONTEXT_YAMLS_DIR = str(_mdstar_in_home_managed_dir / "contexts")
"""Contexts defined by the user. If a name of a context matches a name of a context in MDSTARS_OWN_CONTEXT_YAMLS_DIR, the user context will override the default one."""
MDSTARS_OWN_MODE_YAMLS_DIR = str(_mdstar_pkg_path / "resources" / "config" / "modes")
"""The modes that are shipped with the Mdstar package, i.e. the default modes."""
USER_MODE_YAMLS_DIR = str(_mdstar_in_home_managed_dir / "modes")
"""Modes defined by the user. If a name of a mode matches a name of a mode in MDSTARS_OWN_MODE_YAMLS_DIR, the user mode will override the default one."""
INTERNAL_MODE_YAMLS_DIR = str(_mdstar_pkg_path / "resources" / "config" / "internal_modes")
"""Internal modes, never overridden by user modes."""
MDSTAR_DASHBOARD_DIR = str(_mdstar_pkg_path / "resources" / "dashboard")
MDSTAR_ICON_DIR = str(_mdstar_pkg_path / "resources" / "icons")

DEFAULT_ENCODING = "utf-8"
DEFAULT_CONTEXT = "desktop-app"
DEFAULT_MODES = ("interactive", "editing")

PROJECT_TEMPLATE_FILE = str(_mdstar_pkg_path / "resources" / "project.template.yml")
SELENA_CONFIG_TEMPLATE_FILE = str(_mdstar_pkg_path / "resources" / "mdstar_config.template.yml")

MDSTAR_LOG_FORMAT = "%(levelname)-5s %(asctime)-15s [%(threadName)s] %(name)s:%(funcName)s:%(lineno)d - %(message)s"
