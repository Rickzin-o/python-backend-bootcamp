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


def aplicar_deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"- DEPÓSITO: \tR${valor:.2f}\n"
        print(f"== Você depositou com sucesso R${valor:.2f} ==")
    else:
        print("> ERRO! Você não pode depositar este valor! <")

    return saldo, extrato
        


def aplicar_saque(*, saldo, valor, extrato, limite, numero_de_saques, limite_saques):
    if numero_de_saques >= limite_saques:
        print("Parece que você atingiu seu limite de saques diários.")
        return saldo, extrato
        
    if valor <= saldo and valor <= limite and valor > 0:
        saldo -= valor
        extrato += f"- SAQUE: \tR${valor:.2f}\n"
        print(f"Você sacou com sucesso R${valor:.2f}")
    elif valor > limite:
        print(f"> Você só pode sacar um valor máximo de R${limite:.2f} <")
    elif valor > saldo:
        print(f"> ERRO! Saldo insuficiente! <")
    else:
        print("> ERRO! Você não pode sacar este valor! <")

    return saldo, extrato


def retornar_extrato(saldo, /, *, extrato):
    print(" EXTRATO ".center(50, "-"))
    print("Você não realizou operações" if extrato == "" else extrato)
    print(f"=> SALDO TOTAL: R${saldo:.2f}")
    print("-" * 50)


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("\n> Este usuário já está cadastrado! <")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/uf): ")

    usuarios.append({"nome": nome, "cpf": cpf, "data_de_nascimento": data_nascimento, "endereco": endereco})

    print("== Usuário criado com sucesso! ==")


def filtrar_usuarios(cpf, usuarios):
    filtro_usuarios = [user for user in usuarios if user['cpf'] == cpf]
    return filtro_usuarios[0] if filtro_usuarios else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print(f'== Conta {numero_conta} criada com sucesso! ==')
        return {"agencia": agencia, "numero_da_conta": numero_conta, "usuario": usuario}

    print("> ERRO! Este CPF não está cadastrado no sistema! ==")


def listar_contas(contas):
    for conta in contas:
        texto = f"""
Agência: \t{conta['agencia']}
C/C: \t\t{conta['numero_da_conta']}
Titular: \t{conta['usuario']['nome']}
"""
        print("-" * 40)
        print(texto)


def main():
    AGENCIA = "0001"
    LIMITE_POR_SAQUE = 500
    LIMITE_DE_SAQUES = 3
    
    saldo = 0
    numero_saques = 0
    extrato = ""
    usuarios = []
    contas = []

    while True:
        opcao = mostrar_menu()
        print()

        if opcao == "d":
            deposito = float(input("Insira um valor de depósito: "))
            movimentacao = aplicar_deposito(saldo, deposito, extrato)
            if movimentacao:
                saldo, extrato = movimentacao


        elif opcao == "s":
            saque = float(input("Insira um valor de saque: "))
            movimentacao = aplicar_saque(saldo=saldo, valor=saque, extrato=extrato, limite=LIMITE_POR_SAQUE,
                                         numero_de_saques=numero_saques, limite_saques=LIMITE_DE_SAQUES)
            if movimentacao:
                saldo, extrato = movimentacao
                numero_saques += 1


        elif opcao == "e":
            retornar_extrato(saldo, extrato=extrato)


        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)


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
