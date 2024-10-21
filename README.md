## О проекте

Это классическая игра "Змейка", созданная с применением библиотеки pygame и подходов объектно-ориентированного программирования (ООП). В данной игре пользователю необходимо управлять змейкой, которая стремится собирать еду, растягиваясь в длину и избегая столкновений со своим телом.

## Технологии

- Python — основной язык программирования, использованный в проекте.
- Pygame — библиотека, примененная для создания графики и реализации игровой логики.
- ООП — ключевые элементы игры, такие как змейка и еда, реализованы в виде объектов, что гарантирует чистую и удобную для масштабирования архитектуру проекта.

## Правила игры
- Змейка состоит из множества сегментов.
- Она может двигаться в одном из четырёх направлений: вверх, вниз, влево или вправо. Игрок управляет направлением движения, однако змейка не может останавливаться или двигаться в обратную сторону.
- При каждом поедании яблока змейка увеличивается на один сегмент.
- В классической версии игры столкновение с пределами игрового поля приводит к проигрышу, однако в данной версии змейка может проходить сквозь стену и появляться с противоположной стороны поля.
- Если змейка столкнётся с собственным телом, то игра начнётся сначала.

## Как запустить проект:

### 1. Клонировать репозиторий и перейти в его директорию с помощью командной строки:
https://github.com/EmpIreR777/the_snake
cd the_snake


### 2. Создайте виртуальное окружение в корневой директории проекта:

- Для Windows:
python -m venv venv

- Для Linux/MacOS:
python3 -m venv venv


### 3. Активируйте виртуальное окружение в корневой директории:
- Для Windows:
source venv/Scripts/activate

- Для Linux/MacOS:
source venv/bin/activate


### 4. Обновите пакетный менеджер внутри виртуального окружения:
- Для Windows:
python -m pip install --upgrade pip

- Для Linux/MacOS:
python3 -m pip install --upgrade pip


### 5. Установите необходимые зависимости с помощью команды, находясь в корневой директории:
pip install -r requirements.txt


### 6. Запустите игру:
- Для Windows:
python the_snake.py

- Для Linux/MacOS:
python3 the_snake.py
