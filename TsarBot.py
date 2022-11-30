import requests
import os
import time
import random
import re
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import Fore, Style, init
import json
import pytz
import traceback
from binance.futures import Futures

# NLTK MODULE
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Local Module
from lib.MoneyMachine import GetOrders, FuckShow
from lib.Sentiment import Sentiment

def Banner(config):
    api = config['api']
    api = api[:4]+"****"+api[-4:]
    secret = config['secret']
    secret = secret[:4]+"****"+secret[-4:]
    max_pos = str(config['max_pos'])
    margin = str(config['margin'])


    init(autoreset=True)
    print(Fore.WHITE+Style.BRIGHT+'        .---.\t    '+Fore.WHITE+'\t\t'+Style.BRIGHT+Fore.GREEN+' Tsar Bot')
    print(Fore.WHITE+Style.BRIGHT+'       /     \\\t    '+Fore.WHITE+' '+Style.BRIGHT+Fore.WHITE+'      Crypto Sentiment Bot')
    print(Fore.WHITE+Style.BRIGHT+'       \\.'+Fore.RED+'@'+Fore.WHITE+'-'+Fore.RED+'@'+Fore.WHITE+'./\t    '+Fore.WHITE+'')
    print(Fore.WHITE+Style.BRIGHT+'       /`'+Fore.YELLOW+'\\_/'+Fore.WHITE+'`\\\t    '+Fore.WHITE+'')
    print(Fore.WHITE+Style.BRIGHT+'      //  _  \\\\\t    '+Fore.WHITE+''+Fore.YELLOW+'   Api\t      '+Fore.WHITE+': '+api)
    print(Fore.WHITE+Style.BRIGHT+'     | \\     )|_    '+Fore.WHITE+''+Fore.YELLOW+'   Secret\t      '+Fore.WHITE+': '+secret)
    print(Fore.WHITE+Style.BRIGHT+'    /`\\_`>  <_/ \\   '+Fore.WHITE+''+Fore.YELLOW+'   Max Positions  '+Fore.WHITE+': '+max_pos)
    print(Fore.WHITE+Style.BRIGHT+"    \\__/'---'\\__/   "+Fore.WHITE+""+Fore.YELLOW+"   Margin\t      "+Fore.WHITE+': $'+margin)
    print('\n\n         It is end user full responsibility for\n       any loss from any trade taken by this bot')
    print('   '+'_'*50+"\n\n")

def CurrentTime():
	config = open('config.json').read()
	config = json.loads(config)
	tz_target = pytz.timezone(config['timezone'])
	now = datetime.now(tz_target)
	now = now.strftime('%d/%m/%Y %H:%M:%S')
	return str(now)

def Scrape(username, endpoint):
	headers = {
	    'Host': endpoint,
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Accept-Encoding': 'gzip, deflate',
	    'Upgrade-Insecure-Requests': '1',
	    'Sec-Fetch-Dest': 'document',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-Site': 'none',
	    'Sec-Fetch-User': '?1',
	    'Te': 'trailers',
	    'Connection': 'close',
	}

	try:
		response = requests.get('http://'+endpoint+'/'+username, headers=headers, verify=False)
		if ' UTC">' in response.text:
			Scrape(username,endpoint)
		elif '<div class="tweet-stats">' in response.text:
			return response.text
		else:
			Scrape(username,endpoint)
	except Exception as e:
		Scrape(username,endpoint)
	
	

def Cleaner(tweet_content):
	tweet_content = tweet_content.lower()
	avoid_word = ["$one","$hot","$link","$near","$keep","$ar","$alpha","$ocean","$audio","$omg","$etc",'$ray']
	sentence = ''
	for line in tweet_content.split():
		if line.lower() not in avoid_word:
			sentence = sentence+line.replace('$','')+" "
		else:
			sentence = sentence+line+" "
	tweet_content = sentence.lower()
	tweet_content = tweet_content.replace('/','')
	tweet_content = tweet_content.replace(',',' ')
	tweet_content = tweet_content.replace('#','')
	tweet_content = tweet_content.replace('.',' ')
	tweet_content = tweet_content.replace('\n','  ')
	tweet_content = tweet_content.replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')
	tweet_content = tweet_content.replace(' shib ',' 1000shib ')
	tweet_content = tweet_content.replace(' shiba ',' 1000shib ')
	tweet_content = EmoticonReplace(tweet_content)
	return tweet_content


