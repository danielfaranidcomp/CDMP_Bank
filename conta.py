import json

""" o padrão da lista de contas vai ser o seguinte:
    para cada conta, o primeiro item é o saldo da conta, o segundo o id,
    o terceiro o número n de clientes associados. paralelamente,
    há uma outra lista de contas associadas, com formato:
    'idConta:idCliente' """

def cadastrarConta(saldoInicial, idCliente):
    # primeiro verifica se o cliente existe
    try: 
        with open('clientes.json', 'r', encoding="utf-8") as f:
            dadosClientes = json.load(f)
        achou = False #flag
        for cliente in range(0, len(dadosClientes), 4):
            if str(idCliente) == str(dadosClientes[cliente]):
                achou = True
        if not achou:
            return f"Erro! o cliente de id {idCliente} não existe."
    except:
        return f"Erro! o cliente de id {idCliente} não existe."
        
    # iniciando operação de cadastro da conta
    try:
        # pega tudo que tá em contas e relacaoContaCliente
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        with open('relacaoContaCliente.json', 'r', encoding="utf-8") as f:
            dadosRelacaoContaCliente = json.load(f)
        id = dadosContas[-3] + 1 # determinando o id da conta nova
        dadosContas.extend([id, saldoInicial, 1]) # jogad tudo na lista
        dadosRelacaoContaCliente.append(f"{id}:{idCliente}")
        #colocando de volta no json
        with open('contas.json', 'w', encoding="utf-8") as f:
            json.dump(dadosContas, f, indent=1, ensure_ascii=False)
        with open('relacaoContaCliente.json', 'w', encoding="utf-8") as f:
            json.dump(dadosRelacaoContaCliente, f, indent=1, ensure_ascii=False)
        return f"Conta cadastrada com sucesso. id da conta: {id}." 
    except: # nesse caso aqui, vai ser o primeiro cliente a ser cadastrado
        with open('contas.json', 'w', encoding="utf-8") as f:
            json.dump([0, saldoInicial, 1], f, indent=1, ensure_ascii=False)
        with open('relacaoContaCliente.json', 'w', encoding="utf-8") as f:
            json.dump([f"0:{idCliente}"], f, indent=1, ensure_ascii=False)
            return "Conta cadastrada com sucesso. id da conta: 0."


def associarClienteConta(idConta, idCliente):
    # primeiro verifica se o cliente existe
    try: 
        with open('clientes.json', 'r', encoding="utf-8") as f:
            dadosClientes = json.load(f)
        achou = False #flag
        for cliente in range(0, len(dadosClientes), 4):
            if str(idCliente) == str(dadosClientes[cliente]):
                achou = True
        if not achou:
            return f"Erro! o cliente de id {idCliente} não existe."
    except:
        return f"Erro! o cliente de id {idCliente} não existe."

    # segundo verifica se a conta existe ou nem
    # também já vai buscando o index que vai receber o insert na relacaoContaCliente
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        achou = False
        indexDoInsert = -1
        rangeFinalInsert = 0 #isso vai ser útil lá pra frente
        for conta in range(0, len(dadosContas), 3):
            if str(idConta) == str(dadosContas[conta]):
                indexDoInsert += 1
                rangeFinalInsert = indexDoInsert + dadosContas[conta+2]
                achou = True
                # aproveita e já aumenta o número da qntdd de clientes associados
                dadosContas[conta+2] += 1
            if not achou:
                indexDoInsert += dadosContas[conta+2]
        if not achou:
            return f"Erro! a conta de id {idConta} não existe."
    except:
        return f"Erro! a conta de id {idConta} não existe."

    # vamos agora fazer a inserção ORDENADA e verificar se o já não está associado.
    # não cheguei a  usar try porque se as outras etapas deram certo, com certeza o arquivo existe entao...
    with open('relacaoContaCliente.json', 'r', encoding="utf-8") as f:
        dadosRelacaoContaCliente = json.load(f)
    ehUltimo = True #flag
    for i in range(indexDoInsert, rangeFinalInsert):
        idAtual = list(dadosRelacaoContaCliente[i])[2]
        if idCliente < idAtual:
            dadosRelacaoContaCliente.insert(i, f"{idConta}:{idCliente}")
            ehUltimo = False
        elif idAtual == idCliente:
            return f"O id {idCliente} já está associado à conta."
    if ehUltimo:
        dadosRelacaoContaCliente.insert(i+1, f"{idConta}:{idCliente}")
    # subindo lá dento
    with open('relacaoContaCliente.json', 'w', encoding="utf-8") as f:
        json.dump(dadosRelacaoContaCliente, f, indent=1, ensure_ascii=False)
    with open('contas.json', 'w', encoding="utf-8") as f:
        json.dump(dadosContas, f, indent=1, ensure_ascii=False)
    return "Cliente associado à conta com sucesso"


