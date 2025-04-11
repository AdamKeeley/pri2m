from django.db import connection


def delete_record(tbl_name, pk_field, pk_value):
    with connection.cursor() as cursor:
        sql = f"update {tbl_name} set [ValidTo] = getdate() where {pk_field} = {pk_value}"
        cursor.execute(sql)
        


