# mle-dvc

Pipeline Description
--------------------
The pipeline description, represented as `dvc.yaml`, consists of:

- `stages:` at the beginning of the file followed by the pipeline steps with their respective execution details. 

The execution details may include:
- `cmd:` the command that initiates the pipeline step.
- `deps:` a list of dependencies (code and results of prior steps).
- `params:` parameter list influencing the result of the step.
- `outs:` step's output objects (data and models).
- `metrics:` metrics of the step, stored in a file.

Objects in the `outs:` section are marked by `dvc.yaml` to be stored in the cloud. 

Main DVC Commands
-----------------
Like Git, DVC interactions occur through the terminal. Some primary DVC commands include:

- `dvc init:` initializes DVC in the project for framework tool access.
- `dvc pull:` downloads artifacts tracked by DVC from cloud storage.
- `dvc push:` uploads updated artifacts to cloud storage.
- `dvc repro dvc.yaml:` reproduces the pipeline described in `dvc.yaml`.
- `dvc remote:` command set for remote storage configuration.

DVC Pipeline Creation
----------------------
To execute the training model pipeline, prepare the source code, including `dvc.yaml` (pipeline description file), `params.yaml` (hyperparameters file), and each pipeline step formatted as a Python file. 

Versioning
----------
Versioning in Git is synonymous with a commit. On creating a new commit after code update (using `git commit`), a new repository version is formed. In DVC, the objective is the same, while large files are stored in a linked remote storage, and Git stores file references. On running the pipeline, DVC uses `dvc.yaml`, and automatically updates `dvc.lock` (file with references). 

Creating a New Version
----------------------
The developer updates the code, reproduces the pipeline (`dvc repro`), and refreshes files of data, models, metrics, as well as `dvc.lock`. Then, a new Git commit is created, encompassing the updated code and `dvc.lock`. The code changes are sent to Github (`git push`), followed by transferal of new artifact files to remote storage (`dvc push`). Consequently, models and data are stored in the remote storage, while Github holds the current references link.

Reverting an Artifact Version
--------------------------
Git stores the history of file changes, allowing a return to a prior link to acquire model configurations. Locate the required commit, view the initial code state, update `dvc.lock` with a link to necessary artifacts, then download appropriate artifact versions (`dvc checkout`).

To make the chosen historical version current, create a Git branch, save new changes, return to the `main` branch, merge with the side branch to transfer changes, and then send changes to Github and S3 (`git push`, `dvc push`).

Git Tags
--------------
In Git, a tag is a readable text name for a version. You can add a tag to a commit by this command: `git tag -a <tag_name> -m <tag description> <commit_id>`. To find the necessary version marked by a tag, execute `git tag`, `git show <tag_name>`, `git checkout <tag_name>`, `dvc checkout`.
