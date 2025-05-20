import json
from typing import List
from uuid import UUID

import pyodbc

from app.db.db import Database

from ...src.v1.profiles.schema.input.profiles import BaseProfile
from ...src.v1.profiles.schema.output.profiles import GetProfileListOut


class ProfileDB(Database):
    def update_profile(self, profile: BaseProfile):
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                cursor = cnxn.cursor()
                sql = """
                    UPDATE Profiles 
                    SET FirstName = ?,
                        LastName = ?,
                        Email = ?,
                        Phone = ?,
                        Password = ?,
                        UpdatedAt = GETDATE()
                    WHERE Id = ?
                """
                values = (
                    profile.first_name,
                    profile.last_name,
                    profile.email,
                    profile.phone,
                    profile.password,
                    profile.id,
                )
                cursor.execute(sql, values)
                cnxn.commit()
                print(
                    f"Perfil {profile.first_name} {profile.last_name} alterado com sucesso."
                )
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao alterar perfil: {sqlstate}")
            print(ex)

    def insert_profile(self, profile: BaseProfile):
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                cursor = cnxn.cursor()
                sql = """
                INSERT INTO Profiles (
                    FirstName, LastName, Email, Phone, Password
                )
                VALUES (?, ?, ?, ?, ?)
                """
                values = (
                    profile.first_name,
                    profile.last_name,
                    profile.email,
                    profile.phone,
                    profile.password,
                )
                cursor.execute(sql, values)
                cnxn.commit()
                print(
                    f"Perfil {profile.first_name} {profile.last_name} inserido com sucesso."
                )
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao inserir perfil: {sqlstate}")
            print(ex)

    def select_profile(self, id: UUID = None) -> List[BaseProfile]:
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                query = """
                SELECT 
                    id, FirstName as first_name, LastName as last_name, Email as email, Phone as phone, 
                    Password as password, CreatedAt as created_at, UpdatedAt as updated_at, TenantId as tenant_id
                FROM Profiles 
                WHERE Id = ?
                """
                cursor = cnxn.cursor()
                data = cursor.execute(query, id).fetchone()

                if data:
                    return [
                        BaseProfile(
                            id=data[0],
                            first_name=data[1],
                            last_name=data[2],
                            email=data[3],
                            phone=data[4],
                            password=data[5],
                            created_at=data[6],
                            updated_at=data[7],
                            tenant_id=data[8],
                        )
                    ]
                return []
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao selecionar perfil: {sqlstate}")
            print(ex)

    def list_profiles(self) -> List[GetProfileListOut]:
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                query = """
                SELECT 
                    Id, FirstName, LastName, Email, Phone, 
                    Password, CreatedAt, UpdatedAt, TenantId
                FROM Profiles
                """
                cursor = cnxn.cursor()
                data = cursor.execute(query).fetchall()

                profiles = []
                for row in data:
                    profiles.append(
                        GetProfileListOut(
                            id=row[0],
                            first_name=row[1],
                            last_name=row[2],
                            email=row[3],
                            phone=row[4],
                            password=row[5],
                            created_at=row[6],
                            updated_at=row[7],
                            tenant_id=row[8],
                        )
                    )
                return profiles
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao listar perfis: {sqlstate}")
            print(ex)

    def delete_profile(self, id: UUID):
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                cursor = cnxn.cursor()
                sql = "DELETE FROM Profiles WHERE Id = ?"
                cursor.execute(sql, id)
                cnxn.commit()
                print(f"Perfil com ID {id} excluído com sucesso.")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao excluir perfil: {sqlstate}")
            print(ex)
