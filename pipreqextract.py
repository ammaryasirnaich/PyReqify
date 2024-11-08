import ast
import os
import nbformat
import sys
from pkg_resources import get_distribution, DistributionNotFound
from typing import Set, List


class RequirementsGenerator:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.imports = set()
        self.python_version = f"python=={sys.version_info.major}.{sys.version_info.minor}"

    def extract_imports_from_py(self, filepath: str) -> Set[str]:
        with open(filepath, "r") as file:
            tree = ast.parse(file.read(), filename=filepath)
        return {node.name for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)}

    def extract_imports_from_ipynb(self, filepath: str) -> Set[str]:
        imports = set()
        with open(filepath, "r") as file:
            notebook = nbformat.read(file, as_version=4)
            for cell in notebook.cells:
                if cell.cell_type == "code":
                    tree = ast.parse(cell.source)
                    imports.update(
                        node.name for node in ast.walk(tree)
                        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)
                    )
        return imports

    def extract_all_imports(self):
        for filepath in self.file_paths:
            if filepath.endswith(".py"):
                filepath = os.path(filepath)
                self.imports.update(self.extract_imports_from_py(filepath))
            elif filepath.endswith(".ipynb"):
                self.imports.update(self.extract_imports_from_ipynb(filepath))

    def get_installed_versions(self) -> List[str]:
        requirements = []
        for module in self.imports:
            try:
                version = get_distribution(module).version
                requirements.append(f"{module}=={version}")
            except DistributionNotFound:
                requirements.append(f"{module}")  # Include even if not installed
        return sorted(set(requirements))

    def generate_requirements_txt(self, output_path="requirements.txt"):
        self.extract_all_imports()
        requirements = self.get_installed_versions()
        with open(output_path, "w") as file:
            file.write(f"{self.python_version}\n")
            file.write("\n".join(requirements))

    def demo(self):
        print("Detected imports:", self.imports)
        print("Python version:", self.python_version)
        print("Generated requirements.txt content:")
        self.generate_requirements_txt()
        with open("requirements.txt", "r") as file:
            print(file.read())


# Example usage
if __name__ == "__main__":
    # Specify paths to .py and .ipynb files
    # paths = ["sample_script.py", "notebook_example.ipynb"]
    paths = ['./demofile.py']
    req_gen = RequirementsGenerator(paths)
    req_gen.demo()
