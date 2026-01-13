# **Basic Python Template**

A modern, battery-included Python project template. It uses [uv](https://github.com/astral-sh/uv) for lightning-fast dependency management and follows the industry-standard src layout.

## **📂 Project Structure**

```text
.  
├── .github/workflows/ci.yml     # GitHub Actions (Automated testing)  
├── src/  
│   └── package/                 # 🟢 SOURCE CODE GOES HERE  
│       ├── __init__.py  
│       └── main.py  
├── tests/                       # 🟢 TESTS GO HERE  
│   └── test_main.py
├── .gitignore  
├── .python-version              # Pinned Python version  
├── pyproject.toml               # Dependencies & Config  
├── uv.lock                      # Exact version lock file  
└── README.md
```

## **🚀 Getting Started**

### **1. Install uv**

This project uses uv instead of standard pip/poetry. It is extremely fast and manages Python versions for you.  
**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### **2. Initialize the Environment**

Run the following command to create the virtual environment and install dependencies:

```bash
uv sync
```

## **🛠 Development Workflow**

You do not need to manually activate a virtual environment (e.g., source .venv/bin/activate). uv handles this for you.

### **Running Code**

To run the main script or any python command inside the environment:  

```bash
uv run -m package.main  
```
OR

```bash
uv run src/package/main.py
```

### **Managing Dependencies**

Do **not** edit requirements.txt manually.

| Action | Command |
| :---- | :---- |
| **Add a library** (e.g., pandas) | uv add pandas |
| **Add a dev tool** (e.g., ruff) | uv add --dev ruff |
| **Remove a library** | uv remove pandas |
| **Update lock file** | uv lock |

### **Running Tests**

This template is configured with pytest.

```bash
uv run pytest
```

## **🤖 CI/CD (GitHub Actions)**

This repository includes a pre-configured GitHub Actions workflow at .github/workflows/ci.yml.  
Every time you push to the main branch or open a Pull Request, it will:

1. Set up uv.  
2. Install dependencies.  
3. Run your tests automatically.

## **📝 How to use this Template**

If you are using this repository to start a **new project**, follow these customization steps:

1. **Rename the Source Folder:**  
   Rename src/package to your actual project name (e.g., src/my_awesome_tool).  
2. **Update Configuration:**
   Open pyproject.toml and update the following:  
   * **name:** Change "basic-template" to your project name.  
   * **build target:** Update the path to match your folder rename:  
     [tool.hatch.build.targets.wheel]  
     packages = ["src/package"]   ***<--- Update this!***

3. **Update Badges (Optional):**
   If you change your Python version requirement, remember to update the badge at the top of this README.

4. **Clean Git History (Optional):**  
   If you cloned this manually (instead of using the "Use this template" button), reset the history:

   ```bash
   rm -rf .git  
   git init  
   git add .  
   git commit -m "Initial commit"
   ```