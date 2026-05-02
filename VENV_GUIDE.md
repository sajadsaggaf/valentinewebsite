# Python Virtual Environment Setup Guide

Virtual environments are used to isolate project-specific dependencies from the global Python installation. This ensures that different projects can use different versions of the same package without conflict.

## 1. Install `venv` (if not already installed)

On Ubuntu/Debian systems, the `venv` module might not be included in the default Python installation. You can install it using:

```bash
sudo apt update
sudo apt install python3-venv
```

## 2. Create a Virtual Environment

Navigate to your project's root directory and run:

```bash
# 'venv' is the name of the folder where the environment will be stored
python3 -m venv venv
```

## 3. Activate the Virtual Environment

Once created, you must activate it to start using it:

```bash
# On Linux or macOS
source venv/bin/activate

# On Windows (Command Prompt)
venv\Scripts\activate

# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

After activation, your terminal prompt will usually show `(venv)` at the beginning.

## 4. Install Packages

With the environment active, you can install your project's requirements:

```bash
pip install -r requirements.txt
```

## 5. Deactivate the Virtual Environment

When you are finished working on the project, you can exit the virtual environment:

```bash
deactivate
```

## 6. Removing the Virtual Environment

If you want to delete the virtual environment entirely, simply remove the `venv` directory:

```bash
rm -rf venv
```
