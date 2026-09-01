saldo = 0 #não entendi direito para que serve essa bomba
def armazenar_saldo(valor_saldo):
    global saldo 
    saldo = valor_saldo
    return saldo

def saque_saldo(valor_saque):
    global saldo
    saldo = saldo - valor_saque
    return(saldo)

def consultar_saldo(): #Vai consultar o resultado do saldo anterior que foi o do "saque_saldo"
    return(saldo)

def deposito_saldo(valor_deposito):
    global saldo
    saldo = saldo + valor_deposito
    return(saldo)









