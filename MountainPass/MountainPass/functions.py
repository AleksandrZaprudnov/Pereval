from dotenv import dotenv_values


def get_env(name_const=None):
    """
    Функция для получения переменных окружения из .env.
    :param name_const: имя переменной (константы)
    :return: значение или None
    """
    for el_list in dotenv_values(".env").items():
        if str(el_list[0]) == str(name_const):
            return el_list[1]
    return None