def EmoticonReplace(sentence):
	sentence = sentence.replace('\n',' ')
	sentence = sentence.replace(',',' ')
	sentence = sentence.replace('!',' ')
	sentence = sentence.replace('👀',' eyes ')
	sentence = sentence.replace('🚀',' rocket ')
	sentence = sentence.replace('🤝',' handshake ')
	sentence = sentence.replace('🌖',' moonsir ')
	sentence = sentence.replace('🌗',' moonsir ')
	sentence = sentence.replace('🌕',' moonsir ')
	sentence = sentence.replace('🌙',' moonsir ')
	sentence = sentence.replace('🌔',' moonsir ')
	sentence = sentence.replace('🌓',' moonsir ')
	sentence = sentence.replace('🌒',' moonsir ')
	sentence = sentence.replace('🌑',' moonsir ')
	sentence = sentence.replace('🌘',' moonsir ')
	sentence = sentence.replace('-','')
	sentence = sentence.replace('  ',' ').replace('  ',' ')
	return sentence


def Extractor(response):
	result = []
	soup = BeautifulSoup(response, 'html.parser')
	content = soup.find_all('div', class_='timeline-item')
	for datas in content:
		if "retweet-header" in str(datas):
			continue
		if "pinned" in str(datas):
			continue
		scraper = BeautifulSoup(str(datas), 'html.parser')
		tweet_content = scraper.find('div', class_='tweet-content media-body').get_text()
		tweet_content = Cleaner(tweet_content)

		#WL BUY
		if 'attachment image' in str(scraper):
			image = True
		else:
			image = False

		# EXTRACT LINKS & DATE
		for line in str(datas).splitlines():
			if "tweet-date" in line:
				tweet_link = re.search('href="(.*)" title=',line).group(1)
				tweet_time = re.search('title="(.*)">',line).group(1)
				break

		tweet_time = tweet_time.replace(',','')
		tweet_link = "https://twitter.com"+tweet_link
		result.append([tweet_content,tweet_time,tweet_link,image])

	
	return result[::-1]
	#return result
		
		


# array to store latest tweet for validation
latest_tweet =[]
def TimeValidator(tweet_time,username,tweet_content):
	username = username.lower()
	global latest_tweet
	tweet_time = datetime.strptime(tweet_time, '%d/%m/%Y %H:%M:%S')
	for line in latest_tweet:
		if username in line:
			if tweet_time > line[1]:
				fucker_index = latest_tweet.index(line)
				latest_tweet[fucker_index] = [username,tweet_time,tweet_content]
				#print("Match ->",tweet_content[:20])
				return True
			else:
				#print("Old ->", tweet_content[0:20])
				return False
	
	else:
		latest_tweet.append([username,tweet_time])
		#print("First ->",tweet_content[:20])
		return False

def PairExtractor(tweet_content):
	if "elon" in tweet_content:
		return None
	tweet_content = tweet_content.split()
	futurePair = ['bnb','sol','luna','dot','xrp','ada','axs','doge','sand','matic','ltc','$link','avax','1000shib','gala','mana','$near','eos','atom','xtz','ftm','$etc','fil','1inch','xlm','bch','btt','egld','sushi','uni','trx','algo','crv','lrc','aave','vet','theta','$omg','zec','tlm','rune','enj','srm','$one','chz','chr','sfp','blz','iota','grt','sxp','xmr','rsr','bat','qtum','celr','yfi','iotx','comp','bzrx','ksm','hnt','neo','mask','snx','ankr','c98','$keep','bal','dash','reef','ctk','waves','kava','$alpha','hbar','icx','storj','lina','bake','$ocean','$hot','coti','$audio','ren','dent','mkr','ont','ogn','stmx','iost','knc','zil','skl','cvc','band','ata','zrx','1000xec','bel','sc','xem','yfii','trb','tomo','rlc','rvn','flm','nkn','akro','dydx','bts','alice','mtl','dgb','gtc','$ray','zen','dodo','lit','unfi','icp','celo','$ar']
	known_pair = []
	for line in tweet_content:
		if line in futurePair:
			if line not in known_pair:
				known_pair.append(line)

	if len(known_pair) == 1:
		return known_pair[0].replace('$','')
	else:
		return None


