import telebot 

CHAVE_API = ""

bot = telebot.TeleBot(CHAVE_API)

def verificar(mensagem):
     return True
    
@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
            Digite os ingredientes que você tem separados por virgula

            """

    bot.reply_to(mensagem, "Olá, eu sou o bot nutri, irei te ajudar a controlar suas calorias diarias.")



bot.polling()