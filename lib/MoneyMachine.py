from binance.futures import Futures
import json
import time
import random
def getPositions(status=False):
	position_count = 0
	position_pair = []
	result = client.account()
	for position in result['positions']:
		if float(position['unrealizedProfit']) != 0.0:
			position_count+=1
			if status:
				position_pair.append(position['symbol'])
			else:
				position_pair.append([position['symbol'],position['entryPrice'],position['positionInitialMargin'],position['positionAmt']])
	if status:
		return position_pair
	else:
		return position_count,position_pair

def pricePrecision(ticker):
	result = client.exchange_info()
	for line in result['symbols']:
		if ticker == line['symbol']:
			return [line['quantityPrecision'],line['pricePrecision']]

def getPrice(ticker):
	coinPrice = client.ticker_price(symbol=ticker)  
	coinPrice = json.loads(str(coinPrice).replace("'",'"'))
	coinPrice = coinPrice["price"]
	return coinPrice

def MadeOrder(ticker,margin):
	try:
		price = getPrice(ticker)
		quantity = round(margin*20/float(price),pricePrecision(ticker)[0])
		params = {
			'symbol': ticker,
			'side': 'BUY',
			'type': 'MARKET',
			'quantity': quantity,
		}
		response = client.new_order(**params)
		return True,True
	except Exception as e:
		reason = str(e).split("', {'Content-Type")
		reason = reason[0].split(", '")
		reason = reason[1]
		return False,reason

def CheckPosition(ticker,max_pos):
	position_count,position = getPositions()
	if max_pos <= position_count:
		return False,"Max open positions reached"
	else:
		for line in position:
			if ticker == line[0]:
				return False,"Positions for ticker already exist"
		else:
			return True,True

def TrailingStop(ticker,entry,quantity,margin,tp_roe):
	move_percentage = tp_roe/20/100
	tp_price = round(((margin*20)/quantity)*move_percentage+entry,pricePrecision(ticker)[1])

	ClientID = 'Tsar_TP'+str(random.randint(0,99999))
	try:
		params = {
			'symbol': ticker,
			'side': 'SELL',
			'type': 'TRAILING_STOP_MARKET',
			'activationPrice': tp_price,
			'reduceOnly': 'True',
			'callbackRate': 0.2,
			'quantity': quantity,
			'newClientOrderId': ClientID
		}
		response = client.new_order(**params)
		return True
	except Exception as e:
		print("Error in TrailingStop()")
		print(str(e))

def StopLoss(ticker,entry,quantity,margin,sl_roe):
	move_percentage = sl_roe/20/100
	sl_price = entry-((((margin*20)/quantity)*move_percentage+entry)-entry)
	sl_price = round(sl_price, pricePrecision(ticker)[1])


	ClientID = 'Tsar_SL'+str(random.randint(0,99999))
	try:
		params = {
			'symbol': ticker,
			'side': 'SELL',
			'type': 'STOP_MARKET',
			'stopPrice': sl_price,
			'closePosition': 'True',
			'newClientOrderId': ClientID
		}
		response = client.new_order(**params)
		return True
	except Exception as e:
		print("Error in StopLoss()")
		StopLoss(ticker,entry,quantity,margin,sl_roe)



def FuckShow(coin,config):
	ticker = coin.upper()+"USDT"
	global client
	client = Futures(key=config['api'], secret=config['secret'])
	success,reason = CheckPosition(ticker,config['max_pos'])
	if success:
		status,reason = MadeOrder(ticker,config['margin'])
		if status:
			position_count,position = getPositions()
			for line in position:
				if ticker == line[0]:

					# SL/TP PART, DONT FUCKING TOUCH IT
					entry = float(line[1])
					margin = float(line[2])
					quantity = float(line[3])
					time.sleep(0.5)
					if config['tp_roe'] > 0:
						if not TrailingStop(ticker,entry,quantity,margin,float(config['tp_roe'])):
							print("Set TP Failed")
					time.sleep(0.5)
					if config['sl_roe'] > 0:
						if not StopLoss(ticker,entry,quantity,margin,float(config['sl_roe'])):
							print("Set SL Failed")

					return True,True,line[1]
		else:
			return False,reason,None
	else:
		return success,reason,None



def CancelOrders(ticker,orderId,clientOrderId):
	params = {
		'symbol': ticker,
		'orderId': int(orderId),
		'origClientOrderId': clientOrderId
	}
	result = client.cancel_order(**params)



def GetOrders(api,secret):
	global client
	client = Futures(key=api, secret=secret)
	current_position = getPositions(True)
	# Converting open order to list
	open_orders = client.get_orders()
	order_sorted = []
	for orders_data in open_orders:
		if 'Tsar' in orders_data['clientOrderId']:
			if orders_data['symbol'] not in current_position:
				CancelOrders(orders_data['symbol'],orders_data['orderId'],orders_data['clientOrderId'])

