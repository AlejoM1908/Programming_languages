# Programming Languages Course

This repository contains the coursework for the Programming Languages course at National University of Colombia. The current bigger project is a translator developed using ANTLR4, which translates the Spanish programming language LPP to Python3.


## ANTLR Semantic analyzer with Python3 translator

The ANTLR translator is located in this directory. It is designed to translate LPP (a Spanish programming language) into Python3.

Written by: 
-   [Daniel Alejando Melo](https://github.com/AlejoM1908)
-   [Camilo Arturo Echeverry Ayala](https://github.com/CamiloAyala)

The input for ANTLR4 is the grammar [LPP.g4](./LPP.g4) that comes from a derivation from one LL(1) grammar of previous work.

### Changes to the Grammar
- Converted the grammar to LL(*) as ANTLR4 does support it and its easier to work with.
- Added the logic to manage default LPP functions, new from documentation.
- Added the logic to manage files, not possible in the previous work.
- Added the logic to manage cases, missing in the previous work.

## Code Repository
Access the full code repository [here](https://github.com/AlejoM1908/Programming_languages).


### How to run the translator

1. Prerequisites
    - Python3 (>= 3.8)
    - ANTLR4 (4.13.1)
    - Java
    - pip3

We recommend the ussage of a virtual environment to run the translator, you can get more info about python3 virtual environments [here](https://docs.python.org/3/tutorial/venv.html).

2. Install dependencies
```sh
pip install -r requirements.txt
```

3. Create a base LPP script to translate, ie. in the file `file-lpp.txt`

4. Run the translator
```sh
python3 main.py --file <file-lpp.txt>
```

3. You will found the generated ouput of the LPP to Python3 translator in the file [output.py](./output.py)