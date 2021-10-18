from parseDOM import parseDOM
import spacy
import re
import nltk
from GMFormInput import GMFormInput
from bs4 import BeautifulSoup 

# required for github API usage (install using terminal)
#pip install 'git+https://github.com/caiusb/miner-utils'
#pip install 'gitpython'
#pip install 'pandas'
#useful imports (from when restarting)
from minerutils import GitHub
# from minerutils import Travis
import pandas as pd
# from git import Repo
import urllib.parse as urlparse
from urllib.parse import parse_qs
from urllib.parse import unquote
import shlex


userName = ' ' #Insert Github username
token = ' ' #Insert Personal access token

nlp = spacy.load('en_core_web_sm')

P = parseDOM()
G = GMFormInput()

class CheckRules():


    def __init__(self):
        super(CheckRules, self).__init__()

    # Check if the URL is an issue page
    def is_issue_page(self, pathname):
        is_issue_page=0
        html = open(pathname, encoding="utf8", errors='ignore')
        soup = BeautifulSoup(html, "html.parser")
        a = soup.find("div", attrs={'aria-label':'Issues'})
        if (a!=None):
            is_issue_page=1
        else:
            is_issue_page=0

        return is_issue_page

    # Check Rule 1
    def checkRule1(self, pathname, keywords, fname):
        found=0

        term1 = 'issue'
        term2 = 'issues'
        if (term1 in keywords) or (term2 in keywords):
            is_issue_list = self.is_issue_page(pathname)
            if is_issue_list==1:
                return 1

        # Create the Alltext.txt file
        P.get_text_local(pathname)
        if len(keywords)==0:
            #print(keywords)
            return 1

        with open(fname) as f:
            text = f.read()
            about_doc = nlp(text)

            for keyword in keywords:
                #print(keyword)
                sentences = []
                if(any(keyword in line for line in text.splitlines()))==False:
                    continue
                else:
                    if(len(keywords)==1):
                        found=1
                        return found

                    custom_nlp = spacy.load('en_core_web_sm')
                    custom_nlp.add_pipe(set_custom_boundaries, before='parser')
                    about_doc = custom_nlp(text)
                    sents = list(about_doc.sents)

                    for sent in sents:
                        s = str(sent)
                        s = re.sub('\n', ' ', s)
                        if keyword in s:
                            sentences.append(s)

                    if(len(sentences))>0:
            # #             #3.Find the subtree of the keyword in each sentence
                        for sentence in sentences:
                            sentence = str(sentence)
                            # print(sentence)
                            one_sentence = nlp(sentence)
                            pos = self.index_of_keyword(keyword, sentence)
                            if(pos!=None):
                                subtree = list(one_sentence[pos].subtree)
                                for word in keywords:
                                    # print(sentence)
                                    # print(keyword, "keyword")
                                    # print(subtree)
                                    if ((word!=keyword)):
                                        for x in subtree:
                                            #print(word)
                                            # print("Subtree word:", x)
                                            if (self.check_if_equal(word, x)==1):
                                                # print("found:", x, "in subtree of:", keyword, subtree)
                                                return 1
        return found

    # Check Rule 2
    def checkRule2(self, pathname, row, filename):
        found = 0
        # looking at the before action words
        action_words=[]
        action = G.before_action(row-1, filename)
        # pathname_1 = G.before_pathname(row-1)
        action = nlp(action)

        DOM_words = ['window', 'document', 'header', 'form', 'link', 'field', 'tab', 'button', 'checkbox', 'data', 'information', 'icon']
        #Getting nouns from before action
        for token in action:
            if (token.pos_ == 'NOUN') and (str(token) not in DOM_words): #or token.pos_ == 'ADJ'
               action_words.append(token.text)

        # print(action_words, len(action_words))
        #If word is issue, it only checks for issue lists
        term1 = 'issue'
        term2 = 'issues'
        # print(action_words)
        if (term1 in action_words) or (term2 in action_words):
            is_issue_list = self.is_issue_page(pathname)
            if is_issue_list==1:
                # print("returning 0")
                return 0

        #checking if keyword is a link
        a = str(action_words)
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', a)
        if (len(links)>0):
            return 1

        #if all the link words found on the next webpage, then good

        P.get_text_local(pathname)
        with open('Alltext.txt') as f:
            text = f.read()
            about_doc = nlp(text)

            for keyword in action_words:
                # if self.word_in_linklabel(pathname_1, keyword)==1:
                    # link_label_words+= 1
                if(any(keyword in line for line in text.splitlines()))==True:
                    found+= 1

        #print(action_words)
        if found==len(action_words):
            return 0
        else:
            return 1

    def check_if_equal(self, word, descendant):
        # print("types in func")
        # print(type(word), "for", word, type(descendant), "for", descendant, "\n")
        word = str(word)
        descendant = str(descendant)
        if word.lower() == descendant.lower():
            return 1
        else:
            return 0

    # Check Rule 3
    def checkRule3(self, pathname):
        res = 0
        P.link_labels(pathname)
        with open("Alllinklabels.txt", "r") as f:
            lines = f.readlines()
        with open("Alllinklabels.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != "None":
                    f.write(line)
        with open("Alllinklabels.txt") as file:
                        urls = file.read()
                        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', urls)
            #if len(links)>0:
            #    print(links)
                        res = len(links)

        return res

    def getFirstPageLabeledIssue(self, username, reponame, labelparam):
        gh = GitHub(userName, token)
        #open_labeled_issue = []
        
        # getting the project name
        projectName = username + '/' + reponame
        # get request fo both the open issues and open pull requests
        issues = gh.get("repos/"+ projectName + "/issues/", params={"state": "open", "labels": labelparam})
        pulls = gh.get("repos/" + projectName + "/pulls/", params={"state": "open"})
        
        # create a panda dataframe for the open issues 
        issue_id = []
        issue_url = []
        issue_label = []
        for issue in issues:
                issue_id.append(issue['title'])
                issue_url.append(issue['url'])
                issueLabel = issue["labels"]
                issue_label.append(issue['labels'])
        open_issue_DF = pd.DataFrame({"issue_id": issue_id, "issue_url":issue_url , "label":issue_label})
    
        # create a panda dataframe for the open PRs 
        pr_issue_url = []
        pr_id = []
        for pull in pulls:
                pr_id.append(pull['id'])
                pr_issue_url.append(pull['issue_url'])
        PR_issues_DF = pd.DataFrame({"pr_id": pr_id ,"issue_url":pr_issue_url})
    
       
        open_issues_openPR_merge = open_issue_DF.merge(PR_issues_DF, on = ['issue_url'], how = 'outer')
         # get all issues that are not linked to a PR 
        open_issue_notPR = open_issues_openPR_merge[open_issues_openPR_merge['pr_id'].isnull()]
        open_issue_notPR = open_issue_notPR.reset_index()
        # get the first 25 issues that are not linked to a pr <=> the first page of issues on github
        first25_open_issue_notPR = open_issue_notPR.head(n=25)
    
        #open_issue_notPR
        #open_issue_notPR[open_issue_notPR['label'].str.len()>0]
        # get the subset of labeled issues from the list of 25 issues 
        first25_open_labeled_issue = first25_open_issue_notPR[first25_open_issue_notPR.astype(str)['label'] != '[]']
        #rule 6: 
        # loop through all first25_open_labeled_issue append issue labels in a list of issue 
        # intersection between the above list and a newcomer label list 
        # if intersection not empty then Rule 6 not violated
        result = first25_open_labeled_issue
        return result

    # Check Rule 4
    def checkRule4(self, url):
        result_5 = -999    
        flat_labels_list_first25= []
        # print(url)
        lastUrlString = url.split('/')[-1]
        # print("url:", url)
        # print("lastUrlString:", lastUrlString)
        secondToLastUrl = url.split('/')[-2]
        df = pd.read_excel (r'newcomer_labels.xlsx')
        # print (df)
        newcomers_labels = df["newcomer_labels"].to_list()

        #if the url goes to the issues list with no additional parameters
        if (lastUrlString == "issues"):
            # print('ends in "issues" Rule5')
            reponame = url.split('/')[-2]
            # print('reponame: ', reponame)
            username = url.split('/')[-3]
            # print('username: ', username)
            first25_open_labeled_issue = self.getFirstPageLabeledIssue(username, reponame, "")
            # print('first25_open_labeled_issue: ', first25_open_labeled_issue)
            result_5 = len(first25_open_labeled_issue)

        # For a URL that is an issue list with additional parameters
        # This only works when using labels as the only parameters
        # This works incorrectly when username or other parameters are used - it acts like the URL is the plain URL with no additional parameters --Catherine S July 8 2020
        elif(lastUrlString.startswith("issues")):
            # print('ends with issues then more Rule5')
            reponame = url.split('/')[-2]
            # print('reponame: ', reponame)

            username = url.split('/')[-3]
            # print('username: ', username)

            #getting the list of parameters from url
            parsed = urlparse.urlparse(url)
            url_params = parse_qs(parsed.query)['q'][0]

            list_url_params = shlex.split(url_params)
            #print(list_url_params)
            label_filters = ""

            for param in list_url_params:
                if (param.startswith("label:")):
                    before_keyword, keyword, after_keyword = param.partition("label:")
                    if (label_filters == ""):
                        label_filters = label_filters + (after_keyword)
                    else:
                        label_filters = label_filters +  "," + (after_keyword)

            first25_open_labeled_issue = self.getFirstPageLabeledIssue(username, reponame, label_filters)
            result_5 = len(first25_open_labeled_issue)

        elif (secondToLastUrl == "labels"):
            # print('ends with "labels" Rule5')
            reponame = url.split('/')[-3]
            username = url.split('/')[-4]
            label_filter = unquote(lastUrlString)
            first25_open_labeled_issue = self.getFirstPageLabeledIssue(username, reponame, label_filter)
            result_5 = len(first25_open_labeled_issue)

        return result_5

    # Check Rule 5
    def checkRule5(self,url):
        result_6 = -999
        flat_labels_list_first25 = []
        # print(url)
        lastUrlString = url.split('/')[-1]
        secondToLastUrl = url.split('/')[-2]
        df = pd.read_excel(r'newcomer_labels.xlsx')
        # print (df)
        newcomers_labels = df["newcomer_labels"].to_list()

        # For a URL that is an issue list with no additional parameters
        if (lastUrlString == "issues"):
            # print('ends with /issues Rule6')
            reponame = url.split('/')[-2]
            # print('reponame: ', reponame)

            username = url.split('/')[-3]
            first25_open_labeled_issue = self.getFirstPageLabeledIssue(username, reponame, '')

            labels_series_first25 = first25_open_labeled_issue.label
            labels_as_list = labels_series_first25.tolist()

            # i is an issue with labels
            for i in range(len(labels_as_list)):
                # print ("type ", type(labels_series_first25[i]))
                # j is each label within an issue
                for j in range(len(labels_as_list[i])):
                    flat_labels_list_first25.append(labels_as_list[i][j]['name'])

            result_6 = len(intersection(flat_labels_list_first25, newcomers_labels))

        # For a URL that is an issue list with additional parameters
        # This only works when using labels as the only parameters
        # This works incorrectly when username or other parameters are used - it acts like the URL is the plain URL with no additional parameters --Catherine S July 8 2020
        elif (lastUrlString.startswith("issues")):
            # print('ends with /issues then more Rule6')
            reponame = url.split('/')[-2]
            # print('reponame: ', reponame)

            username = url.split('/')[-3]
            # print('username: ', username)

            # getting the list of parameters from url
            parsed = urlparse.urlparse(url)
            url_params = parse_qs(parsed.query)['q'][0]

            list_url_params = shlex.split(url_params)
            label_filters = ""

            for param in list_url_params:
                if (param.startswith("label:")):
                    before_keyword, keyword, after_keyword = param.partition("label:")
                    if (label_filters == ""):
                        label_filters = label_filters + (after_keyword)
                    else:
                        label_filters = label_filters + "," + (after_keyword)

            first25_open_labeled_issue = self.getFirstPageLabeledIssue(username, reponame, label_filters)

            # start of rule 6
            labels_series_first25 = first25_open_labeled_issue.label
            # print(labels_series_first25)
            labels_as_list = labels_series_first25.tolist()

            # i is an issue with labels
            for i in range(len(labels_as_list)):
                # j is each label within an issue
                for j in range(len(labels_as_list[i])):
                    flat_labels_list_first25.append(labels_as_list[i][j]['name'])
            result_6 = len(intersection(flat_labels_list_first25, newcomers_labels))

        # reset result_6 since the spreadsheet code will look for -999
        if result_6 == None:
            result_6 = -999
        return result_6
        

    def index_of_keyword(self, keyword, sentence):
        one_sentence = nlp(sentence)
        for token in one_sentence:
            if(self.check_if_equal(keyword, token.text)==1):
                return token.i

    def word_in_linklabel(self, pathname, word):
        found = 0
        P.link_labels(pathname)
        #print(keywords)
        with open("Alllinklabels.txt") as f2:
            labels = f2.read()
            if word in labels:
                return 1
            else:
                return 0


       # term = 'issue'
    # words = subgoal.split()
    # if term in words:
    #     #print(words)
    #     issue_page = C.issue_page(pathname)
    #     #print(issue_page) 
    #     if (issue_page==1):
    #         #print("OK")
    #         sheet.cell(row+1, 8).value = 0
    #         workbook.save('ID_Input.xlsx')
    #         continue

def set_custom_boundaries(doc):
# Adds support to use `...` as the delimiter for sentence detection
    for token in doc[:-1]:
        if token.text == '\n':
            doc[token.i+1].is_sent_start = True
    return doc

def intersection(lst1, lst2): 
        lst3 = [value for value in lst1 if value in lst2] 
        return lst3

