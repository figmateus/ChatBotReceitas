import telebot
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Chave de API do Edamam (substitua pela sua chave)
EDAMAM_API_KEY = os.getenv('EDAMAM_API_KEY')
TELEBOT_KEY = os.getenv('TELEBOT') 
bot = telebot.TeleBot(TELEBOT_KEY)
APP_ID = os.getenv('APP_ID')
# Função de boas vindas
@bot.message_handler(commands=['help', 'start'])
def send_welcome(mensagem):
    bot.reply_to(mensagem, """\
                Olá, \n eu sou o bot do Jacão, irei te ajudar a fazer uma receita com os ingredientes que você tem disponivel.
                    """)   

# Função para obter uma receita com base nos ingredientes usando a API Edamam
def get_recipe(ingredients):
    # Convertendo a lista de ingredientes em uma string para a pesquisa
    query = '&'.join(ingredients)

    # URL da API Edamam para buscar receitas por ingredientes
    url = f'https://api.edamam.com/search?q={query}&app_id={APP_ID}&app_key={EDAMAM_API_KEY}'
    print(f'URL da requisição: {url}')
    # Enviando uma solicitação HTTP para a API Edamam
    response = requests.get(url)
    data = response.json()
    print(data)
    # Verificando se foram encontradas receitas com todos os ingredientes
    if 'hits' in data and data['hits']:
        recipes = data['hits']

        # Verificando se cada ingrediente está presente na receita
        for recipe_data in recipes:
            recipe = recipe_data['recipe']
            recipe_ingredients = recipe.get('ingredientLines', [])

            # Verificando se todos os ingredientes estão na receita
            if all(ingredient.lower() in ' '.join(recipe_ingredients).lower() for ingredient in ingredients):
                return recipe['label'], recipe['url']

    return None

# Manipulador para a mensagem recebida
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Obtendo a lista de ingredientes da mensagem do usuário
    ingredients = message.text.split()

    # Verificando se a lista de ingredientes não está vazia
    if not ingredients:
        bot.reply_to(message, "Por favor, forneça uma lista de ingredientes.")
        return

    # Obtendo a receita da API Edamam
    recipe_info = get_recipe(ingredients)

    # Verificando se a receita foi encontrada
    if recipe_info:
        title, source_url = recipe_info
        bot.reply_to(message, f"Aqui está uma receita com os ingredientes fornecidos:\n{title}\n{source_url}")
    else:
        bot.reply_to(message, "Desculpe, não foi possível encontrar uma receita com esses ingredientes.")

# Iniciando o bot
bot.polling()
