### ТЗ
#### Условия: 
    1. Для реализации тестового задания можно использовать любые доступные библиотеки.
    2. Решение должно быть самодостаточным и содержать всё необходимое для запуска, в том числе инструкции по установке и запуску.
    3. Покрытие кода решения тестами будет плюсом.
    4. Решение должно быть выложено в публичный репозиторий на github.com или bitbucket.org.

#### Задача:
    Требуется написать расширение, реализующее автоматическое REST API для всех моделей в Django проекте.

#### Возможности:
    1. Система должна распознавать все существующие модели, подключённых в проект приложений и публиковать REST интерфейс для внешнего взаимодействия
    2. API должно позволять: 
        - запрашивать объекты по нескольким полям (логика - AND) с возможностью сортировки (ORDER BY), ограничения кол-ва (LIMIT) (метод GET) 
        - создавать новые объекты (метод POST) 
        - удалять объекты по первичному ключу (метод DELETE) 
        - обновлять объекты по первичному ключу (метод PUT) 
    3. Данные клиенту должны возвращаться в формате JSON 
 
### REQUIREMENTS
 - python3
 - django 3+

### SETUP
 - cp -r rest_api **projectpath**/
 - cd **projectpath**
 - append "'rest_api'," in <project>/settings.py INSTALLED_APPS
 - append "from rest_api import views" in **project**/urls.py
 - append "from django.urls import include" in **project**/urls.py
 - append "path('rest_api/', include('rest_api.urls'))," in **project**/urls.py urlpatterns
 - python3 manage.py migrate

### API URLS
 http://**hostname**:**port**/rest_api/
