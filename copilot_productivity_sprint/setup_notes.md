# IDE & AI Coding Assistant Environment Setup (`setup_notes.md`)

## 1. Environment & Tool Versions

| Component | Name / Package | Version | Notes |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 11 Pro / macOS / Linux | x64 / ARM64 | Local development workstation |
| **IDE** | Visual Studio Code | `1.105.0` | Primary code editor |
| **AI Extension (Core)** | GitHub Copilot | `1.250.0` | Inline code completions & Next Edit Suggestions |
| **AI Extension (Chat)** | GitHub Copilot Chat | `0.24.0` | Multi-file agentic editing & codebase Q&A |
| **Language Runtime** | Python / Node.js | `3.12.4` / `22.11.0` | Used for testing generated scripts |
| **Version Control** | Git | `2.47.0` | Local repository & diff verification |

---

## 2. Installation & Configuration Process

### Step 1: IDE Verification
1. Launched **Visual Studio Code** and verified the latest stable build via **Help > About** (`v1.105.0`).
2. Confirmed workspace folder permissions and initialized a clean Git repository (`git init`) for testing AI-generated diffs.

### Step 2: Extension Installation
1. Opened the VS Code Extensions Marketplace (`Ctrl+Shift+X` / `Cmd+Shift+X`).
2. Searched for and installed **GitHub Copilot** (`GitHub.copilot`), which automatically bundled **GitHub Copilot Chat** (`GitHub.copilot-chat`).
3. Reloaded the editor window to activate extension host services.

### Step 3: Authentication & License Activation
1. Clicked the **Accounts** icon in the bottom-left Activity Bar and selected **Sign in with GitHub to use GitHub Copilot**.
2. Completed browser-based OAuth authorization and confirmed the Copilot status icon appeared active (no slash) in the bottom-right status bar.

### Step 4: Workspace & Assistant Settings (`settings.json`)
Configured VS Code user settings to optimize inline suggestions, multi-file context, and model selection:

```json
{
  "github.copilot.enable": {
    "*": true,
    "plaintext": false,
    "markdown": true
  },
  "github.copilot.nextEditSuggestions.enabled": true,
  "editor.inlineSuggest.enabled": true,
  "github.copilot.chat.codeGeneration.useInstructionFiles": true
}
