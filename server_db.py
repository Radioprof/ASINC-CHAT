from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, registry
import datetime


class ServerStorage:
    class Clients:
        def __init__(self, username, info):
            self.name = username
            self.info = info
            self.id = None

    class ClientHistory:
        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    class Contacts:
        def __init__(self, own_id, client_id):
            self.id = None
            self.own_id = own_id
            self.client_id = client_id

    def __init__(self):
        SERVER_DATABASE = 'sqlite:///server_base.db3'
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)
        mapper_registry = registry()
        self.metadata = mapper_registry.metadata

        clients_table = Table('Clients', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('name', String, unique=True),
                              Column('info', DateTime)
                              )
        clients_history_table = Table('Client_history', self.metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('user', ForeignKey('Clients.id'), unique=True),
                                      Column('ip_address', String),
                                      Column('port', Integer),
                                      Column('login_time', DateTime))

        contacts = Table('Contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('own_id', Integer, primary_key=True),
                         Column('client_id', Integer, primary_key=True))

        self.metadata.create_all(self.database_engine)

        mapper_registry.map_imperatively(self.Clients, clients_table)
        mapper_registry.map_imperatively(self.ClientHistory, clients_history_table)
        mapper_registry.map_imperatively(self.Contacts, contacts)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

    def client_login(self, username, ip_address, port, info):
        rez = self.session.query(self.Clients).filter_by(name=username)
        if rez.count():
            user = rez.first()
        else:
            user = self.Clients(username, info)
            self.session.add(user)
            self.session.commit()

        history = self.ClientHistory(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(history)

        self.session.commit()


if __name__ == '__main__':
    test_db = ServerStorage()
