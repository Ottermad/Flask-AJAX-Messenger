import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *
import markdown

DATABASE = SqliteDatabase("messaging.db")


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ("-joined_at",)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists.")

    @classmethod
    def get_user(cls, username):
        try:
            user = cls.get(cls.username == username)
            return user
        except:
            raise ValueError("User does not exist.")

    @classmethod
    def get_usernames(cls):
        usernames = []
        query = cls.select()
        for user in query:
            usernames.append(user.username)
        return usernames



class Message(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    to_user = ForeignKeyField(
        rel_model=User,
        related_name="to_user"
    )
    from_user = ForeignKeyField(
        rel_model=User,
        related_name="from_user"
    )
    content = TextField()

    @classmethod
    def create_message(cls, to_user, from_user, content):
        cls.create(
            to_user=to_user,
            from_user=from_user,
            content=content
        )

    """@classmethod
    def get_messages(cls, to_user):
        messages = {}
        usernames = []
        message_query = cls.select() \
            .where(
                (cls.to_user == to_user) | (cls.from_user == to_user)
            )

        usernames_query = Message.select(cls.from_user) \
            .where(cls.to_user == to_user) \
            .distinct()

        for username in usernames_query:
            username_text = username.from_user.username
            usernames.append(username_text)
            messages[username_text] = []

        for message in message_query:
            messages[message.from_user.username].append(message.content)

        return [usernames, messages]"""

    @classmethod
    def get_messages_from(cls, to_user, from_user):
        messages = []
        ids = []
        message_query = Message.select() \
            .where(Message.to_user == to_user) \
            .where(Message.from_user == from_user)

        for message in message_query:
            message_data = [
                message.timestamp,
                markdown.markdown(message.content),
                message.from_user.username,
            ]
            ids.append(message.id)
            messages.append(message_data)

        message_query2 = Message.select() \
            .where(Message.to_user == from_user) \
            .where(Message.from_user == to_user)

        for message in message_query2:
            if message.id not in ids:
                message_data = [
                    message.timestamp,
                    markdown.markdown(message.content),
                    message.from_user.username,
                ]
                messages.append(message_data)
        messages.sort()
        messages.reverse()
        for message in messages:
            message[0] = message[0].strftime("%H:%H %d:%m:%Y")
        return messages

    class Meta:
        database = DATABASE
        order_by = ("-timestamp",)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Message], safe=True)
    DATABASE.close()
