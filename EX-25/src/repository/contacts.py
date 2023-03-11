from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session):
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id)).all()
    return contacts


async def get_contact(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def birthday_list(db: Session):
    contacts_list = []
    dt_now = datetime.now()
    now_year = datetime.now().strftime('%Y')
    contacts_all = db.query(Contact).all()
    for contact in contacts_all:
        delta = contact.birthday.replace(year=int(now_year)) - dt_now
        if timedelta(days=-1) < delta < timedelta(days=7):
            contacts_list.append(contact)
    return contacts_list


async def searcher(part_to_search: str, db: Session):
    contact_list = []
    contacts_all = db.query(Contact).all()
    for contact in contacts_all:
        if part_to_search.capitalize() in contact.name.capitalize() and contact not in contact_list:
            contact_list.append(contact)
        if part_to_search.capitalize() in contact.surname.capitalize() and contact not in contact_list:
            contact_list.append(contact)
        if part_to_search.capitalize() in contact.email.capitalize() and contact not in contact_list:
            contact_list.append(contact)

    return contact_list