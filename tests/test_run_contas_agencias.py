import cliente, conta, agencia

# focado em testar as funcoes de agencia e conta, explorando todas as possibilidades.
# antes de realizar o teste, exclua todos os arquivos .json para aproveitamento total

def test_cpf_valido():
    assert conta.verificarCpf("063.106.910-07") == True

def test_cpf_invalido1():
    assert conta.verificarCpf("123.456.789-01") == False

def test_cpf_invaldo2():
    assert conta.verificarCpf("123") == False

def test_existe_agencia():
    assert agencia.existeAgencia(0) == False

def test_criar_agencia1():
    assert agencia.cadastrarAgencia() == "\nAgência de id 0 criada com sucesso.\n"

def test_criar_agencia2():
    assert agencia.cadastrarAgencia() == "\nAgência de id 1 criada com sucesso.\n"

def test_cadastrar_cliente():
    assert cliente.cadastrar_cliente("063.106.910-07", "daniel", "daniel@gmail.com") == "\nCliente cadastrado com sucesso. ID do cliente: 0.\n"

def test_cadastrar_conta_cliente_inexistente():
    assert conta.cadastrarConta(1, 0, 200, "corrente") == "\nErro! O cliente de id 1 não existe.\n"

def test_cadastrar_conta_agencia_inexistente():
    assert conta.cadastrarConta(0, 12, 200, "salario") == "\nErro! A agência de id 12 não existe.\n"

def test_cadastrar_conta_sucesso1():
    assert conta.cadastrarConta(0, 0, 200, "salario") == "\nConta de id 0 cadastrada com sucesso!\n"

def test_cadastrar_conta_sucesso2():
    assert conta.cadastrarConta(0, 1, 300, "corrente") == "\nConta de id 1 cadastrada com sucesso!\n"

def test_depositar_conta_salario_erro():
    assert conta.depositarConta(0, 100) == "\nErro! O tipo da conta 0 é salário. Depósitos não são possíveis\n"

def test_depositar_conta_sucesso():
    assert conta.depositarConta(1, 300) == "\nValor depositado com sucesso. Saldo atual: R$ 600.00\n"

def test_sacar_superior_erro():
    assert conta.sacarConta(0, 300000) == "\nErro! O valor R$ 300000.00 é superior ao saldo da conta. (R$ 200.00)\n"

def test_sacar_sucesso():
    assert conta.sacarConta(0, 100) == "\nSaque realizado. Saldo atual da conta 0: R$ 100.00\n"