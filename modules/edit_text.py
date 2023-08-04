import pymorphy2

morph = pymorphy2.MorphAnalyzer()
def get_normal_form(text: str):
    if text:
        text = text.replace('(', '').replace(')', '').replace('\'', '')

        prelogs = [' без ', ' безо ', ' близ ', ' в ',  ' во ', ' вместо ', ' вне ', ' для ', ' до ', ' за ', ' из ', ' изо ', ' и ', ' к ',  ' ко ', ' кроме ', ' между ', ' меж ', ' на ', ' над ', ' надо ', ' о ',  ' об ', ' обо ', ' от ', ' ото ', ' перед ', ' передо ', ' предо ', ' пo ', ' под ', ' при ', ' про ', ' ради ', ' с ',  ' со ', ' сквозь ', ' среди ', ' через ', ' чрез ']
        for sumb in prelogs:
            text = text.replace(sumb, ' ')

        normal_form = [morph.parse(i)[0].normal_form for i in text.split()]

        return ' '.join(normal_form)
    else:
        return text