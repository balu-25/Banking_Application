from services.auth_service import hash_password
from database.db import get_connection

conn=get_connection()
cur=conn.cursor()

cur.execute("""
INSERT INTO admins
VALUES
(
'2005',
'Balu',
'Manager',
?
)
""",(hash_password('admin2005'),))

conn.commit()
conn.close()