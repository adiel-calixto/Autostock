import time
from typing import TypeAlias
from sqlalchemy import or_, select
from db import DB
import os
from shared.models import Product


ListaProdutos: TypeAlias = list[tuple[Product, int]]

session = DB.get_session()


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def auto_atendimento():
    opcao = -1

    while opcao != 0:
        print_inicio()

        opcao = int(input())

        if opcao == 1:
            iniciar_compra()
        elif opcao != 0:
            print("Opção inválida")
            pausa()

        limpar_tela()

    print("Encerrando...")


def print_inicio():
    print("--------- AUTO ATENDIMENTO ---------")
    print("1: Iniciar compra")
    print("0: Sair")
    print("------------------------------------")


def iniciar_compra():
    produtos_selecionados: ListaProdutos = []
    opcao = -1
    valor_total = lambda: sum([product.price * quantity for [product, quantity] in produtos_selecionados])

    limpar_tela()

    while opcao != 0:
        print("--------- CARRINHO ---------")
        print("1: Adicionar produto")
        print("0: Finalizar")
        print("\nValor total: R$%.2f | Quantidade de itens: %d" % (valor_total(), len(produtos_selecionados)))
        print("------------------------------------")

        imprimir_carrinho(produtos_selecionados)

        if len(produtos_selecionados) > 0:
            print("------------------------------------")

        opcao = int(input("Opção: "))

        if opcao == 1:
            adicionar_produto(produtos_selecionados)
        elif opcao != 0:
            print("Opção inválida")
            pausa()

        limpar_tela()


def adicionar_produto(lista_produtos: ListaProdutos):
    cod = input("Insira o nome/código de um produto: ")

    session = DB.get_session()
    stmt = select(Product).where(or_(Product.name.like(f"{cod}%"), Product.ref == cod))

    produto = session.scalars(stmt).first()

    if produto == None:
        print("Produto não encontrado")
        pausa()
        return

    print(f"Produto: {produto.name}, Preço: {produto.price}")

    quantidade = int(input("Quantidade (digite 0 para cancelar): "))

    if quantidade == 0:
        return

    idx = -1

    for i, [p, _] in enumerate(lista_produtos):
        if p.id == produto.id:
            idx = i

    if idx == -1:
        lista_produtos.append((produto, quantidade))
    else:
        lista_produtos[idx] = (produto, quantidade + lista_produtos[idx][1])


def imprimir_carrinho(lista_produtos: ListaProdutos):
    for [p, q] in lista_produtos:
        print("ID: %d | Produto: %s, Quantidade: %d" % (p.id, p.name, q))


def pausa():
    time.sleep(1.5)


if __name__ == "__main__":
    auto_atendimento()
