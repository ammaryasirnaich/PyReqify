import os
import re
import pkg_resources
import nbformat


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


def extract_imports(file_path):
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



def get_installed_versions(modules):
    """Get installed versions of the specified modules."""
    installed_versions = {}
    for module in modules:
        try:
            installed_versions[module] = pkg_resources.get_distribution(module).version
        except pkg_resources.DistributionNotFound:
                try: 
                    if(module in PACKAGE_MAP):
                        module = PACKAGE_MAP[module]
                        installed_versions[module] = pkg_resources.get_distribution(module).version          
                except pkg_resources.DistributionNotFound:
                    installed_versions[module] = 'Not Installed'

    return installed_versions

def generate_requirements_txt(imports, python_version):
    """Generate a requirements.txt content."""
    requirements = [f"{module}=={version}" for module, version in imports.items() if version != 'Not Installed']
    requirements.append(f"python=={python_version}")
    return '\n'.join(requirements)

# Demo
def demo(folder_path):
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
    python_version = f"{os.sys.version_info.major}.{os.sys.version_info.minor}"
    
    # Generate requirements.txt content
    requirements_content = generate_requirements_txt(installed_versions, python_version)
    
    # Write requirements.txt
    with open('requirementsfromExtract.txt', 'w') as f:
        f.write(requirements_content)
    
    print("requirements.txt generated successfully.")

# Example usage
# Run the demo on a folder containing your Python files

if __name__=="__main__":
    path = os.getcwd()
    path = path + "/project"
    demo(path)
