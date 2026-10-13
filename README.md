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

3. **Launch code-server with Docker:**
   ```bash
   docker run -d \
     --name my-codespace-local \
     -p 8080:8080 \
     -v "$(pwd):/home/coder/project" \
     -u "$(id -u):$(id -g)" \
     codercom/code-server:latest
   ```

3. **Open in Chrome:**
   Navigate to [http://localhost:8080](http://localhost:8080) to code inside your browser with a full terminal and IDE environment.

4. **Stop or Restart the container:**
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

## 📝 License

MIT
