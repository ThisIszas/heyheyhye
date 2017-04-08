import MySQLdb


class SaveInfo:
    def __init__(self):
        self.db = MySQLdb.Connection('', '', '', '', charset='utf8')
        self.cursor = self.db.cursor()

    def insert_info(self, pic_urls):
        sql = u'insert INTO pic_urls VALUES (\'%s\')' % pic_urls
        print sql
        self.execute_statement(sql)

    def execute_statement(self, sql):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return cursor.fetchall()
        except Exception as e:
            print e
            self.db.rollback()



# w = SaveInfo()
# w.insert_info()