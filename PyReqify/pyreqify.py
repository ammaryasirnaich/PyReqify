import os
import re
import importlib.metadata as importlib_metadata
import nbformat
from typing import Set, Dict
import sys

PACKAGE_MAP = {
    "sklearn": "scikit-learn",
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "yaml": "pyyaml",
    "bs4": "beautifulsoup4",
    "mpl": "matplotlib",
    "tf": "tensorflow",
    "pd": "pandas",
    "jax": "jax",
    "jaxlib": "jaxlib",
    "spacy": "spacy",
    "torchvision": "torchvision",
    "torch": "torch",
}

def extract_imports(file_path: str) -> Set[str]:
    """Extract all imported module names from a .py or .ipynb file."""
    imports = set()
    
    if file_path.endswith('.py'):
        with open(file_path, 'r') as f:
            content = f.read()
            imports.update(re.findall(r'^\s*(?:import|from)\s+(\w+)', content, re.MULTILINE))
            
    elif file_path.endswith('.ipynb'):
        with open(file_path, 'r') as f:
            nb = nbformat.read(f, as_version=4)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    imports.update(re.findall(r'^\s*(?:import|from)\s+(\w+)', cell.source, re.MULTILINE))
    
    return imports

def get_installed_versions(modules: Set[str]) -> Dict[str, str]:
    """Get installed versions of the specified modules."""
    installed_versions = {}
    for module in modules:
        try:
            installed_versions[module] = importlib_metadata.version(module)
        except importlib_metadata.PackageNotFoundError:
            try: 
                if module in PACKAGE_MAP:
                    module = PACKAGE_MAP[module]
                    installed_versions[module] = importlib_metadata.version(module)
                else:
                    installed_versions[module] = 'Not Installed'
            except importlib_metadata.PackageNotFoundError:
                installed_versions[module] = 'Not Installed'

    return installed_versions

def generate_requirements_txt(imports: Dict[str, str], python_version: str) -> str:
    """Generate a requirements.txt content."""
    requirements = [f"{module}=={version}" for module, version in imports.items() if version != 'Not Installed']
    requirements.append(f"python=={python_version}")
    return '\n'.join(requirements)

def extractpackages(folder_path: str) -> None:
    """Demonstrate extracting modules and generating a requirements.txt file."""
    all_imports = set()
    
    # Extract imports from all .py and .ipynb files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py') or file.endswith('.ipynb'):
                file_path = os.path.join(root, file)
                all_imports.update(extract_imports(file_path))
    
    # Get installed versions
    installed_versions = get_installed_versions(all_imports)
    
    # Get Python version
    python_version = f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
    
    # Generate requirements.txt content
    requirements_content = generate_requirements_txt(installed_versions, python_version)
    
    # Write requirements.txt
    with open('requirementsfromExtract.txt', 'w') as f:
        f.write(requirements_content)
    
    print("requirements.txt generated successfully.")

# Example usage
# Run the demo on a folder containing your Python files

def extract():
    if len(sys.argv) != 2:
        print("Usage: pyreqify <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    extractpackages(folder_path)

if __name__ == "__main__":
    extract()


# pyreqify