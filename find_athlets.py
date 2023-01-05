'''
Соревнования
Знакомые вам студенты-программисты уже пережили не одну сессию. Кое-кто из них продемонстрировал потрясающие способности в учебном процессе.
Другим только предстояло проявить себя во всей красе. Однажды в Ваш кабинет уверенно постучался и вошел физрук. 
Начал он свою историю издалека, что, мол, университету нужны таланты, что некому представлять ваше учебное заведения на международных соревнованиях
по плаванию. И словно невзначай спросил - "А нет ли у Вас на примете подходящих кандидатур? Да еще чтоб хотя бы немного знали английский.
Ах да, еще и возрастное ограничение — не младше 20 лет". 
Немного порывшись в памяти вы вспомнили тройку широкоплечих студентов-программистов, которые могли бы быть хорошими кандидатами.
Но вот имен их, как ни старались, припомнить не смогли. Однако вы знали, что при поступлении будущие студенты заполняли анкету.
Потом же на основании этих анкет были созданы списки для разделения по изучаемому языку (чтобы учитывать ранее приобретенные знания и 
не смешивать языковые группы в одну кучу) и списки, описывающие хобби студентов. Дело оставалось за малым — взять тех, кто знает английский 
и одновременно имеет интерес к спорту. Ну и совместить это дело со списком тех, кто перешагнул черту 20-летия, который был получен загодя.

Вам нужно написать функцию find_athlets
Функция find_athlets принимает 3 списка с именами студентов. В первом списке (know_english) — список тех, кто хорошо владеет английским языком. Второй (sportsmen) — содержит имена тех, кто увлекается спортом. Ну и третий (more_than_20_years) — предоставляет информацию о тех, кто старше 20 лет. Функция возвращает список имен студентов, которые подходят под все три критерия.

Пример входных данных приведен ниже.
know_english = ["Vasya","Jimmy","Max","Peter","Eric","Zoi","Felix"]
sportsmen = ["Don","Peter","Eric","Jimmy","Mark"]
more_than_20_years = ["Peter","Julie","Jimmy","Mark","Max"]
'''

def find_athlets(know_english, sportsmen, more_than_20_years):
    athlets = []
    non_athlets = []
    list_all = [know_english, sportsmen, more_than_20_years]
    
    if len(know_english) >= len(sportsmen):
        if len(sportsmen) >= len(more_than_20_years):
            min_len = len(more_than_20_years)
            min_list = more_than_20_years
        else:
            min_len = len(sportsmen)
            min_list = sportsmen
    elif len(know_english) >= len(more_than_20_years):
        if len(more_than_20_years) >= len(sportment):
            min_len = len(sportsmen)
            min_list = sportsmen
        else:
            min_len = len(more_than_20_years)
            min_list = more_than_20_years
    else:
        min_len = len(know_english)
        min_list = know_english
        
    list_all.remove(min_list)
        
    for j in list_all:
        for i in min_list:
            if i in j:
                continue
            else:
                non_athlets.append(i)
                
    for i in min_list:
        if i not in non_athlets:
            athlets.append(i)
                
    print(non_athlets)
    print(athlets)
    return(athlets)
    
print(find_athlets(know_english, sportsmen, more_than_20_years))
