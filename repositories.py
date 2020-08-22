import os
import pathlib
import sqlite3
import models

current_path = pathlib.Path(os.getcwd())
DB_FILE = str(current_path.parent) + '/db/db.sqlite3'

class RepositoryI:
    def save(self, payment: models.Payment):
        raise NotImplementedError('Directly calling interface')

    def load(self):
        raise NotImplementedError('Directly calling interface')

class  SQLiteRepository(RepositoryI): 
    def save(self, payment: models.Payment):
        """
        Save (or update) payment in database
        """
        
        connection = sqlite3.connect(DB_FILE)
        c = connection.cursor()

        c.execute("SELECT COUNT(*) FROM payments WHERE id = ?", payment.id)
        # Payment doesn't exist, create new one
        if (c.fetchone()[0] == 0):
            c.execute(
                '''
                INSERT INTO payments (id, value, currency, transaction_id, created_at, status)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (payment.id, payment.money.get_value(), payment.money.get_currency(), payment.transaction_id, payment.created_at, payment.status)
            )
        # If payment already exists, update it
        else:
            c.execute(
                '''
                UPDATE payments
                SET id = ?, 
                    value = ?,
                    currency = ?,
                    transaction_id = ?,
                    created_at= ?,
                    status = ?
                ''',
                (payment.id, payment.money.get_value(), payment.money.get_currency(), payment.transaction_id, payment.created_at, payment.status)
            )
        
        connection.commit()

        connection.close()
    
    def load(self) -> models.Payment:
        """
        Returns:
            List of all payments
        """
        connection = sqlite3.connect(DB_FILE)
        connection.row_factory = sqlite3.Row
        c = connection.cursor()

        c.execute(
            "SELECT * FROM payments"
        )
        query_list = c.fetchall()

        all_payments = []
        
        for row in query_list:
            current_payment = models.Payment(
                value = row["value"],
                currency = row["currency"],
                transaction_id = row["transaction_id"],
                created_at = row["created_at"],
                status = row["status"]
            )
            current_payment.id = row["id"]

            all_payments.append(current_payment)

        connection.close()

        return all_payments

