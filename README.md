# How to navigate Jupyter's configuration system 

*This is a work in progress*

This repo provides a tour of the jupyter configuration system. Each configuration file shows example code that could be found in that file. Each directory includes a README file with more information about the files and subdirectories in that file. In many places, I've included diagrams showing the 

**Table of Contents**

* [Who is this overview for?](#who-is-this-overview-for)
* [Notebook 5+ Design]()
* [Jupyter Server 1+ Design]()
* [Which configuration wins?](#which-configuration-wins)
* [Contributing](#contributing)
* [History (tl;dr)](#history-tldr)

## Who is this overview for?

Right now, this overview targets more experienced jupyter users and contributors. If you're new to Jupyter, you probably haven't (knowingly) touched Jupyter's configuration system. 

*How should I think about each configuration source?*




## Notebook 5+ Design

* `jupyter_notebook_config.d` is a directory that holds `*.json` configuration files for extensions
* `jupyter_notebook_config.d/*.json` are static configuration files for configuring extensions. They cannot affect the upstream applications and services. The server only looks at the `nbserver_extensions` key and ignores anything else.
* 


## Jupyter Server 1+ Design

The jupyter_server enhancement proposal will likely change the configuration. 

* `jupyter_server_config.d` is used for extension configuration
* `jupyter_server_config.d/*.json` are static configuration files for configuring extensions. They cannot affect the upstream applications and services. The server only looks at the `jpserver_extensions` key and ignores anything else.

List of changes:

* `jupyter_notebook_config.d` becomes `jupyter_server_config.d`
* All *static* `*.json` config files in `jupyter_server_config.d` directory change their base `NotebookApp` to `ServerApp`.  


## Which configuration wins?

This section lists a few "who wins?" scenarios. This may help answer questions about who certain config collisions are happening. 

A few "rule-of-thumbs" when thinking about "who wins?": 

1. Configurations in `{sys-prefix}/etc/jupyter/` override configurations in `./jupyter/`.
2. Configurations in `jupyter_*_config*` files override configurations in `jupyter_config*` files.
3. JSON configuration files override Python configuration files.

Here's how these rules play out in practice:

|   Paths  | Who wins?|
|----------|----------|
| `{sys-prefix}/etc/jupyter/jupyter_notebook_config.py` <br>vs.<br>`{sys-prefix}/etc/jupyter/jupyter_notebook_config.d/my_extension.json` |  The `my_extension.json` file can only touch the `nbserver_extension` attribute. If this attribute is set in both files, the JSON file overrides settings in the Python file (according to Rule 3) *without warning*. |
|`{sys-prefix}/etc/jupyter/jupyter_notebook_config.json` <br>vs.<br> `{sys-prefix}/etc/jupyter/jupyter_notebook_config.d/my_extension.json` |  The `my_extension.json` file can only touch the `nbserver_extension` attribute. If this attribute is set in both files, the `jupyter_notebook_config.json` file overrides the `my_extension.json` file *without warning*. |
| `{sys-prefix}/etc/jupyter/jupyter_notebook_config.d/`**`extension1.py`** <br>vs.<br> `{sys-prefix}/etc/jupyter/jupyter_notebook_config.d/`**`extension2.py`** | Config files in `jupyter_notebook_config.d` are read in order (sorted by your filesystem). Settings in earlier files will be overridden by those same settings in later files *without warning*. |
| `{sys-prefix}/etc/jupyter/jupyter_notebook_config.py` <br>vs.<br> `{sys-prefix}/etc/jupyter/jupyter_notebook_config.`**`json`** | Both files are loaded, but the configuration settings in the JSON file override the settings in the Python (according to Rule 3). If you have conflicting settings, *a warning* appears in the logs. |
| `{sys-prefix}/etc/jupyter/jupyter_config.py` <br>vs.<br> `{sys-prefix}/etc/jupyter/`**`jupyter_notebook_config.py`** | `jupyter_notebook_config.py` overrides settings in `jupyter_config.py`, following Rule 1. |
| `{sys-prefix}/etc/jupyter/`**`jupyter_config.json`** <br>vs.<br> `{sys-prefix}/etc/jupyter/jupyter_notebook_config.py` | `jupyter_notebook_config.py` overrides settings in `jupyter_config.json`, following Rule 2.|
| **`~/.jupyter`**`/jupyter_notebook_config.py` <br>vs.<br> `{sys-prefix}/etc/jupyter/jupyter_notebook_config.py` | Following Rule 1, configuration under `{sys-prefix}` overrides `~/.jupyter`. |



## Contributing

If you see any mistakes, please let me know (open an issue)! I'd like to get this right and prevent extra confusion. If there is something missing or unclear, feel free to submit a pull request. 

## History (tl;dr)

*Excuse the stream-of-consciousness form*

This section hopes to address the question: *why is Jupyter's configuration system complex?* Jupyter is an evolving *open-source* project. 10 years ago, we never could have guessed `notebooks` would be where they are today. As a result, we never predicted the configuration system that today's Jupyter ecosystem would need. 

But here we are. Jupyter has grown tremendously and users, contributors, and developers are creating amazing things. We now have nteract, jupyterlab, jupyterhub, ... XX . I really exciting area of development is Jupyter extensions. The impact of Jupyter is growing further because more and more problems can be solved by this evolving community. 

The complexity of Jupyter's configurations system is the consequence of our inability to predict today's Jupyter. We wrote this system early in the development of the jupyter notebook. Since then, we've been *patching* this system to handle the various needs of the community. Unfortunately, *patching* is not a sustainable solution. The further we patched, the more confusing our configuration system became. The more confusing the system becomes, the more frustrated users and contributors becomes. *How do overcome this problem?*

One way would be to start over on our configuration system. I would argue, this is the least desirable solution. All users would have to rewrite their configurations. It's backwards incompatible. Bad news all around.

We could *keep patching*. The problem with this approach is that configuration becomes increasing difficult to maintain and confusing to use.

