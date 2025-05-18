import json
import os
from typing import List
from uuid import UUID

import pyodbc

from app.db.db import Database
from v1.users.schema.input.users import BaseUser
from v1.users.schema.output.users import GetUserListOut


class UserDB(Database):
    def update_user(self, user: BaseUser):
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                cursor = cnxn.cursor()
                sql = """
                    EXECUTE [dbo].[PRD_API_V1_User_Update] 
                         @UserId = ?
                        ,@FirstName = ?
                        ,@LastName = ?
                        ,@Email = ?
                        ,@Password = ?
                """
                values = (
                    user.user_id,
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.password,
                )
                cursor.execute(sql, values)
                cnxn.commit()
                print(
                    f"Cliente {user.first_name} {user.last_name} alterado com sucesso."
                )
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao alterar cliente: {sqlstate}")
            print(ex)

    def insert_user(self, user: BaseUser):
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                cursor = cnxn.cursor()
                sql = """
                INSERT INTO Users (FirstName, LastName, Email, Password, CreatedAt, UpdatedAt)
                VALUES (?, ?, ?, ?, GETDATE(), GETDATE())
                """
                values = (user.first_name, user.last_name, user.email, user.password)
                cursor.execute(sql, values)
                cnxn.commit()
                print(
                    f"Cliente {user.first_name} {user.last_name} inserido com sucesso."
                )
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao inserir cliente: {sqlstate}")
            print(ex)

    def select_user(self, id: UUID = None) -> List[BaseUser]:
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                query = "SELECT  [dbo].[FN_API_V1_User_ById] (?)"
                params = id
                cursor = cnxn.cursor()

                data = cursor.execute(query, params).fetchone()
                if data[0]:
                    return json.loads(data[0])
                return []

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao selecionar usuario: {sqlstate}")
            print(ex)

    def list_user(self) -> List[GetUserListOut]:
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                query = "select [dbo].[FN_API_V1_User_List] ()"
                cursor = cnxn.cursor()

                data = cursor.execute(query).fetchone()
                if data[0]:
                    return json.loads(data[0])
                return []

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao selecionar usuario: {sqlstate}")
            print(ex)
