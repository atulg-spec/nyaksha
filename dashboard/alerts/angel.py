from dashboard.alerts.utils import is_suscribed, present,get_quantity
from apis.models import angel_api
from dashboard.models import Response
from django.utils import timezone
import pyotp
try:
    from SmartApi import SmartConnect 
except:
    from smartapi import SmartConnect 


# --------------------ANGEL ONE API---------------------
def angel_order(syntax,json_data):
    print('angel one')
    apiob = angel_api.objects.filter(is_trading=True)
    for x in apiob:
        if not present(x.user,json_data[syntax]):
            continue
        if not is_suscribed(x.user):
            continue
        try:
            qty = get_quantity(x.user,json_data[syntax]["symbol"])
            qty = int(qty)
            orderid = ""
            obj = SmartConnect(x.api_key)
            try:
                token = x.t_otp_token
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                error = 'Invalid TOTP token'
                Response.objects.create(user=x.user,broker='Angel ONE',api_name=x.api_name,response=error,syntax_used=json_data[syntax])
                continue
            data = obj.generateSession(x.client_id, x.m_pin, totp)
            if data['status'] == False:
                error = 'Invalid Login Credentials'
                Response.objects.create(user=x.user,broker='Angel ONE',api_name=x.api_name,response=error,syntax_used=json_data[syntax])
                continue
            ptype = json_data[syntax]['ptype']
            if ptype == 'CNC':
                ptype = 'DELIVERY'
            elif ptype == 'NRML':
                ptype = 'CARRYFORWARD'
            orderParams = {
                "variety":json_data[syntax]['variety'],
                "tradingsymbol": json_data[syntax]['symbol'],
                "symboltoken": json_data[syntax]['token'],
                "transactiontype": json_data[syntax]['ttype'],
                "exchange": json_data[syntax]['segment'],
                "ordertype": json_data[syntax]['otype'],
                "producttype": ptype,
                "duration": "DAY",
                "price": json_data[syntax]['price'],
                "stoploss": json_data[syntax]['stoploss'],
                "stoploss": json_data[syntax]['target'],
                "quantity": qty
            }
            print(orderParams)
            authToken = data['data']['jwtToken']
            refreshToken = data['data']['refreshToken']
            feedToken = obj.getfeedToken()
            res = obj.getProfile(refreshToken)
            obj.generateToken(refreshToken)
            orderid=obj.placeOrder(orderParams)
            res = Response.objects.create(user=x.user,broker='Angel ONE',api_name=x.api_name,response=orderid,syntax_used=json_data[syntax])
            book = obj.orderBook()["data"]
            for i in book:
                if i["orderid"] == orderid:
                    res.response_2 = i
        except Exception as e:
            status="failed"
            error = f" Unexpected ERROR found: {e}"
            Response.objects.create(user=x.user,broker='Angel ONE',api_name=x.api_name,response=error,syntax_used=json_data[syntax])
    #-----------------END ANGEL ONE API------------------------------
