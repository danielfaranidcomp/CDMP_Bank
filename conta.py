import json
import agencia as ag
import cliente as cl
 
 
def existeConta(idConta):
    try:
        with open('contas.json', 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        return dadosContas.get(str(idConta), False)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
 
 
def _carregarContas():
    with open('contas.json', 'r', encoding="utf-8") as f:
        return json.load(f)
 
 
def _salvarContas(dadosContas):
    with open('contas.json', 'w', encoding="utf-8") as f:
        json.dump(dadosContas, f, indent=2, ensure_ascii=False)
 
 
def cadastrarConta(idCliente, idAgencia, saldo, tipo):
    # primeiro verifica se o cliente e a agência existem
    if not cl.existe_cliente(idCliente):
        return f"\nErro! O cliente de id {idCliente} não existe.\n"
    if not ag.existeAgencia(idAgencia):
        return f"\nErro! A agência de id {idAgencia} não existe.\n"
    if saldo < 0:
        return "\nErro! O saldo inicial não pode ser negativo.\n"
 
    try:
        dadosContas = _carregarContas()
    except (FileNotFoundError, json.JSONDecodeError):
        # arquivo não existe ou está vazio: primeira conta
        dadosContas = {}
 
    # novo id = maior id existente + 1 (ou 0 se for a primeira)
    novo_id = max((int(k) for k in dadosContas), default=-1) + 1
 
    dadosContas[str(novo_id)] = {"tipo": tipo, "clientesAssociados": [],
                                 "agencia": idAgencia, "saldo": saldo}
    _salvarContas(dadosContas)
 
    ag.associarContaAgencia(idAgencia, novo_id)
    cl.associar_cliente_conta(novo_id, idCliente)
    return f"\nConta de id {novo_id} cadastrada com sucesso!\n"
 
 
def depositarConta(idConta, valor):
    if not existeConta(idConta):
        return f"\nErro! A conta de id {idConta} não existe.\n"
    if valor <= 0:
        return "\nErro! O valor deve ser positivo.\n"
    dadosContas = _carregarContas()
    if dadosContas[str(idConta)]["tipo"] == "salario":
        return f"\nErro! O tipo da conta {idConta} é salário. Depósitos não são possíveis\n"
    dadosContas[str(idConta)]["saldo"] += valor
    _salvarContas(dadosContas)
    saldo = dadosContas[str(idConta)]["saldo"]
    return f"\nValor depositado com sucesso. Saldo atual: R$ {saldo:.2f}\n"
 
 
def sacarConta(idConta, valor):
    if not existeConta(idConta):
        return f"\nErro! A conta de id {idConta} não existe.\n"
    if valor <= 0:
        return "\nErro! O valor deve ser positivo.\n"
    dadosContas = _carregarContas()
    saldo = dadosContas[str(idConta)]["saldo"]
    if saldo < valor:
        return f"\nErro! O valor R$ {valor:.2f} é superior ao saldo da conta. (R$ {saldo:.2f})\n"
    dadosContas[str(idConta)]["saldo"] -= valor
    _salvarContas(dadosContas)
    saldo = dadosContas[str(idConta)]["saldo"]
    return f"\nSaque realizado. Saldo atual da conta {idConta}: R$ {saldo:.2f}\n"
 
 
def transferirConta(idTransfere, idRecebe, valor):
    if not existeConta(idTransfere) and not existeConta(idRecebe):
        return "\nErro! Nenhuma das contas existem.\n"
    if not existeConta(idTransfere):
        return f"\nErro! a conta de id {idTransfere} não existe.\n"
    if not existeConta(idRecebe):
        return f"\nErro! a conta de id {idRecebe} não existe.\n"
    if valor <= 0:
        return "\nErro! O valor deve ser positivo.\n"
 
    dadosContas = _carregarContas()
    origem = dadosContas[str(idTransfere)]
    destino = dadosContas[str(idRecebe)]
 
    if origem["saldo"] < valor:
        return f"\nErro! O valor R$ {valor:.2f} supera o saldo da conta de id {idTransfere}. (R$ {origem['saldo']:.2f})\n"
    if origem["tipo"] == "salario":
        return "\nErro! Uma conta de tipo salário não pode realizar transferências.\n"
    if destino["tipo"] == "salario":
        return "\nErro! Uma conta de tipo salário não pode receber transferências.\n"
 
    origem["saldo"] -= valor
    destino["saldo"] += valor
    _salvarContas(dadosContas)
    return (f"\nTransferência realizada com sucesso! "
            f"Saldo de conta {idTransfere}: R$ {origem['saldo']:.2f}. "
            f"Saldo de conta {idRecebe}: R$ {destino['saldo']:.2f}\n")
 
 
def consultarSaldo(idConta):
    if not existeConta(idConta):
        return f"\nErro! A conta de id {idConta} não existe.\n"
    dadosContas = _carregarContas()
    return f"\nO saldo da conta de id {idConta} é R$ {dadosContas[str(idConta)]['saldo']:.2f}\n"
 
 
def listarContas():
    try:
        dadosContas = _carregarContas()
    except (FileNotFoundError, json.JSONDecodeError):
        return "\nNenhuma conta cadastrada até o momento.\n"
 
    if not dadosContas:
        return "\nNenhuma conta cadastrada até o momento.\n"
 
    for id, conta in dadosContas.items():
        print(f"\nCONTA DE ID {id}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print(f"Tipo: {conta['tipo']}")
        print(f"Agência: {conta['agencia']}")
        clientes = ", ".join(str(c) for c in conta["clientesAssociados"])
        print(f"Clientes associados: {clientes}.")
    return "\nContas listadas com sucesso.\n"
 
 
def verificarCpf(cpf):
    digitos = [c for c in str(cpf) if c not in ".-"]
    if len(digitos) != 11 or not all(d.isdigit() for d in digitos):
        return False
    # CPFs com todos os dígitos iguais (111.111.111-11 etc.) são inválidos
    if len(set(digitos)) == 1:
        return False
 
    def verificaAte(limite, digitos):
        soma = 0
        for i in range(0, limite):
            soma += int(digitos[i]) * (limite + 1 - i)
        resto = soma % 11
        return (resto < 2 and int(digitos[limite]) == 0) or (resto >= 2 and int(digitos[limite]) == 11 - resto)
 
    return verificaAte(9, digitos) and verificaAte(10, digitos)
 
 
def relatorioBanco():
    try:
        dadosContas = _carregarContas()
    except (FileNotFoundError, json.JSONDecodeError):
        return "\nSem contas cadastradas até o momento.\n"
    soma = sum(c["saldo"] for c in dadosContas.values())
    return f"\nMontante total do banco: R$ {soma:.2f}\n"
 
 
def listar_contas_saldo_positivo():
    try:
        dadosContas = _carregarContas()
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {id_conta: conta for id_conta, conta in dadosContas.items()
            if conta["saldo"] > 0}
 
 
def encontrar_maior_menor_saldo():
    try:
        dadosContas = _carregarContas()
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None
    if not dadosContas:
        return None, None
 
    maior = max(dadosContas.items(), key=lambda item: item[1]["saldo"])
    menor = min(dadosContas.items(), key=lambda item: item[1]["saldo"])
    return maior, menor
 
 
def _formatarConta(id_conta, conta):
    clientes = ", ".join(str(c) for c in conta["clientesAssociados"])
    return (f"CONTA DE ID {id_conta}\n"
            f"Saldo: R$ {conta['saldo']:.2f}\n"
            f"Tipo: {conta['tipo']}\n"
            f"Agência: {conta['agencia']}\n"
            f"Clientes associados: {clientes}.\n")
 
 
def relatorioSaldoPositivo():
    positivas = listar_contas_saldo_positivo()
    if not positivas:
        return "\nNenhuma conta com saldo positivo até o momento.\n"
    mensagem = "\n"
    for id_conta, conta in positivas.items():
        mensagem += _formatarConta(id_conta, conta) + "\n"
    return mensagem + "Contas com saldo positivo listadas com sucesso.\n"
 
 
def relatorioMaiorSaldo():
    maior, _ = encontrar_maior_menor_saldo()
    if maior is None:
        return "\nSem contas cadastradas até o momento.\n"
    return "\nCONTA COM O MAIOR SALDO\n" + _formatarConta(*maior)
 
 
def relatorioMenorSaldo():
    _, menor = encontrar_maior_menor_saldo()
    if menor is None:
        return "\nSem contas cadastradas até o momento.\n"
    return "\nCONTA COM O MENOR SALDO\n" + _formatarConta(*menor)


def dadosDashboard():
    # Reúne os números do dashboard: clientes, contas, total, maior, menor e média
    from functools import reduce
    try:
        dadosContas = _carregarContas()
    except (FileNotFoundError, json.JSONDecodeError):
        dadosContas = {}

    saldos = [c["saldo"] for c in dadosContas.values()]
    total = reduce(lambda soma, saldo: soma + saldo, saldos, 0)

    return {
        "clientes": len(cl.carregar_clientes()),
        "contas": len(saldos),
        "total": total,
        "maior": max(saldos, default=0),
        "menor": min(saldos, default=0),
        "media": total / len(saldos) if saldos else 0
    }
