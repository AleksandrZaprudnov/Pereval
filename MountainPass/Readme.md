Документация
Программный интерфейс (API) для сервиса учета географических перевалов.

Интерфейс позволяет принимать (записывать в базу данных, далее БД), получать (читать из БД) сведения о перевалах.
Сведения заносят пользователи, туристы, имеющие доступ к приложению. Дополнительно пользователь регистрируется в 
системе, используется уникалный адрес электронной почты, также пользователь указывает свои персональные данные
(ФИО и номер телефона).

Данные о географическом объекте:
 - дата добавления (устанавливается автоматически);
 - дата создания (устанавливается автоматически);
 - статус записи (устанавливается автоматически, меняется модератором);
 - полное название, дополненное/расширенное (от пользователя);
 - сокращенное название (от пользователя);
 - вид географического объекта (от пользователя);
 - разделитель фраз, слов (от пользователя);
 сложность передвижения по местности:
   - зимнее время (от пользователя);
   - летнее время (от пользователя);
   - весеннее время (от пользователя);
   - осеннее время (от пользователя);
 географические параметры (градусы, высота):
   - широта (гр)
   - долгота (гр)
   - высота (м)
    
Подробная документация к API по адресу http://127.0.0.1:8000/docs
