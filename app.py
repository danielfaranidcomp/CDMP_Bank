import json
from flask import Flask, render_template, request, flash, redirect
from models.contas import ContaCorrente, ContaPoupanca
from models.clientes import Cliente

######### FUNÇÕES ÚTEIS #########
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

def novoId(lista):
    if not lista:
        return 0
    return lista[-1].id + 1

def buscaObjeto(id, lista):
    for item in lista:
        if item.id == id: return item
    return False

def dicionarizar(lista):
    lista_dicionarios = []
    for item in lista:
        lista_dicionarios.append(item.trans_dict())
    return lista_dicionarios


# criando uma lista com os objetos
lista_clientes = []
lista_contas = []

def finaliza_json():
    global lista_clientes, lista_contas

    with open('json/clientes.json', 'w', encoding="utf-8") as f:
        json.dump(dicionarizar(lista_clientes), f, indent=2, ensure_ascii=False)

    with open('json/contas.json', 'w', encoding="utf-8") as f:
        json.dump(dicionarizar(lista_contas), f, indent=2, ensure_ascii=False)

def inicializa_json():
    global lista_clientes, lista_contas

    # jogando os clientes em lista_clientes
    try: 
        with open('json/clientes.json', 'r', encoding="utf-8") as f:
            json_clientes = json.load(f)
        for cliente in json_clientes:
            novo_cliente = Cliente(cliente['id'], cliente['nome'], cliente['cpf'],
                                cliente['email'])
            lista_clientes.append(novo_cliente)
    except:
        pass
        
    # agora jogando as contas
    try:
        with open('json/contas.json', 'r', encoding="utf-8") as f:
            json_contas = json.load(f)
        for conta in json_contas:
            if conta['tipo'] == 'Corrente':
                nova_conta = ContaCorrente(conta['id'], conta['cliente'], conta['saldo'])
            else:
                nova_conta = ContaPoupanca(conta['id'], conta['cliente'], conta['saldo'])
            lista_contas.append(nova_conta)
    except:
        pass

inicializa_json()



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
            
            id = novoId(lista_clientes)
            novo_cliente = Cliente(id, nome, cpf, email)
            lista_clientes.append(novo_cliente)

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
            idCliente = int(request.form.get('id-cliente'))
            saldo = float(request.form.get('saldo'))
            tipo = str(request.form.get('tipo'))

            cliente = buscaObjeto(idCliente, lista_clientes)

            # verifica existencia do cliente
            if not cliente:
                flash("Erro: Cliente informado não existe.", "erro")
                return redirect('/cadastrar-conta')

            # cria e associar em cliente
            id = novoId(lista_contas)
            if tipo == 'Corrente':
                nova_conta = ContaCorrente(id, idCliente, saldo)
            else:
                nova_conta = ContaPoupanca(id, idCliente, saldo)
            lista_contas.append(nova_conta)
            cliente.lista_contas.append(id)

            # pronto
            flash(f"Sucesso: Conta de id {id} cadastrada no sistema.", "sucesso")
            return redirect("/cadastrar-conta")
        except Exception as e:
            flash(f"Erro interno: {str(e)}", "erro")
            return redirect('/cadastrar-conta')
    else:
        return render_template('cadastrar-conta.html')


@app.route('/listar-clientes')
def listarClientes():
    clientes_dict = dicionarizar(lista_clientes)
    return render_template('listar-clientes.html', clientes=clientes_dict)


@app.route('/excluir-cliente/<id>', methods=['POST'])
def excluirCliente(id):
    try:
        for cliente in lista_clientes:
            if cliente.id == int(id): lista_clientes.remove(cliente)
        flash(f"Sucesso: Cliente {id} removido do sistema!", "sucesso")
        return redirect('/listar-clientes')
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=deposito')


@app.route('/listar-contas')
def listarContas():
    contas_dict = dicionarizar(lista_contas)
    filtro = request.args.get('filtro')
    if filtro:
        for conta in contas_dict:
            if conta['saldo'] < 0: contas_dict.remove(conta)
    return render_template('listar-contas.html', contas=contas_dict, filtro=filtro)


