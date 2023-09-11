from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_information_about_new_pet(name='qq', animal_type='taksa', age='5', pet_photo='C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_put_update_information_about_pet(name='qq', animal_type='koshka', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_delete_pet_from_database():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_information_about_new_pet(auth_key, "KOT", "кот", "3", "C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_pets_with_valid_data_without_photo(name='МурзикБезФото', animal_type='кот', age='6'):
    '''Проверяем возможность добавления нового питомца без фото'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_photo_at_pet():
    '''Проверяем возможность добавления новой фотографии питомца'''

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], "C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg")

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")


def test_add_pet_negative_age_number(name='Fedor', animal_type='cat', age='-3', pet_photo='C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.
     '''

    _, api_key = pf.get_api_key(valid_email, valid_password)

    _, result = pf.post_add_information_about_new_pet(api_key, name, animal_type, age, pet_photo)

    assert age not in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле возраст'


def test_add_pet_with_four_digit_age_number(name='Fedor', animal_type='cat', age='1234', pet_photo='C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с числом более трех знаков в переменной age.
    Тест не будет пройден ели питомец будет добавлен на сайт с числом превышающим три знака в поле возраст.'''

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.post_add_information_about_new_pet(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 4, 'Питомец добавлен на сайт с числом привышающим 3 знака в поле возраст'


def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='cat', age='2', pet_photo='C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной name
    Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле "имя"'''

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени'


def test_add_pet_with_a_lot_of_words_in_variable_name(animal_type='cat', age='2', pet_photo='C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg'):
    '''Проверка с негативным сценарием. Добавления питомца имя которого превышает 10 слов
    Тест не будет пройден если питомец будет добавлен на сайт с именем состоящим из более 10 слов'''

    name = 'Пабло Диего Хозе Франциско де Паула Хуан Непомукено Криспин Криспиано де ла Сантисима Тринидад Руиз и Пикассо'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count < 10, 'Питомец добавлен с именем больше 10 слов'


def test_add_pet_with_special_characters_in_variable_animal_type(name='Fedor', age='3', pet_photo='C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с специальными символами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с спец.символами вместо букв в поле порода.
    '''
    animal_type = 'Cat%@'
    symbols = '#$%^&*{}|?/><=+_~@'
    symbol = []

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] not in result['animal_type'], 'Питомец добавлен с недопустимыми спец.символами'


def test_add_pet_with_numbers_in_variable_animal_type(name='Fedor', animal_type='34562', age='3',
                                                      pet_photo='C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с цифрами вместо букв в поле порода.'''

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле порода'


def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Fedor', age='2', pet_photo='C:/Users/marin/PycharmProjects/pythonProject19.7.2/image/qqq.jpeg'):
    '''Проверка с негативным сценарием. Добавления питомца название породы которого превышает 10 слов
    Тест не будет пройден если питомец будет добавлен на сайт с названием породы состоящим из более 10 слов'''

    animal_type = 'артезиано нормандский бассет гриффон миттельшнауцер ньюфаундленд аргентинский дог помесь с бриар басерон'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_information_about_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 10, 'Питомец добавлен с названием породы больше 10 слов'


def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

