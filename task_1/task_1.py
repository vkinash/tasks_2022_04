from csv import writer
from random import choice

import os
import sqlalchemy
import pymongo
import string
import pandas as pd

NUMBER_OF_FIELDS = 1024
NUMBER_OF_COLUMNS = 6
COLUMN_LIST = ['col_'+str(i) for i in range(1, NUMBER_OF_COLUMNS+1)]
LEN_OF_STRING = 8
TEST_DATA_FILE = 'tests/data/data_for_test.csv'
TARGET_FOLDER = 'output'
FILE_A = 'file_a.csv'
FILE_B = 'file_b.csv'
MYSQL_DB_URL = 'mysql+pymysql://admin:admin@localhost/db'
MONGODB_URL = "mongodb://localhost:27017/mydb"
MONGO_USER = 'admin'
MONGO_PASS = 'admin'
MONGO_DB = 'mydb'
MONGO_COLLECTION = 'my_collection'


# A. Сгенерировать csv файл из 1024 записей по 6 столбцов, заполненных
# строками случайных символов (цифры и латинские буквы) длиной по 8 символов.
def file_creator(folder_name, file_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    with open(f'{folder_name}/{file_name}', 'w') as my_file:
        wr = writer(my_file)
        for i in range(NUMBER_OF_FIELDS):
            random_list = [get_random_string(LEN_OF_STRING) for _ in range(NUMBER_OF_COLUMNS)]
            wr.writerow(random_list)


def get_random_string(length):
    symbols = string.ascii_letters + string.digits
    return ''.join(choice(symbols) for _ in range(length))


# B. Считать содержимое файла, заменить нечетные цифры символом #, удалить записи, в которых любая
# из шести строк начинается с гласной буквы, сохранить отредактированный файл с другим именем.
def replace_symbols(output_file):
    df = get_data(f'{TARGET_FOLDER}/{FILE_A}')
    vowels = ('A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u')
    for i in range(NUMBER_OF_COLUMNS):
        df.drop(df[df[i].str.startswith(vowels)].index, inplace=True)

    df.replace('[24680]', '#', regex=True, inplace=True)

    df.to_csv(output_file, index=False, header=False)


def get_data(data_file):
    return pd.read_csv(data_file, header=None, dtype='str')


# C. Считать содержимое файла из пункта А, создать программно базу данных mysql, сохранить все данные в таблицу.
# Средствами sql удалить записи, в которых во втором столбце первый символ цифра.
def get_engine(data_base_url=MYSQL_DB_URL):
    return sqlalchemy.create_engine(data_base_url)


def write_to_mysql():
    df = get_data(f'{TARGET_FOLDER}/{FILE_A}')
    df.columns = COLUMN_LIST

    with get_engine().connect() as conn:
        df.to_sql(name='t_upload_data', con=conn, if_exists='replace')


def delete_data_from_mysql():
    with get_engine().connect() as conn:
        conn.execute(
            """DELETE FROM t_upload_data
            WHERE LEFT(col_2, 1) in ('0','1','2','3','4','5','6','7','8','9');"""
        )


# D. Считать содержимое файла из пункта А, создать программно базу данных mongodb, сохранить все данные в коллекцию.
# Средствами mongo удалить записи, в которых в третьем столбце первый символ буква.
def get_my_collection(mongodb_url=MONGODB_URL,
                      user=MONGO_USER,
                      password=MONGO_PASS,
                      db=MONGO_DB,
                      collection=MONGO_COLLECTION):
    client = pymongo.MongoClient(mongodb_url, username=user, password=password)
    db = client[db]
    return db[collection]


def write_to_mongodb():
    collection = get_my_collection()
    df = get_data(f'{TARGET_FOLDER}/{FILE_A}')
    df.columns = COLUMN_LIST
    collection.insert_many(df.to_dict('records'))


def delete_data_from_mongodb():
    collection = get_my_collection()
    collection.delete_many({'col_3': {'$regex': '^[a-z]+', '$options': 'i'}})


if __name__ == "__main__":
    file_creator(TARGET_FOLDER, FILE_A)
    replace_symbols(f'{TARGET_FOLDER}/{FILE_B}')
    write_to_mysql()
    delete_data_from_mysql()
    write_to_mongodb()
    delete_data_from_mongodb()
