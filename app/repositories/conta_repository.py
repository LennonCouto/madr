from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Conta


def get_by_username_or_email(session: Session, username: str, email: str):
    stmt = session.scalar(
        select(Conta).where(
            (Conta.username == username) | (Conta.email == email)
        )
    )

    return stmt


def create_conta(session: Session, conta: Conta):
    session.add(conta)
    session.commit()
    session.refresh(conta)

    return conta
