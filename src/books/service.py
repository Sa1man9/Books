from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel,BookUpdateModel
from sqlmodel import select,desc
from .models import Book

class BookService:
    async def get_all_Books(self,session:AsyncSession):
        statement= select(Book).order_by(desc(Book.created_at))
        res=await session.exec(statement)
        return res.all()

    async def get_Book(self,book_uuid:str,session:AsyncSession):
        statement= select(Book).where(Book.uid==book_uuid)
        res=await session.exec(statement)
        book= res.first()
        
        return book if book is not None else None

    async def create_Book(self,book_data:BookCreateModel,session:AsyncSession):
        book_data_dict=book_data.model_dump()

        new_book=Book(
            **book_data_dict
        )

        session.add(new_book)

        await session.commit()

        return new_book

    async def update_Book(self,book_uid:str,update_data:BookUpdateModel,session:AsyncSession):
        book_to_update=self.get_Book(book_uid, session)

        if book_to_update is not None:

            update_data_dict=update_data.model_dump()

            for k, v in update_data_dict.items():
                setattr(book_to_update,k,v)

            await session.commit()

            return book_to_update
        else:
            return None
    
    async def delete_Book(self,book_uid:str,session:AsyncSession):
        book_to_delete=self.get_Book(book_uid, session)

        if book_to_delete is not None:

            await session.delete(book_to_delete)

            await session.commit()

            return 
        else:
            return None