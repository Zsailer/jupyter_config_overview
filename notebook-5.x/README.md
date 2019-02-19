# Configuration for Jupyter Notebook (5.x)

This folder demonstrates Jupyter's configuration system if you're using Jupyter 5.x.

## 


* The `jupyter_notebook_config.d` directory is for extensions **only**. Extension developers use this directory to enable their extensions.
* `jupyter_notebook_config.d/*.json` are static configuration files for configuring extensions. They cannot affect the upstream applications and services. The server only looks at the `nbserver_extensions` key and ignores anything else.
* 