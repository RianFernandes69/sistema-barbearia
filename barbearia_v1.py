
# SISTEMA DE BARBEARIA V1.0
from datetime import datetime

# VARIÁVEIS

barbeiro = 'Danilo'
clientes = []
servicos = [
    'Corte',
    'Sobrancelha',
    'Barba',
    'Corte + Barba',
    'Cabelo + Sobrancelha',
    'Sobrancelha + Barba'
]

agendamentos = []

horarios_disponiveis = [
    '08:00',
    '09:00',
    '10:00',
    '11:00',
    '13:00',
    '14:00',
    '15:00',
    '16:00',
    '17:00'
]

# FUNÇÕES

def mostrar_servicos():
    print('\n=== SERVIÇOS DISPONÍVEIS ===')

    for servico in servicos:
        print(servico)

# BARBEIRO RESPONSÁVEL

def mostrar_barbeiro():
    print('=== BARBEIRO RESPONSÁVEL ===')
    print(f'Barbeiro responsável: {barbeiro}')

# CADASTRO DO CLIENTE

def cadastrar_cliente(nome):
    if nome not in clientes:
        clientes.append(nome)
        print('Cliente cadastrado com sucesso!')
    else:
        print('Cliente já cadastrado!')

# FUNÇÃO PARA REALIZAR UM NOVO AGENDAMENTO

def realizar_agendamento():
    nome_cliente = input('Qual o seu nome? ').lower().strip().title()

    if not nome_cliente:
        print('Nome inválido!')
        return

    print('---------------------------------------------------')

    mostrar_servicos()
    mostrar_barbeiro()

    servico_escolhido = input('Qual serviço deseja agendar? ').lower().strip().title()

    servico_encontrado = False

    for servico in servicos:
        if servico == servico_escolhido:
            servico_encontrado = True
            print('Serviço encontrado!')
            break

    if not servico_encontrado:
        print('Serviço inexistente!')
        return

    data_escolhida = input('Qual data deseja agendar? ').lower().strip().title()

    # VALIDAÇÃO DA DATA

    try:
        data_valida = datetime.strptime(data_escolhida, '%d/%m/%Y')
        if data_valida.date() < datetime.now().date():
            print('Não é possível agendar em uma data passada!')
            return
        data_escolhida = data_valida.strftime('%d/%m/%Y')

    except ValueError:
        print('Data inválida!')
        return

    mostrar_horarios(data_escolhida)

    horario_escolhido = input('Qual horário deseja agendar? ').strip()

    agendamento_cliente = [
        nome_cliente,
        servico_escolhido,
        data_escolhida,
        horario_escolhido,
        barbeiro
    ]

    # VALIDAR O HORÁRIO

    if horario_escolhido in horarios_disponiveis:
        print('Horário permitido!')

    else:
        print('Horário inválido!')
        return

    if verificar_disponibilidade(data_escolhida, horario_escolhido, barbeiro):
        print('Horário disponível!')
        cadastrar_cliente(nome_cliente)
        agendamentos.append(agendamento_cliente)
    else:
        print('Esse horário já está ocupado!')

    print('---------------------------------------------------')


# VERIFICAR DISPONIBILIDADE

def verificar_disponibilidade(data,horario,barbeiro):
    for agendamento in agendamentos:
        if (
            agendamento[3] == horario
            and agendamento[2] == data
            and agendamento[4] == barbeiro
        ):
            return False

    return True


# REAGENDAMENTO

def verificar_disponibilidade_reagendamento(novo_agendamento, agendamento_original):
    for agendamento in agendamentos:
        if agendamento is not agendamento_original:
            if (
                agendamento[3] == novo_agendamento[3]
                and agendamento[2] == novo_agendamento[2]
                and agendamento[4] == novo_agendamento[4]
            ):
                return False
    return True


