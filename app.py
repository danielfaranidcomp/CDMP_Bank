from flask import Flask, render_template, request
import agencia
import cliente
import conta

app = Flask(__name__)

# Transforma um número em moeda brasileira. Ex: 1234.5 -> R$ 1.234,50
def moeda(valor):
    return "R$ {:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

# Os módulos devolvem textos. Aqui separamos o que é erro do que deu certo.
def resultado(mensagem):
    mensagem = mensagem.strip()
    return mensagem, not mensagem.startswith("Erro")

# Rota principal da aplicação, carrega e renderiza a página inicial HTML.

@app.route('/')
def index():
    """Página principal: menu com os cadastros e as consultas."""
    return render_template('index.html')

@app.route('/cadastrar-cliente', methods=['GET', 'POST'])
def cadastroCliente():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf = request.form.get('cpf', '').strip()
        email = request.form.get('email', '').strip()
        mensagem, sucesso = resultado(cliente.cadastrar_cliente(cpf, nome, email))
        return render_template('cadastrar-cliente.html', mensagem=mensagem, sucesso=sucesso)
    return render_template('cadastrar-cliente.html')

@app.route('/cadastrar-conta', methods=['GET', 'POST'])
def cadastroConta():
    if request.method == 'POST':
        try:
            idCliente = int(request.form.get('id-cliente', '').strip())
            idAgencia = int(request.form.get('id-agencia', '').strip())
            saldo = float(request.form.get('saldo', '').replace(',', '.'))
        except ValueError:
            return render_template('cadastrar-conta.html', sucesso=False,
                                   mensagem="Erro! Os IDs devem ser números inteiros e o saldo um valor numérico.")
        tipo = request.form.get('tipo_conta', '')
        mensagem, sucesso = resultado(conta.cadastrarConta(idCliente, idAgencia, saldo, tipo))
        return render_template('cadastrar-conta.html', mensagem=mensagem, sucesso=sucesso)
    return render_template('cadastrar-conta.html')

@app.route('/cadastrar-agencia', methods=['GET', 'POST'])
def cadastroAgencia():
    if request.method == 'POST':
        endereco = request.form.get('endereco', '').strip()
        mensagem, sucesso = resultado(agencia.cadastrarAgencia(endereco))
        return render_template('cadastrar-agencia.html', mensagem=mensagem, sucesso=sucesso)
    return render_template('cadastrar-agencia.html')

@app.route('/clientes')
def listarClientes():
    dados = cliente.carregar_clientes()
    linhas = [[id, c["nome"], c["cpf"], c["email"], ", ".join(str(x) for x in c["contas_associadas"]) or "-"]
              for id, c in dados.items()]
    return render_template('listar.html', titulo="Clientes",
                           colunas=["ID", "Nome", "CPF", "E-mail", "Contas"],
                           linhas=linhas, vazio="Nenhum cliente cadastrado até o momento.")

@app.route('/agencias')
def listarAgencias():
    linhas = [[a["id"], a["endereco"], ", ".join(str(x) for x in a["contas_associadas"]) or "-"]
              for a in agencia.listarAgencias()]
    return render_template('listar.html', titulo="Agências",
                           colunas=["ID", "Endereço", "Contas associadas"],
                           linhas=linhas, vazio="Nenhuma agência cadastrada até o momento.")

@app.route('/contas')
def listarContas():
    # Só as contas com saldo positivo, mais o resumo de saldos do banco
    positivas = conta.listar_contas_saldo_positivo()
    linhas = [[id, c["tipo"].capitalize(), c["agencia"], moeda(c["saldo"])]
              for id, c in positivas.items()]
    d = conta.dadosDashboard()
    resumo = [("Saldo Total", moeda(d["total"])),
              ("Maior Saldo", moeda(d["maior"])),
              ("Menor Saldo", moeda(d["menor"]))]
    return render_template('listar.html', titulo="Contas com Saldo Positivo", resumo=resumo,
                           colunas=["ID", "Tipo", "Agência", "Saldo"],
                           linhas=linhas, vazio="Nenhuma conta com saldo positivo.")

@app.route('/dashboard')
def dashboard():
    d = conta.dadosDashboard()
    return render_template('dashboard.html', clientes=d["clientes"], contas=d["contas"],
                           total=moeda(d["total"]), maior=moeda(d["maior"]), media=moeda(d["media"]))

if __name__ == '__main__':
    print("Servidor iniciado em http://127.0.0.1:5000")
    app.run(debug=True)
