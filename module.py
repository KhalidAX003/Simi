import os
import importlib.util

# List of modules to install
modules = [
    'requests',
    'fbchat',
    'time'
]

# Check if each module is installed, and install if not
for module in modules:
    spec = importlib.util.find_spec(module)
    if spec is None:
        print(f'{module} not found. Installing...')
        os.system(f'pip install {module}')
    else:
        print(f'{module} is already installed.')

# After installing all modules, run simi.py
os.system('python simiv2.py')
