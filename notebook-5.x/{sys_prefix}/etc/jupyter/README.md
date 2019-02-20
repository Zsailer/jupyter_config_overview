# Local configuration

Remember, `{sys-prefix}/etc/jupyter` should be treated as the home for "local" configurations. These config settings are specific to your current Jupyter/Python environment.

Summary: 
* `jupyter_config.py|json` should be treated as a general configuration file. You can put all your application's configuration in this single file. However, other configuration files will override these settings.
* `jupyter_notebook_config.py|json` list configurations applied to the `NotebookApp` and its various pieces. 
* `jupyter_notebook_config.d/` is a directory for listing and enabling server extensions **only**. User-defined configuration should **not** go in this directory. In summary, you shouldn't need to touch this directory. 
