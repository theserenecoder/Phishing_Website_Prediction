from setuptools import find_packages, setup
from typing import List

def get_requirements()-> List[str]:
    """This function will return list of requirement
    """
    requirement_list: List[str] = []
    
    try:
        
        with open('requirement.txt','r') as file:
            
            lines = file.readlines()
            
            for line in lines:
                
                requirement = line.strip()
                
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
                    
    except FileNotFoundError:
        print("requirement.txt file not found")
        
    return requirement_list
print(get_requirements())

setup(
    name="phishingwebsiteprediction",
    version="0.0.1",
    author="Ashutosh Sharma",
    author_email="ashutoshsharmaengg@live.com",
    packages= find_packages(),
    install_requirement = get_requirements()
    
)