@app.route('/excluir-conta/<id>', methods=['POST'])
def excluirConta(id):
    try:
        for conta in lista_contas:
            if conta.id == int(id): lista_contas.remove(conta)
        flash(f"Sucesso: Conta {id} removida do sistema!", "sucesso")
        return redirect('/listar-contas')
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=deposito')


# dashboard agora!
@app.route('/dashboard')
def dashboard():
    # cálculos!
    numClientes = len(lista_clientes)
    numContas = len(lista_contas)
    numAgencias = 1

    # vamos pegar todos os saldos e colocar numa lista e a partir disso tirar alguns dados
    # também fazer o cálculo da porcentagem de contas correntes e poupança. a porc de poupanca
    # se infere a partir de corrente
    listaSaldos = []
    corrente = 0

    for conta in lista_contas:
        listaSaldos.append(float(conta.saldo))
        if conta.retornar_tipo() == "Corrente":
            corrente += 1 


    saldoTotal = sum(listaSaldos)
    saldoMedio = saldoTotal / numContas
    maiorSaldo = max(listaSaldos)
    porcCorrente = corrente / numContas * 100
    porcPoupanca = 100 - porcCorrente

    return render_template('dashboard.html', numClientes=numClientes, numContas=numContas,
                           numAgencias=numAgencias, saldoTotal=saldoTotal, saldoMedio=saldoMedio, 
                           maiorSaldo=maiorSaldo, porcCorrente=porcCorrente, porcPoupanca=porcPoupanca)


# realizar transferência entre contas, ativada pelo envio do formulário
# as de saque e depósito adotarão comportamento semelhante.
@app.route('/transferencia', methods=['POST'])
def transferencia():
    try:
        # pega os valores
        idPagador = int(request.form.get('id-pagador'))
        idReceptor = int(request.form.get('id-receptor'))
        valor = float(request.form.get('valor'))

        # verificar se não tá tentando transferir pra mesma conta
        if idReceptor == idPagador:
            flash("Erro: você não pode transferir para a mesma conta.", "erro")
            return redirect('/?modal=transferencia')

        # verificar se o valor não é zero ou menor
        if valor <= 0:
            flash("Erro: o valor da transferência deve ser maior que zero.", "erro")
            return redirect('/?modal=transferencia')

        # verifica se as contas de fato existem.
        pagador = buscaObjeto(idPagador, lista_contas)
        receptor = buscaObjeto(idReceptor, lista_contas)
        if not pagador or not receptor:
            flash("Erro: as contas não existem", "erro")
            return redirect('/?modal=transferencia')

        # transferência
        pagador.transferir(valor, receptor)
        flash("Transferência realizada com sucesso!", "sucesso")
        return redirect('/?modal=transferencia')       
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=transferencia')

@app.route('/deposito', methods=['POST'])
def deposito():
    try:
        # pega valores
        idConta = int(request.form.get('id-conta'))
        valor = float(request.form.get('valor'))

        # deposito deve ser maior que zero
        if valor <= 0:
            flash("Erro: o valor do deposito deve ser maior que zero.", "erro")
            return redirect('/?modal=deposito')

        conta = buscaObjeto(idConta, lista_contas)
        if not conta:
            flash("Erro: a conta não existe", "erro")
            return redirect('/?modal=deposito')

        # deposita
        conta.depositar(valor)
        flash("Depósito realizado com sucesso!", "sucesso")
        return redirect('/?modal=deposito')        
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=deposito')


@app.route('/saque', methods=['POST'])
def saque():
    try:
        # pega valores
        idConta = int(request.form.get('id-conta'))
        valor = float(request.form.get('valor'))

        # saque deve ser maior que zero
        if valor <= 0:
            flash("Erro: o valor do saque deve ser maior que zero.", "erro")
            return redirect('/?modal=saque')

        conta = buscaObjeto(idConta, lista_contas)
        if not conta:
            flash("Erro: a conta não existe", "erro")
            return redirect('/?modal=saque')

        # saque
        conta.sacar(valor)
        flash("Saque realizado com sucesso!", "sucesso")
        return redirect('/?modal=saque')          
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "erro")
        return redirect('/?modal=saque')


@app.route('/salvar-dados', methods=['POST'])
def salvar():
    finaliza_json()
    flash("Dados salvos com sucesso!", "sucesso")
    return redirect('/')   


if __name__ == '__main__':
    app.run(debug=True)

