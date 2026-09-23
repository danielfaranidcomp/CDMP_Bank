import json
import agencia

""" o padrão da lista de contas vai ser o seguinte:
    para cada conta, o primeiro item é o saldo da conta, o segundo o id,
    o terceiro o id da agencia, o quarto o número n de clientes associados. 
    paralelamente, há uma outra lista de contas associadas, com formato:
    'idConta:idCliente' """

def cadastrarConta(saldoInicial, idCliente, idAgencia):
    # primeiro verifica se o cliente existe
    try: 
        with open('clientes.json', 'r', encoding="utf-8") as f:
            dadosClientes = json.load(f)
        achou = False #flag
        for cliente in range(0, len(dadosClientes), 4):
            if idCliente == dadosClientes[cliente]:
                achou = True
        if not achou:
            return f"\nErro! o cliente de id {idCliente} não existe.\n"
    except:
        return f"\nErro! o cliente de id {idCliente} não existe.\n"

    # verifica se a agência exsite
    try:
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dadosAgencia = json.load(f)
        # procurar e já salvar o index em indexAgencia
        achou = False
        i = 0
        while i < len(dadosAgencia) and not achou:
            if dadosAgencia[i] == idAgencia:
                achou = True
                i += 2
            else:
                i += dadosAgencia[i+1] + 2
        if not achou:
            return "\nErro! Agência não cadastrada,\n"
    except:
        return "\nErro! Agência não cadastrada.\n"
        
    # iniciando operação de cadastro da conta
    try:
        # pega tudo que tá em contas e relacaoContaCliente
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        with open('relacaoContaCliente.json', 'r', encoding="utf-8") as f:
            dadosRelacaoContaCliente = json.load(f)
        id = dadosContas[-4] + 1 # determinando o id da conta nova
        dadosContas.extend([id, saldoInicial, idAgencia , 1]) # joga tudo na lista
        dadosRelacaoContaCliente.append(f"{id}:{idCliente}")
        #colocando de volta no json
        with open('contas.json', 'w', encoding="utf-8") as f:
            json.dump(dadosContas, f, indent=1, ensure_ascii=False)
        with open('relacaoContaCliente.json', 'w', encoding="utf-8") as f:
            json.dump(dadosRelacaoContaCliente, f, indent=1, ensure_ascii=False)
        print(agencia.associarContaAgencia(idAgencia, id, i))
        return f"\nConta cadastrada com sucesso. id da conta: {id}.\n" 
    except: # nesse caso aqui, vai ser o primeiro cliente a ser cadastrado
        print(agencia.associarContaAgencia(idAgencia, 0, i))
        with open('contas.json', 'w', encoding="utf-8") as f:
            json.dump([0, saldoInicial, idAgencia, 1], f, indent=1, ensure_ascii=False)
        with open('relacaoContaCliente.json', 'w', encoding="utf-8") as f:
            json.dump([f"0:{idCliente}"], f, indent=1, ensure_ascii=False)
            return "\nConta cadastrada com sucesso. id da conta: 0.\n"


def associarClienteConta(idConta, idCliente):
    # primeiro verifica se o cliente existe
    try: 
        with open('clientes.json', 'r', encoding="utf-8") as f:
            dadosClientes = json.load(f)
        achou = False #flag
        for cliente in range(0, len(dadosClientes), 4):
            if idCliente == dadosClientes[cliente]:
                achou = True
        if not achou:
            return f"\nErro! o cliente de id {idCliente} não existe.\n"
    except:
        return f"\nErro! o cliente de id {idCliente} não existe.\n"

    # segundo verifica se a conta existe ou nem
    # também já vai buscando o index que vai receber o insert na relacaoContaCliente
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        achou = False
        indexDoInsert = -1
        rangeFinalInsert = 0 #isso vai ser útil lá pra frente
        for conta in range(0, len(dadosContas), 4):
            if idConta == dadosContas[conta]:
                indexDoInsert += 1
                rangeFinalInsert = indexDoInsert + dadosContas[conta+3]
                achou = True
                # aproveita e já aumenta o número da qntdd de clientes associados
                dadosContas[conta+3] += 1
            if not achou:
                indexDoInsert += dadosContas[conta+3]
        if not achou:
            return f"\nErro! a conta de id {idConta} não existe.\n"
    except:
        return f"\nErro! a conta de id {idConta} não existe.\n"

    # vamos agora fazer a inserção ORDENADA e verificar se o já não está associado.
    # não cheguei a  usar try porque se as outras etapas deram certo, com certeza o arquivo existe entao...
    with open('relacaoContaCliente.json', 'r', encoding="utf-8") as f:
        dadosRelacaoContaCliente = json.load(f)
    ehUltimo = True #flag
    for i in range(indexDoInsert, rangeFinalInsert):
        idAtual = int(list(dadosRelacaoContaCliente[i])[2])
        if idCliente < idAtual:
            dadosRelacaoContaCliente.insert(i, f"{idConta}:{idCliente}")
            ehUltimo = False
        elif idAtual == idCliente:
            return f"\nO id {idCliente} já está associado à conta.\n"
    if ehUltimo:
        dadosRelacaoContaCliente.insert(i+1, f"{idConta}:{idCliente}")
    # subindo lá dento
    with open('relacaoContaCliente.json', 'w', encoding="utf-8") as f:
        json.dump(dadosRelacaoContaCliente, f, indent=1, ensure_ascii=False)
    with open('contas.json', 'w', encoding="utf-8") as f:
        json.dump(dadosContas, f, indent=1, ensure_ascii=False)
    return "\nCliente associado à conta com sucesso\n"


def listarContas():
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosConta = json.load(f)
        with open('relacaoContaCliente.json', 'r', encoding="utf-8") as f:
            dadosRelacaoContaCliente = json.load(f)
        contadorClienteConta = -1
        for i in range(0, len(dadosConta), 4):
            print(f"\nCONTA DE ID: {dadosConta[i]}")
            print(f"Saldo da conta: {dadosConta[i+1]:.2f}")
            print(f"Id da agência da conta: {dadosConta[i+2]}")
            print("Id do(s)) cliente(s) associado(s) à conta: ", end="")
            for j in range(0, dadosConta[i+3]):
                contadorClienteConta += 1
                informacao = list(dadosRelacaoContaCliente[contadorClienteConta])
                # só deixando bonitinho, separando por vírgula e ponto final tlgd
                if str(j+1) != str(dadosConta[i+3]):
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
        for i in range(0, len(dadosContas), 4):
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
        for i in range(0, len(dadosContas), 4):
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


# valorPuro = True retorna somente o número, valorPuro = False retorna uma frase.
def consultarSaldo(idConta, valorPuro): 
    # primeiro vamos verificar se a conta existe e já salvar o endereço do saldo na lista
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        achou = False
        index = 0
        for i in range(0, len(dadosContas), 4):
            if dadosContas[i] == idConta:
                achou = True
                index = i+1
        if not achou:
            if valorPuro:
                return False
            else:
                return f"\nErro! A conta não existe.\n"
    except:
        if valorPuro:
            return False
        else:
            return f"\nErro! A conta não existe.\n"

    # agora vamos retornar o valor so saldo
    if valorPuro:
        return dadosContas[index]
    else:
        return f"\nO valor do saldo é R$ {dadosContas[index]:.2f}\n"


def montanteTotal():
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosConta = json.load(f)
        total = 0
        for i in range(1, len(dadosConta), 4):
            total += dadosConta[i]
        return f"\nMontante total do banco: R$ {total:.2f}\n"
    except:
        return "\nMontante total do banco: R$ 0.00\n"
