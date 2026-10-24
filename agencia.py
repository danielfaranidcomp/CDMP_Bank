import json

# função interna que verifica a existência de uma agência
def existeAgencia(idAgencia):
    try:
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dadosAgencia = json.load(f)
        return dadosAgencia.get(str(idAgencia), False)
    except:
        return False


def cadastrarAgencia(endereco="Endereço não informado"):
    try: # caso já exista alguma agência cadastrada
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dadosAgencia = json.load(f)
        
        # Pega a última chave, converte para int, incrementa e converte para string
        novo_id = str(int(list(dadosAgencia)[-1]) + 1)
        
        dadosAgencia[novo_id] = {
            "endereco": endereco,
            "contasAssociadas": []
        }
        
        with open('agencias.json', 'w', encoding="utf-8") as f:
            json.dump(dadosAgencia, f, indent=2, ensure_ascii=False)       
        return f"\nAgência de id {novo_id} criada com sucesso.\n"
    
    except Exception: # caso o arquivo esteja vazio ou não exista (sendo a primeira agência)
        dadosAgencia = {
            "0": {
                "endereco": endereco,
                "contasAssociadas": []
            }
        }
        with open('agencias.json', 'w', encoding="utf-8") as f:
            json.dump(dadosAgencia, f, indent=2, ensure_ascii=False)
        return "\nAgência de id 0 criada com sucesso.\n"


def associarContaAgencia(idAgencia, idConta):
    # sem necessidade de verificações pois todas elas já serão realizadas por cadastrarConta
    with open('agencias.json', 'r', encoding="utf-8") as f:
        dadosAgencia = json.load(f)
    dadosAgencia[str(idAgencia)]["contasAssociadas"].append(idConta)
    with open('agencias.json', 'w', encoding="utf-8") as f:
        json.dump(dadosAgencia, f, indent=2, ensure_ascii=False)


def listarAgencias():
    try:
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dados_agencia = json.load(f)
        
        lista = []
        for id_ag, ag in dados_agencia.items():
            lista.append({
                "id": id_ag,
                "endereco": ag.get("endereco", "Não informado"),
                "contas_associadas": ag["contasAssociadas"]
            })
        return lista
    except:
        return []