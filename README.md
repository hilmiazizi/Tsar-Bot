# Update Regarding Twitter New Policy
### Due to new twitter policy, it seems like nitter has much problem going on and being not reliable to use for this bot. Thats policy mark the end of this bot, buying twitter API is not viable options. Therefore, i will archive this repo in hope that twitter will reverse its decision. I will revive this bot if there any options available.
<br>
<br>
<br>
<br>

## Tsar Bot - Crypto Sentiment Bot
![](https://i.ibb.co/3vfVwXs/asd.jpg)

Tsar Bot is a Twitter Crypto Sentiment Bot that have ability to make a trade based on influencers tweets. This bot using a project called [Nitter](https://github.com/zedeus/nitter "Nitter") - an twitter like website as a source to scrape twitter without any limit. For decision making, this bot using Vader Lexicon via NLTK to rate tweets polarity.

# Installation
#### 1. Nim Installation


    apt -y install build-essential libsass-dev redis python3-pip tmux
    curl https://nim-lang.org/choosenim/init.sh -sSf | sh
    export PATH=/root/.nimble/bin:$PATH

#### 2. Nitter Installation
In this step, nitter will be installed using tmux session manager to keep it running. Nitter will run on yourIP:8080 as your endpoint


    git clone https://github.com/hilmiazizi/nitter.git
    cd nitter
    nimble build -d:release
    nimble scss
    nimble md
    cp nitter.example.conf nitter.conf
    tmux
    ./nitter
    
#### 3. Binance Api Installation
Official Binance python module have a bug on cancel order so you need to install the module from my fork repository.


    git clone https://github.com/hilmiazizi/binance-futures-connector-python.git
    cd binance-futures-connector-python
    python3 setup.py install
    cd ../ && rm -rf binan*
    
#### 4. Bot Installation
Install required module:


    pip3 install bs4 pytz vaderSentiment nltk colorama

Install Vader Lexicon:
```bash
python3
import nltk
nltk.download('vader_lexicon')
```
# Informations
- This bot only allow you to use default leverage and margin type on your account
- This bot use Trailing Stop on take profit so it will take profit as high as it can as long as the coin keep pumping
- This bot use ROE percentage on SL/TP setting, 50 mean the bot will take profit 50% ROE
- Whitelist mean the bot will buy if the whitelisted users tweets a picture with less than 3 words, you can see [0xd0n](https://twitter.com/0xd0n/status/1483795095451324422 "0xd0n") tweets for reference
- You can configure keywords on lib/Sentiment.py
- Default trailing stop callback is 0.2%, you can change it on lib/MoneyMachine.py
- You can set TP/SL to 0 if you dont want to have TP/SL
- Dont forget to enable Futures while making API on binance
- Please use Nitter version from specific commit that i  have mentioned
- Fill endpoint with Nitter url that you've deployed before

# Disclaimer
I'm not responsible for any loss from trade taken by this bot. Run this bot with caution

# Get in touch & Donation


    This is a free & open source program but you can show some support here:
    BEP20 - 0xc7083befcde51fb2ab76f3a5d50f5ae27a4083bd
You can get in touch with me on twitter [@monkasalami](https://twitter.com/monkasalami "@monkasalami").

