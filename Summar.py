import sys
import bs4 as bs
import urllib.request
import re
import nltk
import heapq

arg = len(sys.argv)
	
if arg == 3 :

	link = sys.argv[1]
	n = int(sys.argv[2])
	scraped_data = urllib.request.urlopen(link)
	article = scraped_data.read()

	parsed_article = bs.BeautifulSoup(article,'lxml')

	paragraphs = parsed_article.find_all('p')

	article_text = ""

	for p in paragraphs:
	    article_text += p.text
	# Sub numpers, white Spaces and new lines
	article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
	article_text = re.sub(r'\s+', ' ', article_text)

	# Sub non alphapets, white Spaces and new lines
	formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
	formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

	sentence_list = nltk.sent_tokenize(article_text)

	stopwords = nltk.corpus.stopwords.words('english')

	word_frequencies = {}
	for word in nltk.word_tokenize(formatted_article_text):
	    if word not in stopwords:
	        if word not in word_frequencies.keys():
	            word_frequencies[word] = 1
	        else:
	            word_frequencies[word] += 1

	maximum_frequncy = max(word_frequencies.values())

	for word in word_frequencies.keys():
	    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

	sentence_scores = {}
	for sent in sentence_list:
	    for word in nltk.word_tokenize(sent.lower()):
	        if word in word_frequencies.keys():
	            if len(sent.split(' ')) < 30:
	                if sent not in sentence_scores.keys():
	                    sentence_scores[sent] = word_frequencies[word]
	                else:
	                    sentence_scores[sent] += word_frequencies[word]


	summary_sentences = heapq.nlargest(n, sentence_scores, key=sentence_scores.get)

	summary = ' '.join(summary_sentences)
	print(summary)                   
else:
	print("[usage]:Please give a link to the article needed to be Summarized and number of sentences of the output")
	print("python summar.py http:examble.com 7")