from itertools import count

from django import template


register = template.Library()


censorship = ["редиска"]

@register.filter()
def censor(value: str):


    if not isinstance(value, str):
        raise TypeError("Фильтр censor может применяться только к строкам.")

    text = value.split()
    censored_text = []

    for word in text:
        word_lower = word.lower()
        if word_lower in [i.lower() for i in censorship]: # Список comprehension для сравнения в нижнем регистре
            symbols = len(word)
            censored_word = word[0] + '*' * (symbols - 1)
            censored_text.append(censored_word)
        else:
            censored_text.append(word) # Добавляем оригинальное слово, если оно не в списке цензуры

    return " ".join(censored_text)