def MoneyMaker(username, config, first=True):
	global source_list
	username = username.lower()
	scrape_result = Scrape(username,config['endpoint'])
	if scrape_result:
		result = Extractor(scrape_result)
		for line in result:
			tweet_content = line[0]
			tweet_time = line[1]
			tweet_link = line[2]
			tweet_image = line[3]
			time_check =  TimeValidator(tweet_time,username,tweet_content)
			if time_check and first:
				#print(username,'-> masok')
				pair = PairExtractor(tweet_content)
				

				# CHECK WHITELIST
				# Currently stand for 3 Words+image and 'foan'

				if pair:
					pair = pair.upper()
					for whitelist in config['whitelist']:
						whitelist = whitelist.lower()

						# CUSTOM FILTERS
						temp = tweet_content.split(' ')
						PairOnly = len(temp) < 4 and tweet_image
						FOAN = "foan" in tweet_content

						# END OF CUSTOM FILTERS	

						if username in whitelist:
							if PairOnly:
								status,reason,entry = FuckShow(pair,config)
								if status:
									print(OutputFormat("buy")+username+" -> "+Fore.CYAN+pair+Fore.WHITE+" | Entry : ",entry)
									write_format = CurrentTime()+","+username+","+pair+","+tweet_content.replace(',','.')+","+tweet_link+",WHITELISTED,BUY,None,"+entry+"\n"
									f = open('result.csv','a+')
									f.write(write_format)
									f.close()
									return


					score = Sentiment(tweet_content)
					if score >= 0.2:
						status,reason,entry = FuckShow(pair,config)
						if status:
							print(OutputFormat("buy")+username+" -> "+Fore.CYAN+pair+Fore.WHITE+" | Entry : ",entry)
							write_format = CurrentTime()+","+username+","+pair+","+tweet_content.replace(',','.')+","+tweet_link+","+str(score)+",BUY,None,"+entry+"\n"
							f = open('result.csv','a+')
							f.write(write_format)
							f.close()
						else:
							print(OutputFormat("no")+username+" -> "+Fore.CYAN+pair+Fore.WHITE+" | Reason: ",reason)
							write_format = CurrentTime()+","+username+","+pair+","+tweet_content.replace(',','.')+","+tweet_link+","+str(score)+",NO ACTION,"+reason+",None\n"
							f = open('result.csv','a+')
							f.write(write_format)
							f.close()
					else:
						print(OutputFormat("no")+username+" -> "+Fore.CYAN+pair+Fore.WHITE+" | Reason: No Sufficient Score")
						write_format = CurrentTime()+","+username+","+pair+","+tweet_content.replace(',','.')+","+tweet_link+","+str(score)+",NO ACTION,No Sufficient Score,None\n"
						f = open('result.csv','a+')
						f.write(write_format)
						f.close()


def OutputFormat(action):
	if action == "info":
		return Fore.WHITE+"["+Fore.CYAN+str(CurrentTime())+Fore.WHITE+"] ["+Fore.WHITE+"INFO"+Fore.WHITE+"] "+Style.RESET_ALL
	if action == "buy":
		return Fore.WHITE+"["+Fore.CYAN+str(CurrentTime())+Fore.WHITE+"] "+Fore.WHITE+"["+Fore.GREEN+"BUY"+Fore.WHITE+"] "+Style.RESET_ALL
	if action == "no":
		return Fore.WHITE+"["+Fore.CYAN+str(CurrentTime())+Fore.WHITE+"] "+Fore.WHITE+"["+Fore.YELLOW+"NO ACTION"+Fore.WHITE+"] "+Style.RESET_ALL
	if action == "warning":
		return Fore.WHITE+"["+Fore.CYAN+str(CurrentTime())+Fore.WHITE+"] "+Fore.WHITE+"["+Fore.RED+"WARNING"+Fore.WHITE+"] "+Style.RESET_ALL



init(autoreset=True)
os.system('clear')
config = open('config.json').read()
config = json.loads(config)
Banner(config)

source_list = open('source.txt').readlines()
print(OutputFormat("info")+"Gathering latest tweets", end='')
for i in range(0,3):
	for line in source_list:
		if line:
			MoneyMaker(line.rstrip(),config,False)
	print(" .",end='')
		


print('\n'+OutputFormat("info")+"Latest tweets recorded, waiting for new tweets")
if not os.path.isfile("result.csv"):
	f = open('result.csv','a+')
	f.write("TWEET TIME,USERNAME,PAIR,TWEET,TWEET LINK,SCORE,ACTION,REASON,ENTRY PRICE\n")
	f.close()
	
while True:
	config = open('config.json').read()
	config = json.loads(config)
	GetOrders(config['api'],config['secret'])
	source_list = open('source.txt').readlines()
	for username in source_list:
		username = username.rstrip()
		if username:
			try:
				MoneyMaker(username,config)
			except Exception as e:
				error = str(traceback.format_exc())
				f = open('log.txt','a+')
				f.write(error+"\n")
				f.close()
				print(OutputFormat("warning")+"Error detected, please submit issue with log.txt included")
				continue