def listarContas():
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosConta = json.load(f)
        with open('relacaoContaCliente.json', 'r', encoding="utf-8") as f:
            dadosRelacaoContaCliente = json.load(f)
        contadorClienteConta = -1
        for i in range(0, len(dadosConta), 3):
            print(f"\nCONTA DE ID: {dadosConta[i]}")
            print(f"Saldo da conta: {dadosConta[i+1]:.2f}")
            print("Id dos clientes associados à conta: ", end="")
            for j in range(0, dadosConta[i+2]):
                contadorClienteConta += 1
                informacao = list(dadosRelacaoContaCliente[contadorClienteConta])
                # só deixando bonitinho, separando por vírgula e ponto final tlgd
                if str(j+1) != str(dadosConta[i+2]):
                    print(f"{informacao[2]}, ", end="")
                else:
                    print(f"{informacao[2]}.")
        return "\nContas listadas com sucesso.\n"
    except:
        return "\nNenhuma conta cadastrada até o momento!\n"


def sacarConta(idConta, valor):
    # primeiro vamos verificar se a conta existe, se o saque é possível
    # e já salvar o endereço do saldo na lista
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        achou = False
        index = 0
        for i in range(0, len(dadosContas), 3):
            if dadosContas[i] == idConta:
                achou = True
                index = i+1
                if dadosContas[index] < valor:
                    return f"\nErro! o valor ultrapassa o saldo da conta. (R$ {dadosContas[index]:.2f})\n"
        if not achou:
            return f"\nErro! A conta não existe.\n"
    except:
        return f"\nErro! A conta não existe.\n"

    # agora vamos fazer a operação
    dadosContas[index] -= valor

    # joga la dentro dnv
    with open('contas.json', 'w', encoding="utf-8") as f:
        json.dump(dadosContas, f, indent=1, ensure_ascii=False)
    return f"\nValor de R$ {valor:.2f} sacado com sucesso. Saldo atual: R$ {dadosContas[index]:.2f}\n"


def depositarConta(idConta, valor):
    # primeiro vamos verificar se a conta existe e já salvar o endereço do saldo na lista
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        achou = False
        index = 0
        for i in range(0, len(dadosContas), 3):
            if dadosContas[i] == idConta:
                achou = True
                index = i+1
        if not achou:
            return f"\nErro! A conta não existe.\n"
    except:
        return f"\nErro! A conta não existe.\n"

    # agora vamos fazer a operação
    dadosContas[index] += valor

    # joga la dentro dnv
    with open('contas.json', 'w', encoding="utf-8") as f:
        json.dump(dadosContas, f, indent=1, ensure_ascii=False)
    return f"\nValor de R$ {valor:.2f} depositado com sucesso. Saldo atual: R$ {dadosContas[index]:.2f}\n"


def consultarSaldo(idConta):
    # primeiro vamos verificar se a conta existe e já salvar o endereço do saldo na lista
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        achou = False
        index = 0
        for i in range(0, len(dadosContas), 3):
            if dadosContas[i] == idConta:
                achou = True
                index = i+1
        if not achou:
            return f"\nErro! A conta não existe.\n"
    except:
        return f"\nErro! A conta não existe.\n"

    # agora vamos retornar o valor so saldo
    return f"\nO valor do saldo é R$ {dadosContas[index]:.2f}\n"


def montanteTotal():
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosConta = json.load(f)
        total = 0
        for i in range(1, len(dadosConta), 3):
            total += dadosConta[i]
        return f"\nMontante total do banco: R$ {total:.2f}\n"
    except:
        return "\nMontante total do banco: R$ 0.00\n"
