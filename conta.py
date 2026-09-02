saldo = 0 
def armazenar_saldo(valor_saldo):
    global saldo 
    saldo = valor_saldo
    return saldo

def saque_saldo(valor_saque):
    global saldo
    if saldo < valor_saque:
        return -1
    saldo = saldo - valor_saque
    return(saldo)

def consultar_saldo():
    return(saldo)

def deposito_saldo(valor_deposito):
    global saldo
    saldo = saldo + valor_deposito
    return(saldo)









