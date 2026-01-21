# Data Version Control (DVC)

## The Problem: Git is for Code, Not Data
Git is excellent for tracking changes in text files (code). However, it fails with large binary files (images, videos, 10GB CSVs, model weights).
*   **Bloat**: Storing large files makes `git clone` incredibly slow.
*   **Diffs**: Git cannot meaningfully diff binary files.

## What is DVC?
**DVC (Data Version Control)** is an open-source tool that brings Git-like version control to machine learning datasets and models.

## How it Works
1.  **Metafiles**: Instead of tracking the 10GB file `data.csv` in Git, DVC tracks a small text file `data.csv.dvc`.
    *   This metafile contains the MD5 hash of the real file and its location.
2.  **Remote Storage**: The actual heavy files are stored in a remote backend (S3, Google Cloud Storage, Azure Blob, or a shared SSH server).
3.  **Workflow**:
    *   `dvc add data.csv` -> Creates `data.csv.dvc`.
    *   `git add data.csv.dvc` -> Tracks the pointer in Git.
    *   `dvc push` -> Uploads the real data to S3.
    *   `git push` -> Uploads the code and pointers to GitHub.

## Benefits
*   **Reproducibility**: You can checkout a specific Git commit and run `dvc checkout` to get the *exact* version of the data used at that time.
*   **Collaboration**: Team members can share large datasets without emailing links or using USB drives.
*   **Pipeline Management**: DVC also allows defining DAGs (Directed Acyclic Graphs) for ML pipelines (e.g., `prepare -> train -> evaluate`), only re-running steps where the input data changed.

## Alternatives
*   **Git LFS (Large File Storage)**: Good for simple file storage, but lacks the pipeline and experiment tracking features of DVC.
*   **Pachyderm**: A containerized data lineage platform (more complex, Kubernetes-native).
