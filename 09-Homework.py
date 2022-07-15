#!/usr/bin/env python
# coding: utf-8

# In[3]:


# 10+ hours, 4 days, three rewatched lectures, and outside help (TA, library, interweb) I'm afraid I have to waive the white flag and admit defeat.

# No one to blame but me but I easily spent more time (and tears) on this assignment and have the least to show for it.


# In[5]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[ ]:


# Scrape the following into CSV files. Each one is broken up into multiple tiers – the more you scrape the tougher it is!
# Scrape https://www.congress.gov/members (Links to an external site.)
# Tier 1: Scrape their name and full profile URL
# Tier 2: Separate their state/party/etc into separate columns


# In[4]:


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}


# In[33]:


response = requests.get("https://www.congress.gov/members", headers=headers)
doc = BeautifulSoup(response.text)
doc


# In[41]:


elected = doc.select('.expanded')
rows = []

for elect in elected:
    # print("-----")
    row = {}
    # print(elect.text.strip())
    row['name'] = (elect.select_one('.result-heading').text.strip())
    row['url'] = ("https://www.congress.gov/") + (elect.select_one('a')['href'])
    row['state'] = (elect.select_one('.result-item span').text.strip())
    row['party'] = (elect.select('.result-item span')[2].text.strip())
    row['served'] = (elect.select_one('.member-served').text.strip())
    
    print(row)
    rows.append(row)


# In[42]:


import pandas as pd

df = pd.DataFrame(rows)
df


# In[ ]:


# Scrape https://www.marylandpublicschools.org/stateboard/Pages/Meetings-2018.aspx
# Tier 1: Scrape the date, URL to agenda, URL to board minutes
# Tier 2: Download agenda items to an "agendas" folder and board minutes to a "minutes" folder


# In[16]:


response = requests.get("https://www.marylandpublicschools.org/stateboard/Pages/Meetings-2018.aspx", headers=headers)
doc = BeautifulSoup(response.text)
doc


# In[27]:


links = doc.find_all("a",href=True)

for link in links:
    if link['href'].endswith(".pdf"):
        print(link['href'])


# In[54]:


links = doc.select('.mdgov_contentWrapper a')

for link in links:
    if link['href'].endswith(".pdf"):
        print(link['href'])


# In[52]:


import re


# In[155]:


minute_urls = []

minutes = doc.find_all("a")

for minute in minutes:  
    if "minutes" in minute['href']:
        minute_url = (("https://www.marylandpublicschools.org") + (minute['href']))
        minute_urls.append(minute_url)

minute_urls


# In[156]:


agenda_urls = []

agendas = doc.find_all("a")

for agenda in agendas:  
    if "agenda" in agenda['href']:
        agenda_url = (("https://www.marylandpublicschools.org") + (agenda['href']))
        agenda_urls.append(agenda_url)

agenda_urls


# In[157]:


file_content = '\n'.join(minute_urls)

with open("urls.txt", "w") as f:
    f.write(file_content)


# In[158]:


get_ipython().system('wget -i urls.txt')


# In[159]:


file_content = '\n'.join(agenda_urls)

with open("urls.txt", "w") as f:
    f.write(file_content)


# In[160]:


get_ipython().system('wget -i urls.txt')


# In[ ]:


#  Scrape http://www.nvmcsd.org/our-school-board/meetings/agendas
# Tier 1: Scrape the name of the link and the URL
# Tier 2: Add a column for the date (you'll need to manually edit some, probably [but using pandas!])
# Tier 3: Download the PDFs but name them after the date


# In[46]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[47]:


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}


# In[58]:


response = requests.get("https://nvmcsd.org/our-school-board/meetings/agendas", headers=headers)
doc = BeautifulSoup(response.text)
doc


# In[105]:


doc.select('.kt-accordion-panel-inner a').text.strip()


# In[57]:


links = doc.select('.kt-accordion-panel-inner a')

urls = []

for link in links:
    url = link['href']
    urls.append(url)
urls


# In[59]:


import pandas as pd
from urllib.parse import urlparse


# In[60]:


parts = urlparse(url)
parts


# In[61]:


directories = parts.path.strip('/').split('/')
print(directories)


# In[97]:


def url_parser(url):
    
    parts = urlparse(url)
    directories = parts.path.strip('/').split('/')
    queries = parts.query.strip('&').split('&')
    
    elements = {
        'scheme': parts.scheme,
        'netloc': parts.netloc,
        'path': parts.path,
        'params': parts.params,
        'query': parts.query,
        'fragment': parts.fragment,
        'directories': directories,
        'queries': queries,
    }
    
    return elements


# In[63]:


elements = url_parser(url)


# In[98]:


elements


# In[106]:


for url in urls:
    print(url_parser(url))
    print('--------')


# In[87]:


print(elements.keys())


# In[90]:


print(elements['directories'][2])


# In[92]:


years = (elements['directories'][2])
months = (elements['directories'][3])


# In[151]:


import pandas as pd

df = pd.DataFrame(urls)
pd.set_option('display.max_columns', None)
df


# In[152]:


df.columns = ['url']


# In[137]:


df.url


# In[156]:


# df.url.str.extract("Detail.aspx?id=(.*)&session=2021")
df['year month'] = df.url.str.extract("https://nvmcsd.wpengine.com/wp-content/uploads/(.*)/")
df


# In[ ]:


# Scrape https://rocktumbler.com/blog/rock-and-mineral-clubs/
# Tier 1: Scrape all of the name and city
# Tier 2: Scrape the name, city, and URL
# Tier 3: Scrape the name, city, URL, and state name (you'll probably need to learn about "parent" nodes)


# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}


# In[3]:


response = requests.get("https://rocktumbler.com/blog/rock-and-mineral-clubs/", headers=headers)
doc = BeautifulSoup(response.text)
doc


# In[14]:


cities = elected = doc.select('.font12 td')

for city in cities:
    print("-----")
    print(city.text.strip())


# In[29]:


cities = doc.select('.font12')

for city in cities:
    print("-----")
    print(city.select("td")[1].text.strip())

    try:
        print(city.select("td")[2].text.strip())
    except:
        print("Couldn't find a tag!")
    
    print(city.select_one('a')['href'])


# In[ ]:




