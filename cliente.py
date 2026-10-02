import json


def carregarClientes():
    # Tenta abrir o arquivo onde estão salvos os clientes
    try:
        with open("clientes.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except:
        return {}


def salvarClientes(dadosClientes):
    # Salva todos os clientes de volta no arquivo JSON
    # Permite salvar nomes e outros textos com acentos normalmente
    with open("clientes.json", "w", encoding="utf-8") as arquivo:
        json.dump(dadosClientes, arquivo, indent=2, ensure_ascii=False)


def existeCliente(idCliente):
    # Procura o cliente pelo ID
    # Se encontrar, devolve os dados dele
    return carregarClientes().get(str(idCliente), False)


def verificarCliente(cpf):

    import conta as ct

    cpf = str(cpf)

    # Verifica se o CPF realmente é válido
    try:
        cpfValido = ct.verificarCpf(cpf)
    except:
        cpfValido = False

    if not cpfValido:
        print("\nErro! O CPF '{}' é inválido.\n".format(cpf))
        return False

    # Depois verifica se esse CPF já foi usado por outro cliente
    dadosClientes = carregarClientes()

    for idCliente in dadosClientes:
        if dadosClientes[idCliente]["cpf"] == cpf:
            print("\nErro! O CPF '{}' já está cadastrado no sistema.\n".format(cpf))
            return False

    # Se passou pelas duas verificações, o CPF pode ser cadastrado
    return True

def cadastrar_cliente(cpf, nome, email):
    cpf = str(cpf)

    # Antes de cadastrar, conferimos se o CPF pode ser utilizado
    if not verificarCliente(cpf):
        return

    dadosClientes = carregarClientes()

    # O novo ID será o último ID existente + 1
    # Se ainda não houver nenhum cliente, começamos pelo ID 0
    if dadosClientes:
        novoId = int(list(dadosClientes)[-1]) + 1
    else:
        novoId = 0

    # Criamos o cadastro do cliente e começamos a lista de contas vazia
    dadosClientes[str(novoId)] = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "contasAssociadas": []
    }

    salvarClientes(dadosClientes)

    print("\nCliente cadastrado com sucesso. ID do cliente: {}.\n".format(novoId))
def listarclientes():
    # Carrega todos os clientes que estão salvos
    dadosClientes = carregarClientes()

    # Se não tiver nenhum cliente, avisamos e encerramos a função
    if not dadosClientes:
        print("\nNenhum cliente cadastrado até o momento!\n")
        return

    # Percorremos cada cliente para mostrar suas informações
    for idCliente in dadosClientes:
        cliente = dadosClientes[idCliente]

        print("CLIENTE DE ID: {}".format(idCliente))
        print("Nome: {}".format(cliente["nome"]))
        print("CPF: {}".format(cliente["cpf"]))
        print("E-mail: {}".format(cliente["email"]))
        print("Contas associadas: {}\n".format(cliente["contasAssociadas"]))

    print("Clientes listados com sucesso.\n")


def associarContaCliente(idCliente, idConta):
    # Atualiza o cadastro do cliente,
    # adicionando o ID da conta na lista de contas associadas
    dadosClientes = carregarClientes()

    # Verifica se a conta já está na lista para evitar repetição
    if idConta not in dadosClientes[str(idCliente)]["contasAssociadas"]:
        dadosClientes[str(idCliente)]["contasAssociadas"].append(idConta)
        salvarClientes(dadosClientes)


def associarClienteConta(idConta, idCliente):
    # Essa função faz a associação dos dois lados:
    # a conta passa a ter o cliente associado
    # e o cliente passa a ter a conta registrada no seu cadastro
    import conta as ct

    # Primeiro verificamos se a conta realmente existe
    if not ct.existeConta(idConta):
        return "\nErro! A conta de id {} não existe.\n".format(idConta)

    # Depois verificamos se o cliente existe
    if not existeCliente(idCliente):
        return "\nErro! O cliente de id {} não existe.\n".format(idCliente)

    # Abrimos o arquivo de contas para atualizar os dados
    with open("contas.json", "r", encoding="utf-8") as arquivo:
        dadosContas = json.load(arquivo)

    # Se o cliente já estiver associado à conta, não precisamos adicionar novamente
    if idCliente in dadosContas[str(idConta)]["clientesAssociados"]:
        return "\nO cliente {} já está associado à conta {}.\n".format(
            idCliente, idConta
        )

    # Adicionamos o cliente à lista de clientes daquela conta
    dadosContas[str(idConta)]["clientesAssociados"].append(idCliente)

    # Salvamos novamente o arquivo de contas com a alteração
    with open("contas.json", "w", encoding="utf-8") as arquivo:
        json.dump(dadosContas, arquivo, indent=2, ensure_ascii=False)

    # Também atualizamos o cadastro do cliente
    associarContaCliente(idCliente, idConta)

    return "\nCliente {} associado à conta {} com sucesso!\n".format(
        idCliente, idConta
    )
