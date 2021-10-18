# import urllib3
# import urllib3.request
#import urllib.request, base64, urllib.error
# from urllib3.request import urlopen
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import ssl


class parseDOM():
	"""
	This class parses the HTML of a URL, to check it against keywords or newcomer-friendly issue labels.
	"""
	def __init__(self):
		super(parseDOM, self).__init__()
		#self.arg = arg
		#self.url = url



#Get the entire HTML code of the website

	def get_html(self, url):
	# url = 'https://github.com/kubernetes/kubernetes'
		# url = str(url)
		# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		# headers={'User-Agent':user_agent,}
		#request=urllib.request.Request(url,None,headers)
		# response = requests.get(url, headers=headers, verify=False)
		# response = urllib3.request.urlopen(url)
		r = requests.get(url)
		data = r.text

		f = open('current_html.html', 'w')
		f.write(data)
		f.close

	def get_text_from_url(self, url):
		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		headers={'User-Agent':user_agent,}
		response = requests.get(url, headers=headers, verify=False)
		# self.get_html(url)
		soup = BeautifulSoup(response.text, "lxml")
		for script in soup(["script", "style"]):
			script.extract()
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = '\n'.join(chunk for chunk in chunks if chunk)


        #print(soup.get_text())
		f=open('Alltext.txt','w')
		# All_Text_On_Page = soup.get_text()
		# All_Text_On_Page = All_Text_On_Page.lower()
		# f.write(All_Text_On_Page)
		f.write(text)
		f.close()


#Get all the text in the file which contains the HTML page

	# def get_text(self, url):
	# 	self.get_html(url)
	# 	soup = BeautifulSoup(open("htmlcode.txt"), 'html.parser')
	# 	#print(soup.get_text())
	# 	f=open('Alltext.txt','w')
	# 	All_Text_On_Page = soup.get_text()
	# 	All_Text_On_Page = All_Text_On_Page.lower()
	# 	f.write(All_Text_On_Page)
	# 	f.close()

	def tag_visible(self, element):
		if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
			return False
		if isinstance(element, Comment):
			return False
		if re.match(r"[\n]+",str(element)): return False
		return True

	def get_text_local(self, pathname):
		f = open(pathname)
		# print(pathname)
		soup = BeautifulSoup(f, 'html.parser')
		texts = soup.findAll(text=True)
		visible_texts = filter(self.tag_visible, texts)  
		text = u"\n".join(t.strip() for t in visible_texts)
		text = text.lstrip().rstrip()
		text = text.split(',')
		clean_text = ''
		for sen in text:
			if sen:
				sen = sen.rstrip().lstrip()
				clean_text += sen+','

		clean_text = clean_text.lower()

		f=open('Alltext.txt','w')
		f.write(clean_text)
		f.close()


		vis_text = [button.text for button in soup.select('button')]
		text = u"\n".join(t.strip() for t in vis_text)
		text = text.lstrip().rstrip()
		text = text.split(',')
		clean_text = ''
		for sen in text:
			if sen:
				sen = sen.rstrip().lstrip()
				clean_text += sen+','

		clean_text = clean_text.lower()

		f=open('Alltext.txt','a')
		f.write(clean_text)
		f.close()

		# f = open(pathname, encoding="utf8")     
		# soup = BeautifulSoup(f, 'html.parser')
		# f.close() 

		# f=open('Alltext.txt','w')
		# All_Text_On_Page = soup.get_text()
		# All_Text_On_Page = All_Text_On_Page.lower()
		# f.write(All_Text_On_Page)
		# f.close()

#Find all link-labels on the webpage
	# def link_labels_internet(self, url):
	# 	remove_element = "None"
	# 	self.get_html(url)
	# 	soup = BeautifulSoup(open("htmlcode.txt"), 'html.parser')
	# 	open("Alllinklabels.txt", "w").close()
	# 	table = soup.findAll('div',{'class':'f4'})
	# 	try:
	# 		for x in table:
	# 			remove_element = (x.find('a').text)
	# 	except AttributeError:
	# 		pass

	# 	f=open('Alllinklabels.txt','a')
	# 	All_LinkLabels = []
	# 	for link in soup.find_all('a'):
	# 		if self.check_if_equal(link.string, remove_element)==0:
	# 			All_LinkLabels.append(link.string)
	# 			f.write(str(link.string))
	# 			#print(link.string)
	# 			f.write('\n')

	def link_labels(self, pathname):
		remove_element = "None"
		#self.get_html(url)
		f = open(pathname, encoding="utf8", errors='ignore')     
		soup = BeautifulSoup(f, 'html.parser')
		open("Alllinklabels.txt", "w").close()
		table = soup.findAll('div',{'class':'f4'})
		try:
			for x in table:
				remove_element = (x.find('a').text)
		except AttributeError:
			pass

		f=open('Alllinklabels.txt','a')
		All_LinkLabels = []
		for link in soup.find_all('a'):
			if self.check_if_equal(link.string, remove_element)==0:
				All_LinkLabels.append(link.string)
				f.write(str(link.string))
				#print(link.string)
				f.write('\n')

	def check_if_equal(self, word, descendant):
        # print("types in func")
        # print(type(word), "for", word, type(descendant), "for", descendant, "\n")
								word = str(word)
								descendant = str(descendant)
								if word.lower() == descendant.lower():
									return 1
								else:
									return 0



