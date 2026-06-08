# =====================================================================
#  MONITORAMENTO DE MISSAO ESPACIAL
#  GS2026.1 — Data Structure and Algorithms (FIAP)
#
#  Sistema interativo de terminal que monitora temperatura, energia e
#  comunicacao de uma missao espacial, com verificacao automatica de
#  alertas e historico de leituras. Usa listas, funcoes, condicionais
#  e laços de repeticao.
# =====================================================================

import random

# ----- Estrutura de dados principal: historico de leituras (lista/vetor) -----
# Cada leitura e um dicionario armazenado nesta lista.
historico = []

# Codigos de cor ANSI (opcional, deixa o terminal mais legivel)
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
AZUL = "\033[96m"
RESET = "\033[0m"
NEGRITO = "\033[1m"


# =====================================================================
#  ENTRADA DE DADOS
# =====================================================================
def ler_numero(mensagem, minimo, maximo):
    """Le um numero do usuario validando o intervalo permitido."""
    while True:
        try:
            valor = float(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"  {VERMELHO}Valor fora do intervalo ({minimo} a {maximo}). Tente de novo.{RESET}")
        except ValueError:
            print(f"  {VERMELHO}Entrada invalida. Digite um numero.{RESET}")


def inserir_dados_manual():
    """Opcao 1: o usuario digita os dados dos sensores."""
    print(f"\n{AZUL}--- Inserir dados manualmente ---{RESET}")
    temperatura = int(ler_numero("  Temperatura da nave (C): ", -100, 200))
    energia = int(ler_numero("  Nivel de energia (%): ", 0, 100))
    comunicacao = int(ler_numero("  Comunicacao (1 = ativa, 0 = sem sinal): ", 0, 1))
    registrar_leitura(temperatura, energia, comunicacao)
    print(f"  {VERDE}Leitura registrada com sucesso!{RESET}")


def simular_leitura():
    """Opcao 2: gera dados aleatorios simulando os sensores."""
    print(f"\n{AZUL}--- Simulando leitura dos sensores ---{RESET}")
    temperatura = random.randint(-20, 120)
    energia = random.randint(0, 100)
    comunicacao = random.choice([0, 1, 1, 1])  # falha de sinal e mais rara
    registrar_leitura(temperatura, energia, comunicacao)
    print(f"  Temperatura: {temperatura}C | Energia: {energia}% | "
          f"Comunicacao: {'ativa' if comunicacao else 'sem sinal'}")
    print(f"  {VERDE}Leitura simulada registrada!{RESET}")


def registrar_leitura(temperatura, energia, comunicacao):
    """Adiciona uma nova leitura ao historico (lista)."""
    leitura = {
        "id": len(historico) + 1,
        "temperatura": temperatura,
        "energia": energia,
        "comunicacao": comunicacao,
    }
    historico.append(leitura)


# =====================================================================
#  VERIFICACAO AUTOMATICA (regras de alerta)
# =====================================================================
def analisar_leitura(leitura):
    """Aplica as regras de alerta e devolve (lista_de_alertas, status)."""
    alertas = []

    if leitura["temperatura"] > 80:
        alertas.append("ALERTA DE SUPERAQUECIMENTO (temperatura acima de 80C)")
    if leitura["energia"] < 20:
        alertas.append("MODO DE ECONOMIA DE ENERGIA (energia abaixo de 20%)")
    if leitura["comunicacao"] == 0:
        alertas.append("FALHA DE COMUNICACAO (sem sinal com a base)")

    # Status operacional derivado da quantidade de alertas
    if len(alertas) == 0:
        status = "OPERACIONAL"
    elif len(alertas) == 1:
        status = "EM ATENCAO"
    else:
        status = "CRITICO"

    return alertas, status


def cor_status(status):
    if status == "OPERACIONAL":
        return VERDE
    if status == "EM ATENCAO":
        return AMARELO
    return VERMELHO


# =====================================================================
#  EXIBICAO
# =====================================================================
def exibir_leitura(leitura):
    alertas, status = analisar_leitura(leitura)
    com_txt = "ativa" if leitura["comunicacao"] else "sem sinal"
    print(f"  Leitura #{leitura['id']}")
    print(f"    Temperatura : {leitura['temperatura']}C")
    print(f"    Energia     : {leitura['energia']}%")
    print(f"    Comunicacao : {com_txt}")
    print(f"    Status      : {cor_status(status)}{status}{RESET}")
    if alertas:
        for a in alertas:
            print(f"      {VERMELHO}>> {a}{RESET}")


def visualizar_status():
    """Opcao 3: mostra a leitura mais recente."""
    print(f"\n{AZUL}--- Status atual ---{RESET}")
    if not historico:
        print(f"  {AMARELO}Nenhuma leitura registrada ainda.{RESET}")
        return
    exibir_leitura(historico[-1])


def executar_analise():
    """Opcao 4: analisa todas as leituras do historico."""
    print(f"\n{AZUL}--- Analise de todas as leituras ---{RESET}")
    if not historico:
        print(f"  {AMARELO}Nenhuma leitura para analisar.{RESET}")
        return
    criticos = 0
    for leitura in historico:
        alertas, status = analisar_leitura(leitura)
        if status == "CRITICO":
            criticos += 1
        exibir_leitura(leitura)
        print()
    print(f"  Total de leituras: {len(historico)} | "
          f"Leituras criticas: {criticos}")


def exibir_historico():
    """Opcao 5: lista resumida de todas as leituras."""
    print(f"\n{AZUL}--- Historico das leituras ---{RESET}")
    if not historico:
        print(f"  {AMARELO}Historico vazio.{RESET}")
        return
    for leitura in historico:
        _, status = analisar_leitura(leitura)
        com_txt = "ativa" if leitura["comunicacao"] else "sem sinal"
        print(f"  #{leitura['id']:>2} | Temp: {leitura['temperatura']:>4}C | "
              f"Energia: {leitura['energia']:>3}% | Com: {com_txt:>9} | "
              f"{cor_status(status)}{status}{RESET}")


# =====================================================================
#  MENU PRINCIPAL
# =====================================================================
def mostrar_menu():
    print(f"\n{NEGRITO}{'=' * 50}{RESET}")
    print(f"{NEGRITO}   MONITORAMENTO DE MISSAO ESPACIAL{RESET}")
    print(f"{NEGRITO}{'=' * 50}{RESET}")
    print("  1 - Inserir dados manualmente")
    print("  2 - Simular leitura dos sensores")
    print("  3 - Visualizar status atual")
    print("  4 - Executar analise")
    print("  5 - Historico das leituras")
    print("  0 - Encerrar sistema")


def main():
    print(f"{VERDE}Bem-vindo ao Mission Control AI!{RESET}")
    while True:
        mostrar_menu()
        opcao = input("  Escolha uma opcao: ").strip()

        if opcao == "1":
            inserir_dados_manual()
        elif opcao == "2":
            simular_leitura()
        elif opcao == "3":
            visualizar_status()
        elif opcao == "4":
            executar_analise()
        elif opcao == "5":
            exibir_historico()
        elif opcao == "0":
            print(f"\n{VERDE}Encerrando o sistema. Missao concluida!{RESET}")
            break
        else:
            print(f"  {VERMELHO}Opcao invalida. Escolha um numero do menu.{RESET}")


if __name__ == "__main__":
    main()
