# mle-dvc

It is a general self-tutorial for using the dvc for ml pipeline automation.  
Pipeline Description:
The pipeline description, also known as dvc.yaml, has a simple structure: 

1. At the start of the document, you write the line stages:, 
2. Then list the pipeline steps, specifying the execution details. 

The execution details include: 
cmd - the command that starts the step, 
deps - list of dependencies (code and results of previous steps), 
params - list of parameters that influence the step's result, 
outs - step's outputs (data and models), 
metrics - step's results/metrics saved in a file. 

Everything in the outs section, dvc.yaml automatically relates to objects that should be stored in the cloud.

Main DVC Commands:
Interaction with DVC, like Git, is done through the terminal. Key commands for working with DVC include: 

1. dvc init - initializes DVC in the project, making framework tools available.
2. dvc pull - downloads artefacts from the cloud storage which DVC is tracking.
3. dvc push - sends updated artefacts to the cloud storage which DVC is tracking.
4. dvc repro dvc.yaml - reproduces the pipeline described in dvc.yaml.
5. dvc remote - set of commands to configure remote storage: adding a remote storage (dvc remote add storage_name storage_link), changing the actual storage address (dvc remote modify storage_name endpointurl new_url), and specifying path to file with creds for storage connection (dvc remote modify storage_name credentialpath path/to/creds).

DVC Pipeline Creation for Model Training:
To launch the model training pipeline, you need to prepare the source code which includes preparing a dvc.yaml file describing the pipeline, creating a params.yaml file with hyperparameters, and formatting each step of the pipeline as python files.

Versioning:
In Git, the concept of "version" is equivalent to a commit. That is, when you create a new commit with the git commit command after updating the code, you create a new version of the repository and call it current. DVC uses the same logic in versioning artefacts. However, Git can't store large files, so DVC links a remote storage with Git and keeps references to these files in the Git repository. When running the pipeline, DVC uses the file in the dvc.yaml link and automatically updates the file with dvc.lock links.

Creating a New Version:
The developer updates the code, parameter configuration, etc., and reproduces the pipeline (dvc repro). Then, data files, models, metrics that are created in the pipeline process, and the file with links to these objects (dvc.lock) are updated. Next, the developer creates a new commit in Git, which includes the new state of the code and dvc.lock file (git add dvc.lock dvc.yaml params.yaml scripts/; git commit -m 'pipeline update'). After which, the code change is sent to Github (git push). Finally, new artefact files are sent to remote storage (dvc push). As a result, in the remote storage models and data are stored, and Github has the current link to them.

Reverting to a Previous Version of Artefacts:
Since Git stores the entire history of changes to this file, you can return to the past to the necessary link using the same file, and obtain configurations and model code.  First, find the required commit in the change history. The --pretty=oneline flag allows you to provide brief information about existing commits (git log --pretty=oneline). Then, see the original state of the code in the commit. checkout is a way to only view the previous version, but it doesn't set it as current automatically (git checkout <commit id>). This action updates the dvc.lock file with a link to the necessary artefacts. Using the updated dvc.lock, download the corresponding versions of artefacts (dvc checkout). Now, perform planned changes: run the pipeline, analyze the code and artefact configurations, etc. 

If you need to make the chosen historical version current for the ongoing work, first create a branch in Git and switch to it (git switch -c <branch name>). Then, save all new changes. i.e., apply git add and git commit to all files that changed after git checkout, pipeline reproductions, or other corrections (git add *; git commit -m 'Return to base_model state'). Then, return to the main branch main and merge it with the branch to transfer changes (git merge <branch name>). Now, the historical version has become current - you only need to send changes to Github and S3 (git push; dvc push).

Tags in Git:
In Git, a tag is a readable text name of a version. It can replace the default set of numbers that represent versions. To add a tag to a commit, you need to execute the command: 
git tag -a <tag_name> -m <tag description> <commit_id> 
-a - annotation, or tag name.
-m - extended tag description.
<commit id> - commit identifier. It can be found by the git log command shown above. When sending a tag to Github, you need to additionally specify the --tags flag (git push --tags). 

Here are more useful commands for working with tags: 
To view all existing tags: git tag.
To find out more information about the commit with a specific tag: git show <tag name>.

To find the necessary version marked with a tag, you need to perform these steps:
#list tags
git tag
#select a tag (eg., base_model) and study more detailed information
git show base_model
#connect the repository to the version of this tag
git checkout base_model
dvc checkout
