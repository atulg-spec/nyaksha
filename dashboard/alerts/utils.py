from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_list(plan_type):
    try:
        users = []
        ob = ""
        if 'FREE' in plan_type.upper():
            ob = User.objects.filter(plan_type='Free')
            for x in ob:
                users.append(x.email)
        if 'BASIC' in plan_type.upper():
            ob = User.objects.filter(plan_type='Basic')
            for x in ob:
                users.append(x.email)
        if 'PRO' in plan_type.upper():
            ob = User.objects.filter(plan_type='Pro')
            for x in ob:
                users.append(x.email)
        if 'VIP' in plan_type.upper():
            ob = User.objects.filter(plan_type='VIP')
            for x in ob:
                users.append(x.email)
        if 'PREMIUM' in plan_type.upper():
            ob = User.objects.filter(plan_type='Premium')
            for x in ob:
                users.append(x.email)
        return users
    except:
        return False


def present(user,syntax):
    plan_type = syntax['users']
    userlist = get_user_list(plan_type)
    if not userlist:
        return False
    if str(user) in userlist:
        return True
    else:
        return False


def is_suscribed(user):
    if user.is_suscribed:
        return True
    else:
        return False

def get_quantity(user,symbol):
    qty = 0
    if 'CRUDEOIL' in symbol:
        qty = user.crudeoil_quantity
    elif 'BANKNIFTY' in symbol:
        qty = user.bank_nifty_quantity
    elif 'FINNIFTY' in symbol:
        qty = user.fin_nifty_quantity
    elif 'NIFTY' in symbol:
        qty = user.nifty_quantity
    elif 'SENSEX' in symbol:
        qty = user.sensex_quantity
    elif 'BANKEX' in symbol:
        qty = user.bankex_quantity
    else:
        qty = user.default_quantity
    return qty