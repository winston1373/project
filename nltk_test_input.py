# -*- coding: utf-8 -*-
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
mport requests       #引入requests模組
from lxml import etree

def max_key(dic):
    val = list(dic.values())
    keys = list(dic.keys())  

    return keys[val.index(max(val))]


def options_type(options):
	options_counts= {}
	for word in options:
		word_counts = {}
		for synset in wn.synsets(word):
			word_type = synset.lexname().split('.')[0]
			if word_type not in word_counts:
				word_counts[word_type] = 1
			else:
				word_counts[word_type] +=1

		
		# print(word, word_counts)
		word_type = max_key(word_counts)

		if word_type not in options_counts:
				options_counts[word_type] = 1
		else:
			options_counts[word_type] +=1

	return max_key(options_counts).upper()


def find_index(forward_index, backward_index, find_type, back=True, forward=True):
	backward_move = back
	forward_move = forward
	type_index = -1
	while(forward_index >= 0 or backward_index < len(a)):

			if (forward_index >= 0 and 
				forward_move == True
				):
				if(a[forward_index][0] in MARKS):
					forward_move = False
				if a[forward_index][1] == find_type:
					# print("f",a[forward_index])
					type_index = forward_index
					break;

			if (backward_index < len(a)
				and backward_move == True
				):
				if(a[backward_index][0] in MARKS):
					backward_move = False
				if (a[backward_index][1] == find_type):
					# print("b",a[backward_index])
					type_index = backward_index
					break
			forward_index = forward_index - 1 
			backward_index = backward_index + 1

	return type_index


def substring(first, last):
	substring = ""
	for i in range(first, last+1, 1):
		if i == last :
			substring += a[i][0]
			break
		substring += a[i][0] + " " 
	return substring


def google_search(string, choice):
    
    key = string.split()
    # key=['dangerous','object']

    key_added='+'.join(key)
    #print(key_added)
    url = f"https://www.google.com/search?hl=en&q={key_added}"

    # print("input your choice:")      #choice=0or1  0為一般搜尋 1為進階搜尋
    # choice = int(input())
    #print("%d" %choice )


    #用GET下載網頁
    #一般搜尋
    if choice == 0:
        url = f"https://www.google.com/search?hl=en&q={key_added}"
        #print(url)
    #進階搜尋
    elif choice == 1:
        url = f"https://www.google.com/search?hl=en&q=\"{key_added}\"&oq=\"{key_added}\""
        #print(url)
    #錯誤輸入
    else:
        print("Wrong input")

    #if同時有一般也有進階 eat "apple pie"


    #加上user agent讓網頁識別身分
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }

    response = requests.get(url, headers=headers)

    html = response.text
    page = etree.HTML(html)
    result = 0
    if html.find("did not match any documents") > 0 or html.find("No results found for") > 0:
        # print("0 result")
        result = 0

    else:
        #print(page.xpath(u'//*[@id="result-stats"]/text()'))
        
        #print(response.status_code)       #伺服器回應的狀態碼

        result=page.xpath(u'//*[@id="result-stats"]/text()')
        result="".join(result)     #List to string
        result=result.split(" ")
        # print(result[1])
        result = int(result[1].replace(',',''))

    return result



string = input("string:")
blank = "_____"
n_options = int(input("Number of options:"))
options = []


for i in range(n_options):
	temp = input(str(i+1) + ":")
	options.append(temp)


search_string = ""
a = pos_tag(word_tokenize(string), tagset='universal')
target_index = -1
for i in range(len(a)):
	if a[i][0] == blank:
		target_index = i
		break
if target_index == -1:
	print("blank does not match")


target_type = options_type(options)
print("type:", target_type)
a[target_index] = (blank, target_type)

forward_index = target_index-1
backward_index = target_index+1

VERB_index = target_index
NOUN_index = target_index
ADJ_index = target_index
MARKS = [',', '.', ';']
BeVERB = ['is', 'am', 'are', 'was', 'were']




if a[target_index][1] == 'ADJ':
	VERB_index = find_index(forward_index, backward_index, 'VERB')
	if VERB_index < target_index:
		if a[VERB_index][0] in BeVERB:
			NOUN_index = find_index(forward_index, backward_index, 'NOUN', back=False)
			search_string = substring(NOUN_index, target_index)
		else:
			NOUN_index = find_index(forward_index, backward_index, 'NOUN', forward=False)
			search_string = substring(VERB_index, NOUN_index)
			

	else:
		search_string = substring(target_index, VERB_index)


elif a[target_index][1] == 'NOUN':
	
	VERB_index = find_index(forward_index, backward_index, 'VERB')
	if VERB_index < target_index :
		search_string = substring(VERB_index, target_index)
	else:
		ADJ_index = find_index(target_index, backward_index, 'ADJ', back=False)
		# print(ADJ_index)
		if(ADJ_index != -1):
			search_string = substring(ADJ_index, VERB_index)
		else:
			search_string = substring(target_index, VERB_index)	
		

elif a[target_index][1] == 'VERB':
	
	NOUN_index = find_index(forward_index, backward_index, 'NOUN', forward=False)
	if NOUN_index == -1:
		NOUN_index = find_index(forward_index, backward_index, 'NOUN', back=False)

	if NOUN_index < target_index :
		search_string = substring(NOUN_index, target_index)
	else:
		search_string = substring(target_index, NOUN_index)	

elif a[target_index][1] == 'ADV':
	if (a[target_index+1][1] == 'VERB'):
		backward_index += 1

		NOUN_index = find_index(forward_index, backward_index, 'NOUN', forward=False)
		if NOUN_index == -1:
			NOUN_index = find_index(forward_index, backward_index, 'NOUN', back=False)

		if NOUN_index < target_index :
			search_string = substring(NOUN_index, target_index+1)
		else:
			search_string = substring(target_index, NOUN_index)	
	elif (a[target_index-1][1] == 'VERB'):
		backward_index += 1

		NOUN_index = find_index(forward_index, backward_index, 'NOUN', forward=False)
		if NOUN_index == -1:
			NOUN_index = find_index(forward_index, backward_index, 'NOUN', back=False)

		if NOUN_index < target_index :
			search_string = substring(NOUN_index, target_index)
		else:
			search_string = substring(target_index-1, NOUN_index)	


options_string = []
for i in range(n_options):
	options_string.append(search_string.replace(blank, options[i]))
print(search_string)
print(options_string)	
print()
print(a)
