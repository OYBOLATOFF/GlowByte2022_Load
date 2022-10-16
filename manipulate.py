# В модуле initByORM создаю классы и декларативный объект. Импортирую их сюда
import random

from initByORM import *

# Открыл сессию для транзакций
with Session(bind=engine) as current_session:
    try:
        names = ['Рамазан', 'Павел', 'Андрей', 'Анастасия', 'Алексей', 'Дмитрий']
        families = ['Ойболатов', 'Калинин', 'Сунцов', 'Журавлёва', 'Рязанцев', 'Преснухин']
        for i in range(len(names)):
            new_person = Person(
                first_name = names[i],
                last_name = families[i],
                age = random.randint(18, 20)
            )
            current_session.add(new_person)
    except Exception as error:
        print(error)
    finally:
        current_session.commit()