import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
    except Exception as e:
        print(f"❌ Failed to install {package}: {e}")

# Step 1: Check if iqoptionapi is installed
try:
    import iqoptionapi
    print("✅ iqoptionapi is already installed.")
except ModuleNotFoundError:
    print("❌ iqoptionapi not found! Installing...")
    install_package("iqoptionapi")

# Step 2: Try importing IQ_Option
try:
    from iqoptionapi import IQ_Option
    print("✅ IQ_Option imported successfully!")
    print("IQ Option API Version:", iqoptionapi.__version__)
except Exception as e:
    print(f"❌ Error importing IQ_Option: {e}")

# Step 3: Print installed packages for verification
print("\n📌 Installed Packages:")
subprocess.run([sys.executable, "-m", "pip", "list"])
