import random
import time
import os

class Pokemon:
    def __init__(self, nome, tipo, hp, ataques):
        self.nome = nome
        self.tipo = tipo
        self.hp_max = hp
        self.hp_atual = hp
        self.ataques = ataques
        self.nivel = random.randint(50, 100)
    
    def esta_vivo(self):
        return self.hp_atual > 0
    
    def receber_dano(self, dano):
        self.hp_atual = max(0, self.hp_atual - dano)
        print(f"💥 {self.nome} recebeu {dano} de dano!")
        if not self.esta_vivo():
            print(f"💀 {self.nome} desmaiou!")
    
    def curar(self, quantidade):
        self.hp_atual = min(self.hp_max, self.hp_atual + quantidade)
        print(f"💚 {self.nome} recuperou {quantidade} HP!")
    
    def mostrar_status(self):
        barra_hp = "█" * int((self.hp_atual / self.hp_max) * 20)
        barra_vazia = "░" * (20 - len(barra_hp))
        print(f"{self.nome} (Nv.{self.nivel}) - {self.tipo}")
        print(f"HP: [{barra_hp}{barra_vazia}] {self.hp_atual}/{self.hp_max}")

class Ataque:
    def __init__(self, nome, tipo, dano, precisao):
        self.nome = nome
        self.tipo = tipo
        self.dano = dano
        self.precisao = precisao

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_titulo():
    print("=" * 50)
    print("🎮 POKÉMON BATTLE GAME 🎮")
    print("=" * 50)

def criar_pokemon_disponiveis():
    pokemons = {
        "Charizard": Pokemon("Charizard", "Fogo/Voador", 120, [
            Ataque("Lança-chamas", "Fogo", 90, 85),
            Ataque("Garra de Dragão", "Dragão", 80, 90),
            Ataque("Ataque Aéreo", "Voador", 75, 95),
            Ataque("Soco de Fogo", "Fogo", 70, 100)
        ]),
        "Blastoise": Pokemon("Blastoise", "Água", 130, [
            Ataque("Jato d'Água", "Água", 85, 90),
            Ataque("Raio de Gelo", "Gelo", 80, 85),
            Ataque("Cabeçada", "Normal", 70, 95),
            Ataque("Hidro Bomba", "Água", 100, 75)
        ]),
        "Venusaur": Pokemon("Venusaur", "Planta/Veneno", 125, [
            Ataque("Raio Solar", "Planta", 95, 85),
            Ataque("Vine Whip", "Planta", 75, 90),
            Ataque("Pó do Sono", "Planta", 0, 90),
            Ataque("Terremoto", "Terra", 80, 85)
        ]),
        "Pikachu": Pokemon("Pikachu", "Elétrico", 100, [
            Ataque("Choque do Trovão", "Elétrico", 85, 90),
            Ataque("Ataque Rápido", "Normal", 60, 100),
            Ataque("Onda T", "Elétrico", 70, 95),
            Ataque("Raio", "Elétrico", 95, 80)
        ]),
        "Gengar": Pokemon("Gengar", "Fantasma/Veneno", 110, [
            Ataque("Bola Sombria", "Fantasma", 90, 85),
            Ataque("Hipnose", "Psíquico", 0, 90),
            Ataque("Veneno", "Veneno", 70, 95),
            Ataque("Pesadelo", "Fantasma", 80, 85)
        ]),
        "Dragonite": Pokemon("Dragonite", "Dragão/Voador", 140, [
            Ataque("Hiper Raio", "Normal", 100, 80),
            Ataque("Garra de Dragão", "Dragão", 85, 90),
            Ataque("Ataque Aéreo", "Voador", 75, 95),
            Ataque("Trovão", "Elétrico", 80, 85)
        ])
    }
    return pokemons

def escolher_pokemon(pokemons_disponiveis, jogador):
    print(f"\n🎯 {jogador}, escolha seu Pokémon:")
    print("-" * 30)
    
    pokemons_lista = list(pokemons_disponiveis.keys())
    for i, nome in enumerate(pokemons_lista, 1):
        pokemon = pokemons_disponiveis[nome]
        print(f"{i}. {nome} - {pokemon.tipo} (HP: {pokemon.hp_max})")
    
    while True:
        try:
            escolha = int(input(f"\nDigite o número do Pokémon (1-{len(pokemons_lista)}): ")) - 1
            if 0 <= escolha < len(pokemons_lista):
                nome_escolhido = pokemons_lista[escolha]
                pokemon_escolhido = pokemons_disponiveis[nome_escolhido]
                print(f"\n✅ {jogador} escolheu {nome_escolhido}!")
                return pokemon_escolhido
            else:
                print("❌ Escolha inválida! Tente novamente.")
        except ValueError:
            print("❌ Por favor, digite um número válido!")

