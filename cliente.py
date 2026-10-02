import json


def carregar_clientes():
    # Tenta abrir o arquivo onde estão salvos os clientes
    try:
        with open("clientes.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except:
        # Se o arquivo não existir ou estiver vazio,
        # retorna um dicionário vazio
        return {}


def salvar_clientes(dados_clientes):
    # Salva todos os clientes de volta no arquivo JSON
    # O ensure_ascii=False permite salvar acentos normalmente
    with open("clientes.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_clientes, arquivo, indent=2, ensure_ascii=False)


def existe_cliente(id_cliente):
    # Procura o cliente pelo ID
    # Se encontrar, retorna os dados do cliente
    # Se não encontrar, retorna False
    return carregar_clientes().get(str(id_cliente), False)


def verificar_cliente(cpf):

    # Importa o módulo conta para utilizar a função
    # que verifica se o CPF é válido
    import conta as ct

    # Verifica se o CPF é válido
    if not ct.verificarCpf(cpf):
        print("Error")
        return False

    # Carrega os clientes cadastrados
    dados_clientes = carregar_clientes()

    # Percorre todos os clientes procurando o CPF
    for id_cliente in dados_clientes:

        # Verifica se o CPF já pertence a algum cliente
        if dados_clientes[id_cliente]["cpf"] == cpf:
            return "\nErro! O CPF '{}' já está cadastrado no sistema.\n".format(
                cpf
            )

    # Se passou pelas duas verificações,
    # o CPF pode ser utilizado
    return True


def cadastrar_cliente(cpf, nome, email):

    # Converte o CPF para string
    cpf = str(cpf)

    # Antes de cadastrar, verifica se o CPF pode ser utilizado
    resultado = verificar_cliente(cpf)

    # Se a verificação retornar uma mensagem de erro,
    # devolve essa mensagem para quem chamou a função
    if resultado is not True:
        return resultado

    # Carrega os clientes que já estão cadastrados
    dados_clientes = carregar_clientes()

    # O novo ID será o último ID existente + 1
    # Se ainda não houver nenhum cliente, começamos pelo ID 0
    if dados_clientes:
        novo_id = int(list(dados_clientes)[-1]) + 1
    else:
        novo_id = 0

    # Cria o cadastro do novo cliente
    # A lista de contas começa vazia
    dados_clientes[str(novo_id)] = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "contas_associadas": []
    }

    # Salva os dados atualizados no arquivo JSON
    salvar_clientes(dados_clientes)

    # Retorna a mensagem de sucesso
    # O main será responsável por imprimir essa mensagem
    return "\nCliente cadastrado com sucesso. ID do cliente: {}.\n".format(
        novo_id
    )


def listar_clientes():

    # Carrega todos os clientes que estão salvos
    dados_clientes = carregar_clientes()

    # Se não houver nenhum cliente cadastrado,
    # retorna uma mensagem informando isso
    if not dados_clientes:
        return "\nNenhum cliente cadastrado até o momento!\n"

    # Criamos uma string vazia para montar
    # a mensagem com todos os clientes
    mensagem = ""

    # Percorre cada cliente cadastrado
    for id_cliente in dados_clientes:

        # Pega os dados do cliente atual
        cliente = dados_clientes[id_cliente]

        # Adiciona as informações do cliente à mensagem
        mensagem += "CLIENTE DE ID: {}\n".format(id_cliente)
        mensagem += "Nome: {}\n".format(cliente["nome"])
        mensagem += "CPF: {}\n".format(cliente["cpf"])
        mensagem += "E-mail: {}\n".format(cliente["email"])
        mensagem += "Contas associadas: {}\n\n".format(
            cliente["contas_associadas"]
        )

    # Adiciona a mensagem final
    mensagem += "Clientes listados com sucesso.\n"

    # Retorna toda a mensagem para o main
    return mensagem


def associar_conta_cliente(id_cliente, id_conta):

    # Carrega os clientes cadastrados
    dados_clientes = carregar_clientes()

    # Verifica se a conta já está associada ao cliente
    if id_conta in dados_clientes[str(id_cliente)]["contas_associadas"]:
        return "\nA conta {} já está associada ao cliente {}.\n".format(
            id_conta, id_cliente
        )

    # Adiciona o ID da conta à lista de contas do cliente
    dados_clientes[str(id_cliente)]["contas_associadas"].append(id_conta)

    # Salva os dados atualizados
    salvar_clientes(dados_clientes)

    # Retorna a mensagem de sucesso
    return "\nConta {} associada ao cliente {} com sucesso!\n".format(
        id_conta, id_cliente
    )


def associar_cliente_conta(id_conta, id_cliente):

    # Importa o módulo conta para verificar
    # se a conta realmente existe
    import conta as ct

    # Primeiro verificamos se a conta existe
    if not ct.existe_conta(id_conta):
        return "\nErro! A conta de id {} não existe.\n".format(id_conta)

    # Depois verificamos se o cliente existe
    if not existe_cliente(id_cliente):
        return "\nErro! O cliente de id {} não existe.\n".format(id_cliente)

    # Abre o arquivo de contas para atualizar os dados
    with open("contas.json", "r", encoding="utf-8") as arquivo:
        dados_contas = json.load(arquivo)

    # Verifica se o cliente já está associado à conta
    if id_cliente in dados_contas[str(id_conta)]["clientes_associados"]:
        return "\nO cliente {} já está associado à conta {}.\n".format(
            id_cliente, id_conta
        )

    # Adiciona o cliente à lista de clientes daquela conta
    dados_contas[str(id_conta)]["clientes_associados"].append(id_cliente)

    # Salva novamente o arquivo de contas
    with open("contas.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_contas, arquivo, indent=2, ensure_ascii=False)

    # Também atualiza o cadastro do cliente,
    # adicionando a conta à lista de contas associadas
    associar_conta_cliente(id_cliente, id_conta)

    # Retorna a mensagem de sucesso
    # O main será responsável por imprimir
    return "\nCliente {} associado à conta {} com sucesso!\n".format(
        id_cliente, id_conta
    )
