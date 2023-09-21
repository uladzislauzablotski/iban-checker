from typing import List, TypeVar, Union

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import expression

from server.core.enums import StatusEnum
from server.core.models import Base

TableType = TypeVar("TableType", bound=Base)
CreateBaseSchema = TypeVar("CreateBaseSchema", bound=BaseModel)
UpdateBaseSchema = TypeVar("UpdateBaseSchema", bound=BaseModel)


class BaseMixin:
    table: TableType = None  # type: ignore

    @classmethod
    async def _execute_commit(cls, query: expression, session: AsyncSession):
        await session.execute(query)
        await session.commit()

    @classmethod
    def get_pk_attr(cls):
        """Get PK attribute of table"""
        return getattr(cls.table.__table__.c, cls.table.pk_name())

    @classmethod
    def get_specified_field(cls, field: str):
        return getattr(cls.table.__table__.c, field)

    @classmethod
    def _check_object(cls, obj: table) -> Union[bool, HTTPException]:
        """Check if object exist"""
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return True


class CreateMixin(BaseMixin):
    create_scheme: CreateBaseSchema = None  # type: ignore

    @classmethod
    async def create(cls, input_data: create_scheme, session: AsyncSession):
        """Create model"""
        obj = cls.table(**input_data.dict())
        session.add(obj)
        await session.commit()
        # await session.refresh(obj)
        return obj

    @classmethod
    async def bulk_create(cls, input_data: List[create_scheme],
                          session: AsyncSession):
        objs = [cls.table(**item.dict()) for item in input_data]
        session.add_all(objs)
        await session.commit()
        return objs


class ListMixin(BaseMixin):
    table: TableType = None  # type: ignore

    @classmethod
    async def list(cls, session: AsyncSession) -> table:
        """Get list of filtered objects"""
        query = select(cls.table).order_by(cls.table.id)
        objects = await session.execute(query)
        return objects.scalars().all()

    # TODO: retrieve with filters and get with all relations or specified?
    @classmethod
    async def retrieve(cls, pk: int, session: AsyncSession, field: str = None) -> \
            Union[table, HTTPException]:
        """Get object by primary key"""
        column = cls.get_specified_field(field) if field else cls.get_pk_attr()
        query = select(cls.table).where(column == pk)
        res = await session.execute(query)
        obj = res.scalars().first()
        cls._check_object(obj)
        await session.refresh(obj)
        return obj

    @classmethod
    async def bulk_retrieve(cls, pks: List[int], session: AsyncSession) -> \
            List[table] or HTTPException:
        """Get object by primary key"""
        query = select(cls.table).where(cls.get_pk_attr().in_(pks))
        res = await session.execute(query)
        objs = res.scalars().all()
        [cls._check_object(obj) for obj in objs]
        [await session.refresh(obj) for obj in objs]
        return objs


class UpdateMixin(ListMixin, BaseMixin):
    table: TableType = None  # type: ignore
    update_scheme: UpdateBaseSchema = None  # type: ignore

    @classmethod
    async def update(
            cls,
            pk: int,
            input_data: update_scheme,
            session: AsyncSession,
            partial: bool = False,
            field: str = None
    ) -> Union[table, HTTPException]:
        """Update object by specified primary key"""
        column = cls.get_specified_field(field) if field else cls.get_pk_attr()
        retrieved_obj = await cls.retrieve(pk, session, field)
        query = update(cls.table).where(column == pk).values(
            **input_data.dict(exclude_unset=partial, exclude_none=True))
        await cls._execute_commit(query, session)
        return retrieved_obj

    @classmethod
    async def bulk_update(
            cls,
            pks: List[int],
            input_data: update_scheme,
            session: AsyncSession,
            partial: bool = False,
    ) -> List[table] or HTTPException:
        """Update object by specified primary key"""
        retrieved_objs = await cls.bulk_retrieve(pks, session)
        query = update(cls.table).where(cls.get_pk_attr().in_(pks)).values(
            **input_data.dict(exclude_unset=partial))
        await cls._execute_commit(query, session)
        return retrieved_objs


class DeleteMixin(BaseMixin):
    @classmethod
    async def delete(cls, pk: int,
                     session: AsyncSession) -> dict or HTTPException:
        """Delete object by specified primary key"""
        await cls.retrieve(pk, session)
        query = delete(cls.table).where(cls.get_pk_attr() == pk)
        await cls._execute_commit(query, session)
        return {"status": StatusEnum.success.value}

    @classmethod
    async def delete_all(cls, session: AsyncSession):
        query = delete(cls.table)
        await cls._execute_commit(query, session)
        return {"status": StatusEnum.success.value}


class CreateUpdateMixin(CreateMixin, UpdateMixin):
    table: TableType = None  # type: ignore
    update_scheme: UpdateBaseSchema = None  # type: ignore

    @classmethod
    async def update_or_create(
            cls,
            pk: int,
            input_data: update_scheme,
            session: AsyncSession,
            field: str = None
    ) -> List[table] or HTTPException:
        retrieved_obj = cls.safe_retrieve(pk, session, field)

        if not retrieved_obj:
            return await cls.create(input_data=input_data, session=session)

        return await cls.update(pk=pk, input_data=input_data, session=session,
                                field=field)