def calcular_efetividade(ataque, pokemon_alvo):
    super_efetivo = {
        "Fogo": ["Planta", "Gelo"],
        "Água": ["Fogo", "Terra"],
        "Planta": ["Água", "Terra"],
        "Elétrico": ["Água", "Voador"],
        "Gelo": ["Planta", "Terra", "Voador", "Dragão"],
        "Terra": ["Fogo", "Elétrico", "Veneno", "Pedra"],
        "Fantasma": ["Fantasma", "Psíquico"],
        "Dragão": ["Dragão"]
    }
    
    nao_efetivo = {
        "Fogo": ["Água", "Pedra", "Dragão"],
        "Água": ["Planta", "Dragão"],
        "Planta": ["Fogo", "Veneno", "Voador", "Inseto", "Dragão"],
        "Elétrico": ["Planta", "Dragão"],
        "Gelo": ["Fogo", "Água", "Pedra"],
        "Terra": ["Planta", "Inseto"],
        "Fantasma": ["Normal"],
        "Normal": ["Pedra"]
    }
    
    tipos_alvo = pokemon_alvo.tipo.split("/")
    
    for tipo_alvo in tipos_alvo:
        if ataque.tipo in super_efetivo and tipo_alvo in super_efetivo[ataque.tipo]:
            return 2.0  # Super efetivo
        elif ataque.tipo in nao_efetivo and tipo_alvo in nao_efetivo[ataque.tipo]:
            return 0.5  # Não muito efetivo
    
    return 1.0  # Normal

def executar_ataque(atacante, alvo, ataque):
    print(f"\n⚡ {atacante.nome} usou {ataque.nome}!")
    time.sleep(1)
    
    # Verificar precisão
    if random.randint(1, 100) > ataque.precisao:
        print(f"❌ {atacante.nome} errou o ataque!")
        return
    
    # Calcular dano base
    dano_base = ataque.dano
    
    # Aplicar efetividade
    efetividade = calcular_efetividade(ataque, alvo)
    dano_final = int(dano_base * efetividade)
    
    # Aplicar variação aleatória (±10%)
    variacao = random.uniform(0.9, 1.1)
    dano_final = int(dano_final * variacao)
    
    # Aplicar dano
    alvo.receber_dano(dano_final)
    
    # Mensagens de efetividade
    if efetividade > 1:
        print("🔥 É super efetivo!")
    elif efetividade < 1:
        print("😐 Não é muito efetivo...")
    
    time.sleep(1)

def mostrar_ataques(pokemon):
    print(f"\n📋 Ataques de {pokemon.nome}:")
    print("-" * 30)
    for i, ataque in enumerate(pokemon.ataques, 1):
        print(f"{i}. {ataque.nome} - {ataque.tipo} (Dano: {ataque.dano}, Precisão: {ataque.precisao}%)")

def escolher_acao(pokemon_jogador, pokemon_inimigo):
    print(f"\n🎮 Sua vez! O que {pokemon_jogador.nome} vai fazer?")
    print("1. Atacar")
    print("2. Curar (recupera 30 HP)")
    print("3. Ver ataques")
    print("4. Ver status dos Pokémon")
    
    while True:
        try:
            escolha = int(input("\nEscolha uma ação (1-4): "))
            if escolha == 1:
                return "atacar"
            elif escolha == 2:
                return "curar"
            elif escolha == 3:
                mostrar_ataques(pokemon_jogador)
                input("\nPressione Enter para continuar...")
                return escolher_acao(pokemon_jogador, pokemon_inimigo)
            elif escolha == 4:
                mostrar_status_batalha(pokemon_jogador, pokemon_inimigo)
                input("\nPressione Enter para continuar...")
                return escolher_acao(pokemon_jogador, pokemon_inimigo)
            else:
                print("❌ Escolha inválida! Tente novamente.")
        except ValueError:
            print("❌ Por favor, digite um número válido!")

def mostrar_status_batalha(pokemon1, pokemon2):
    print("\n" + "=" * 50)
    print("📊 STATUS DA BATALHA")
    print("=" * 50)
    pokemon1.mostrar_status()
    print()
    pokemon2.mostrar_status()
    print("=" * 50)

