from database.db import get_connection

def apply_loan(userid, loan_type,
               amount, interest, duration):

    si = (amount * interest * duration) / 100

    total_amount = amount + si

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO loans(
        userid,
        typeofloan,
        amount,
        interest,
        duration,
        total_amount,
        amtpaid
    )
    VALUES(?,?,?,?,?,?,?)
    """,
    (
        userid,
        loan_type,
        amount,
        interest,
        duration,
        total_amount,
        0
    ))

    # Add loan amount to user's account
    cur.execute(
        "SELECT balance FROM users WHERE userid=?",
        (userid,)
    )

    balance = cur.fetchone()[0]

    new_balance = balance + amount

    cur.execute(
        """
        UPDATE users
        SET balance=?
        WHERE userid=?
        """,
        (new_balance, userid)
    )

    conn.commit()
    conn.close()

def pay_loan(userid, payment):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id,
           total_amount,
           amtpaid
    FROM loans
    WHERE userid=?
    ORDER BY id DESC
    LIMIT 1
    """,
    (userid,)
    )

    loan = cur.fetchone()

    if not loan:
        conn.close()
        return False

    loan_id = loan[0]
    total_amount = loan[1]
    paid_amount = loan[2]

    pending = total_amount - paid_amount

    if payment > pending:
        conn.close()
        return False

    # Check balance
    cur.execute(
        "SELECT balance FROM users WHERE userid=?",
        (userid,)
    )

    balance = cur.fetchone()[0]

    if payment > balance:
        conn.close()
        return False

    # Deduct from balance
    balance -= payment

    cur.execute(
        """
        UPDATE users
        SET balance=?
        WHERE userid=?
        """,
        (balance, userid)
    )

    cur.execute(
        """
        UPDATE loans
        SET amtpaid=?
        WHERE id=?
        """,
        (paid_amount + payment, loan_id)
    )

    conn.commit()
    conn.close()

    return True
def get_pending_loan(userid):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT total_amount, amtpaid
    FROM loans
    WHERE userid=?
    ORDER BY id DESC
    LIMIT 1
    """,
    (userid,)
    )

    row = cur.fetchone()

    conn.close()

    if row:

        total = row[0]
        paid = row[1]

        return total - paid

    return 0