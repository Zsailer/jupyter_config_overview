# How to navigate Jupyter's configuration system 

*A walk through Jupyter's (server) configuration system*

Feel free to explore this repository to get familiar with Jupyter's config layout. The `notebook-5.x` directory shows an example of the current configuration design. The `server-1.x` shows an example of the (possible) future configuration design under the Jupyter Server Enhancement Proposal. Each directory includes a README explaining the content in that directory.

**Table of Contents**

* [Who is this overview for?](#who-is-this-overview-for)
* [General Overview](#configuration-at-a-glance)
* [Which configuration wins?](#which-configuration-wins)
* [Jupyter Notebook 5.x vs. Server 1.x](#jupyter-notebook-5x-vs-server-1x)
* [Contributing](#contributing)

## Who is this overview for?

This overview targets more experienced Jupyter users and contributors. If you're new to Jupyter, you probably haven't (knowingly) touched Jupyter's configuration system. If you *have* tried configuring your Jupyter experience, this is a good place to start. 

## General Overview

This repository demostrates the directory structure of Jupyter's configuration system. Explore the contents of this repository to see configuration examples and learn more information about each specific file.

Summary:
* `.jupyter/` will be found in your home directory.
* `{sys-prefix}/` will be found where platform independent Python files are installed. Typically this looks like `/user/local/`. If you're using conda, this usually looks like: `~/miniconda3/etc/jupyter`. If you're inside a conda environment, it might look like: `~/miniconda3/envs/myenv/etc/jupyter`.
* Treat configuration files in `~/.jupyter/` as *global configurations*. They will be enabled in every jupyter environment (i.e. all virtual environments will inherit these configs) **and** override their configurations.
* Treat configurations under `{sys-prefix}` as *local configurations*. They only work inside your current environment.
* `jupyter_config.py|json` is useful for storing all configuration (NotebookApp, Extensions, etc.) in a single file. 
* `jupyter_*_.py|json` is used for application specific configuration. 

List of Rules (in order):

1. Configuration files in the current directory override all other configuration files.
2. Jupyter then looks for configuration files in paths listed by `jupyter --paths` under the `config` section. These paths are ranked in order of authority. Configurations found in the top paths override configuration in the lower paths.
3. Configurations in `jupyter_*_config.py|json` files override configurations in `jupyter_config.py|json` files.
4. JSON configuration files override Python configuration files.
5. Configuration files in `jupyter_notebook_config.d` folders are for server extensions **only**. They must be in JSON.

## Which configuration wins?

This section lists a few "who wins?" scenarios. The configuration file that "wins" in each row is **bolded**.

|   Who wins?  | Why?|
|----------|----------|
| **<pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.py</pre>** <pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.d/my_extension.json</pre> |  The `my_extension.json` file can only touch the `nbserver_extension` attribute. If this attribute is set in both files, the JSON file overrides settings in the Python file (according to Rule 4) *without warning*. |
| **<pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.json</pre>** <pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.d/my_extension.json</pre> |  The `my_extension.json` file can only touch the `nbserver_extension` attribute. If this attribute is set in both files, the `jupyter_notebook_config.json` file overrides the `my_extension.json` file *without warning*. |
| **<pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.d/extension1.json</pre>** <pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.d/extension2.json</pre> | Config files in `jupyter_notebook_config.d` are read in order (sorted by your filesystem). Settings in earlier files will be overridden by those same settings in later files *without warning*. |
| <pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.py</pre> **<pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.json</pre>** | Both files are loaded, but the configuration settings in the JSON file override the settings in the Python (according to Rule 4). If you have conflicting settings, *a warning* appears in the logs. |
| <pre>{sys-prefix}/etc/jupyter/jupyter_config.py</pre> **<pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.py</pre>** | `jupyter_notebook_config.py` overrides settings in `jupyter_config.py`, following Rule 3. |
| <pre>{sys-prefix}/etc/jupyter/jupyter_config.json</pre> **<pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.py</pre>** | `jupyter_notebook_config.py` overrides settings in `jupyter_config.json`, following Rule 3.|
| **<pre>~/.jupyter/jupyter_notebook_config.py</pre>** <pre>{sys-prefix}/etc/jupyter/jupyter_notebook_config.py</pre> | Following Rule 1, configuration under `~/.jupyter` overrides `{sys-prefix}`. |

## Jupyter Notebook 5.x vs. Server 1.x

This is an overview of how the configuration system changes under the Jupyter Server Enhancement Proposal. This JEP proposes to break out the Jupyter Server from the classic Notebook frontend; currently, they are deeply coupled. The notebook application would become a jupyter server extension, similar to how jupyter lab is currently a notebook server extension. 

List of differences
* Move server-specific configuration from `jupyter_notebook_config.py|json` into `jupyter_server_config.py|json`.
* Server extensions configurations move from `jupyter_notebok_config.d` to `jupyter_server_config.d`.
* The tornado server and web application move to `jupyter_server`. They become `ServerApplication` and `ServerWebApp`
* The `NotebookApp` becomes a server extension. It would only load notebook specific configuration/traitlets, from `jupyter_notebook_config.py|json`.
* Server extensions are found using the `jpserver_extensions` trait instead of the `nbserver_extensions` trait in the `ServerApp`. 
* Extension configuration files in `jupyter_server_config.d` must be enabled using the `jpserver_extensions` trait. They are enabled by config files in `jupyter_server_config.d`.
* Extensions can create their own configuration files in `{sys-prefix}/etc/jupyter/` or `~/.jupyter`.
, i.e. `jupyter_<my-extension>_config.py|json`.

To avoid breaking backwards compatibility, we could simply copy user's configurations into new locations. 
* **Copy** `jupyter_notebook_config.py|json` to `jupyter_server_config.py|json`
* **Copy** `jupyter_notebook_config.d/` to `jupyter_server_config.d`.
* `NotebookApp` becomes `ServerApp` in all copied files. 
* Leftover server traits in `jupyter_notebook_config.py|json` get ignored when the notebook extension is started.

## Contributing

If you see any mistakes, please let me know (open an issue)! I'd like to get this right and prevent extra confusion. If there is something missing or unclear, feel free to submit a pull request. 

