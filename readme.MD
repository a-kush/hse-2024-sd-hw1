## Начальная реализация домашнего задания
Данная реализация:

- не выполняет функциональные требования
- предусмотренно нарушает принципы SOLID, и, как следствие, не выполняет требования по Maintainability
- не имеет в наличии БД, то есть не выполняет требования по Reliability
- ничего не говорит про развертывание и не выполняет требования по Scalability

Тем не менее, тут описаны некоторые основные API, и можно сделать вывод о том, куда будет развиваться приложение
Некоторые подходы сознательно применены (например, выделен слой доступа к данным и объекты DTO), но некоторые
сознательно нарушены :)

Содержательная часть вашей работы состоит в том, чтобы не фокусируясь на бизнес-логике -- благо, тут она довольно
простая -- сформировать подходящую архитектуру и написать вашу реализацию с учетом принципов SOLID.

### Описание

- main.py содержит несколько функций-реализаций бизнес-логики для примера
    - Также, содержит 2 тестовых сценария работы
- Вы можете использовать у себя неимоверной сложности модуль 'fastapi_stubs.py' для отладки/дебага :)