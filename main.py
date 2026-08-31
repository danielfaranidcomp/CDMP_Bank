import cliente
import conta

print("=-"*40)
print("SEJA BEM-VINDO AO CDMP BANK, VAMOS CADASTRAR O CLIENTE!")
print("=-"*40)

# cadastrando o cliente
cpf = int(input('\n➥ Digite o cpf: '))
nome = str(input('➥ Digite o nome: '))
senha = str(input('➥ Digite a senha: '))

cliente.criar_cliente(cpf, nome, senha)

# agora criando a conta

print("=-"*40)
print('AGORA VAMOS CRIAR UMA CONTA!')
print("=-"*40)

valor = float(input('\n➥ Digite o saldo: '))
print(f'Conta criada com sucesso! valor do saldo: {conta.armazenar_saldo(valor)}\n')


#vamos fazer um depósito
print("=-"*40)
print('AGORA VAMOS REALIZAR UM DEPÓSITO!')
print("=-"*40)

valor = float(input('\n➥ Digite o valor do depósito: '))
print(f'Depósito realizado! saldo era de R$ {conta.consultar_saldo()} e após depósito R$ {conta.deposito_saldo(valor)}\n')

#vamos realizar um saque
print("=-"*40)
print('AGORA VAMOS REALIZAR UM SAQUE!')
print("=-"*40)

valor = float(input('\n➥ Digite o valor do saque: '))
if (conta.saque_saldo(valor) >= 0):
    print(f'Saque realizado! saldo era de R$ {conta.consultar_saldo() + valor} e após depósito R$ {conta.consultar_saldo()}')
else:
    print(f'Erro! o seu saque de R$ {valor} foi NEGADO devido a saldo insuficiente. (R$ {conta.consultar_saldo()})')