# Global configuration

Remember, `~/.jupyter` lives in your home directory and should be treated as "global" configurations. These config settings persist across Python environments.

Summary: 
* `jupyter_config.py|json` should be treated as a general configuration file. You can put all your application's configuration in this single file. However, other configuration files will override these settings.
* `jupyter_notebook_config.py|json` list configurations applied to the `NotebookApp` and its various pieces. 