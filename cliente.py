import json


# Funcao que cadastra clientes
def cadastrar_cliente(cpf, nome, email):

    cpf = str(cpf)

    try:
        with open("clientes.json", "r", encoding="utf-8") as f:
            dadosClientes = json.load(f)

        # Verifica se o CPF ja esta cadastrado
        for i in range(0, len(dadosClientes), 4):

            if dadosClientes[i + 2] == cpf:
                print(f"\nErro! O CPF '{cpf}' ja esta cadastrado no sistema.\n")
                return

        # Cria o ID do novo cliente
        idnovo = dadosClientes[-4] + 1

        dadosClientes.extend([idnovo, nome, cpf, email])

        # Salva os clientes no arquivo
        with open("clientes.json", "w", encoding="utf-8") as f:
            json.dump(dadosClientes, f, indent=1, ensure_ascii=False)

        print(f"\nCliente cadastrado com sucesso. ID do cliente: {idnovo}.\n")

    except:

        # Se o arquivo nao existir ou estiver vazio
        # cadastra o primeiro cliente
        with open("clientes.json", "w", encoding="utf-8") as f:
            json.dump([0, nome, cpf, email], f, indent=1, ensure_ascii=False)

        print("\nCliente cadastrado com sucesso. ID do cliente: 0.\n")


# Funcao que lista os clientes
def listarclientes():

    try:
        with open("clientes.json", "r", encoding="utf-8") as f:
            dadosClientes = json.load(f)

        if not dadosClientes:
            print("Nenhum cliente cadastrado ate o momento!")
            return

        for i in range(0, len(dadosClientes), 4):

            print(f"CLIENTE DE ID: {dadosClientes[i]}")
            print(f"Nome: {dadosClientes[i + 1]}")
            print(f"CPF: {dadosClientes[i + 2]}")
            print(f"E-mail: {dadosClientes[i + 3]}\n")

        print("\nClientes listados com sucesso.\n")

    except:

        print("\nNenhum cliente cadastrado ate o momento!\n")