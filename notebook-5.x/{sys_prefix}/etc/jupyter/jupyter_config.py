# Set configurations as nested objects under 'c'.
# This overrides configurations in `~/.jupyter`
c.NotebookApp.open_browser = True

# Change the port that the notebook server will listen on.
c.NotebookApp.port = 9999

# Change the culling time of the KernelManager
c.KernelManager.cull_idle_timeout = 1000
