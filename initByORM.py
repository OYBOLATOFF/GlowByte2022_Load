# Импортирую необходимые типы данных и прочие классы/функции
from sqlalchemy import create_engine, Integer, \
    Column, DateTime, ForeignKey, Numeric, CHAR, VARCHAR, Date, TIMESTAMP

# Импортирую декларативный класс, от которого наследую все классы, которые хочу связать с БД
from sqlalchemy.ext.declarative import declarative_base

# Импортирую Session из sqlalchemy.orm для обработки транзакций в файле manipulate.py
from sqlalchemy.orm import Session

# Создаю декларативный класс, чтоб от него далее унаследоваться
Base = declarative_base()

# Создаю движок, который соединит меня с БД по адресу
engine = create_engine(
    "postgresql+psycopg2://dwh_voronezh:dwh_voronezh_qhi8P4t4@de-edu-db.chronosavant.ru:5432/dwh")


# Инфа касательно всего кода в файле 'Заметки.py'
class FactPayments(Base):
    __tablename__ = 'fact_payments'
    transaction_id = Column(Integer, nullable=False, primary_key=True, unique=True)
    card_num = Column(VARCHAR(16), nullable=False)
    transaction_amt = Column(Numeric(7, 2), nullable=False)
    transaction_dt = Column(TIMESTAMP(0), nullable=False)


class Person(Base):
    __tablename__ = 'person'
    first_name = Column(VARCHAR(50), nullable=False, primary_key=True)
    last_name = Column(VARCHAR(50), nullable=False, primary_key=True)
    age = Column(Integer, nullable=False)


class DimCars(Base):
    __tablename__ = 'dim_cars'
    plate_num = Column(CHAR(9), nullable=False, unique=True, primary_key=True)
    start_dt = Column(Date(), nullable=False, primary_key=True)
    model_name = Column(VARCHAR(30), nullable=False)
    revision_dt = Column(Date(), nullable=False)
    delete_flag = Column(CHAR(1), nullable=False)
    end_dt = Column(Date(), nullable=False)


class DimDrivers(Base):
    __tablename__ = 'dim_drivers'
    personnel_num = Column(Integer, nullable=False, unique=True, primary_key=True)
    start_dt = Column(Date(), nullable=False, primary_key=True)
    last_name = Column(VARCHAR(50), nullable=False)
    first_name = Column(VARCHAR(50), nullable=False)
    middle_name = Column(VARCHAR(50), nullable=False)
    birth_dt = Column(Date(), nullable=False)
    card_num = Column(CHAR(19), nullable=False)
    driver_license_num = Column(CHAR(12), nullable=False)
    driver_license_dt = Column(Date(), nullable=False)
    deleted_flag = Column(CHAR(1), nullable=False)
    end_dt = Column(Date(), nullable=False)


class DimClients(Base):
    __tablename__ = 'dim_clients'
    phone_num = Column(VARCHAR(15), nullable=False, unique=True, primary_key=True)
    start_dt = Column(Date(), nullable=False, primary_key=True)
    card_num = Column(VARCHAR(16), nullable=False)
    deleted_flag = Column(CHAR(1), nullable=False)
    end_dt = Column(Date(), nullable=False)


class FactRides(Base):
    __tablename__ = 'fact_rides'
    ride_id = Column(Integer, nullable=False, unique=True, primary_key=True)
    point_from_txt = Column(VARCHAR(200), nullable=False)
    point_to_txt = Column(VARCHAR(200), nullable=False)
    distance_val = Column(Numeric(5, 2), nullable=False)
    price_amt = Column(Numeric(7, 2), nullable=False)
    client_phone_num = Column(VARCHAR(15), ForeignKey('dim_clients.phone_num'))
    driver_pers_num = Column(Integer, ForeignKey('dim_drivers.personnel_num'))
    car_plate_num = Column(CHAR(9), ForeignKey('dim_cars.plate_num'))
    ride_arrival_dt = Column(TIMESTAMP(0))
    ride_start_dt = Column(TIMESTAMP(0))
    ride_end_dt = Column(TIMESTAMP(0), nullable=False)


class FactWaybills(Base):
    __tablename__ = 'fact_waybills'
    waybill_num = Column(VARCHAR(6), nullable=False, primary_key=True)
    driver_pers_num = Column(Integer, ForeignKey('dim_drivers.personnel_num'))
    car_plate_num = Column(CHAR(9), ForeignKey('dim_cars.plate_num'))
    work_start_dt = Column(TIMESTAMP(0), nullable=False)
    work_end_dt = Column(TIMESTAMP(0), nullable=False)
    issue_dt = Column(TIMESTAMP(0), nullable=False)


# Если скрипт запускается напрямую, а не как модуль для импорта классов, то создаю БД
if __name__ == '__main__':
    # Перед сохранением удалим предыдущую структуру
    Base.metadata.drop_all(engine)

    # Заново создаём всю структуру
    Base.metadata.create_all(engine)
