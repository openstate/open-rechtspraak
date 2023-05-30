"""Database module, including the SQLAlchemy database object and DB-related utilities."""
import logging
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class UpsertMixin:
    @classmethod
    def get_or_create(cls, filter_by, default_kwargs=None, commit=True):
        """Fetches one record by filter criteria and creates one with defaults if missing"""
        instance = (
            db.session.query(cls).filter_by(**filter_by).with_for_update().first()
        )
        if instance:
            return instance, False

        instance = cls(**filter_by, **(default_kwargs or {}))
        instance.save(commit)
        return instance, True

    @classmethod
    def update_or_create(cls, filter_by, update_kwargs=None, commit=True):
        """Fetches one record by filter criteria and updates with kwargs"""
        instance, created = cls.get_or_create(filter_by, update_kwargs or {})
        if not created:
            for k, v in update_kwargs.items():
                setattr(instance, k, v)
            instance.save(commit)
        return instance


class TimestampsMixin:
    created_at = Column(db.DateTime, default=func.now())
    updated_at = Column(db.DateTime, default=func.now(), onupdate=func.now())


class Model(CRUDMixin, UpsertMixin, TimestampsMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``"""

    __abstract__ = True
    id = Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any((isinstance(record_id, (int, float)),)):
            return cls.query.get(int(record_id))
        return None


class UUIDModel(Model):
    __abstract__ = True
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        try:
            return cls.query.get(uuid.UUID(record_id))
        except ValueError:
            logging.warning(f"Record-ID not a valid UUID: {record_id}")
            return None


def reference_col(
    tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign key reference.
    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )
