import mysql.connector
from mysql.connector import Error

import env as v

"""
-- Copiando estrutura para tabela github.repo_dev
CREATE TABLE IF NOT EXISTS `repo_dev` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repo` varchar(200) DEFAULT NULL,
  `developer` varchar(200) DEFAULT NULL,
  `commits` varchar(200) DEFAULT NULL,
  `commits_link` varchar(200) DEFAULT NULL,
  `lines_add` varchar(200) DEFAULT NULL,
  `lines_del` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
"""

def query(query):
    results = []
    try:
        con = mysql.connector.connect(host=v.DB_HOST, database=v.DB_DATABASE, user=v.DB_USER, password=v.DB_PASS)
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    except Error as e:
        print("Erro ao acessar tabela MySQL", e)

    if con.is_connected():
        con.close()
        cursor.close()
    return results

def execute_query(execute):
    con = mysql.connector.connect(host=v.DB_HOST, database=v.DB_DATABASE, user=v.DB_USER, password=v.DB_PASS)
    cursor = con.cursor()
    try:
        cursor.execute(execute)
        con.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def insert_repo_info_db(NOME_REPO, DEVS):
    query = f''' DELETE FROM {v.TABLE_INFO} where repo = '{NOME_REPO}' '''
    print("Executando => ")
    print(query)
    execute_query(query)
    
    for index, DEV in enumerate(DEVS):
        query = f'''INSERT INTO {v.TABLE_INFO} 
            (
                repo, 
                developer,
                commits,
                commits_link,
                lines_add,
                lines_del
            ) 
            VALUES 
            (
                '{DEV["repo"]}', 
                '{DEV["developer"]}',
                '{DEV["commits_link"]}',
                '{DEV["commits"]}',
                '{DEV["lines_add"]}',
                '{DEV["lines_del"]}'
            )
        '''
        print("Executando => ")
        print(query)
        
    return execute_query(query)