def batalha_pokemon():
    limpar_tela()
    mostrar_titulo()
    
    print("🎮 Bem-vindo ao Pokémon Battle Game!")
    print("Prepare-se para uma batalha épica!")
    
    # Criar Pokémon disponíveis
    pokemons_disponiveis = criar_pokemon_disponiveis()
    
    # Escolher Pokémon
    pokemon_jogador = escolher_pokemon(pokemons_disponiveis, "Jogador")
    pokemon_inimigo = escolher_pokemon(pokemons_disponiveis, "Inimigo")
    
    print(f"\n🎯 {pokemon_jogador.nome} VS {pokemon_inimigo.nome}")
    print("A batalha vai começar!")
    input("\nPressione Enter para começar...")
    
    # Loop da batalha
    turno = 1
    while pokemon_jogador.esta_vivo() and pokemon_inimigo.esta_vivo():
        limpar_tela()
        mostrar_titulo()
        print(f"🔄 TURNO {turno}")
        mostrar_status_batalha(pokemon_jogador, pokemon_inimigo)
        
        # Vez do jogador
        acao = escolher_acao(pokemon_jogador, pokemon_inimigo)
        
        if acao == "atacar":
            mostrar_ataques(pokemon_jogador)
            while True:
                try:
                    escolha_ataque = int(input(f"\nEscolha um ataque (1-{len(pokemon_jogador.ataques)}): ")) - 1
                    if 0 <= escolha_ataque < len(pokemon_jogador.ataques):
                        ataque_escolhido = pokemon_jogador.ataques[escolha_ataque]
                        executar_ataque(pokemon_jogador, pokemon_inimigo, ataque_escolhido)
                        break
                    else:
                        print("❌ Escolha inválida!")
                except ValueError:
                    print("❌ Por favor, digite um número válido!")
        
        elif acao == "curar":
            pokemon_jogador.curar(30)
        
        input("\nPressione Enter para continuar...")
        
        # Verificar se o inimigo ainda está vivo
        if not pokemon_inimigo.esta_vivo():
            break
        
        # Vez do inimigo (IA simples)
        print(f"\n🤖 Vez do {pokemon_inimigo.nome}!")
        time.sleep(1)
        
        # IA: 70% chance de atacar, 30% chance de curar
        if random.random() < 0.7 and pokemon_inimigo.hp_atual < pokemon_inimigo.hp_max * 0.5:
            pokemon_inimigo.curar(25)
        else:
            ataque_inimigo = random.choice(pokemon_inimigo.ataques)
            executar_ataque(pokemon_inimigo, pokemon_jogador, ataque_inimigo)
        
        input("\nPressione Enter para continuar...")
        turno += 1
    
    # Fim da batalha
    limpar_tela()
    mostrar_titulo()
    print("🏁 BATALHA FINALIZADA!")
    print("=" * 50)
    
    if pokemon_jogador.esta_vivo():
        print(f"🎉 PARABÉNS! {pokemon_jogador.nome} venceu a batalha!")
        print(f"🏆 {pokemon_jogador.nome} derrotou {pokemon_inimigo.nome}!")
    else:
        print(f"💀 {pokemon_inimigo.nome} venceu a batalha!")
        print(f"😔 {pokemon_jogador.nome} foi derrotado...")
    
    print(f"\n📊 Estatísticas da batalha:")
    print(f"• Total de turnos: {turno}")
    print(f"• HP final do {pokemon_jogador.nome}: {pokemon_jogador.hp_atual}")
    print(f"• HP final do {pokemon_inimigo.nome}: {pokemon_inimigo.hp_atual}")

def menu_principal():
    while True:
        limpar_tela()
        mostrar_titulo()
        print("\n🎮 MENU PRINCIPAL")
        print("1. Iniciar Batalha")
        print("2. Sobre o Jogo")
        print("3. Sair")
        
        try:
            escolha = int(input("\nEscolha uma opção (1-3): "))
            if escolha == 1:
                batalha_pokemon()
                input("\nPressione Enter para voltar ao menu...")
            elif escolha == 2:
                limpar_tela()
                mostrar_titulo()
                print("\n📖 SOBRE O JOGO")
                print("=" * 50)
                print("Pokémon Battle Game é um jogo de batalha por turnos")
                print("inspirado na franquia Pokémon!")
                print("\n🎯 Como jogar:")
                print("• Escolha seu Pokémon e o do inimigo")
                print("• Em cada turno, escolha atacar ou curar")
                print("• Diferentes tipos de Pokémon têm vantagens")
                print("• Use estratégia para vencer!")
                print("\n🎮 Características:")
                print("• 6 Pokémon diferentes para escolher")
                print("• Sistema de tipos e efetividade")
                print("• IA inteligente para o inimigo")
                print("• Interface colorida e divertida")
                input("\nPressione Enter para voltar...")
            elif escolha == 3:
                print("\n👋 Obrigado por jogar Pokémon Battle Game!")
                print("Até a próxima batalha! 🎮")
                break
            else:
                print("❌ Opção inválida!")
                time.sleep(1)
        except ValueError:
            print("❌ Por favor, digite um número válido!")
            time.sleep(1)

if __name__ == "__main__":
    menu_principal()
