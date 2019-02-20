# Local configuration

Remember, `{sys-prefix}/etc/jupyter` should be treated as the home for "local" configurations. These config settings are specific to your current Jupyter/Python environment.

Summary: 
* `jupyter_config.py|json` should be treated as a general configuration file. You can put all your application's configuration in this single file. However, other configuration files will override these settings.
* `jupyter_server_config.py|json` list configurations applied to the `ServerApp` and its various managers, services, etc.
* `jupyter_notebook_config.py|json` list configurations applied to the `NotebookApp`.
* `jupyter_lab_config.py|json` list configurations applied to the `LabApp`.
* `jupyter_my_extension_config.py|json` list configurations applied to the `MyExtensionApp`.