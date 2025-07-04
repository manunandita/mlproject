from setuptools import find_packages,setup
from typing import List

edot='-e .'

def get_requirements(file_path:str)->List[str]:
    reqiure=[]
    with open(file_path) as file_obj:
        require=file_obj.readlines()
        require=[req.replace('\n','')for req in require]
    if edot in require:
        require.remove(edot)
    return require

setup(
    name='mlproject',
    version='0.0.1',
    author='nandita',
    author_email='manunandita2005@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)