from django.db import connection
import os
import sys

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("insert into new_table_name1 select shengfen,FROM_UNIXTIME ((floor(reg1)-19-70*365)*86400-8*3600) as mydate,count(id) as total from (select shengfen,id,FLOOR(reg) as reg1 from users_alilaxin) as total  group by shengfen,reg1 order by shengfen")
        row = cursor.fetchone()

    return row
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mxonline3.settings")
    my_custom_sql()
