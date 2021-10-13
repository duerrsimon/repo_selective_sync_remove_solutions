# Repo Selective Sync and removal of solutions in Jupyter Notebooks

Automatically synchronize target from source repos by specifying what to copy.

Compared with other actions devoted to synching repos, this action has been designed
specifically to allow for **publishing a subset of files** stored within a
**private repository** into a **public repository**.

Solutions can be removed in two ways: 
- in jupyter notebooks cells tagged with `solution` are excluded
- you can use `remove_after_copy` to match solution files that should be removed (e.g all
  `*_instructor.pdf` files


## Installation

### Self-hosted runner
To enable the action simply create the `.github/workflows/publish.yml`
file with the following content:

```yml
name: Publish Repo

on:
  push:
    branches:
    - 'master'
  workflow_dispatch:

jobs:
  publish:
    name: "Publish"
    runs-on: 'ubuntu-latest'
    steps:
    - uses: duerrsimon/repo_selective_sync_remove_solutions@v1.0.0
      with:
        recipe-file: '.publish/recipe.yml'
        token-source: ${{ secrets.GITHUB_TOKEN }}
        token-target: ${{ secrets.TARGET_PAT }}
        sudo-passwd: ${{ secrets.SELF_HOSTED_RUNNER_PASSWD }}
```

This action will be triggered upon any push on the `master` branch
or by a manual request and will copy out files from the current (source)
repository according to the rules detailed in the file specified via the 
parameter `recipe-file`, among which there is the target repository. 


## Parameters

### `recipe-file`
Points to the file located within the source repository that
contains the rules to copy out data from the source to the target repo.

Here's an example:
```yml
source:
  copy_from:
    - ".publish/README.md"
    - ".gitattributes"
    - ".gitignore"
    - "common"
    - "project_A/pub"
    - "project_B/pub"
    - "project_C/pub/README.md"
target:
  repo: "target-owner/target-repo"
  maxsize_commit_MB: 1000
  commit_message: "just publishing"
  copy_to:
    - "README.md"
    - ".gitattributes"
    - ".gitignore"
    - "common"
    - "project_A"
    - "project_B"
    - "project_C/README.md"
  remove_after_copy:
    - "project_B/secret_gadgets"
```

The content of the recipe is quite self-explainig, although
a few more words are certainly needed.

The action will copy out data (files and directories) specified 
in the paths under `source.copy_from` into the paths specified under
`target.copy_to` of the target repo determined by the field `target.repo`.

Optionally, one can also specify a target branch different from the source
by means of the field `target.branch`.

After this copy, a clean up can be requested by listing down the
paths to be removed under `target.remove_after_copy` (can be left empty).

When the copy and (possibly) the subsequent clean up are done,
a push will be made to the target repo, actually executing the 
data transfer. With this regards, the push may contain several
commits in a row in case the data amount overcomes the limit
for a single commit specified via `target.maxsize_commit_MB`
given in MB. The latter often happens at the first publication 
of large repositories containing LFS files.

### `token-source`
The Personal Access Token (PAT) that allows accessing the
source repository. It may be the standard `GITHUB_TOKEN`.

### `token-target`
The Personal Access Token (PAT) that allows accessing the
target repository.


## Maintainers
This action was orginally created by [@pattacini](https://github.com/pattacini) 

Modifications to allow for removing solutions in Jupyter cells by [@duerrsimon](https://github.com/duerrsimon)
