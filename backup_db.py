import os
import time
import pipes


# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.
def backup():
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_USER_PASSWORD = '1'
    # DB_NAME = '/backup/dbnameslist.txt'
    DB_NAME = 'automacao_residencial'
    BACKUP_PATH = 'backup_db'
    MYSQL_BIN_PATH = 'C:/wamp/bin/mysql/mysql5.7.26/bin/'  # ENDEREÇO DA PASTA BIN MYSQL

    # Getting current DateTime to create the separate backup folder like "20180817-123433".
    DATETIME = time.strftime('%Y%m%d-%H%M%S')
    TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

    # Checking if backup folder already exists or not. If not exists will create it.
    try:
        os.stat(TODAYBACKUPPATH)
    except:
        os.mkdir(TODAYBACKUPPATH)

    # Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
    retorno1='checking for databases names file.'
    if os.path.exists(DB_NAME):
        file1 = open(DB_NAME)
        multi = 1
        retorno2='Databases file found...'
        retorno3='Starting backup of all dbs listed in file ' + DB_NAME
    else:
        retorno2='Databases file not found...'
        retorno3='Starting backup of database ' + DB_NAME
        multi = 0

    # Starting actual database backup process.
    if multi:
        in_file = open(DB_NAME, "r")
        flength = len(in_file.readlines())
        in_file.close()
        p = 1
        dbfile = open(DB_NAME, "r")

        while p <= flength:
            db = dbfile.readline()  # reading database name from file
            db = db[:-1]  # deletes extra line
            dumpcmd = MYSQL_BIN_PATH + 'mysqldump -h ' + DB_HOST + ' -u ' + DB_USER + ' -p' + DB_USER_PASSWORD + ' ' + db + ' > ' + pipes.quote(
                TODAYBACKUPPATH) + '/' + db + '.sql'
            os.system(dumpcmd)

            p = p + 1
        dbfile.close()
    else:
        db = DB_NAME
        dumpcmd = MYSQL_BIN_PATH + 'mysqldump -h ' + DB_HOST + ' -u ' + DB_USER + ' -p' + DB_USER_PASSWORD + ' ' + db + ' > ' + pipes.quote(
            TODAYBACKUPPATH) + '/' + db + '.sql'
        os.system(dumpcmd)


    retorno4='Backup script completed'
    retorno5='Your backups have been created in ' + TODAYBACKUPPATH + ' directory'

    saida = retorno1 + '\n\n' + retorno2 + '\n\n' + retorno3 + '\n\n' + retorno4 + '\n\n' + retorno5
    return saida