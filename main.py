import cliente
import conta
import agencia

#Menu do Administrador 
print("[1] - Cadastrar Cliente")
print("[2] - Criar uma conta")
print("[3] - Listar clientes")
print("[4] - Listar contas")
print("[5] - Listar agencias")
print("[6] - Sacar")
print("[7] - Depositar")
print("[8] - Consultar saldo")
print("[9] - Sair")
print("[10] - Apresentar relatorio do banco")
print("[11] - Apresentar montante total da agencia")
print("[12] - Apresentar montante total do banco")
print("[13] - Associar um cliente a uma conta existente")
print("[14] - Cadastrar agencia")
opcao = input("Digite a opção desejada: ")

if opcao == "1":
#Aqui vai cadastrar o cliente,aonde vai pegar os dados basicos, nome , cpf , emails e vai armazenar o id dele
    nome = input("Digite o nome do cliente: ")
    cpf = input("Digite o CPF do cliente: ")
    email = input("Digite o email do cliente: ")

    cliente.cadastrar_cliente(cpf, nome, email)


elif opcao == "2":
#Aqui o sistema vai criar uma conta, onde vai inserir inicialmente um saldo para que possa criar a conta,e para saber quem é vai puxar o ID do cliente e o da Agencia
    saldo = float(input("Digite o saldo inicial: "))
    idCliente = int(input("Digite o ID do cliente: "))
    idAgencia = int(input("Digite o ID da agencia: "))  

    print(conta.cadastrarConta(saldo, idCliente, idAgencia))

 
elif opcao == "3":
#Aqui vai listar todos os clientes cadastrados no sistema 
    cliente.listarclientes()


elif opcao == "4":
#Vai mostrar todas as contas cadastradas no sistema, com o ID da conta, ID do cliente e ID da agencia
    print(conta.listarContas())


elif opcao == "5":
#Aqui vai listar todas as agencias cadastradas no sistema, com o ID da agencia e o nome dela
    print(agencia.listarAgencias())


elif opcao == "6":
#Aqui vai fazer o saque , onde vai pegar o ID da conta e o valor a qual vai ser depositado o dinheiro
    idConta= int(input("Digite o ID da conta: "))
    valor = float(input("Digite o valor do saque:"))

    print(conta.sacarConta(idConta, valor))


elif opcao == "7":
# Aqui vai fazer o deposito, onde vai pegar o ID da conta e o valor a qual vai ser depositado o dinheiro
    IDconta = int(input("Digite o ID da conta: "))
    valor = float(input("Digite o valor do deposito:"))
    print(conta.depositarConta(IDconta, valor))


elif opcao == "8":
# consultar o saldo da conta, onde vai pegar o ID da conta e vai mostrar o saldo dele,e lembrando sempre armazenando os dados para que n possa ser perdido
    idConta = int(input("Digite o ID da conta: "))
    print(conta.consultarSaldo(idConta,False))


elif opcao == "9":
# Sair do programa somente.
    print("Programa encerrado.")


elif opcao == "10":
#   
    print(agencia.relatorioBanco())


elif opcao == "11":
    idAgencia = int(input("Digite o ID da agencia: "))
    print(agencia.montanteAgencia(idAgencia))


elif opcao == "12":
    print(conta.montanteTotal())


elif opcao == "13":
    idConta = int(input("Digite o ID da conta: "))
    idCliente = int(input("Digite o ID do cliente: "))
    print(conta.associarClienteConta(idConta, idCliente))

elif opcao == "14":
    print(agencia.criarNovaAgencia())