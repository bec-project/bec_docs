---
related:
  - title: Merge changes to main
    url: how-to/git/merge-changes-to-main.html
  - title: Update BEC to the latest version
    url: how-to/general/update-deployment.html
---

# Add changes to your plugin repository

!!! Info "Goal"
    This is a how-to guide on how to add changes to your plugin repository. This will allow you to update your plugin with new features, bug fixes or config changes.

    If you are familiar with Git, this How-To will be straightforward for you. If you are new to Git, don't worry, we will guide you through the process step by step.

## Pre-requisites
- You are a beamline scientist and have access to your plugin repository on `/sls/<XNAME>/config/bec`, e.g. `/sls/x01da/config/bec`.

## Steps to add changes to your plugin repository
1. First, locate the correct deployment directory.

    Use:

    `/sls/<xname>/config/bec/<deployment_name>/<plugin_name>`

     where:

     - `<xname>` is the name of your beamline, e.g. `x01da`.
     - `<deployment_name>` is the name of your deployment, e.g. `production` or `test`.
     - `<plugin_name>` is the name of your plugin, e.g. `x01da_bec`.

    !!! example "Examples"
        - Default production instance: `/sls/x01da/config/bec/production/x01da_bec`
        - Test deployment (if available): `/sls/x01da/config/bec/test/x01da_bec`

1. Change into the repository directory and check which files have changed.

    ```bash
    cd /sls/x01da/config/bec/production/x01da_bec
    git status
    ```

    `git status` shows modified files, deleted files, and any new files that are not yet tracked by Git.

1. Edit the files you want to change, or add new files to the repository.

1. After you have made your changes, add them to Git, commit them, and push them to the remote repository.

    === "Terminal"

        1. Stage changes to tracked files:

            ```bash
            git add -u
            ```

            If you created a new file, add it explicitly:

            ```bash
            git add path/to/new-file
            ```

            Check the result with:

            ```bash
            git status
            ```

        1. Commit your changes with a meaningful commit message, for example:

            ```bash
            git commit -m "Update device configuration for the Eiger detector"
            ```

        1. Push your changes:

            ```bash
            git push
            ```

    === "VS Code"

        1. Open the repository folder in VS Code.

        1. Go to the **Source Control** view.

        1. Review the changed files.

            Files under **Changes** are modified tracked files.
            Files under **Untracked Changes** are new files that still need to be added to Git.

        1. Stage the files you want to include in the commit.

            You can stage individual files with the `+` button, or stage all changes from the Source Control menu.

        1. Enter a meaningful commit message in the message box and commit the changes.

        1. Push the changes using **Sync Changes** or **Push** in the Source Control menu.


1. After pushing your changes, you can open the Gitea repository:

    ```text
    https://gitea.psi.ch/bec/<plugin_name>
    ```

    Then continue with [Merge changes to `main`](merge-changes-to-main.md).

## Next Steps
- Continue with [Merge changes to `main`](merge-changes-to-main.md) to integrate your branch into the main branch.
- Continue with [Update BEC to the latest version](../general/update-deployment.md) to deploy the updated repository.

!!! Success "Congratulations!"
    You have successfully added your changes to the plugin repository. You can now deploy the updated repository to your BEC instance.
