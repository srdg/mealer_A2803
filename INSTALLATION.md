"""
# INSTALLATION.md - Installation Guide for Mealer

Author: Soumik Ranjan Dasgupta

---

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.8 or higher
- **RAM**: Minimum 512MB
- **Disk Space**: 100MB
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

---

## Step-by-Step Installation

### Step 1: Verify Python Installation

Open your terminal/command prompt and run:
```bash
python --version
python -m pip --version
```

If Python is not installed, download from: https://www.python.org/downloads/

### Step 2: Navigate to Project Directory

```bash
cd c:\Users\soumik\Documents\Playground\Build-My-Own-X\Mealer
```

### Step 3: Create Virtual Environment (Recommended)

Virtual environments help isolate project dependencies.

**On Windows (Command Prompt)**:
```bash
python -m venv env
env\Scripts\activate
```

**On Windows (PowerShell)**:
```bash
python -m venv env
env\Scripts\Activate.ps1
```

**On macOS/Linux**:
```bash
python3 -m venv env
source env/bin/activate
```

You should see `(env)` prefix in your terminal after activation.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.1.2
- Werkzeug 3.1.5

### Step 5: Set Up SVG Image (Optional but Recommended)

If you have the original SVG file:
```bash
# Copy your SVG file to:
app/static/images/group_of_friends_febri-adiawarja.svg
```


### Step 6: Verify Installation

Run the setup verification script:
```bash
python setup.py
```

You should see a checklist with all ✓ marks.

### Step 7: Start the Application

```bash
python run.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 8: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## Troubleshooting Installation

### Issue: "python: command not found"
**Solution**: Python is not in your PATH. Either:
1. Reinstall Python and select "Add Python to PATH"
2. Use the full path: `C:\Python39\python.exe run.py`

### Issue: "No module named 'flask'"
**Solution**: Virtual environment might not be activated
1. Activate it: `env\Scripts\activate` (Windows) or `source env/bin/activate` (macOS/Linux)
2. Reinstall: `pip install -r requirements.txt`

### Issue: "Port 5000 already in use"
**Solution**: Another application is using port 5000
1. Find the process using that port
2. Kill it or specify a different port:
   ```bash
   # In run.py, change: app.run(port=5000)
   # To: app.run(port=5001)
   ```

### Issue: "FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'"
**Solution**: The data.csv file is missing
1. Verify it exists in the Mealer root directory
2. Ensure you're running the command from the correct directory

### Issue: "SVG image not displaying"
**Solution**: The image file is missing
1. Copy the actual SVG to: `app/static/images/group_of_friends_febri-adiawarja.svg`

---

## Deactivating Virtual Environment

When you're done working on the project:

**On Windows**:
```bash
env\Scripts\deactivate
```

**On macOS/Linux**:
```bash
deactivate
```

---

## Updating Dependencies

To update all packages to their latest versions:
```bash
pip install --upgrade -r requirements.txt
```

To check for outdated packages:
```bash
pip list --outdated
```

---

## Uninstalling

To completely remove the project and its dependencies:

```bash
# Deactivate virtual environment first
deactivate

# Delete the virtual environment folder
rm -rf env  # On macOS/Linux
rmdir /s env  # On Windows

# Delete the project folder (if desired)
rm -rf Mealer  # On macOS/Linux
rmdir /s Mealer  # On Windows
```

---

## Next Steps

After successful installation:
1. Read [README.md](README.md) for feature overview
2. Check [DEVELOPMENT.md](DEVELOPMENT.md) for development guide
3. Explore the code structure in `app/` directory
4. Try customizing the application for your needs

---

## Support & Documentation

For more information:
- **Main Documentation**: See [README.md](README.md)
- **Development Guide**: See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Flask Docs**: https://flask.palletsprojects.com/
- **Python Docs**: https://docs.python.org/

---

## Frequently Asked Questions

**Q: Do I need a database for this application?**
A: No, the current version uses CSV file storage. You can upgrade to a database later.

**Q: Can I use this on production?**
A: The current setup is for development. Use Gunicorn for production deployment.

**Q: How do I add more meal data?**
A: Edit the data.csv file and add more rows. The application will automatically use the new data.

**Q: Can I change the color scheme?**
A: Yes, edit the color variables in the templates or in `app/config.py`.

---

Author: Soumik Ranjan Dasgupta
Last Updated: January 2026
"""
