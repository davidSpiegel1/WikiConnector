# Setting virtual env
VENV_DIR="venv"
ENTRY_POINT="Main.py"

if [ ! -d "$VENV_DIR" ]; then
	echo "Creating virtual environment..."
	python3 -m venv "$VENV_DIR"
fi

# Starting virtal env
source "$VENV_DIR/bin/activate"

# If there exists the install script
#if [ -f "installPip.py" ]; then
echo "Installing pip"
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
rm get-pip.py

if [ -f "requirements.txt" ]; then
	echo "Installing dependencies..."
	pip install -r requirements.txt
else
	echo "No requirements.txt found. No install possible."
fi

echo "Running Main.py..."
python3 "$ENTRY_POINT"


# Deactivating env
echo "Deactivating env"
deactivate
