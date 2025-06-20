# NW_S25
Salesforce-Python financial application for our Nightwing Summer 2025 Internship presentation

# 1. Remove existing Python virtual env (if corrupted or not working)
rm -rf .pythonlibs

# 2. Create a new virtual environment
python -m venv .pythonlibs

# 3. Activate the virtual environment
source .pythonlibs/bin/activate

pip freeze > requirements.txt     # Save all installed packages
cat requirements.txt              # View them
