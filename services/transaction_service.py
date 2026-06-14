from database.db import get_connection
from datetime import datetime

def get_balance(userid):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute(
        "SELECT balance FROM users WHERE userid=?",
        (userid,)
    )

    balance=cur.fetchone()[0]

    conn.close()

    return balance

def deposit(userid, amount):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM users WHERE userid=?",
        (userid,)
    )

    balance = cur.fetchone()[0]

    balance += amount

    cur.execute(
        """
        UPDATE users
        SET balance=?
        WHERE userid=?
        """,
        (balance, userid)
    )

    from datetime import datetime

    cur.execute(
        """
        INSERT INTO transactions
        (userid,amount,balance,function,date)
        VALUES(?,?,?,?,?)
        """,
        (
            userid,
            amount,
            balance,
            "Deposit",
            datetime.now().strftime("%Y-%m-%d")
        )
    )

    conn.commit()
    conn.close()
    
def withdraw(userid, amount):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM users WHERE userid=?",
        (userid,)
    )

    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    balance = row[0]

    if amount > balance:
        conn.close()
        return False

    balance -= amount

    cur.execute(
        """
        UPDATE users
        SET balance=?
        WHERE userid=?
        """,
        (balance, userid)
    )

    from datetime import datetime

    cur.execute(
        """
        INSERT INTO transactions
        (userid,amount,balance,function,date)
        VALUES(?,?,?,?,?)
        """,
        (
            userid,
            amount,
            balance,
            "Withdraw",
            datetime.now().strftime("%Y-%m-%d")
        )
    )

    conn.commit()
    conn.close()

    return True