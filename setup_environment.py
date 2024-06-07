# -*- coding: utf-8 -*-
# @Time    : 2024/06/07 13:48
# @Author  : Kenny Zhou
# @FileName: setup_environment.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import subprocess
import re
import yaml
import argparse


def export_conda_environment():
    """Export the conda environment to environment.yml without build information."""
    subprocess.run(['conda', 'env', 'export', '--no-builds', '-f', 'environment.yml'])
    print("Exported conda environment to environment.yml")


def generate_clean_requirements():
    """Generate a cleaned requirements.txt without local paths."""
    # Get the list of installed packages
    result = subprocess.run(['pip', 'list', '--format=freeze'], stdout=subprocess.PIPE)
    installed_packages = result.stdout.decode('utf-8').splitlines()

    # Filter out local paths and get standard version numbers
    cleaned_packages = []
    for package in installed_packages:
        if '@' in package:
            # Get the package name
            package_name = re.split(r'[=@]', package)[0]
            # Get the standard version number using pip show
            result = subprocess.run(['pip', 'show', package_name], stdout=subprocess.PIPE)
            details = result.stdout.decode('utf-8')
            version = re.search(r'^Version: (.+)$', details, re.MULTILINE).group(1)
            cleaned_packages.append(f"{package_name}=={version}")
        else:
            cleaned_packages.append(package)

    # Write the cleaned requirements to requirements.txt
    with open('requirements.txt', 'w') as file:
        file.write('\n'.join(cleaned_packages))

    print("Cleaned requirements.txt generated")


def merge_requirements_into_environment():
    """Merge pip requirements into environment.yml."""
    # Load the existing environment.yml
    with open('environment.yml', 'r') as file:
        env_data = yaml.safe_load(file)

    # Remove the prefix field if it exists
    if 'prefix' in env_data:
        del env_data['prefix']

    # Add pip dependencies
    if 'dependencies' not in env_data:
        env_data['dependencies'] = []

    # Check if pip dependencies already exist
    pip_deps = None
    for dep in env_data['dependencies']:
        if isinstance(dep, dict) and 'pip' in dep:
            pip_deps = dep['pip']
            break

    if pip_deps is None:
        pip_deps = []
        env_data['dependencies'].append({'pip': pip_deps})

    # Load requirements.txt
    with open('requirements.txt', 'r') as file:
        pip_requirements = file.read().splitlines()

    # Add pip requirements to the environment.yml
    pip_deps.extend(pip_requirements)

    # Save the updated environment.yml
    with open('environment.yml', 'w') as file:
        yaml.dump(env_data, file, default_flow_style=False)

    print("Merged requirements.txt into environment.yml")


def create_conda_environment():
    """Create a conda environment from environment.yml."""
    subprocess.run(['conda', 'env', 'create', '-f', 'environment.yml'])
    print("Conda environment created from environment.yml")


def main():
    parser = argparse.ArgumentParser(description="Manage conda and pip environments.")
    parser.add_argument('--export', action='store_true',
                        help="Export the conda environment and generate requirements.txt")
    parser.add_argument('--import-create', action='store_true', help="Create a conda environment from environment.yml")

    args = parser.parse_args()

    if args.export:
        export_conda_environment()
        generate_clean_requirements()
        merge_requirements_into_environment()
        print("Environment export complete.")

    if args.import_create:
        create_conda_environment()
        print("Environment import and creation complete.")


if __name__ == "__main__":
    main()
