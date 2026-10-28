import json
from flask import Flask, render_template, request, flash, redirect

######### FUNÇÕES ÚTEIS #########

#carrega o arquivo e se não existir envia um dicionário vazio
def carregarArquivos(url): 
    try:
        with open(url, 'r', encoding="utf-8") as f:
            dadosContas = json.load(f)
        return dadosContas
    except:
        return {}   

# joga o dicionário passado na url passada
def salvarArquivos(url, arquivo):
    with open(url, 'w', encoding="utf-8") as f:
        json.dump(arquivo, f, indent=2, ensure_ascii=False)

# verificador de cpf
def verificarCpf(cpf):
    digitos = list(filter(lambda x: x != '.' and x != '-', cpf))
    if len(digitos) != 11: return False
    def verificaAte(limite, digitos):
        soma = 0
        for i in range(0, limite):
            soma += int(digitos[i]) * (limite + 1 - i)
        resto = soma % 11
        return (resto < 2 and int(digitos[limite]) == 0) or (resto >= 2 and int(digitos[limite]) == 11 - resto)
    return verificaAte(9, digitos) and verificaAte(10, digitos)

def existeNoArquivo(url, termo):
    try:
        with open(url, 'r', encoding="utf-8") as f:
            dados = json.load(f)
        return dados.get(termo, False)
    except:
        return False

def retornarSaldo(idConta):
    dadosContas = carregarArquivos('contas.json')
    return float(dadosContas[str(idConta)]["saldo"])

######### ROTAS #########

app = Flask(__name__)
app.secret_key = 'naomehackeia'

# rota do index
@app.route('/')
def index():
    modal_aberto = request.args.get('modal')
    return render_template('index.html', modal_aberto=modal_aberto)

@app.route('/cadastrar-cliente', methods=['GET', 'POST'])
def cadastroCliente():
    if request.method == 'POST':
        try:
            # pega os dados
            nome = str(request.form.get('nome')).title().strip()
            cpf = str(request.form.get('cpf')).strip()
            email = str(request.form.get('email')).strip()

            # verificar cpf
            if not verificarCpf(cpf):
                flash(f"Erro: o cpf informado é inválido.", "erro")
                return redirect('/cadastrar-cliente')
            
            dadosClientes = carregarArquivos('clientes.json')
            # o id será 0 se a lista estiver vazia e o último + 1 se não estiver vazia
            id = str(int(list(dadosClientes)[-1]) + 1) if dadosClientes else "0"
            dadosClientes[id] = {"nome": nome, "cpf": cpf, "email": email, "contasAssociadas": []}
            salvarArquivos('clientes.json', dadosClientes)
            flash(f"Sucesso: cliente de id {id} cadastrado no sistema.", "sucesso")
            return redirect("/cadastrar-cliente")
        except Exception as e:
            flash(f"Erro interno: {str(e)}", "erro")
            return redirect('/cadastrar-cliente')
    else:
        return render_template('cadastrar-cliente.html')

@app.route('/cadastrar-conta', methods=['GET', 'POST'])
def cadastroConta():
    if request.method == 'POST':
        try:
            idCliente = str(request.form.get('id-cliente'))
            idAgencia = str(request.form.get('id-agencia'))
            saldo = float(request.form.get('saldo'))
            tipo = str(request.form.get('tipo'))

            # verifica existencia do cliente e da agência
            if not existeNoArquivo('clientes.json', idCliente) or not existeNoArquivo('agencias.json', idAgencia):
                flash("Erro: Agência ou Cliente informado(s) não existe(m).", "erro")
                return redirect('/cadastrar-conta')

            # adiciona ao json agora
            dadosContas = carregarArquivos('contas.json')
            dadosClientes = carregarArquivos('clientes.json')
            dadosAgencias = carregarArquivos('agencias.json')

            id = str(int(list(dadosContas)[-1]) + 1) if dadosContas else "0"
            dadosContas[id] = {"tipo": tipo, "clientesAssociados": [int(idCliente)],
                            "agencia": idAgencia, "saldo": saldo}
            dadosClientes[idCliente]["contasAssociadas"].append(int(id))#.sort()
            dadosClientes[idCliente]["contasAssociadas"].sort()
            dadosAgencias[idAgencia]["contasAssociadas"].append(int(id))#.sort()
            dadosAgencias[idAgencia]["contasAssociadas"].sort()

            salvarArquivos('contas.json', dadosContas)
            salvarArquivos('clientes.json', dadosClientes)
            salvarArquivos('agencias.json', dadosAgencias)

            flash(f"Sucesso: Conta de id {id} cadastrada no sistema.", "sucesso")
            return redirect("/cadastrar-conta")
        except Exception as e:
            flash(f"Erro interno: {str(e)}", "erro")
            return redirect('/?modal=deposito')
    else:
        return render_template('cadastrar-conta.html')

