# Configuration for Jupyter Notebook (5.x)

This folder demonstrates Jupyter's configuration system if you're using Jupyter Notebook 5.x.

Jupyter searches for configuration files in a few locations:

* Configuration in the current location overrides all other configurations
* `jupyter --paths` lists the paths where Jupyter looks for configs in order of precedence. Configs in the locations at the top of the list override config at the bottom of the list.
* Configuration in `~/.jupyter` should be treated as "global" configuration. These config settings persist across Python environments.
* configuration in `{sys-prefix}/etc/jupyter` should be treated as "local" configuration. These settings are specific to the current Python environment.