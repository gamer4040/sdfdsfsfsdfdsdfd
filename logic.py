from random import randint
import requests
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        
        # Добавляем поля здоровья и силы
        self.hp = randint(50, 100)
        self.power = randint(10, 30)
        
        # Время последнего кормления (инициализируем как None или текущее время)
        self.last_feed_time = None

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sprites = data.get('sprites', {})
            other = sprites.get('other', {})
            official_artwork = other.get('official-artwork', {})
            # official-artwork предпочтителен; иначе обычный спрайт
            return official_artwork.get('front_default') or sprites.get('front_default')
        else:
            return "https://upload.wikimedia.org/wikipedia/ru/7/77/Pikachu_rus.png"
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"


    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покемона: {self.name}\nЗдоровье: {self.hp}\nСила: {self.power}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    
    # Метод атаки
    def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!"
    
    # Метод кормления покемона
    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        
        # Если покемон еще не кормили, можно покормить сразу
        if self.last_feed_time is None:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        
        # Проверяем, прошло ли достаточно времени
        time_since_last_feed = current_time - self.last_feed_time
        if time_since_last_feed >= delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            # Вычисляем время следующего кормления
            next_feed_time = self.last_feed_time + delta_time
            remaining_time = next_feed_time - current_time
            remaining_seconds = int(remaining_time.total_seconds())
            return f"Следующее время кормления покемона: через {remaining_seconds} секунд"
    
    # Метод для создания случайного вражеского покемона
    @staticmethod
    def create_enemy():
        enemy_type = randint(1, 3)
        if enemy_type == 1:
            return Pokemon("enemy")
        elif enemy_type == 2:
            return Wizard("enemy")
        else:
            return Fighter("enemy")


# Класс Wizard - покемон-волшебник с магическим щитом
class Wizard(Pokemon):
    def attack(self, enemy):
        # Проверяем, является ли враг волшебником
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        return super().attack(enemy)
    
    def feed(self, feed_interval=20, hp_increase=15):
        # Волшебник получает больше здоровья при кормлении
        return super().feed(feed_interval, hp_increase)


# Класс Fighter - покемон-боец с супер-атакой
class Fighter(Pokemon):
    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой: {super_power}"
    
    def feed(self, feed_interval=10, hp_increase=10):
        # Боец имеет уменьшенный интервал кормления (10 секунд вместо 20)
        return super().feed(feed_interval, hp_increase)


