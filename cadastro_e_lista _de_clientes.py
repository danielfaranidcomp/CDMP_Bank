
#importar o json
import json
# funcao que cadastra clientes e verifica se eles ja estao cadastrados
def cadastrar_cliente(cpf,nome,email):
    cpf=str(cpf)
    try:
        with open("clientes.json","r", encoding="utf-8") as f:
            dadosClientes = json.load(f)
        # Aqui o laço vai de 4 em 4 ver se os dados ja estao cadastrados  
        for i in range(0, len(dadosClientes), 4):
            if dadosClientes[i + 2] == cpf:
              print( f" Erro! O CPF '{cpf}' já está cadastrado no sistema.")    
            return
        idnovo= dadosClientes[-4]+1
        dadosClientes.extend([idnovo,nome,cpf,email])
        
        with open('clientes.json', 'w', encoding="utf-8") as f:
            json.dump(dadosClientes, f, indent=1, ensure_ascii=False)
            
        print (f"Cliente cadastrado com sucesso. ID do cliente: {idnovo}.")

    except:
        # Se o arquivo não existir ou estiver vazio, cadastra o primeiro cliente 
        with open('clientes.json', 'w', encoding="utf-8") as f:
            json.dump([0, nome, cpf, email], f, indent=1, ensure_ascii=False)
            
        return "Cliente cadastrado com sucesso. ID do cliente: 0."
    
    
def listarclientes(): 
    # A lista vai passar de 4 em 4 e mostrar suas posiçoes
    try:
        with open('clientes.json', 'r', encoding="utf-8") as f:
            dadosClientes = json.load(f)
    # A condição ve se o cliente não  esta cadastrado
        if not dadosClientes:
            print ("Nenhum cliente cadastrado até o momento!")
            return
        for i in range(0, len(dadosClientes), 4):
            print(f"CLIENTE DE ID: {dadosClientes[i]}")
            print(f"Nome: {dadosClientes[i+1]}")
            print(f"CPF: {dadosClientes[i+2]}")
            print(f"E-mail: {dadosClientes[i+3]}")

        print (f"Clientes listados com sucesso.")

    except:
        print (f"Nenhum cliente cadastrado até o momento!")   