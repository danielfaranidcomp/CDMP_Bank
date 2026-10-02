import cliente
import conta
import agencia

#Menu do Administrador 
menu = False
while not menu: 
    print("="*20)
    print("MENU DE OPÇÕES".center(20))
    print("="*20)
    print("\n[1] - Cadastrar Cliente")
    print("[2] - Cadastrar uma conta")
    print("[3] - Listar clientes")
    print("[4] - cadastrar agência")
    print("[5] - Sacar")
    print("[6] - Depositar")
    print("[7] - Consultar saldo")
    print("[8] - Transferir entre contas")
    print("[9] - Associar um cliente a uma conta existente")
    print("[10] - Sair\n")
    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
    #Aqui vai cadastrar o cliente,aonde vai pegar os dados basicos, nome , cpf , emails e vai armazenar o id dele
        nome = input("Digite o nome do cliente: ").replace("ç","c").replace("í","i").replace("ã","a").replace("ô","o").replace("é","e").lower()
        cpf = input("Digite o CPF do cliente: ")
        email = input("Digite o email do cliente: ").replace("ç","c").replace("í","i").replace("ã","a").replace("ô","o").replace("é","e").lower()

        cliente.cadastrar_cliente(str(cpf), nome, email)


    elif opcao == "2":
    #Aqui o sistema vai criar uma conta, onde vai inserir inicialmente um saldo para que possa criar a conta,e para saber quem é vai puxar o ID do cliente e o da Agencia

        idCliente = int(input("Digite o ID do cliente: "))
        idAgencia = int(input("Digite o ID da agencia: ")) 
        saldo = float(input("Digite o saldo inicial: ").replace(",",".")) 
        tipo= str(input("Qual o tipo da conta:")).replace("ç","c").replace("á","a").lower()

        print(conta.cadastrarConta( idCliente, idAgencia,saldo,tipo))

    
    elif opcao == "3":
    #Aqui vai listar todos os clientes cadastrados no sistema 
        cliente.listarclientes()


    elif opcao == "4":
        # Aqui ira ocorrer o cadastro de uma nova agencia
         print(agencia.cadastrarAgencia())

    elif opcao == "5":
    #Aqui vai fazer o saque , onde vai pegar o ID da conta e o valor a qual vai ser depositado o dinheiro
        idConta= int(input("Digite o ID da conta: "))
        valor = float(input("Digite o valor do saque:").replace(",","."))

        print(conta.sacarConta(idConta, valor))


    elif opcao == "6":
    # Aqui vai fazer o deposito, onde vai pegar o ID da conta e o valor a qual vai ser depositado o dinheiro
        IDconta = int(input("Digite o ID da conta: "))
        valor = float(input("Digite o valor do deposito:").replace(",","."))
        print(conta.depositarConta(IDconta, valor))


    elif opcao == "7":
    # consultar o saldo da conta, onde vai pegar o ID da conta e vai mostrar o saldo dele,e lembrando sempre armazenando os dados para que n possa ser perdido
        idConta = int(input("Digite o ID da conta: "))
        print(conta.consultaSaldo(idConta))


    elif opcao == "8":
    #Aqui é onde vai ocorrer a transferencia de uma conta para a outra    
        idContaOrigem = int(input("Digite o id da conta que vai transferir: "))
        idContaDestino = int(input("Digite o id da conta que vai receber: "))
        valor = float(input("Digite o valor a ser transferido: ").replace(",","."))
        print(conta.transferirConta(idContaOrigem, idContaDestino, valor))

    elif opcao == "9":
    # Associar cliente a uma conta existente    
        idCliente = int(input("Digite o ID do cliente: "))
        idConta = int(input("Digite o ID da conta: "))
        print(cliente.associarClienteConta(idCliente, idConta))

    elif opcao == "10":
        menu = True
        print("Encerrando o programa...")

    else:
        print("Opção inválida! Tente novamente!")