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
        print("Depósito")

    elif opcao == "s":
        print("Saque")

    elif opcao == "e":
        print("Extrato")

    elif opcao == "q":
        print("Encerrando programa... Obrigado por utilizar nosso banco!")
        break

    else:
        print("OPÇÃO INVÁLIDA! Por favor, digite uma opção da lista.")


