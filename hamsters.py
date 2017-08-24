#!/usr/bin/env python
import csv
import sys
import configargparse
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass


HOST = "dbHost"
USER = "dbUser"
NAME = "dbName"
PASSWD = "dbPassword"
PORT = "dbPort"

def connect_db(host, port, user, password, db):
    try:
        return pymysql.connect(host=host, port=port, user=user, passwd=password, db=db)
    except pymysql.Error, e:
        sys.stderr.write("[ERROR] % d: % s\n" % (e.args[0], e.args[1]))
        return False


def main():
    parser = configargparse.ArgParser(description='Hamster wheel 9000')
    parser.add_argument('-dir','--directory', help='Directory and filename of csv. ex: accounts/hive1.csv',required=True)
    parser.add_argument('-w','--workers', help='amount of lines per csv',required=True)
    parser.add_argument('-t','--table', help='db table to get hamsters from.',required=True)
    args = parser.parse_args()

    QUERY = "SELECT auth,username,password FROM {} order by last_timestamp limit {};".format(args.table, args.workers)
    UPDATEQUERY = "UPDATE {} set last_timestamp=now() order by last_timestamp limit {}".format(args.table, args.workers)
    FILENAME = "{}".format(args.directory)

    db = connect_db(HOST, int(PORT), USER, PASSWD, NAME)
    dump_writer = csv.writer(open(FILENAME, 'w'), delimiter=',', quoting=csv.QUOTE_NONE)
    cur = db.cursor()
    cur.execute(QUERY)
    for row in cur.fetchall():
        dump_writer.writerow(row)
    print("hamsters have been sent to their inevitable demise!")

    cur.execute(UPDATEQUERY)
    db.commit()
    print("their last timestamp has been updated")
    db.close()

    with open(FILENAME) as f:
        print "".join(line for line in f if not line.isspace())

if __name__ == "__main__":
    main()