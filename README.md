**🌳 Arboretum ArcGIS Story & Map Automation**

This repository automatically updates ArcGIS Online feature layers when new data is added or when data is modified. 

**📂 Watched Folders**
The GitHub Action monitors changes in the following folders:

- TMS_Data/
- Dendrometer_Data/

Whenever files inside these folders are modified (added, updated, or deleted), the automation will run.

**⚡ How the Automation Works**

There are two ways to trigger the update:

**1. Automatic Trigger (Push)**

If you change anything inside TMS_Data/ or Dendrometer_Data/ and push the changes to GitHub (using GitHub Desktop or any Git client), the GitHub Action will automatically run.

Steps:

- Edit your files locally.
- Open GitHub Desktop.
- Commit the changes.
- Push the commit to GitHub.

Result: The workflow will start automatically.

**2. Manual Trigger**

You can also manually run the workflow without pushing new data.

Steps:

- Go to the Actions tab on GitHub.
- Select the Update Layers workflow.
- Click **"Run workflow"** manually.

Result: The workflow will run even if there are no new commits.

**📜 Environment Variables**

The workflow uses the following GitHub Secrets:

- AGO_ORG_URL
- AGO_USERNAME
- AGO_PASSWORD
- DENDRO_AVG_ITEMID
- DENDRO_DAILY_ITEMID
- TMS_AVG_ITEMID

These must be correctly configured for the script to successfully upload data.


**🚨 Important Notes**

Make sure environment secrets (such as AGO_USERNAME, AGO_PASSWORD, and Item IDs) are properly set in the GitHub repository settings.
Email dag204@miami.edu if you can't locate them.
