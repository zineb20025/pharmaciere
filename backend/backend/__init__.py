import pymysql

pymysql.version_info = (2, 2, 1, "final", 0) # Cette ligne règle le problème de version
pymysql.install_as_MySQLdb()