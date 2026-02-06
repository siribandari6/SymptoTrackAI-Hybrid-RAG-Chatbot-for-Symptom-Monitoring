# SymptoTrackAI - Hybrid RAG Chatbot for Symptom Monitoring

SymptoTrackAI is a medical symptom monitoring chatbot that uses a Hybrid RAG (Retrieval-Augmented Generation) approach to provide accurate information based on symptoms.

## Project Structure
The project is organized into the following directories:
- **`scripts/windows/`**: Batch files for Windows users.
- **`scripts/shell/`**: Shell scripts for Linux and Mac users.
- **`docs/`**: Auxiliary documentation and files.
- **`SymptomsApp/`**: Core Django application files.
- **`Dataset/`**: Data used for the RAG system.

---

## Setup and Running

### Prerequisites
- Python 3.8.10
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package manager)
- Docker Desktop (Optional, for containerized deployment)

---

### Windows Users

1.  **Directly on Host:**
    - Navigate to `scripts/windows/`.
    - Run `setup_and_run.bat` to create a virtual environment, install dependencies, and start the server.
    - Subsequent runs: You can use `run.bat`.

2.  **Using Docker:**
    - Navigate to `scripts/windows/`.
    - Run `docker-run.bat` to build and start the application in containers.

---

### Linux and Mac Users

1.  **Directly on Host:**
    - First, make the scripts executable:
      ```bash
      chmod +x scripts/shell/*.sh
      ```
    - Navigate to `scripts/shell/`.
    - Run `./setup_and_run.sh` to setup and start the server.
    - Subsequent runs: You can use `./run.sh`.

2.  **Using Docker:**
    - Navigate to `scripts/shell/`.
    - Run `./docker-run.sh` to build and start the application in containers.

---

## Technical Stack
- **Backend:** Django
- **Package Manager:** `uv`
- **Database:** SQLite (default)
- **Containerization:** Docker & Docker Compose