def reagendar():
    nome_cliente = input('Qual o seu nome? ').lower().strip().title()
    if not nome_cliente:
        print('Nome inválido!')
        return
    data_atual = input('Qual a data do seu agendamento? ').strip()
    try:
        data_validada = datetime.strptime(data_atual, '%d/%m/%Y')
        data_atual = data_validada.strftime('%d/%m/%Y')
    except ValueError:
        print('Data inválida!')
        return
    horario_atual = input('Qual o horário do seu agendamento? ').strip()
    

    for agendamento in agendamentos:
        if (
            agendamento[0].lower().strip().title() == nome_cliente
            and agendamento[2].strip() == data_atual
            and agendamento[3].strip() == horario_atual
        ):
            agendamento_original = agendamento
            
            print('Agendamento encontrado!')
            nova_data = input('Qual a nova data do seu agendamento? ').strip()

            try:
                data_validada = datetime.strptime(nova_data, '%d/%m/%Y')
                if data_validada.date() < datetime.now().date():
                    print('Não é possível reagendar para uma data passada!')
                    return
                nova_data = data_validada.strftime('%d/%m/%Y')

            except ValueError:
                print('Data inválida!')
                return
            mostrar_horarios(nova_data, agendamento_original)

            novo_horario = input('Qual o novo horário do seu agendamento? ').strip()

            if novo_horario in horarios_disponiveis:
                print('Horário permitido!')

                novo_agendamento = [
                    agendamento_original[0],
                    agendamento_original[1],
                    nova_data,
                    novo_horario,
                    agendamento_original[4]
                ]

                if verificar_disponibilidade_reagendamento(
                    novo_agendamento, agendamento_original
                ):
                    print('Horário disponível!')
                    agendamento_original[2] = nova_data
                    agendamento_original[3] = novo_horario
                    print('Reagendamento feito com sucesso!')
                else:
                    print('Horário escolhido já está ocupado!')
                    print('Não foi possível reagendar.')
            else:
                print('Horário inválido!')

            break

    else:
        print('Nenhum agendamento encontrado!')


# HORÁRIOS DISPONÍVEIS

def mostrar_horarios(data_escolhida, agendamento_original=None):
    print('=== HORÁRIOS DISPONÍVEIS ===')

    for horario in horarios_disponiveis:
        if agendamento_original is None:
            verificar = verificar_disponibilidade(data_escolhida, horario, barbeiro)
        else:
            novo_agendamento = [

                agendamento_original[0],
                agendamento_original[1],
                data_escolhida,
                horario,
                agendamento_original[4]

            ]

            verificar = verificar_disponibilidade_reagendamento(novo_agendamento,agendamento_original)

        if verificar:
            print(horario)


# CANCELAMENTO

def cancelar_agendamento():
    nome_cancelamento = input('Qual o seu nome? ').lower().strip()
    data_cancelamento = input('Qual a data que deseja cancelar? ').strip()
    try:
        data_validada = datetime.strptime(data_cancelamento, '%d/%m/%Y')
        data_cancelamento = data_validada.strftime('%d/%m/%Y')
    except ValueError:
        print('Data inválida!')
        return
    horario_cancelamento = input('Qual o horário que você deseja cancelar? ').lower().strip()
    

    for agendamento in agendamentos:
        if (
            agendamento[0].lower().strip() == nome_cancelamento
            and agendamento[2].strip() == data_cancelamento
            and agendamento[3].strip() == horario_cancelamento
        ):
            print('Cliente encontrado!')
            print('Data encontrada!')
            print('Horário encontrado!')
           
            agendamentos.remove(agendamento)
            print('Cancelamento feito com sucesso!')
            return

    else:
        print('Nenhum agendamento encontrado!')


# CLIENTES CADASTRADOS

def mostrar_clientes():
    print('\n=== CLIENTES CADASTRADOS ===')

    for cliente in clientes:
        print(cliente)

    print('---------------------------------------------------')


# INFORMAÇÕES DO AGENDAMENTO

def mostrar_agendamentos():
    print('\n=== AGENDAMENTOS ===\n')

    for agendamento in agendamentos:
        print(f'Cliente: {agendamento[0]}')
        print(f'Serviço: {agendamento[1]}')
        print(f'Data: {agendamento[2]}')
        print(f'Horário: {agendamento[3]}')
        print(f'Barbeiro: {agendamento[4]}')

        print('---------------------------------------------------')


# PROGRAMA PRINCIPAL

print('=== SISTEMA DE BARBEARIA ===')

# MENU PRINCIPAL

escolha = '0'

while escolha != '5':
    print(
        '1 - Cadastrar agendamento\n'
        '2 - Cancelar agendamento\n'
        '3 - Reagendar agendamento\n'
        '4 - Mostrar agendamentos\n'
        '5 - Sair'
    )

    escolha = input('Escolha uma das opções: ').strip()

    if escolha == '5':
        print('Encerrando sistema...')

    elif escolha == '4':
        mostrar_agendamentos()

    elif escolha == '3':
        reagendar()

    elif escolha == '2':
        cancelar_agendamento()

    elif escolha == '1':
        realizar_agendamento()
    else:
        print('Opção inválida! Tente novamente.')

print(f'Total de clientes: {len(clientes)}')
mostrar_clientes()
