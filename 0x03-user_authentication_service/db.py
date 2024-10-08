#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class for managing the SQLAlchemy ORM database."""

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.
        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments
        Args:
            kwargs: Arbitrary keyword arguments to filter users.
        Returns:
            User: The first user found based on the filter.
        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the query is invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise
        except NoResultFound:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes based on the given keyword arguments.
        Args:
            user_id (int): The ID of the user to update.
            kwargs: Arbitrary keyword arguments representing
            the attributes to update.
        Returns:
            None
        Raises:
            ValueError: If any of the provided arguments
            do not correspond to valid attributes.
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"{key} is not an attribute of User")
                setattr(user, key, value)
            self._session.commit()
        except NoResultFound:
            raise ValueError("User not found")
