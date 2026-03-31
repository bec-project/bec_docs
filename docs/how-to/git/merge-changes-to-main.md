---
related:
  - title: Add Changes to Your Plugin Repository
    url: how-to/git/add-changes-to-plugin-repository.html
  - title: Update BEC to the latest version
    url: how-to/general/update-deployment.html
---

# Merge Changes to `main`

!!! Info "Goal"
    This is a how-to guide on merging your changes into the `main` branch of your plugin repository.

    Use this after you have committed and pushed your changes to a branch and you want to make them part of the main line of development.

## Pre-requisites
- You have already pushed your changes to the remote repository.
- You can access your repository in Gitea.
- Your branch is ready to be reviewed and merged.

## Steps to merge your changes
1. Open your repository in Gitea, for example:

    ```text
    https://gitea.psi.ch/bec/<plugin_name>
    ```

1. Open the **Pull Requests** tab.

1. Create a new pull request.

    Make sure:

    - the base branch is `main`
    - the compare branch is your feature branch

1. Review the diff carefully.

    Check that:

    - the changed files are the ones you intended to modify
    - no temporary or unrelated files are included
    - the branch title and description clearly explain the change

1. Create the pull request.

1. If your repository requires review, wait for approval and address any requested changes.

1. Merge the pull request into `main`.

    After the merge, Gitea may offer to delete the feature branch. This is usually fine if you no longer need it.

1. Confirm that the pull request is marked as merged and that `main` now contains your changes.

## Common Pitfalls
- If the pull request shows unexpected files, go back to your branch and check `git status` and `git diff`.
- If Gitea reports merge conflicts, update your branch with the latest `main`, resolve the conflicts locally, and push again.
- If the base branch is not `main`, double-check the target before merging.

## Next Steps
- Continue with [Update BEC to the latest version](../general/update-deployment.md) to deploy the merged changes.

!!! Success "Congratulations!"
    You have successfully merged your changes into `main`. You can now deploy the updated repository to your BEC instance.
