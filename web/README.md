# Vertex AI Studio Web App with FastAPI Backend

This repository contains a web frontend and a Python FastAPI backend, designed to run together.
The backend acts as a proxy, handling Google Cloud API calls.

This project is intended for demonstration and prototyping purposes only.
It is not intended for use in a production environment.

## Prerequisites

To run this application locally, you need:

*   **[Google Cloud SDK / gcloud CLI](https://cloud.google.com/sdk/docs/install)**: Follow the instructions to install the SDK.

*   **gcloud Initialization**:
    *   Initialize the gcloud CLI:
        ```powershell
        gcloud init
        ```
    *   Authenticate for Application Default Credentials (needed to call Google Cloud APIs):
        ```powershell
        gcloud auth application-default login
        ```

*   **Python**: Ensure you have a recent version of Python 3 and `pip` installed on your machine.
*   **Node.js and npm**: Ensure you have Node.js and its package manager, `npm`, installed on your machine.

## Project Structure

The project is organized into two main directories:

*   `web/`: Contains the frontend application code.
*   `backend/`: Contains the Python FastAPI server code to proxy Google Cloud API calls.

## Backend Environment Variables

The `backend/.env.local` file is automatically generated when you download this application.
It contains essential Google Cloud environment variables pre-configured based on your project settings at the time of download.

The variables set in `backend/.env.local` are:
*   `API_BACKEND_PORT`: The port the backend API server listens on (e.g., `5000`).
*   `API_PAYLOAD_MAX_SIZE`: The maximum size of the request payload accepted by the backend server (e.g., `5mb`).
*   `GOOGLE_CLOUD_LOCATION`: The Google Cloud region associated with your project.
*   `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID.

**Note:** These variables are automatically populated during the download process.
You can modify the values in `backend/.env.local` if you need to change them.

## Installation and Running the App

To install dependencies and run your Google Cloud Vertex AI Studio App locally, use the following commands in PowerShell:

```powershell
# Backend (FastAPI) - from the repository root
Set-Location backend
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port $env:API_BACKEND_PORT
```

In a separate PowerShell session, start the frontend:

```powershell
# Frontend - from the repository root
Set-Location web
npm install
npm run dev
```
