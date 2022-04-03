from csv import writer
from random import choice

import sqlalchemy
import string
import pandas as pd

NUMBER_OF_FIELDS = 1024
NUMBER_OF_COLUMNS = 6
LEN_OF_STRING = 8
TEST_DATA_FILE = 'tests/data/data_for_test.csv'


# A. Сгенерировать csv файл из 1024 записей по 6 столбцов, заполненных
# строками случайных символов (цифры и латинские буквы) длиной по 8 символов.
def file_creator():
    with open('output/file_a.csv', 'w') as my_file:
        wr = writer(my_file)
        for i in range(NUMBER_OF_FIELDS):
            random_list = [get_random_string(LEN_OF_STRING) for _ in range(NUMBER_OF_COLUMNS)]
            wr.writerow(random_list)


def get_random_string(length):
    symbols = string.ascii_letters + string.digits
    return ''.join(choice(symbols) for _ in range(length))


# B. Считать содержимое файла, заменить нечетные цифры символом #, удалить записи, в которых любая
# из шести строк начинается с гласной буквы, сохранить отредактированный файл с другим именем.
def replace_symbols(data_file='output/file_b.csv'):
    df = get_data()
    vowels = ('A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u')
    for i in range(NUMBER_OF_COLUMNS):
        df.drop(df[df[i].str.startswith(vowels)].index, inplace=True)

    df.replace('[24680]', '#', regex=True, inplace=True)

    df.to_csv(data_file, index=False, header=False)


def get_data(data_file='output/file_a.csv'):
    return pd.read_csv(data_file, header=None, dtype='str')


# C. Считать содержимое файла из пункта А, создать программно базу данных mysql, сохранить все данные в таблицу.
# Средствами sql удалить записи, в которых во втором столбце первый символ цифра.

def get_engine():
    return sqlalchemy.create_engine('mysql+pymysql://admin:admin@localhost/db')


def write_to_mysql():
    df = get_data()
    df.columns = ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6']

    with get_engine().connect() as conn:
        df.to_sql(name='t_upload_data', con=conn, if_exists='replace')


def delete_data_from_mysql():
    with get_engine().connect() as conn:
        conn.execute(
            """DELETE FROM t_upload_data
            WHERE LEFT(col_2, 1) in ('0','1','2','3','4','5','6','7','8','9');"""
        )


if __name__ == "__main__":
    file_creator()
    replace_symbols()
    write_to_mysql()
    delete_data_from_mysql()