@app.route('/associar-cliente-conta', methods=['POST'])
def associarClienteConta():
    try:
        idCliente = str(request.form.get('id-cliente'))
        idConta = str(request.form.get('id-conta'))

        if not existeNoArquivo('clientes.json', idCliente) or not existeNoArquivo('contas.json', idConta):
            flash("Erro! A conta ou o cliente não existe(m) no sistema.", "erro")
            return redirect('/cadastrar-conta')

        dadosClientes = carregarArquivos('clientes.json')
        dadosContas = carregarArquivos('contas.json')

        dadosClientes[idCliente]["contasAssociadas"].append(int(idConta))
        dadosClientes[idCliente]["contasAssociadas"].sort()
        dadosContas[idConta]["clientesAssociados"].append(int(idCliente))
        dadosContas[idConta]["clientesAssociados"].sort()

        salvarArquivos('clientes.json', dadosClientes)
        salvarArquivos('contas.json', dadosContas)

        flash("Sucesso! Cliente associado à conta no sistema.", "sucesso")
        return redirect('/cadastrar-conta')
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=deposito')

@app.route('/cadastrar-agencia', methods=['GET', 'POST'])
def cadastroAgencia():
    if request.method == 'POST':
        try:
            endereco = str(request.form.get('endereco'))
            dadosAgencias = carregarArquivos('agencias.json')
            id = str(int(list(dadosAgencias)[-1]) + 1) if dadosAgencias else "0"
            dadosAgencias[id] = {"endereco": endereco, "contasAssociadas": []}
            salvarArquivos('agencias.json', dadosAgencias)
            flash("Sucesso: Agência registrada no sistema", "sucesso")
            return redirect('/cadastrar-agencia')
        except Exception as e:
            flash(f"Erro interno: {str(e)}", "erro")
            return redirect('/?modal=deposito')
    else:
        return render_template('cadastrar-agencia.html')

@app.route('/listar-clientes')
def listarClientes():
    dadosClientes = carregarArquivos('clientes.json')
    listaClientes = []
    #como o json está organizado como vários dicionários que a primeira
    #key é  o id e o valor é todas as informações, a gente concatena a key com os valores,
    #as próximas funções de listar adotarão comportamento semelhante
    for id, informacoes in dadosClientes.items():
        listaClientes.append({"id": id} | informacoes)
    return render_template('listar-clientes.html', clientes=listaClientes)

# exclui do json o cliente com o id específicado. as próximas funções de exclusão
# adotarão comportamento semelhante.
@app.route('/excluir-cliente/<id>', methods=['POST'])
def excluirCliente(id):
    try:
        dadosClientes = carregarArquivos('clientes.json')
        del dadosClientes[id]
        salvarArquivos('clientes.json', dadosClientes)
        flash(f"Sucesso: Cliente {id} removido do sistema!", "sucesso")
        return redirect('/listar-clientes')
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=deposito')


@app.route('/listar-contas')
def listarContas():
    dadosContas = carregarArquivos('contas.json')
    listaContas = []
    filtro = request.args.get('filtro')
    for id, informacoes in dadosContas.items():
        # a diferença aqui se dá na inclusão ou não do filtro de contas com saldo positivo
        if (not filtro) or (filtro == 'positivo' and informacoes["saldo"] >= 0):
            informacoes["clientesAssociados"] = str(informacoes["clientesAssociados"])
            listaContas.append({"id": id} | informacoes)
    return render_template('listar-contas.html', contas=listaContas, filtro=filtro)

@app.route('/excluir-conta/<id>', methods=['POST'])
def excluirConta(id):
    try:
        dadosContas = carregarArquivos('contas.json')
        del dadosContas[id]
        salvarArquivos('contas.json', dadosContas)
        flash(f"Sucesso: Conta {id} removida do sistema!", "sucesso")
        return redirect('/listar-contas')
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=deposito')

@app.route('/listar-agencia')
def listarAgencias():
    dadosAgencias = carregarArquivos('agencias.json')
    listaAgencias = []
    for id, informacoes in dadosAgencias.items():
        # vamos realizar a soma do montante da agencia
        montante = 0
        for idConta in informacoes["contasAssociadas"]:
            montante += retornarSaldo(idConta)
        informacoes["contasAssociadas"] = str(informacoes["contasAssociadas"])
        listaAgencias.append({"id": id, "montante": montante} | informacoes)
    return render_template('listar-agencias.html', agencias=listaAgencias)

@app.route('/excluir-agencia/<id>', methods=['POST'])
def excluirAgencia(id):
    try:
        dadosAgencias = carregarArquivos('agencias.json')
        del dadosAgencias[id]
        salvarArquivos('agencias.json', dadosAgencias)
        flash(f"Sucesso: Agencia {id} removida do sistema!", "sucesso")
        return redirect('/listar-agencia')
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=deposito')

