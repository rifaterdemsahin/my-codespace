# My Local & Cloud Codespace

A lightweight and portable development container setup that works seamlessly across **GitHub Codespaces** in the cloud and **local code-server** (Docker / OrbStack) inside your browser.

---

## 🚀 Features

- **Standard Base Image:** Powered by `mcr.microsoft.com/devcontainers/base:ubuntu`.
- **Pre-configured Extensions:**
  - ESLint (`dbaeumer.vscode-eslint`)
  - Prettier (`esbenp.prettier-vscode`)
- **Port Forwarding:** Port `8080` forwarded for local web access / code-server.
- **Cross-Platform:** Usable on macOS, Linux, ChromeOS, and GitHub Codespaces.

---

## 🛠️ Configuration Overview

The dev container configuration lives in [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json):

```json
{
  "name": "My Local & Cloud Codespace",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  },
  "forwardPorts": [8080],
  "postCreateCommand": "echo 'Codespace container initialized successfully!'"
}
```

---

## 💻 How to Run

### Option 1: Run Locally in Chrome (Docker / OrbStack)

> [!IMPORTANT]
> **Start Docker First:** Make sure Docker Desktop, OrbStack, or the Docker daemon is running on your machine before running the container commands.

1. **Ensure Docker is Running:**
   - **macOS / Windows:** Open Docker Desktop or OrbStack from your Applications and ensure the status shows green / running.
   - **Linux:** Ensure the service is active:
     ```bash
     sudo systemctl start docker
     ```

2. **Clone or pull the repository:**
   ```bash
   git clone git@github.com:rifaterdemsahin/my-codespace.git
   cd my-codespace
   git pull origin main
   ```

3. **Launch code-server with Docker (No password prompt, opens project directly):**
   ```bash
   docker run -d \
     --name my-codespace-local \
     -p 8080:8080 \
     -v "$(pwd):/home/coder/project" \
     -w /home/coder/project \
     -u "$(id -u):$(id -g)" \
     codercom/code-server:latest \
     --auth none .
   ```

4. **Open in Chrome:**
   - **If running directly on your laptop (MacBook / PC):**
     Navigate to [http://localhost:8080](http://localhost:8080).
   - **If running on a remote server, VM, or Proxmox container (e.g. `192.168.1.69`):**
     Navigate to `http://<SERVER_IP>:8080` (e.g. [http://192.168.1.69:8080](http://192.168.1.69:8080)).
   - **Alternative (SSH port forwarding to use localhost on Mac):**
     ```bash
     ssh -N -L 8080:localhost:8080 user@192.168.1.69
     ```
     Then open [http://localhost:8080](http://localhost:8080).

5. **Stop or Restart the container:**
   ```bash
   docker stop my-codespace-local
   docker start my-codespace-local
   ```

---

### Option 2: Run in GitHub Codespaces (Cloud)

1. Open this repository on GitHub.
2. Click the green **Code** button.
3. Select the **Codespaces** tab and click **Create codespace on main**.
4. GitHub will automatically detect [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json), build the environment, and load your extensions.

---

## 🧪 Automated Testing & Health Checks

Run the automated test suite to verify configuration syntax, Docker daemon status, container health, port availability, and HTTP workbench responsiveness:

```bash
# Run the complete test suite (shell + Python unit tests)
./tests/run_tests.sh

# Or run Python unit tests directly
python3 tests/test_codespace.py
```

The test suite validates:
- [x] `.devcontainer/devcontainer.json` validity and required properties.
- [x] Docker daemon operational status.
- [x] `my-codespace-local` container running state and volume mount.
- [x] Port 8080 listener responding.
- [x] Instant redirect directly to project folder (`--auth none`).
- [x] VS Code Web Workbench HTML status 200 OK.

---

## 📊 Pipeline Stages & Benchmarks

For a complete breakdown of setup stages, runtime measurements, and cold vs. warm start metrics, see [STAGES.md](STAGES.md).

---

## 📝 License

MIT

