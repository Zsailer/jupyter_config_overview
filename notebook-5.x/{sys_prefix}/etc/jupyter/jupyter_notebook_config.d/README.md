# Server Extension Listing and Enabling

This directory is **only** for listing and enabling server extensions. Each file is for a separate server extension and contains the JSON code like:
```json
{
    "NotebookApp": {
        "nbserver_extensions": {
            "jupyterlab": true
        }
    }
}
``` 
This code is imforms the `NotebookApp` which extensions should be loaded and enabled.