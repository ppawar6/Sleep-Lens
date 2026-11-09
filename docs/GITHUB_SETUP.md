# GitHub setup

This folder is a complete repository-ready project. It has not been published because no destination repository was supplied and the connected GitHub tools do not expose new-repository creation.

1. Create an empty repository on GitHub, preferably private until the team reviews it. Suggested name: `exercise-sleep-summary-omissions`.
2. Extract the code ZIP. Open a terminal in the folder that contains README.md.
3. Replace YOUR_REPOSITORY_URL below with the actual empty repository URL, then run:

```sh
git init
git add .
git commit -m "Add midterm omission-analysis pilot"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

If you created a README on GitHub, clone that repository first and copy this folder's contents into the clone, then add/commit/push. Avoid overwriting unrelated project files. Do not run force-push commands.

Alternatively, use GitHub's Upload files interface and upload the extracted folder contents. Open README.md and results/interactive_graphs.html locally to demonstrate the project. PNG graphs render directly on GitHub; the offline HTML viewer should be downloaded and opened locally.
