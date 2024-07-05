import abc


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self. data_nascimento = data_nascimento


class Transacao(abc.ABC):
    @property
    @abc.abstractproperty
    def valor(self):
        pass

    @abc.abstractclassmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor
            }
        )


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print(f"> ERRO! Saldo insuficiente! <")
        elif valor < 0:
            print("> ERRO! Você não pode sacar este valor! <")
        else:
            self._saldo -= valor
            print(f"Você sacou com sucesso R${valor:.2f}")
            return True

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"== Você depositou com sucesso R${valor:.2f} ==")
            return True
        else:
            print("> ERRO! Você não pode depositar este valor! <")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if valor > self._limite:
            print(f"> Você só pode sacar um valor máximo de R${self._limite:.2f} <")
        elif numero_saques > self._limite_saques:
            print("> Parece que você atingiu seu limite de saques diários! <")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
Agência: \t{self.agencia}
C/C: \t\t{self.numero}
Titular: \t{self.cliente.nome}
"""



def mostrar_menu():
    print(" BEM-VINDO AO BANCO ".center(50, "="))
    menu = """
* Escolha uma operação *
[d] Depósito
[s] Saque
[e] Extrato
[nc] Nova Conta
[lc] Listar Contas
[nu] Novo Usuário
[q] Sair

==> """

    return input(menu)


def get_conta_cliente(cliente):
    if not cliente.contas:
        print("> ERRO! Este usuário não possui uma conta no sistema! <")
        return None
    return cliente.contas[0]


def aplicar_deposito(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_usuarios(cpf, clientes)
    if not cliente:
        print("> ERRO! Este CPF não está cadastrado no sistema! <")
        return
    
    deposito = float(input("Insira um valor de depósito: "))
    transacao = Deposito(deposito)

    conta = get_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def aplicar_saque(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_usuarios(cpf, clientes)
    if not cliente:
        print("> ERRO! Este CPF não está cadastrado no sistema! <")
        return
    
    saque = float(input("Insira um valor de saque: "))
    transacao = Saque(saque)

    conta = get_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def retornar_extrato(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_usuarios(cpf, clientes)
    if not cliente:
        print("> ERRO! Este CPF não está cadastrado no sistema! <")
        return

    conta = get_conta_cliente(cliente)
    if not conta:
        return

    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas transações")
    else:
        extrato = ""
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo'].upper()}:\n\tR${transacao['valor']:.2f}"
        
        print(" EXTRATO ".center(50, "-"))
        print(extrato)
        print(f"\n=> SALDO TOTAL: R${conta.saldo:.2f}")
        print("-" * 50)


def criar_usuario(clientes):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuarios(cpf, clientes)

    if usuario:
        print("\n> Este usuário já está cadastrado! <")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/uf): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, endereco=endereco, cpf=cpf)
    clientes.append(cliente)
    
    print("== Usuário criado com sucesso! ==")


def filtrar_usuarios(cpf, usuarios):
    filtro_usuarios = [user for user in usuarios if user.cpf == cpf]
    return filtro_usuarios[0] if filtro_usuarios else None


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuarios(cpf, clientes)

    if not usuario:
        print("> ERRO! Este CPF não está cadastrado no sistema! <")
        return

    nova_conta = ContaCorrente.nova_conta(numero_conta, usuario)
    usuario.adicionar_conta(nova_conta)
    contas.append(nova_conta)
    print(f'== Conta {numero_conta} criada com sucesso! ==')


def listar_contas(contas):
    for conta in contas:
        print("-" * 50)
        print(str(conta))


def main():
    usuarios = []
    contas = []

    while True:
        opcao = mostrar_menu()
        print()

        if opcao == "d":
            aplicar_deposito(usuarios)


        elif opcao == "s":
            aplicar_saque(usuarios)


        elif opcao == "e":
            retornar_extrato(usuarios)


        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)


        elif opcao == "nu":
            criar_usuario(usuarios)


        elif opcao == "q":
            print("Encerrando programa... Obrigado por utilizar nosso banco!")
            break


        else:
            print("OPÇÃO INVÁLIDA! Por favor, digite uma opção da lista.")

main()
