import html2text
import pickle as pkl
import nltk

#html = open('leaves-of-grass-clean.html')
#docs = html2text.html2text(html)
#docs = nltk.clean_html(html)

#print(doc[0])

from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()
url="https://whitmanarchive.org/published/books/other/rhys.html"
response = http.request('GET', url)
soup = BeautifulSoup(response.data, "html.parser")

result = soup.find(attrs={'class':'myclass'})
print ("The result of soup.find:")
print (result)

print ("\nresult.contents:")
print (result.contents)
print ("\nresult.get_text():")
print (result.get_text())
for r in result:
  if (r.string is None):
    r.string = ' '

print ("\nAfter replacing all the 'None' with ' ':")
print (result.get_text())
