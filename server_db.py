from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import sessionmaker, registry
import datetime


class ServerStorage:
    class Clients:
        def __init__(self, username, pas_hash):
            self.name = username
            self.pas_hash = pas_hash
            self.pubkey = None
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
                              Column('passwd_hash', String),
                              Column('pubkey', Text)
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

        session = sessionmaker(bind=self.database_engine)
        self.session = session()

    def add_client(self, name, passwd_hash):
        user_row = self.Clients(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.ClientHistory(user_row.id)
        self.session.add(history_row)
        self.session.commit()


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

    def process_message(self, sender, recipient):
        sender = self.session.query(self.Clients).filter_by(name=sender).first().id
        recipient = self.session.query(self.Clients).filter_by(name=recipient).first().id
        # # Запрашиваем строки из истории и увеличиваем счётчики
        # sender_row = self.session.query(self.ClientHistory).filter_by(user=sender).first()
        # sender_row.sent += 1
        # recipient_row = self.session.query(self.ClientHistory).filter_by(user=recipient).first()
        # recipient_row.accepted += 1

        self.session.commit()

    def add_contact(self, user, contact):
        user = self.session.query(self.Clients).filter_by(name=user).first()
        contact = self.session.query(self.Clients).filter_by(name=contact).first()
        if not contact or self.session.query(self.Contacts).filter_by(own_id=user.id, client_id=contact.id).count():
            return
        contact_row = self.Contacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def del_contact(self, user, contact):
        user = self.session.query(self.Clients).filter_by(name=user).first()
        contact = self.session.query(self.Clients).filter_by(name=contact).first()
        if not contact:
            return
        print(self.session.query(self.Contacts).filter(self.Contacts.own_id == user.id, self.Contacts.client_id == contact.id).delete())
        self.session.commit()

    def get_contacts(self, username):
        user = self.session.query(self.Clients).filter_by(name=username).one()
        query = self.session.query(self.Contacts, self.Clients.name).filter_by(own_id=user.id).join(self.Clients, self.Contacts.client_id == self.Clients.id)

        # выбираем только имена пользователей и возвращаем их.
        return [contact[1] for contact in query.all()]

    def get_hash(self, name):
        user = self.session.query(self.Clients).filter_by(name=name).first()
        return user.pas_hash

    def get_pubkey(self, name):
        user = self.session.query(self.Clients).filter_by(name=name).first()
        return user.pubkey


if __name__ == '__main__':
    test_db = ServerStorage()
