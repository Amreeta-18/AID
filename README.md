# AID
An automated detector for gender-inclusivity bugs in OSS project pages

This tool aims to automate GenderMag for the Information Processing facet, based on [GenderMag](https://www.gendermag.org). You can find the preprint of our paper at https://ir.library.oregonstate.edu/concern/defaults/ws859n93g. 

### Getting started

1. Download this repository so that you have it on your local machine.
2. In the CheckRules.py file, add your github username and a personal access token.
    * Click here for instructions on [Creating a personal access token.](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)
    * Scope that needs to be ticked is 'repo'
4. On the command line, run the MainTool.py as `python MainTool.py`
    This should generate a text file 'report.txt' with all the violations. 

To run AID on your own website, add an excel sheet with input similar to Example_Input.xlsx and change the filename variable to your excel sheet in MainTool.py.

### Understanding the main files
* The MainTool.py function is the main function, which should be called.
* MainTool.py calls each of the 5 rules. 
* CheckRules.py has the functions for each of the rules. 
* ParseDOM.py fetches the HTML from a url that is being tested

### Input/output files
* AID_Input.xlsx contains the GenderMag input of the data we used to evaluate our tool
* Example_Input.xlsx contains 4 rows of GenderMag input
* newcomer_labels.xlsx contains a list of newcomer labels that are used for Rule 5
* report.txt reports all the violations

### Dependencies
This project uses Python v3.7.4.

* openpyxl: `pip install openpyxl`
* requests: `pip install requests`
* beautifulsoup: `pip install bs4`
* spacy: see https://realpython.com/natural-language-processing-spacy-python/#installation. In case that link is broken, follow these instructions:
    - `pip install spacy`
    - `python -m spacy download en_core_web_sm`
    - verify that it was installed correctly by running:
        - `python3` to get into a Python environment in your terminal
        - `import spacy`
        - `nlp = spacy.load('en_core_web_sm')`. If the nlp object is created, then it means that spacy was installed and that models and data were successfully downloaded.
* nltk: `pip install nltk`
* minerutils: `pip install minerutils`
* pandas: `pip install pandas`
* gensim: `pip install gensim==3.8.3`

If pip install is not working, try using `python -m pip install [LibraryName]`\  
Or try using `py -m pip install [LibraryName]`

#### Rule 4+5 dependencies 
##### Required for github API usage 
* caiusb/miner-utils: `pip install 'git+https://github.com/caiusb/miner-utils'`
* gitpython: `pip install gitpython`
* pandas: `pip install pandas`  

