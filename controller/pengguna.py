from sqlalchemy.sql.functions import random
from config.db import conn
from model.pengguna import pgn, idle, plprn
from sqlalchemy import select
from config.redis import r
from config.bot import bot


def getData(id):
    query = pgn.select().where(pgn.c.id_user ==  f'{id}')
    cek = conn.execute(query).fetchone()
    return cek

def insertData(data):
    query = pgn.insert().values(data)
    conn.execute(query)

def insertDataIddle(data):
    query = idle.insert().values(data)
    conn.execute(query)

def updateDataIddle(data, id):
    query = idle.update().values(data).where(idle.c.id_user ==  f'{id}')
    conn.execute(query)

def updateData(data, id):
    query = pgn.update().values(data).where(pgn.c.id_user ==  f'{id}')
    conn.execute(query)

def cekUmur(id):
    query = pgn.select().where(pgn.c.id_user ==  f'{id}')
    cek = conn.execute(query).fetchone()
    return cek['umur_user']

def cekJenKel(id):
    query = pgn.select().where(pgn.c.id_user ==  f'{id}')
    cek = conn.execute(query).fetchone()
    return cek['jeniskelamin_user']

def cekKetertarikan(id):
    query = pgn.select().where(pgn.c.id_user ==  f'{id}')
    cek = conn.execute(query).fetchone()
    return cek['ketertarikan_user']

def cariPartner(id, mssge_id, msg):
    iddle = {
        'status': True,
        'mssg_id': mssge_id
    }
    updateDataIddle(iddle, id)
    identitas = getData(id)
    query = select([pgn.columns.id_user, pgn.columns.jeniskelamin_user, 
                    pgn.columns.ketertarikan_user, 
                    pgn.columns.umur_user, 
                    idle.columns.status]).where(
                        pgn.c.id_user == idle.c.id_user).where(
                            pgn.c.id_user !=  f'{id}').where(
                                pgn.c.jeniskelamin_user == identitas['ketertarikan_user']).where(
                                    idle.c.status == 'true'
                                    ).where(
                                    pgn.c.umur_user.between(
                                        identitas['umur_user']-5 if identitas['jeniskelamin_user'] == 'L' else identitas['umur_user']-3, identitas['umur_user']+3 if identitas['jeniskelamin_user'] == 'L' else identitas['umur_user']+5)).order_by(random()).limit(1)
    data = conn.execute(query).fetchone()
    if data is not None and r.exists("inchat_{}".format(data['id_user'])) == 0:
        toRedis = {
            mssge_id: data['id_user'],
            data['id_user']: mssge_id
        }
        r.hmset("inchat_"+str(mssge_id),toRedis)
        r.hmset("inchat_"+str(data['id_user']),toRedis)
        # ini yang ngirim
        bot.send_message(msg.chat.id,"""\
<strong>Yeeeayy, kamu mendapatkan teman ngobrol.</strong>
🔹Gender            : {}
🔹Umur               : {} Tahun 🎂
    \
            """.format("Laki-Laki 👦" if data['jeniskelamin_user'] == 'L' else "Perempuan 👧", 
                       data['umur_user']), parse_mode='HTML')
        # ini yang nerima
        bot.send_message(data['id_user'],"""\
<strong>Yeeeayy, kamu mendapatkan teman ngobrol.</strong>
🔹Gender            : {}
🔹Umur               : {} Tahun 🎂
    \
            """.format("Laki-Laki 👦" if identitas['jeniskelamin_user'] == 'L' else "Perempuan 👧", 
                       identitas['umur_user']), parse_mode='HTML')
    # print(conn.execute(query).fetchone())

def pisahPartner(id, mssge_id):
    satu = "inchat_"+str(mssge_id)
    dua = "inchat_"+r.hget("inchat_{}".format(mssge_id), mssge_id).decode("utf8")
    iddle = {
        'status': False,
        'mssg_id': None
    }
    updateDataIddle(iddle, id)
    iddle = {
        'status': False,
        'mssg_id': None
    }
    updateDataIddle(iddle, r.hget("inchat_{}".format(mssge_id), mssge_id).decode("utf8"))
    
    r.delete(satu)
    r.delete(dua)
    
# Ini tambah laporan
def tambahLaporan(data):
    query = plprn.insert().values(data)
    conn.execute(query)
