import json
import conta

""" agencia.json funcionará da seguinte forma: id da agência, número n de contas
associadas à agência, próximos n itens serão a relação no seguinte formato:
'idAgencia: idConta' """

def criarNovaAgencia():
    try:
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dadosAgencia = json.load(f)
        # descobrir o último id registrado
        if dadosAgencia[-1] == 0: # verifica se a última agencia nao tem nenhuma conta associada
            id = dadosAgencia[-2] + 1
        else:
            id = int(list(dadosAgencia[-1])[0]) + 1
        dadosAgencia.extend([id, 0]) 
        with open('agencias.json', 'w', encoding="utf-8") as f:
            json.dump(dadosAgencia, f, indent=1, ensure_ascii=False)
        return f"\nAgência cadastrada com sucesso. Id da agência: {id}.\n"
    except:
        with open('agencias.json', 'w', encoding="utf-8") as f:
            json.dump([0, 0], f, indent=1, ensure_ascii=False)
        return f"\nAgência cadastrada com sucesso. Id da agência: 0.\n"


def associarContaAgencia(idAgencia, idConta, indexAgencia):
    # não precisamos verificar se a conta nem a agencia existe porque essa 
    # função só será chamado no momento da criação da conta, com a agencia verificada.
    with open('agencias.json', 'r', encoding="utf-8") as f:
        dadosAgencia = json.load(f)
    # vamos fazer a inserção ORDENADA
    indexFinal = indexAgencia + dadosAgencia[indexAgencia-1] 
    dadosAgencia[indexAgencia-1] += 1 # aumenta o número n de contas associadas à agência
    ehUltimo = True
    for indexAgencia in range(indexAgencia, indexFinal):
        idAtual = int(list(dadosAgencia[indexAgencia])[2])
        if idConta < idAtual and ehUltimo: # esse ehUltimo é pra n repetir
            dadosAgencia.insert(indexAgencia, f"{idAgencia}:{idConta}")
            ehUltimo = False
        elif (indexAgencia + 1) == indexFinal: # se está no final
            indexAgencia += 1
    if ehUltimo:
        dadosAgencia.insert(indexAgencia, f"{idAgencia}:{idConta}")
    with open('agencias.json', 'w', encoding="utf-8") as f:
        json.dump(dadosAgencia, f, indent=1, ensure_ascii=False)
    return f"\nConta de id {idConta} associada à agência de id {idAgencia} com sucesso.\n"


def montanteAgencia(idAgencia):
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

    # começar a análise do montante:
    montante = 0
    if dadosAgencia[i-1]:
        indexFinal = i + dadosAgencia[i-1]
        for i in range(i, indexFinal):
            idAtual = int(list(dadosAgencia[i])[2])
            montante += conta.consultarSaldo(idAtual, True)
        return f"\nO montante da agência de id {idAgencia} é R$ {montante}\n"
    else:
        return f"\nO montante da agência de id {idAgencia} é R$ 0.00\n"


def listarAgencias():
    try:
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dadosAgencias = json.load(f)

        i = 0
        while i < len(dadosAgencias):
            print(f"\nAGÊNCIA DE ID: {dadosAgencias[i]}")
            print(f"Contas associadas à agência: ", end="")
            i += 1
            if (dadosAgencias[i]):
                i += 1
                final = i + dadosAgencias[i-1]
                for i in range(i, final):
                    contaAtual = int(list(dadosAgencias[i])[2])
                    if i != (final - 1):
                        print(f"{contaAtual}, ", end="")
                    else:
                        print(f"{contaAtual}.")
            else:
                print("Nenhuma.")
            i+= 1
        return "\nContas listadas com sucesso.\n"
            
    except:
        return "\nSem agências cadastradas até o momento.\n"

def relatorioBanco():
    try:
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dadosAgencias = json.load(f)

        i = 0
        while i < len(dadosAgencias):
            # imprime o motante da agência atual
            print(montanteAgencia(dadosAgencias[i]))
            i += dadosAgencias[i+1] + 2 # calcula a posição do próximo id

        # apresenta o montante total do banco
        print(conta.montanteTotal())
        return "\nRelatório do banco exibido com sucesso.\n"
    except:
        return "\nNão foi possível exibir o relatório do banco.\n"