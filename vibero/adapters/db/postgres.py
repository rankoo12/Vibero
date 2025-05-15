from typing import Sequence, Optional, Type, Any, Awaitable, Callable
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from vibero.adapters.db.models import FallbackModel, Base
from vibero.core.persistence.common import Where
from vibero.core.loggers import Logger
from vibero.core.persistence.document_database import (
    BaseDocument,
    DocumentDatabase,
    DocumentCollection,
    TDocument,
    InsertResult,
    UpdateResult,
    DeleteResult,
)



# === Database access layer ===
class PostgresDB:
    def __init__(self, logger: Logger):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        load_dotenv() # loads variables from .env into environment

        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL is not set in the environment.")
        
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._logger = logger
        self._collections: dict[str, PostgresTableCollection[Any]] = {}
    
    def init_db(self):
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()
    
    async def create_collection(
        self,
        name: str,
        schema: type[TDocument],
    ) -> DocumentCollection[TDocument]:
        raise NotImplementedError("create_collection not implemented yet")

    async def get_or_create_collection(
        self,
        name: str,
        schema: type[TDocument],
        document_loader: Callable[[BaseDocument], Awaitable[Optional[TDocument]]],
        orm_model=None
    ) -> DocumentCollection[TDocument]:
        return await self.get_collection(name, schema, document_loader, orm_model)

    async def get_collection(
        self,
        name: str,
        schema: Type[TDocument],
        document_loader=None,
        orm_model=None
    ) -> DocumentCollection[TDocument]:
        if name not in self._collections:
            self._logger.warning(f"No ORM model found for collection '{name}', using fallback.")
            self._collections[name] = PostgresTableCollection(schema=schema, db=self, logger=self._logger, orm_model=orm_model or FallbackModel)
        return self._collections[name]

    async def delete_collection(self, name: str) -> None:
        raise NotImplementedError("delete_collection not implemented yet")


# === Main DocumentDatabase ===
class PostgresDocumentDatabase(DocumentDatabase):
    def __init__(self, logger: Logger):
        self._logger = logger
        self.db = PostgresDB(logger)
        self._collections: dict[str, PostgresTableCollection[Any]] = {}

    async def create_collection(
        self,
        name: str,
        schema: type[TDocument],
    ) -> DocumentCollection[TDocument]:
        raise NotImplementedError("create_collection not implemented yet")

    async def get_or_create_collection(
        self,
        name: str,
        schema: type[TDocument],
        document_loader: Callable[[BaseDocument], Awaitable[Optional[TDocument]]],
    ) -> DocumentCollection[TDocument]:
        return await self.get_collection(name, schema, document_loader)

    async def get_collection(
        self,
        name: str,
        schema: Type[TDocument],
        document_loader=None,
    ) -> DocumentCollection[TDocument]:
        if name not in self._collections:
            self._logger.warning(f"No ORM model found for collection '{name}', using fallback.")
            self._collections[name] = PostgresTableCollection(schema=schema, db=self.db, logger=self._logger, orm_model=FallbackModel)
        return self._collections[name]

    async def delete_collection(self, name: str) -> None:
        raise NotImplementedError("delete_collection not implemented yet")


# === Collection wrapper ===
class PostgresTableCollection(DocumentCollection[TDocument]):
    def __init__(self, schema: Type[TDocument], orm_model: type[Any], db: PostgresDB, logger: Logger):
        self.db = db
        self.schema = schema
        self.orm_model = orm_model  # ✅ Add this line
        self._logger = logger

    async def find(self, filters: Where) -> Sequence[TDocument]:
        with self.db.get_session() as session:
            return session.query(self.orm_model).filter_by(**filters).all()

    async def find_one(self, filters: Where) -> Optional[TDocument]:
        with self.db.get_session() as session:
            return session.query(self.orm_model).filter_by(**filters).first() 

    async def insert_one(self, document: TDocument) -> InsertResult:
        with self.db.get_session() as session:
            orm_obj = self.orm_model(**document.__dict__)
            session.add(orm_obj)
            session.commit()
            return InsertResult(acknowledged=True)

    async def update_one(
    self,
    filters: Where,
    params: dict,
    upsert: bool = False,
) -> UpdateResult[TDocument]:
     with self.db.get_session() as session:
        obj = session.query(self.orm_model).filter_by(**filters).first()
        
        if obj:
            for k, v in params.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
            session.commit()

            # Detach so it's safe to return
            session.refresh(obj)
            session.expunge(obj)

            return UpdateResult(True, 1, 1, obj)

        elif upsert:
            new_obj = self.orm_model(**params)
            session.add(new_obj)
            session.commit()

            session.refresh(new_obj)
            session.expunge(new_obj)

            return UpdateResult(True, 0, 1, new_obj)

        else:
            return UpdateResult(False, 0, 0, None)

    async def delete_one(self, filters: Where) -> DeleteResult[TDocument]:
        with self.db.get_session() as session:
            obj = session.query(self.orm_model).filter_by(**filters).first() 
            if obj:
                session.delete(obj)
                session.commit()
                return DeleteResult(True, 1, obj)
            return DeleteResult(True, 0, None)
