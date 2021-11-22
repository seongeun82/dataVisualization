import pymysql
import pandas as pd


class DbConnection:
    def getConnectionWithCfg(self, dataConfig):
        dataConfig.update({'autocommit': True,
                           'cursorclass': pymysql.cursors.DictCursor,
                           'charset': 'utf8'}
                          )
        connection = pymysql.connect(**dataConfig)
        return connection

    def getDFFromQuery(self, dataConfig, query=''):
        connection = self.getConnectionWithCfg(dataConfig)
        cursor = connection.cursor()
        sqlString = query
        cursor.execute(sqlString)
        res = pd.DataFrame(cursor.fetchall())
        cursor.close()
        connection.close()
        return res

    def executeQuery(self, dataConfig, query=''):
        connection = self.getConnectionWithCfg(dataConfig)
        cursor = connection.cursor()
        sqlString = query
        res = cursor.execute(sqlString)
        cursor.close()
        connection.close()
        return res

    def getTbCols(self, dataConfig, dbnm, tbnm):
        query = f'''
        select column_name from information_schema.columns
        where table_Schema = '{dbnm}'
        and TABLE_NAME = '{tbnm}'; 
        '''
        return self.getDFFromQuery(dataConfig=dataConfig, query=query)
