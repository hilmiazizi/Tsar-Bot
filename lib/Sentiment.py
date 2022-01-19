from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def WordDetect(sentence):
	pos1 = ["v recovery","extreme volatility","added some","price discovery","under valued","under value","look strongs","ATH retest","fast recovery","trend flip"]
	pos2 = ["incentive program"]
	pos3 = ["to the moon","to the mooon","to the moooon","perfect retest","squeezes up","short squeeze","long squeeze","beras liquidated","bear liquidated","strongest coin"]
	negative = ["@delta_exchange","shitcoin","doordash","under resistance","below resistance","under resist","below resist"]
	score = 0.0

	for line in pos1:
		if line in sentence:
			score = score+0.1
	for line in pos2:
		if line in sentence:
			score = score+0.2
	for line in pos3:
		if line in sentence:
			score = score+0.3

	for line in negative:
		if line in sentence:
			score = score-0.2
	return score


def Sentiment(sentence):
	additional_score = WordDetect(sentence)
	sentence = sentence.lower()
	analyzer = SentimentIntensityAnalyzer()
	keyword = {
			"invalidation":-1,
			"indavlid": -1,
			"added":1,
			"bear":-1,
			"bearish":-1,
			"bull":1,
			"bullish":1,
			"launch ":1,
			"launching":1,
			"momentum ":1,
			"bought":1,
			"bottom":1,
			"project":1,
			"sauce":1,
			"entered":1,
			"volume ":1,
			"reversal":1,
			"buy":1,
			"buying":1,
			"sell":1,
			"selling ":1,
			"lfg":1,
			"failed":-1,
			"doordash":-10,
			"oversold":1,
			"drop": -1,
			"drops": -2,
			"bags":1,
			"baggs":1,
			"bag":1,
			"perfect":1,
			"hold":1,
			"holding":1,
			"dip":1,
			"long":1,
			"longed":1,
			"shorted ":-1,
			"ready":1,
			"rocket":1,
			"fire ":1,
			"mooonsir":1,
			"moon":1,
			"mooon":1,
			"moooon":1,
			"pew ":1,
			"adding":1,
			"tp":1,
			"bye ":1,
			"pump":2,
			"pamp":2,
			"pumped":2,
			"up":1,
			"pumping":2,
			"parabolic":1,
			"move":1,
			"start":1,
			"started":1,
			"bounce":1,
			"uptrend":1,
			"breakout":1,
			"undervalue":1,
			"under-valued":1,
			"under-value":1,
			"unvervalued":1,
			"strong":1,
			"rotatoooors":1,
			"rotators":1,
			"rotator":1,
			"scooping":1,
			"scope":1,
			"carefull":-1,
			"cautious":-1,
			"caution":-1,
			"close":-1,
			"closed":-1,
			"parabolic":1
		}

	analyzer.lexicon.update(keyword)
	score = analyzer.polarity_scores(sentence)
	sentence = sentence.replace('\n',' ')
	return score['pos']-score['neg']+additional_score
