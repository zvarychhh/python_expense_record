import sqlite3
from datetime import date
from datetime import datetime


class App:
    u_name = None
    u_id = None
    connection = sqlite3.connect("control.db")
    cur = connection.cursor()

    @staticmethod
    def validate(date_text: str) -> bool:  # Метод для перевірки валідності дати
        try:
            datetime.strptime(date_text, '%Y-%m-%d')  # Приведення дати до вигляду '%Y-%m-%d'
            return True
        except ValueError:
            return False

    def main(self):
        while True:
            print('_________________________________________________________')
            if self.u_id and self.u_name:
                print('''
1. Створити новий запис
2. Отримати Статистику витрат
3. Очистити дані користувача  
4. Вийти з акаунта
Для виходу натисніть Enter.                
''')
                number_menu = input('Введіть пункт меню: ')
                if not number_menu:
                    print("Хорошого вам дня!")
                    break
                elif number_menu == '1':
                    print('''
1. Створення запиту за поточною датою
2. Створення запуту за вибраною датою
Для виходу натисніть Enter.                
                    ''')
                    number_menu = input('Введіть пункт меню: ')
                    if number_menu == '1':
                        self.create_record()
                    elif number_menu == '2':
                        rec_date = input("Введіть дату (Приклад YYYY-MM-DD): ")
                        if self.validate(rec_date):
                            rec_date = str(datetime.strptime(rec_date, '%Y-%m-%d'))[:10]
                            self.create_record(rec_date=rec_date)
                        else:
                            print("Введено невірну дату")
                elif number_menu == '2':
                    print('''
1. Показати всю статистику
2. Показати статистику за категорією
3. Показати статистику за датою
Для виходу натисніть Enter.                
                            ''')
                    number_menu = input('Введіть пункт меню: ')
                    if number_menu == '1':
                        self.show_statistics()
                    elif number_menu == '2':
                        self.show_statistics_by_title()
                    elif number_menu == '3':
                        print('''
1. За днем
2. за місяцем
3. за роком
Для виходу натисніть Enter.   
                        ''')
                        number_menu = input('Введіть пункт меню: ')
                        if number_menu == '1':
                            self.show_statistics_by_day()
                        elif number_menu == '2':
                            self.show_statistics_by_month()
                        elif number_menu == '3':
                            self.show_statistics_by_year()
                elif number_menu == '3':
                    self.clear_data()
                elif number_menu == '4':
                    self.u_name = None
                    self.u_id = None
                    print('Вихід успішно виконано')
                else:
                    print('Введено невірний номер пункту меню.')
            else:
                print('''
1. Авторизація
2. Реєстрація нового користувача
Для виходу натисніть Enter.          
                ''')
                number_menu = input('Введіть пункт меню: ')
                if not number_menu:
                    print("Хорошого вам дня!")
                    break
                elif number_menu == '1':
                    self.authorization()
                elif number_menu == '2':
                    self.registration()
                else:
                    print('Введено невірний номер пункту меню.')

    def authorization(self, username=None):
        if not username:
            username = input('Введіть ім\'я користувача: ')
    # Перевірка на переданий параметр для авторизації щойно зареєстрованих користувачів
        if list(self.cur.execute('''SELECT * FROM USERS WHERE Username=? ''',
                                 (username,))):  # Перевірка на наявність username в БД
            for row in self.cur.execute('''SELECT * FROM USERS WHERE Username=? ''', (username,)):
                self.u_id = row[0]  # Передача параметрів з бд в клас App
                self.u_name = row[1]
                print(f'Ви успішно ввійшли як {username}')
                return f'Ви успішно ввійшли як {username}'
        else:
            print(f'Користувача з іменем — {username} неіснує.')
            return f'Користувача з іменем — {username} неіснує.'

    def registration(self):
        username = input('Введіть ім\'я користувача: ')
        if list(self.cur.execute('''SELECT Username FROM USERS where Username=?''',
                                 (username,))):  # Перевірка на вже існуючих користувачів
            print(f'Користувач з іменем — {username} вже існує.')
            return f'Користувач з іменем — {username} вже існує.'
        self.cur.execute('''INSERT INTO USERS(Username) VALUES (?) ''',
                         (username,))  # Створення користувача, та додавання в БД
        self.connection.commit()
        print(f'Користувача {username} успішно створено.')
        self.authorization(username=username)
        return 'Cтворено'

    def create_record(self, rec_date=None):
        if not rec_date:
            rec_date = date.today()  # Перевірка на передану дату
        title = input("Введіть категорію витрати: ").title()
        try:
            prise = float(input('Введіть суму витрати: '))
        except ValueError:
            print('Суму витрат введено невірно.')
            return ''
        self.cur.execute(f''' INSERT INTO COSTS(Title, Price, cost_date,user_id) 
                                    VALUES (?, ?, ?, ?) ''', (title, prise, rec_date, self.u_id,))
        # Передача даних в БД
        self.connection.commit()
        print("Успішно додано новий запис.")
        return "Успішно додано новий запис."

    def clear_data(self):  # Видалення всіх даних користувача
        if list(self.cur.execute('''SELECT * FROM COSTS WHERE user_id=?''', (self.u_id,))):
            self.cur.execute(f'DELETE FROM COSTS WHERE user_id =? ', (self.u_id,))
            self.connection.commit()
            print('Дані успішно видалені.')
            return ''
        print('Дані відсутні')

    def show_statistics(self):
        self.cur.execute('''SELECT Title, Price, cost_date FROM COSTS WHERE user_id=?''',
                         (self.u_id,))  # Перевірка на наявність даних
        rows = self.cur.fetchall()
        if not rows:
            print('Даних немає.')
            return ''
        for row in rows:  # Вивід даних
            print(f'Категорія: {row[0]}, сума витрати: {row[1]}, дата: {row[2]}')
        self.cur.execute('''SELECT SUM(Price), COUNT(Price) FROM COSTS WHERE user_id=?''', (self.u_id,))
        result = self.cur.fetchall()
        print(f'Загальна сума витрат: {result[0][0]}, к-сть {result[0][1]}.')

    def show_statistics_by_title(self):
        title = input("Введіть категорію: ")
        self.cur.execute('''SELECT Title, Price, cost_date FROM COSTS WHERE user_id=? and Title=?''',
                         (self.u_id, title)) # Перевірка на наявність даних
        rows = self.cur.fetchall()
        if not rows:
            print('Даних немає.')
            return ''
        for row in rows:   # Вивід даних
            print(f'Категорія: {row[0]}, сума витрати: {row[1]}, дата: {row[2]}')
        self.cur.execute('''SELECT SUM(Price), COUNT(Price) FROM COSTS WHERE user_id=? 
        and Title=?''', (self.u_id, title,))
        result = self.cur.fetchall()
        print(f'Загальна сума витрат: {result[0][0]}, к-сть {result[0][1]}.')

    def show_statistics_by_day(self):
        rec_date = input("Введіть День(1-31): ")
        if rec_date not in [str(i) for i in range(1, 32)]:  # Перевірка на валідність даних
            print("Введено невірну дату")
            return ''
        rec_date = '0' + rec_date if len(rec_date) == 1 else rec_date
        self.cur.execute('''SELECT Title, Price, cost_date FROM COSTS WHERE user_id=? 
        and strftime('%d',cost_date)=?  ''', (self.u_id, rec_date,))
        rows = self.cur.fetchall()
        for row in rows:
            print(f'Категорія: {row[0]}, сума витрати: {row[1]}, дата: {row[2]}')
        self.cur.execute('''SELECT SUM(Price), COUNT(Price) FROM COSTS WHERE user_id=? 
        and strftime('%d',cost_date)=? ''', (self.u_id, rec_date,))
        result = self.cur.fetchall()
        print(f'Загальна сума витрат: {result[0][0] if result[0][0] else 0}, к-сть {result[0][1]}.')

    def show_statistics_by_month(self):
        rec_date = input("Введіть Місяць(1-12): ")
        if rec_date not in [str(i) for i in range(1, 13)]:  # Перевірка на валідність даних
            print("Місяць введено невірно.")
            return ''
        rec_date = '0' + rec_date if len(rec_date) == 1 else rec_date
        self.cur.execute('''SELECT Title, Price, cost_date FROM COSTS WHERE user_id=? 
        and strftime('%m',cost_date)=?  ''', (self.u_id, rec_date,))
        rows = self.cur.fetchall()
        for row in rows:
            print(f'Категорія: {row[0]}, сума витрати: {row[1]}, дата: {row[2]}')
        self.cur.execute('''SELECT SUM(Price), COUNT(Price) FROM COSTS WHERE user_id=? 
        and strftime('%m',cost_date)=? ''', (self.u_id, rec_date,))
        result = self.cur.fetchall()
        print(f'Загальна сума витрат: {result[0][0] if result[0][0] else 0}, к-сть {result[0][1]}.')

    def show_statistics_by_year(self):
        year = date.today().year
        rec_date = input(f"Введіть рік(1-{year}): ")    # Перевірка на валідність даних
        if rec_date not in [str(i) for i in range(1, year + 1)]:
            print("Рік введено невірно.")
            return ''
        self.cur.execute('''SELECT Title, Price, cost_date FROM COSTS WHERE user_id=? 
        and strftime('%Y',cost_date)=?  ''', (self.u_id, rec_date,))
        rows = self.cur.fetchall()
        for row in rows:
            print(f'Категорія: {row[0]}, сума витрати: {row[1]}, дата: {row[2]}')
        self.cur.execute('''SELECT SUM(Price), COUNT(Price) FROM COSTS WHERE user_id=? 
        and strftime('%Y',cost_date)=? ''', (self.u_id, rec_date,))
        result = self.cur.fetchall()
        print(f'Загальна сума витрат: {result[0][0] if result[0][0] else 0}, к-сть {result[0][1]}.')
