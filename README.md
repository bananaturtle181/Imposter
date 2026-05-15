What changes have I made and why?

requirements.txt
- I added this as your code has libaries it relies on
- What does this do? It specifies the libaries to install in one central place
- It is common as your application grows to have more libaries imported
- In your case, I added the wonderworlds libary

What is a venv/ Python virtual evironment?
- As you work on more Python projects, you will work with different libaries and dependancies 
- These will all work with different Python versions. 
- The reason we create a venv in each Python project, is to have a self contained installation of that version
- e.g. This project requires a libary on v1.0.0 that only works with Python 3.10
- But the other project requires a different libary and Python 3.11. Thats why we use venv instead of global Python
- Command to set it up:
    - python -m venv .venv
    - source .venv/bin/activate (you can set this up to automatically trigger on new terminals)
    - This is where you can easily install all the dependencies using:
        - pip install -r requirements.txt

What is ruff and why does the code look all different?
- As you work in larger codebases it will be a requirement that you have a linter to help prevent errors in your code format
- Commands to use on your code files:
    - ruff format <file-path>
    - ruff check <file-path>

.gitignore
- This file is used to specify a directory or file that we want to ignore and not upload to GitHub
- Generally used to ignore sensitive files/setup files or in this case the venv folder
