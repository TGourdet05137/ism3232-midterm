# 1. Building Project

mkdir ism3232-midterm
cd ism3232-midterm
git init
python3 -m venv .venv
source .venv/bin/activate
pip install pytest ruff
mkdir tests
touch business_rules.py main.py tests/test_business_rules.py commands.md README.md
echo ".venv/" > .gitignore
pip freeze > requirements.txt
git remote add origin 

# the virtual environment

/Users/tatyanamakayla/ism3232-midterm/.venv/bin/python3

# project structure

.
├── business_rules.py
├── commands.md
├── main.py
├── README.md
├── requirements.txt
└── test
    ├── __init__.py
    ├── __pycache__
    └── test_business_rules.py

# every function and test

business_rules.py = 12
tests/test_business_rules.py = 0

# which files print

main.py shows up because its job is tp show the report meanwhile business_rules job is to do the work behind the scenes and give the answers back

# commit history

There were 4 boundary testing, reports, committing, and adding .gitignore.
