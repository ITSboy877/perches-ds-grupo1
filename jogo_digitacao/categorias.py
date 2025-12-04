import random

CATEGORIAS = {
    "programador": {
        "nome": "Programação",
        "icone": "💻",
        "textos": [
            "def calcular_soma(a, b): return a + b",
            "for i in range(10): print(i)",
            "class Usuario: def __init__(self, nome): self.nome = nome",
            "if __name__ == '__main__': main()",
            "import tkinter as tk from tkinter import messagebox",
            "while True: user_input = input('Digite algo: ')",
            "lista = [x for x in range(100) if x % 2 == 0]",
            "try: resultado = 10 / 0 except ZeroDivisionError: print('Erro')",
        ]
    },
    "escritor": {
        "nome": "Literatura",
        "icone": "📚",
        "textos": [
            "Era uma vez, em um reino distante, um jovem aventureiro que sonhava em explorar terras desconhecidas.",
            "O silêncio da noite era quebrado apenas pelo som distante dos grilos cantando em harmonia.",
            "As palavras fluíam naturalmente, como um rio que segue seu curso sem pressa ou preocupação.",
            "Sob o céu estrelado, ela refletia sobre os caminhos que a vida havia lhe apresentado.",
            "A biblioteca antiga guardava segredos entre suas páginas amareladas pelo tempo.",
        ]
    },
    "negocios": {
        "nome": "Negócios",
        "icone": "💼",
        "textos": [
            "A reunião está agendada para as 14h. Por favor, confirme sua presença com antecedência.",
            "Prezado cliente, informamos que seu pedido foi enviado e chegará em 3 dias úteis.",
            "O relatório trimestral apresenta um crescimento de 15% nas vendas em relação ao período anterior.",
            "Solicitamos o envio da proposta comercial até o final desta semana para análise.",
            "A empresa atingiu suas metas estabelecidas e superou as expectativas do mercado.",
        ]
    },
    "casual": {
        "nome": "Casual",
        "icone": "😊",
        "textos": [
            "Bom dia! Como você está hoje? Espero que esteja tudo bem com você e sua família!",
            "Vamos nos encontrar no parque às 15h para conversar e tomar um café?",
            "Adorei o filme que assistimos ontem! Foi incrível e muito emocionante!",
            "Que tal irmos ao shopping no fim de semana? Podemos almoçar juntos!",
            "Obrigado por toda a ajuda! Você é uma pessoa muito especial para mim!",
        ]
    },
    "tecnologia": {
        "nome": "Tecnologia",
        "icone": "🔧",
        "textos": [
            "A inteligência artificial está transformando a maneira como interagimos com a tecnologia.",
            "O desenvolvimento de aplicativos móveis requer conhecimento em diversas linguagens de programação.",
            "A segurança cibernética é fundamental para proteger dados sensíveis de empresas e usuários.",
            "Cloud computing permite armazenar e acessar dados de qualquer lugar do mundo.",
        ]
    }
}

def gerar_texto_categoria(categoria):
    if categoria in CATEGORIAS:
        return random.choice(CATEGORIAS[categoria]["textos"])
    return "Texto padrão para digitação."

def obter_categorias():
    return [(cat_id, info["nome"], info["icone"]) 
            for cat_id, info in CATEGORIAS.items()]
