import requests
import argparse

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('task_number')
args = parser.parse_args()

page = requests.get(
    f'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewTopic&topicId={args.task_number}')

soup = BeautifulSoup(page.text, "html.parser")
attributes = {'class': 'topicview'}
data = soup.find("td", attrs=attributes).find('script')
text = data.text.strip()

text = text[text.find("'") + 1:]
text = text[:text.rfind("'")]
text = text.replace('<br/>', '\n')

text = text.replace('<sup>', '{')
text = text.replace('</sup>', '}')

if '<sup>' in text:
    res = ''
    sups = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
    in_sup = False
    for symb in text:
        if symb == '{':
            in_sup = True
            continue
        elif symb == '}':
            in_sup = False
            continue
        if in_sup:
            res += sups[symb]
        else:
            res += symb
    text = res

if '<sub>' in text:
    text = text.replace('<sub>', '}')
    text = text.replace('</sub>', '{')

    res = ''
    subs = {'0': '₀', '1': '₁', '2': '₂', '3': '₅', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'}

    in_sub = False
    for symb in text:
        if symb == '{':
            in_sub = True
            continue
        elif symb == '}':
            in_sub = False
            continue
        if in_sub:
            res += subs[symb]
        else:
            res += symb
    text = res

print(text)
