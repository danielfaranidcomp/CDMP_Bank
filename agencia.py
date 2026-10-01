import json

# função interna que verifica a existência de uma agência
def existeAgencia(idAgencia):
    try:
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dadosAgencia = json.load(f)
        return dadosAgencia.get(str(idAgencia), False)
    except:
        return False


def cadastrarAgencia():
    try: # caso já exista alguma agência
        with open('agencias.json', 'r', encoding="utf-8") as f:
            dadosAgencia = json.load(f)
        id = int(list(dadosAgencia)[-1]) + 1
        dadosAgencia[id] = {"contasAssociadas": []}
        with open('agencias.json', 'w', encoding="utf-8") as f:
            json.dump(dadosAgencia, f, indent=2, ensure_ascii=False)       
        return f"\nAgência de id {id} criada com sucesso.\n"
    except: # sendo a primeira agência
        dadosAgencia = {"0": {"contasAssociadas": []}}
        with open('agencias.json', 'w', encoding="utf-8") as f:
            json.dump(dadosAgencia, f, indent=2, ensure_ascii=False)


def associarContaAgencia(idAgencia, idConta):
    # sem necessidade de verificações pois todas elas já serão realizadas por cadastrarConta
    with open('agencias.json', 'r', encoding="utf-8") as f:
        dadosAgencia = json.load(f)
    dadosAgencia[str(idAgencia)]["contasAssociadas"].append(idConta)
    with open('agencias.json', 'w', encoding="utf-8") as f:
        json.dump(dadosAgencia, f, indent=2, ensure_ascii=False)
