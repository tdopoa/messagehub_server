from typing import List
from uuid import UUID

import pyodbc

from ..contacts.resource.base_contacts import BaseContact
from .db import Database


class ContactDB(Database):
    def __init__(self):
        super().__init__()

    def update_contact(self, contact: BaseContact):
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                cursor = cnxn.cursor()
                sql = """
                    UPDATE Contacts 
                    SET FirstName = ?,
                        LastName = ?,
                        Organization = ?,
                        Mobile = ?,
                        Email = ?,
                        Fax = ?,
                        Custom1 = ?,
                        Custom2 = ?,
                        Custom3 = ?,
                        Custom4 = ?,
                        Address = ?,
                        UpdatedAt = GETDATE()
                    WHERE Id = ?
                """
                values = (
                    contact.first_name,
                    contact.last_name,
                    contact.organization,
                    contact.mobile,
                    contact.email,
                    contact.fax,
                    contact.custom1,
                    contact.custom2,
                    contact.custom3,
                    contact.custom4,
                    contact.address,
                    contact.id,
                )
                cursor.execute(sql, values)
                cnxn.commit()
                print(
                    f"Contato {contact.first_name} {contact.last_name} alterado com sucesso."
                )
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao alterar contato: {sqlstate}")
            print(ex)

    def insert_contact(self, contact: BaseContact):
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                cursor = cnxn.cursor()
                sql = """
                INSERT INTO Contacts (
                    FirstName, LastName, Organization, Mobile, Email, 
                    Fax, Custom1, Custom2, Custom3, Custom4, Address
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                values = (
                    contact.first_name,
                    contact.last_name,
                    contact.organization,
                    contact.mobile,
                    contact.email,
                    contact.fax,
                    contact.custom1,
                    contact.custom2,
                    contact.custom3,
                    contact.custom4,
                    contact.address,
                )
                cursor.execute(sql, values)
                cnxn.commit()
                print(
                    f"Contato {contact.first_name} {contact.last_name} inserido com sucesso."
                )
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao inserir contato: {sqlstate}")
            print(ex)

    def select_contact(self, id: UUID = None) -> List[BaseContact]:
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                query = """
                SELECT 
                    Id, FirstName, LastName, Organization, Mobile, 
                    Email, Fax, Custom1, Custom2, Custom3, Custom4, 
                    Address, CreatedAt, UpdatedAt
                FROM Contacts 
                WHERE Id = ?
                """
                cursor = cnxn.cursor()
                data = cursor.execute(query, id).fetchone()

                if data:
                    return [
                        BaseContact(
                            id=data[0],
                            first_name=data[1],
                            last_name=data[2],
                            organization=data[3],
                            mobile=data[4],
                            email=data[5],
                            fax=data[6],
                            custom1=data[7],
                            custom2=data[8],
                            custom3=data[9],
                            custom4=data[10],
                            address=data[11],
                            created_at=data[12],
                            updated_at=data[13],
                        )
                    ]
                return []
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao selecionar contato: {sqlstate}")
            print(ex)

    def list_contacts(self) -> List[BaseContact]:
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                query = """
                SELECT 
                    Id, FirstName, LastName, Organization, Mobile, 
                    Email, Fax, Custom1, Custom2, Custom3, Custom4, 
                    Address, CreatedAt, UpdatedAt
                FROM Contacts
                """
                cursor = cnxn.cursor()
                data = cursor.execute(query).fetchall()

                contacts = []
                for row in data:
                    contacts.append(
                        BaseContact(
                            id=row[0],
                            first_name=row[1],
                            last_name=row[2],
                            organization=row[3],
                            mobile=row[4],
                            email=row[5],
                            fax=row[6],
                            custom1=row[7],
                            custom2=row[8],
                            custom3=row[9],
                            custom4=row[10],
                            address=row[11],
                            created_at=row[12],
                            updated_at=row[13],
                        )
                    )
                return contacts
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao listar contatos: {sqlstate}")
            print(ex)

    def delete_contact(self, id: UUID):
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                cursor = cnxn.cursor()
                sql = "DELETE FROM Contacts WHERE Id = ?"
                cursor.execute(sql, id)
                cnxn.commit()
                print(f"Contato com ID {id} excluído com sucesso.")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao excluir contato: {sqlstate}")
            print(ex)
            print(ex)
            print(ex)
            print(ex)
