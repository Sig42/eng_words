import PySimpleGUI as sg
import json


def add_word(word, translation):
    if word and translation:
        if word in [i["word"] for i in words]:
            sg.popup('Such word is already in the list', no_titlebar=True, background_color="Black")
        else:
            words.append({"word": f"{word}", "translation": f"{translation}", "level": 0})
            sg.popup('Word was successfully added', no_titlebar=True, background_color="Black")
    else:
        sg.popup('Enter word and translation', no_titlebar=True, background_color="Red")
    window['-WordInput-'].update(value='')
    window['-TransInput-'].update(value='')


def menu_button():
    window['-WordsNumberActually-'].update(value=f'{len(words)}')
    window['-LearnLayout-'].update(visible=False)
    window['-AddLayout-'].update(visible=False)
    window['-StartLayout-'].update(visible=True)
    window['-LearnInput-'].update(value='', background_color='White')
    window['-NextButton-'].update(disabled=True)
    window['-WordInput-'].update(value='')
    window['-TransInput-'].update(value='')
    window['-JustLearnedText-'].update(value=f'Just learned: {just_learned_cnt}')
    window['-TransText-'].update(value=f'{current_word["translation"]} {current_word["level"]}')


def check(user_ans, w):
    if user_ans == w:
        current_word["level"] += 1
        window['-LearnInput-'].update(background_color='Green')
        window['-NextButton-'].update(disabled=False)
    else:
        window['-LearnInput-'].update(background_color='Red')


def tip():
    current_word["level"] -= 6
    sg.popup(f'{current_word["word"]}', no_titlebar=True, background_color='Black')


def next_word(jlc):
    jlc += 1
    window['-JustLearnedText-'].update(value=f'Just learned: {jlc}')
    window['-TransText-'].update(value=f'{current_word["translation"]} {current_word["level"]}')
    window['-LearnInput-'].update(value='', background_color='White')
    window['-NextButton-'].update(disabled=True)
    return jlc


with open('words_list.json', 'r', encoding='utf-8') as file:
    words = json.loads(file.read())
words.sort(key=lambda x: x["level"])
iter_words = iter(words)
current_word = next(iter_words)
just_learned_cnt = 0

start_layout = [[sg.Sizer(h_pixels=800, v_pixels=0)],
                [sg.Text(text='Number of words:', font=('Cascadia Code', 14), pad=(0, 20),
                         background_color='#696969', key='-WordsNumberText-')],
                [sg.Text(text=f'{len(words)}', font=('Cascadia Code', 14), pad=(0, 20),
                         background_color='#696969', key='-WordsNumberActually-')],
                [sg.Button(button_text='Learn words', font=('Cascadia Code', 14), button_color='#696969',
                           border_width=0, key='-LearnButton-', pad=(20, 20)),
                 sg.Button(button_text='Add a word', font=('Cascadia Code', 14), button_color='#696969',
                           border_width=0, key='-AddButton-', pad=(20, 20))]]

add_layout = [[sg.Sizer(h_pixels=800, v_pixels=0)],
              [sg.Text(text='Word:       ', font=('Cascadia Code', 14), pad=(0, 20),
                       background_color='#696969', key='-WordText-'),
               sg.Input(font=('Cascadia Code', 14), key='-WordInput-', focus=True, pad=(30, 0))],
              [sg.Text(text='Translation:', font=('Cascadia Code', 14), background_color='#696969', pad=(0, 20),
                       key='-TransText-'),
               sg.Input(font=('Cascadia Code', 14), key='-TransInput-', focus=False, pad=(30, 0))],
              [sg.Button(button_text='Add', font=('Cascadia Code', 14), button_color='#696969',
                         border_width=0, key='-AddWordButton-', pad=(20, 20)),
               sg.Button(button_text='Menu', font=('Cascadia Code', 14), button_color='#696969',
                         border_width=0, key='-MenuButtonAL-', pad=(20, 20))]]

learn_layout = [[sg.Sizer(h_pixels=1000, v_pixels=0)],
                [sg.Text(text=f'Just learned: {just_learned_cnt}', font=('Cascadia Code', 14), pad=(0, 20),
                         background_color='#696969', key='-JustLearnedText-')],
                [sg.Text(text=f'{current_word["translation"]} {current_word["level"]}', font=('Cascadia Code', 14),
                         pad=(10, 20), background_color='#696969', key='-TransText-'),
                 sg.Input(font=('Cascadia Code', 14), key='-LearnInput-', focus=True, pad=(30, 0))],
                [sg.Button(button_text='Menu', font=('Cascadia Code', 14), button_color='#696969',
                           border_width=0, key='-MenuButtonLL-', pad=(20, 20)),
                 sg.Button(button_text='Next', font=('Cascadia Code', 14), button_color='#696969',
                           border_width=0, key='-NextButton-', pad=(20, 20), disabled=True),
                 sg.Button(button_text='Tip', font=('Cascadia Code', 14), button_color='#696969',
                           border_width=0, key='-TipButton-', pad=(20, 20)),
                 sg.Button(button_text='Check', font=('Cascadia Code', 14), button_color='#696969',
                           border_width=0, pad=(20, 20), bind_return_key=True, visible=False, key='-CheckButton-')]]

layout = [[sg.Column(layout=start_layout, background_color='#696969', pad=(20, 20), key='-StartLayout-',
                     visible=True, element_justification='center'),
           sg.Column(layout=learn_layout, background_color='#696969', pad=(20, 20), key='-LearnLayout-',
                     visible=False, element_justification='center'),
           sg.Column(layout=add_layout, background_color='#696969', pad=(20, 20), key='-AddLayout-',
                     visible=False, element_justification='center')]]

window = sg.Window(title='Window', layout=layout, background_color='Black')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == '-LearnButton-':
        window['-StartLayout-'].update(visible=False)
        window['-LearnLayout-'].update(visible=True)

    elif event == '-AddButton-':
        window['-StartLayout-'].update(visible=False)
        window['-AddLayout-'].update(visible=True)

    elif event == '-AddWordButton-':
        add_word(values["-WordInput-"], values["-TransInput-"])

    elif event in ('-MenuButtonAL-', '-MenuButtonLL-'):
        words.sort(key=lambda x: x["level"])
        iter_words = iter(words)
        current_word = next(iter_words)
        just_learned_cnt = 0
        menu_button()

    elif event == '-CheckButton-':
        check(values['-LearnInput-'], current_word["word"])

    elif event == '-TipButton-':
        tip()

    elif event == '-NextButton-':
        try:
            current_word = next(iter_words)
            just_learned_cnt = next_word(just_learned_cnt)
        except StopIteration:
            sg.popup('The list is exhausted', no_titlebar=True, background_color='Black')
            words.sort(key=lambda x: x["level"])
            iter_words = iter(words)
            current_word = next(iter_words)
            just_learned_cnt = 0
            menu_button()


with open('words_list.json', 'w', encoding='UTF-8') as file:
    file.write(json.dumps(words))

window.close()
