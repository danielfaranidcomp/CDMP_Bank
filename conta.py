import json
import agencia as ag
import cliente as cl

def existeConta(idCliente):
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosClientes = json.load(f)
        return dadosClientes.get(str(idCliente), False)
    except:
        return False


def cadastrarConta(idCliente, idAgencia, saldo, tipo):
    # primeiro verifica se o cliente e a agência existem
    if not cl.existeCliente(idCliente):
        return f"\nErro! O cliente de id {idCliente} não existe.\n"
    if not ag.existeAgencia(idAgencia):
        return f"\nErro! A agência de id {idAgencia} não existe.\n"

    try: # caso já existam contas criadas
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        id = int(list(dadosContas)[-1]) + 1 # novo id = ultimo id + 1
        dadosContas[str(id)] = {"tipo": tipo, "clientesAssociados": [idCliente], 
                           "agenciaAssociada": idAgencia, "saldo": saldo}
        ag.associarContaAgencia(idAgencia, id)
        with open('contas.json', 'w', econding="utf-8") as f:
            json.dump(dadosContas, f, indent=2, ensure_ascii=False) # insere alterações
        return f"\nConta de id {id} cadastrada com sucesso!\n"
    except: # primeira conta criada
        dadosContas = {"0": {"tipo": tipo, "clientesAssociados": [idCliente], 
                            "agenciaAssociada": idAgencia, "saldo": saldo}}
        ag.associarContaAgencia(idAgencia, 0)
        with open('contas.json', 'w', encoding="utf-8") as f:
            json.dump(dadosContas, f, indent=2, ensure_ascii=False)
        return "\nConta de id 0 cadastrada com sucesso!\n"


def depositarConta(idConta, valor):
    if not existeConta(idConta):
        return f"\nErro! A conta de id {idConta} não existe.\n"
    with open('contas.json', 'r', encoding="utf-8") as f:
        dadosContas = json.load(f)
    if dadosContas[str(idConta)]["tipo"] == "salário":
        return f"\nErro! O tipo da conta {idConta} é salário. Depósitos não são possíveis\n"
    dadosContas[str(idConta)]["saldo"] += valor    
    with open('contas.json', 'w', encoding="utf-8") as f:
        json.dump(dadosContas, f, indent="utf-8", ensure_ascii=False)
    return f"\nValor depositado com sucesso. Saldo atual: R$ {dadosContas[str(idConta)]["saldo"]:.2f}\n"


def sacarConta(idConta, valor):
    if not existeConta(idConta):
        return f"\nErro! A conta de id {idConta} não existe.\n"
    with open('contas.json', 'r', encoding="utf-8") as f:
        dadosConta = json.load(f)
    if dadosConta[str(idConta)]["saldo"] < valor:
        return f"\nErro! O valor R$ {valor:.2f} é superior ao saldo da conta. (R$ {dadosConta[str(idConta)]["saldo"]})\n"
    dadosConta[str(idConta)]["saldo"] -= valor
    with open('contas.json', 'w', encoding="utf-8") as f:
        json.dump(dadosConta, f, indent=2, ensure_ascii=False)


def transferirConta(idTransfere, idRecebe, valor):
    if not existeConta(idTransfere) and existeConta(idRecebe):
        return "\nErro! Nenhuma das contas existem.\n"
    if not existeConta(idTransfere):
        return f"\nErro! a conta de id {idTransfere} não existe.\n"
    if not existeConta(idRecebe):
        return f"\nErro! a conta de id {idRecebe} não existe.\n"

    with open('contas.json', 'r', encoding="utf-8") as f:
        dadosConta = json.load(f)
    if dadosConta[str(idTransfere)]["saldo"] < valor:
        return f"\nErro! O valor R$ {valor:.2f} supera o saldo da conta de id {idTransfere}. (R$ {dadosConta[(str(idTransfere))]["saldo"]})\n"

    dadosConta[str(idTransfere)]["saldo"] -= valor
    dadosConta[str(idRecebe)]["saldo"] += valor

    with open('contas.json', 'w', encoding="utf-8") as f:
        json.dump(dadosConta, f, indent=2, ensure_ascii=False)
    return f"\nTransferência realizada com sucesso! Saldo de conta {idTransfere}: R$ {dadosConta[str(idTransfere)]["saldo"]:.2f}. Saldo de conta {idRecebe}: R$ {dadosConta[str(idRecebe)]["saldo"]:.2f}\n"


def consultaSaldo(idConta):
    if not existeConta(idConta):
        return f"\nErro! A conta de id {idConta} não existe.\n"
    with open('contas.json', 'r', encoding="utf-8") as f:
        dadosConta = json.load(f)
    return f"\nO saldo da conta de id {idConta} é R$ {dadosConta[str(idConta)]["saldo"]:.2f}\n"


def verificarCpf(cpf):
    digitos = list(filter(lambda x: x != '.' and x != '-', cpf))
    def verificaAte(limite, digitos):
        soma = 0
        for i in range(0, limite):
            soma += int(digitos[i]) * (limite + 1 - i)
        resto = soma % 11
        return (resto < 2 and int(digitos[limite]) == 0) or (resto >= 2 and int(digitos[limite]) == 11 - resto)
    return verificaAte(9, digitos) and verificaAte(10, digitos)
