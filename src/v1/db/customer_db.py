import json
from typing import Any, Dict, List, Optional

import pyodbc

from v1.customers.resource.customers_in import BaseCustomer
from v1.customers.resource.customers_out import GetCustomerListOut

from .db import Database


class CustomerDB(Database):
    def __init__(self):
        super().__init__()

    def create_customer(
        self,
        tenant_id: str,
        first_name: str,
        email: str,
        last_name: Optional[str] = None,
        organization: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
        profile_image: Optional[str] = None,
        temporary_password: Optional[str] = None,
    ) -> str:
        query = """
        INSERT INTO Customers (
            TenantId, FirstName, LastName, Organization, Email, Phone,
            Address, City, State, ZipCode, Country, ProfileImage, TemporaryPassword
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    tenant_id,
                    first_name,
                    last_name,
                    organization,
                    email,
                    phone,
                    address,
                    city,
                    state,
                    zip_code,
                    country,
                    profile_image,
                    temporary_password,
                ),
            )
            conn.commit()
        return email

    def update_customer(self, tenant_id: str, email: str, **kwargs) -> bool:
        allowed_fields = {
            "first_name",
            "last_name",
            "organization",
            "phone",
            "address",
            "city",
            "state",
            "zip_code",
            "country",
            "profile_image",
            "temporary_password",
        }

        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not update_fields:
            return False

        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        query = f"""
        UPDATE Customers 
        SET {set_clause}, UpdatedAt = GETDATE()
        WHERE TenantId = ? AND Email = ?
        """

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*update_fields.values(), tenant_id, email))
            conn.commit()
            return cursor.rowcount > 0

    def delete_customer(self, tenant_id: str, email: str) -> bool:
        query = "DELETE FROM Customers WHERE TenantId = ? AND Email = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id, email))
            conn.commit()
            return cursor.rowcount > 0

    def get_customer(self, tenant_id: str, email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM Customers WHERE TenantId = ? AND Email = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id, email))
            row = cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in cursor.description], row))
            return None

    def list_customers(self, tenant_id: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Customers WHERE TenantId = ? ORDER BY CreatedAt DESC"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id,))
            return [
                dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()
            ]

    def search_customers(
        self, tenant_id: str, search_term: str
    ) -> List[Dict[str, Any]]:
        query = """
        SELECT * FROM Customers 
        WHERE TenantId = ? 
        AND (
            FirstName LIKE ? 
            OR LastName LIKE ? 
            OR Email LIKE ? 
            OR Organization LIKE ?
            OR Phone LIKE ?
        )
        ORDER BY CreatedAt DESC
        """
        search_pattern = f"%{search_term}%"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    tenant_id,
                    search_pattern,
                    search_pattern,
                    search_pattern,
                    search_pattern,
                    search_pattern,
                ),
            )
            return [
                dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()
            ]

    def select_customer(self, tenant_id: str) -> List["BaseCustomer"]:
        from v1.customers.resource.customers_in import BaseCustomer

        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                query = """
                    SELECT [TenantId]
                        ,[FirstName]
                        ,[LastName]
                        ,[Organization]
                        ,[Email]
                        ,[Phone]
                        ,[Address]
                        ,[City]
                        ,[State]
                        ,[ZipCode]
                        ,[Country]
                        ,[CreatedAt]
                        ,[UpdatedAt]
                        ,[ProfileImage]
                        ,[TemporaryPassword]
                    FROM [dbo].[Customers]
                    WHERE TenantId = ?
                """
                cursor = cnxn.cursor()
                data = cursor.execute(query, tenant_id).fetchone()

                if data:
                    return [
                        BaseCustomer(
                            tenant_id=data[0],
                            first_name=data[1],
                            last_name=data[2],
                            organization=data[3],
                            email=data[4],
                            phone=data[5],
                            address=data[6],
                            city=data[7],
                            state=data[8],
                            zip_code=data[9],
                            country=data[10],
                            created_at=data[11],
                            updated_at=data[12],
                            profile_image=data[13],
                            temporary_password=data[14],
                        )
                    ]
                return []
        except Exception as ex:
            print(f"Erro ao selecionar cliente: {ex}")
            print(ex)

    def list_customer(self) -> List["GetCustomerListOut"]:
        try:
            with pyodbc.connect(self._build_connection_string()) as cnxn:
                query = "select [dbo].[FN_API_V1_Customer_List] ()"
                cursor = cnxn.cursor()

                data = cursor.execute(query).fetchone()
                if data[0]:
                    return json.loads(data[0])
                return []

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Erro ao selecionar cliente: {sqlstate}")
            print(ex)
            print(ex)
