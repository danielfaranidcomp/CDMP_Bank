import json
 
 
def carregar_clientes():
    # Tenta abrir o arquivo onde estão salvos os clientes
    try:
        with open("clientes.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio/corrompido,
        # retorna um dicionário vazio
        return {}
 
 
def salvar_clientes(dados_clientes):
    # Salva todos os clientes de volta no arquivo JSON
    # O ensure_ascii=False permite salvar acentos normalmente
    with open("clientes.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_clientes, arquivo, indent=2, ensure_ascii=False)
 
 
def normalizar_cpf(cpf):
    # Mantém só os dígitos, para que "123.456.789-09" e "12345678909"
    # sejam tratados como o mesmo CPF
    return "".join(c for c in str(cpf) if c.isdigit())
 
 
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
        return "\nErro! O CPF é inválido.\n"
 
    cpf_limpo = normalizar_cpf(cpf)
 
    # Percorre todos os clientes procurando o CPF
    dados_clientes = carregar_clientes()
    for id_cliente in dados_clientes:
        if normalizar_cpf(dados_clientes[id_cliente]["cpf"]) == cpf_limpo:
            return "\nErro! O CPF '{}' já está cadastrado no sistema.\n".format(
                cpf
            )
 
    # Se passou pelas duas verificações, o CPF pode ser utilizado
    return True
 
 
def cadastrar_cliente(cpf, nome, email):
    cpf = str(cpf).strip()
 
    # Antes de cadastrar, verifica se o CPF pode ser utilizado
    resultado = verificar_cliente(cpf)
 
    # Se a verificação retornar uma mensagem de erro,
    # devolve essa mensagem para o main imprimir
    if resultado is not True:
        return resultado
 
    dados_clientes = carregar_clientes()
 
    # O novo ID será o maior ID existente + 1
    # Se ainda não houver nenhum cliente, começamos pelo ID 0
    if dados_clientes:
        novo_id = max(int(k) for k in dados_clientes) + 1
    else:
        novo_id = 0
 
    # Cria o cadastro do novo cliente (CPF salvo só com dígitos)
    dados_clientes[str(novo_id)] = {
        "nome": nome,
        "cpf": normalizar_cpf(cpf),
        "email": email,
        "contas_associadas": []
    }
 
    salvar_clientes(dados_clientes)
 
    return "\nCliente cadastrado com sucesso. ID do cliente: {}.\n".format(
        novo_id
    )
 
 
def listar_clientes():
    dados_clientes = carregar_clientes()
 
    if not dados_clientes:
        return "\nNenhum cliente cadastrado até o momento!\n"
 
    mensagem = ""
    for id_cliente in dados_clientes:
        cliente = dados_clientes[id_cliente]
        mensagem += "CLIENTE DE ID: {}\n".format(id_cliente)
        mensagem += "Nome: {}\n".format(cliente["nome"])
        mensagem += "CPF: {}\n".format(cliente["cpf"])
        mensagem += "E-mail: {}\n".format(cliente["email"])
        mensagem += "Contas associadas: {}\n\n".format(
            cliente["contas_associadas"]
        )
 
    mensagem += "Clientes listados com sucesso.\n"
    return mensagem
 
 
def associar_conta_cliente(id_cliente, id_conta):
    # Atualiza o cadastro do cliente com o ID da conta
    dados_clientes = carregar_clientes()
 
    if id_conta in dados_clientes[str(id_cliente)]["contas_associadas"]:
        return "\nA conta {} já está associada ao cliente {}.\n".format(
            id_conta, id_cliente
        )
 
    dados_clientes[str(id_cliente)]["contas_associadas"].append(id_conta)
    salvar_clientes(dados_clientes)
 
    return "\nConta {} associada ao cliente {} com sucesso!\n".format(
        id_conta, id_cliente
    )
 
 
def associar_cliente_conta(id_conta, id_cliente):
    # Importa o módulo conta para verificar
    # se a conta realmente existe
    import conta as ct
 
    if not ct.existeConta(id_conta):
        return "\nErro! A conta de id {} não existe.\n".format(id_conta)
 
    if not existe_cliente(id_cliente):
        return "\nErro! O cliente de id {} não existe.\n".format(id_cliente)
 
    # Abre o arquivo de contas para atualizar os dados
    with open("contas.json", "r", encoding="utf-8") as arquivo:
        dados_contas = json.load(arquivo)
 
    if id_cliente in dados_contas[str(id_conta)]["clientesAssociados"]:
        return "\nO cliente {} já está associado à conta {}.\n".format(
            id_cliente, id_conta
        )
 
    dados_contas[str(id_conta)]["clientesAssociados"].append(id_cliente)
 
    with open("contas.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_contas, arquivo, indent=2, ensure_ascii=False)
 
    # Também atualiza o cadastro do cliente
    associar_conta_cliente(id_cliente, id_conta)
 
    return "\nCliente {} associado à conta {} com sucesso!\n".format(
        id_cliente, id_conta
    )