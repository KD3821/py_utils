'''
Набор новых студентов
Подходило 1 сентября, университет готовился к наплыву абитуриентов. Так вышло, что Вы, как программист, должны были помочь в отборе тех абитуриентов, кто поступит в университет на конкурсной основе на специальность программиста.
Схема была проста: есть абитуриент, у него есть результаты сданных экзаменов по математике, русскому и информатике. Соответственно, у каждого потенциального студента есть сумма баллов по этим экзаменам. Также есть дополнительные (extra_scores) баллы: за волонтерство, участие в олимпиадах и другие активности.
Вам нужно отобрать 20 человек, у которых суммарный балл выше, чем у других. В случае, если не получается однозначно определить 20 человек (например, 2 человека набрали одинаковое СУММАРНОЕ количество баллов и претендуют на 20 место в списке, стоит их ранжировать по "профильным" дисциплинам - "информатике" и "математике").

Напишите функцию find_top_20
Функция принимает на вход список сводной информации по абитуриентам (candidates)  и возвращает список с  именами 20 человек, набравших наибольшее СУММАРНОЕ количество баллов (с учетом extra баллов), которые станут студентами университета.
Пример входных данных приведен ниже.
candidates = [
 {"name": "Vasya",  "scores": {"math": 58, "russian_language": 62, "computer_science": 48}, "extra_scores":0},
 {"name": "Fedya",  "scores": {"math": 33, "russian_language": 85, "computer_science": 42},  "extra_scores":2},
 {"name": "Petya",  "scores": {"math": 92, "russian_language": 33, "computer_science": 34},  "extra_scores":1}
]
'''

candidates = [
{"name": "Vasya",  "scores": {"math": 58, "russian_language": 62, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya",  "scores": {"math": 33, "russian_language": 85, "computer_science": 42},  "extra_scores":2},
{"name": "Petya",  "scores": {"math": 92, "russian_language": 33, "computer_science": 34},  "extra_scores":1},
{"name": "Vasya1",  "scores": {"math": 59, "russian_language": 62, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya1",  "scores": {"math": 34, "russian_language": 85, "computer_science": 42},  "extra_scores":2},
{"name": "Petya1",  "scores": {"math": 93, "russian_language": 77, "computer_science": 34},  "extra_scores":1},
{"name": "Vasya2",  "scores": {"math": 60, "russian_language": 81, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya2",  "scores": {"math": 35, "russian_language": 92, "computer_science": 42},  "extra_scores":2},
{"name": "Petya2",  "scores": {"math": 94, "russian_language": 41, "computer_science": 34},  "extra_scores":2},
{"name": "Vasya3",  "scores": {"math": 61, "russian_language": 64, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya3",  "scores": {"math": 36, "russian_language": 85, "computer_science": 42},  "extra_scores":2},
{"name": "Petya3",  "scores": {"math": 95, "russian_language": 33, "computer_science": 34},  "extra_scores":1},
{"name": "Vasya4",  "scores": {"math": 62, "russian_language": 61, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya4",  "scores": {"math": 37, "russian_language": 85, "computer_science": 42},  "extra_scores":2},
{"name": "Petya4",  "scores": {"math": 96, "russian_language": 33, "computer_science": 34},  "extra_scores":1},  
{"name": "Vasya",  "scores": {"math": 58, "russian_language": 62, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya",  "scores": {"math": 33, "russian_language": 85, "computer_science": 42},  "extra_scores":2},
{"name": "Petya",  "scores": {"math": 92, "russian_language": 33, "computer_science": 34},  "extra_scores":1},
{"name": "Vasya1",  "scores": {"math": 59, "russian_language": 62, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya1",  "scores": {"math": 34, "russian_language": 85, "computer_science": 42},  "extra_scores":2},
{"name": "Petya1",  "scores": {"math": 93, "russian_language": 77, "computer_science": 34},  "extra_scores":1},
{"name": "Vasya2",  "scores": {"math": 60, "russian_language": 81, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya2",  "scores": {"math": 35, "russian_language": 92, "computer_science": 42},  "extra_scores":2},
{"name": "Petya2",  "scores": {"math": 94, "russian_language": 41, "computer_science": 34},  "extra_scores":2},
{"name": "Vasya3",  "scores": {"math": 61, "russian_language": 64, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya3",  "scores": {"math": 87, "russian_language": 85, "computer_science": 42},  "extra_scores":2}, #+ 51 m
{"name": "Petya3",  "scores": {"math": 95, "russian_language": 33, "computer_science": 34},  "extra_scores":1},
{"name": "Vasya4",  "scores": {"math": 62, "russian_language": 61, "computer_science": 48}, "extra_scores":0},
{"name": "Fedya4",  "scores": {"math": 37, "russian_language": 85, "computer_science": 42},  "extra_scores":2},
{"name": "Petya4",  "scores": {"math": 96, "russian_language": 33, "computer_science": 34},  "extra_scores":2}] #+1 ex 

def find_top_20(candidates):
    list_score = []
    list_sametotal = []
    list_new = []
    list_names = []
    for i in candidates:
        name = i['name']
        score_m = i['scores']['math']
        score_ru = i['scores']['russian_language']
        score_cs = i['scores']['computer_science']
        score_x = i['extra_scores']
        total = score_m + score_ru + score_cs + score_x
        total_pro = score_m + score_cs
        list_score.append({'name': name, 'total': total, 'm_cs': total_pro})
    list_score = sorted(list_score, key=lambda x: x['total'], reverse=True)
    if len(list_score) <= 20:
        list_new = list_score
    else:
        val = list_score[19]['total']
        for i in list_score:
            if i['total'] == val:
                list_sametotal.append(i)
        if len(list_sametotal) > 1:
            list_sametotal = sorted(list_sametotal, key=lambda y: y['m_cs'], reverse=True)
            top_list = list_score[:20]
            for i in top_list:
                if i['total'] != val:
                    list_new.append(i)
            amount = 20 - len(list_new)
            if amount == 1:
                list_new.append(list_sametotal[0])
            else:
                list_new = list_new + list_sametotal[:amount]
        else:
            list_new = list_score[:20]
    for i in list_new:
        list_names.append(i['name'])
    return list_names
    
