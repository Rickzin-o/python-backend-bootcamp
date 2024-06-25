print(" BEM-VINDO AO BANCO ".center(50, "="))
menu = """
* Escolha uma operação *
[d] Depósito
[s] Saque
[e] Extrato
[q] Sair

==> """

saldo = 0
numero_saques = 0
LIMITE_POR_SAQUE = 500
LIMITE_DE_SAQUES = 3
extrato = ""

while True:
    opcao = input(menu).strip()
    print()

    if opcao == "d":
        deposito = float(input("Insira um valor de depósito: "))
        if deposito > 0:
            saldo += deposito
            print(f"Você depositou com sucesso R${deposito:.2f}")
            extrato += f"- DEPÓSITO: R${deposito:.2f}\n"
            
        else:
            print("ERRO! Você não pode depositar este valor!")


    elif opcao == "s":
        if numero_saques >= 3:
            print("Parece que você atingiu seu limite de saques diários.")
            continue
        
        saque = float(input("Insira um valor de saque: "))
        if saque <= saldo and saque <= LIMITE_POR_SAQUE and saque > 0:
            saldo -= saque
            numero_saques += 1
            print(f"Você sacou com sucesso R${saque:.2f}")
            extrato += f"- SAQUE: R${saque:.2f}\n"
            
        elif saque > LIMITE_POR_SAQUE:
            print(f"Você só pode sacar um valor máximo de R${LIMITE_POR_SAQUE:.2f}")

        elif saque > saldo:
            print("SALDO INSUFICIENTE!")

        else:
            print("ERRO! Você não pode sacar este valor!")


    elif opcao == "e":
        print(" EXTRATO ".center(50, "-"))
        print("Você não realizou operações" if extrato == "" else extrato)
        print(f"=> SALDO TOTAL: R${saldo:.2f}")
        print("-" * 50)


    elif opcao == "q":
        print("Encerrando programa... Obrigado por utilizar nosso banco!")
        break


    else:
        print("OPÇÃO INVÁLIDA! Por favor, digite uma opção da lista.")


