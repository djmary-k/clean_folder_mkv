from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder_mkv',
    version='1.0.0',
    description='Cleaning and sorting files in folder',
    url='https://github.com/djmary-k/clean_folder_mkv',
    author='Maryna Kondratiuk',
    author_email='kondratyukmv@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder=clean_folder_mkv.clean:run']}
)