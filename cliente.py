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
                print(f"Erro! O CPF '{cpf}' ja esta cadastrado no sistema.")
                return

        # Cria o ID do novo cliente
        idnovo = dadosClientes[-4] + 1

        dadosClientes.extend([idnovo, nome, cpf, email])

        # Salva os clientes no arquivo
        with open("clientes.json", "w", encoding="utf-8") as f:
            json.dump(dadosClientes, f, indent=1, ensure_ascii=False)

        print(f"Cliente cadastrado com sucesso. ID do cliente: {idnovo}.")

    except:

        # Se o arquivo nao existir ou estiver vazio
        # cadastra o primeiro cliente
        with open("clientes.json", "w", encoding="utf-8") as f:
            json.dump([0, nome, cpf, email], f, indent=1, ensure_ascii=False)

        print("Cliente cadastrado com sucesso. ID do cliente: 0.")


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
            print(f"E-mail: {dadosClientes[i + 3]}")
            print()

        print("Clientes listados com sucesso.")

    except:

        print("Nenhum cliente cadastrado ate o momento!")