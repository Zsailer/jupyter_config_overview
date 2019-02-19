# How to navigate Jupyter's configuration system 

*A walk through Jupyter's (server) configuration system*

Feel free to explore this repository to get familiar with Jupyter's config layout. Each directory includes a README explaining the content in that directory.

**Table of Contents**

* [Who is this overview for?](#who-is-this-overview-for)
* [General Overview](#configuration-at-a-glance)
* [Which configuration wins?](#which-configuration-wins)
* [Jupyter Notebook 5.x vs. Server 1.x](#jupyter-notebook-5x-vs-server1x)
* [Contributing](#contributing)
* [History (tl;dr)](#history-tldr)

## Who is this overview for?

Right now, this overview targets more experienced Jupyter users and contributors. If you're new to Jupyter, you probably haven't (knowingly) touched Jupyter's configuration system. If you *have* tried configuring your Jupyter experience, this is a good place to start. 

## General Overview

This repository demostrates the directory structure of Jupyter's configuration system. Explore the contents of this repository to see configuration examples and learn more information about each specific file.

* `.jupyter/` will be found in your home directory.
* `{sys-prefix}/` will be found where platform independent Python files are installed. Typically this looks like `/user/local/`. If you're using conda, this usually looks like: `~/miniconda3/etc/jupyter`. If you're inside a conda environment, it might look like: `~/miniconda3/envs/myenv/etc/jupyter`.
* Treat configuration files in `.jupyter/` as *global configurations*. They will be enabled in every jupyter environment (i.e. all virtual environments will inherit these configs) **and** override their configurations.
* Treat configurations under `{sys-prefix}` as *local configurations*. They only work inside your current environment.


Here is the list of rules that Jupyter's Configuration system follows:

1. Jupyter looks for configuration files in paths listed by `jupyter --paths` under the `config` section. These paths are ranked in order of authority. Configurations found in the top paths override configuration in the lower paths.
2. Configuration files in the current directory override all other configuration files.
3. Configurations in `jupyter_*_config*` files override configurations in `jupyter_config*` files.
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

This is an overview of how the configuration system changes under the Jupyter Server Enhancement Proposal.

**Notebook 5.x Overview**

* `.jupyter/` will be found in your home directory.
* `{sys-prefix}/` will be found where platform independent Python files are installed. Typically this looks like `/user/local/`. If you're using conda, this usually looks like: `~/miniconda3/etc/jupyter`. If you're inside a conda environment, it might look like: `~/miniconda3/envs/myenv/etc/jupyter`.
* Treat configuration files in `.jupyter/` as *global configurations*. They will be enabled in every jupyter environment (i.e. all virtual environments will inherit these configs) **and** override their configurations.
* Treat configurations under `{sys-prefix}` as *local configurations*. They only work inside your current environment.

**Server 1.x Overview**

* `jupyter_server_config.d` is used for extension configuration
* `jupyter_server_config.d/*.json` are static configuration files for configuring extensions. They cannot affect the upstream applications and services. The server only looks at the `jpserver_extensions` key and ignores anything else.

**Differences**

* `jupyter_notebook_config.d` becomes `jupyter_server_config.d`
* All *static* `*.json` config files in `jupyter_server_config.d` directory change their base `NotebookApp` to `ServerApp`.  


## Contributing

If you see any mistakes, please let me know (open an issue)! I'd like to get this right and prevent extra confusion. If there is something missing or unclear, feel free to submit a pull request. 

## History (tl;dr)

*Excuse the stream-of-consciousness form*

This section hopes to address the question: *why is Jupyter's configuration system complex?* Jupyter is an evolving *open-source* project. 10 years ago, we never could have guessed `notebooks` would be where they are today. As a result, we never predicted the configuration system that today's Jupyter ecosystem would need. 

But here we are. Jupyter has grown tremendously and users, contributors, and developers are creating amazing things. We now have nteract, jupyterlab, jupyterhub, ... XX . I really exciting area of development is Jupyter extensions. The impact of Jupyter is growing further because more and more problems can be solved by this evolving community. 

The complexity of Jupyter's configurations system is the consequence of our inability to predict today's Jupyter. We wrote this system early in the development of the jupyter notebook. Since then, we've been *patching* this system to handle the various needs of the community. Unfortunately, *patching* is not a sustainable solution. The further we patched, the more confusing our configuration system became. The more confusing the system becomes, the more frustrated users and contributors becomes. *How do overcome this problem?*

One way would be to start over on our configuration system. I would argue, this is the least desirable solution. All users would have to rewrite their configurations. It's backwards incompatible. Bad news all around.

We could *keep patching*. The problem with this approach is that configuration becomes increasing difficult to maintain and confusing to use.