# dashboard agora!
@app.route('/dashboard')
def dashboard():
    # primeiro vamos pegar todos os dados logo
    dadosContas = carregarArquivos('contas.json')
    dadosAgencias = carregarArquivos('agencias.json')
    dadosClientes = carregarArquivos('clientes.json')

    # cálculos!
    numClientes = len(dadosClientes)
    numContas = len(dadosContas)
    numAgencias = len(dadosAgencias)

    # vamos pegar todos os saldos e colocar numa lista e a partir disso tirar alguns dados
    # também fazer o cálculo da porcentagem de contas correntes e poupança. salário dá pra inferir
    #  a partir dos outros.
    listaSaldos = []
    corrente = 0
    poupanca = 0
    for c in dadosContas.values():
        listaSaldos.append(float(c["saldo"]))
        if c["tipo"] == "Corrente":
            corrente += 1 
        elif c["tipo"] == "Poupança":
            poupanca += 1 

    saldoTotal = sum(listaSaldos)
    saldoMedio = saldoTotal / numContas
    maiorSaldo = max(listaSaldos)
    porcCorrente = corrente / numContas * 100
    porcPoupanca = poupanca / numContas * 100 + porcCorrente

    return render_template('dashboard.html', numClientes=numClientes, numContas=numContas,
                           numAgencias=numAgencias, saldoTotal=saldoTotal, saldoMedio=saldoMedio, 
                           maiorSaldo=maiorSaldo, porcCorrente=porcCorrente, porcPoupanca=porcPoupanca)

# realizar transferência entre contas, ativada pelo envio do formulário
# as de saque e depósito adotarão comportamento semelhante.
@app.route('/transferencia', methods=['POST'])
def transferencia():
    try:
        # pega os valores
        idPagador = str(request.form.get('id-pagador'))
        idReceptor = str(request.form.get('id-receptor'))
        valor = float(request.form.get('valor'))

        # verificar se não tá tentando transferir pra mesma conta
        if idReceptor == idPagador:
            flash("Erro: você não pode transferir para a mesma conta.", "erro")
            return redirect('/?modal=transferencia')

        # verificar se o valor não é zero ou menor
        if valor <= 0:
            flash("Erro: o valor da transferência deve ser maior que zero.", "erro")
            return redirect('/?modal=transferencia')

        dadosContas = carregarArquivos('contas.json')

        # verifica se o dicionário está vazio
        if dadosContas:
            # verifica se as contas de fato existem.
            pagador = dadosContas.get(idPagador, False)
            receptor = dadosContas.get(idReceptor, False)
            if not pagador or not receptor:
                flash("Erro: as contas não existem", "erro")
                return redirect('/?modal=transferencia')

            # transferência
            dadosContas[idPagador]["saldo"] -= valor
            dadosContas[idReceptor]["saldo"] += valor

            #devolve
            salvarArquivos('contas.json', dadosContas)
            flash("Transferência realizada com sucesso!", "sucesso")
            return redirect('/?modal=transferencia')    
        flash("Erro: As contas não existem", "erro")
        return redirect('/?modal=transferencia')         
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=transferencia')

@app.route('/deposito', methods=['POST'])
def deposito():
    try:
        # pega valores
        idConta = str(request.form.get('id-conta'))
        valor = float(request.form.get('valor'))

        # deposito deve ser maior que zero
        if valor <= 0:
            flash("Erro: o valor do deposito deve ser maior que zero.", "erro")
            return redirect('/?modal=deposito')

        dadosContas = carregarArquivos('contas.json')

        # verifica se o dicionário está vazio
        if dadosContas:
            # verifica se a conta de fato existe.
            conta = dadosContas.get(idConta, False)
            if not conta:
                flash("Erro: a conta não existe", "erro")
                return redirect('/?modal=deposito')

            # deposita
            dadosContas[idConta]["saldo"] += valor

            #devolve
            salvarArquivos('contas.json', dadosContas)
            flash("Depósito realizado com sucesso!", "sucesso")
            return redirect('/?modal=deposito')    
        flash("Erro: A conta não existe", "erro")
        return redirect('/?modal=deposito')         
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=deposito')

@app.route('/saque', methods=['POST'])
def saque():
    try:
        # pega valores
        idConta = str(request.form.get('id-conta'))
        valor = float(request.form.get('valor'))

        # saque deve ser maior que zero
        if valor <= 0:
            flash("Erro: o valor do saque deve ser maior que zero.", "erro")
            return redirect('/?modal=saque')

        dadosContas = carregarArquivos('contas.json')

        # verifica se o dicionário está vazio
        if dadosContas:
            # verifica se a conta de fato existe.
            conta = dadosContas.get(idConta, False)
            if not conta:
                flash("Erro: a conta não existe", "erro")
                return redirect('/?modal=saque')

            # saque
            dadosContas[idConta]["saldo"] -= valor

            #devolve
            salvarArquivos('contas.json', dadosContas)
            flash("Saque realizado com sucesso!", "sucesso")
            return redirect('/?modal=saque')    
        flash("Erro: A conta não existe", "erro")
        return redirect('/?modal=saque')         
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=saque')

if __name__ == '__main__':
    app.run(debug=True)

