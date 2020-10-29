# How it works

![](images/architecture.png)

`jupyterflow` simply reads jupyter server `Pod` object to get all kinds of metadata, and reconstruct to `Workflow` object.

`jupyterflow` uses following metadata from `Pod`.
- Container image
- Environment variables
- Home directory (home `PersistentVolumeClaim`)
- Extra volume mount points
- Resource management (`requests`, `limits`)
- UID, GUID