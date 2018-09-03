import requests
import urllib.request
from lxml import html
#import re
import time

def rm_parenthesis(input):
  result = ''
  paren_level = 0
  last_ch = ''
  link = 0
  
  for ch in input:
    if last_ch == '<' and ch == 'a':
      link = 1
    elif link and ch == '>':
      link = 0
      
    if ch == '(' and not link:
      paren_level += 1
    elif (ch == ')') and paren_level and not link:
      paren_level -= 1
    elif not paren_level:
      result += ch
      
    last_ch = ch
  return result

def rm_table(input):
  result = ''
  table_level = 0
  
  for ch in input:
    if ch == '<table':
      table_level += 1
    elif (ch == '</table>') and table_level:
      table_level -= 1
    elif not table_level:
      result += ch
  return result

url = "https://en.wikipedia.org"

while True:
  article =  input("Please input wikipedia article name: ")
  page = "/wiki/" + article
  request = requests.get(url + page)
  if request.status_code != 200:
    continue
  break
  
peges_visit = [page]

while True:
  # get page source code
  response = urllib.request.urlopen(url+page).read().decode()
  
  # remove parentheses  
  response = rm_parenthesis(response)
  
  #remove tables
  response = rm_table(response)
  
  
  # get links in main content
  tree = html.fromstring(response)
  links = tree.xpath('//div[@class="mw-parser-output"]/p/a')
  
  if len(links) == 0:
    print('There is no link in this article!')
    print(page + "\n\n")
    list(map(print, peges_visit)) 
    break
  
  for link in links:
    #get parent
    parent = link.getparent()
    if len(parent.xpath('@id')) == 0 and len(parent.xpath('@class')) == 0:
      page = link.xpath('@href')[0]
      break
    
  #check if it stuck in loop
  if page in peges_visit:
    print('Stuck in Loop!')
    print(page + "\n\n")
    list(map(print, peges_visit)) 
    break
  
  # add page to visited page list
  peges_visit.append(page)
     
  #check if page is "Philosophy"
  if page == "/wiki/Philosophy":
    list(map(print, peges_visit)) 
    break
  
  time.sleep(0.5)

