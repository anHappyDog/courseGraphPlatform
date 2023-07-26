from enum import Enum


class AppInfo:
    class DatabaseInfo:
        user = 'root'
        password = 'ilikeyou2003'
        database = 'test1'
        host = 'localhost'
        courseDbName = 't2'
        platformDbName = 'platform'
        userNeo4jListDbName = 'userneo4jlist'
        courseNameDb = 'course'

    class SUB_WINDOW(Enum):
        GRAPH_LIST = 0
        BOOK_MARK = 1
        GRAPH_SHOW = 2
        NODE_RESULT = 3
        USER_INFO = 4

    class Neo4jInfo:
        url = 'bolt://localhost:7687'
        auth = ('neo4j', 'ilikeyou2003')
