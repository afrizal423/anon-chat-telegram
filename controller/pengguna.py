from sqlalchemy.sql.functions import random
from config.db import conn
from model.pengguna import pgn, idle, plprn
from sqlalchemy import select
from config.redis import r
from config.bot import bot
from datetime import datetime
import time




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

def cariPartner(id, mssge_id, msg, loopnya):
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
    
    query2 = """
select id_user, username_user, firstname_user, jeniskelamin_user, ketertarikan_user, umur_user, (
select status from tbl_iddle where id_user = tbl_pengguna.id_user) as statusnya
from tbl_pengguna
where ( id_user in (
select id_user from tbl_iddle
where status = 'true') and
jeniskelamin_user = 'L' and
id_user != '{}') or (
id_user in (
select id_user from tbl_iddle
where status = 'true') and
jeniskelamin_user = 'P' and
id_user != '{}')
order by random() 
    """.format(identitas['id_user'], identitas['id_user'])
    data = conn.execute(query2).fetchone()
    if data is not None and r.exists("inchat_{}".format(data['id_user'])) == 0:
        # hapus antrean
        id_antrian = "antrian_{}".format(identitas['id_user'])
        id_antrian2 = "antrian_{}".format(data['id_user'])
        # print("hapus ", id_antrian)
        # print("hapus ", id_antrian2)
        r.delete(id_antrian)
        r.delete(id_antrian2)
        #
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

<strong>Pastikan obrolan tidak melanggar /rules ya.</strong>
<strong>Jika partnermu melanggar silahkan /lapor.</strong>
    \
            """.format("Laki-Laki 👦" if data['jeniskelamin_user'] == 'L' else "Perempuan 👧"), parse_mode='HTML')
        # ini yang nerima
        bot.send_message(data['id_user'],"""\
<strong>Yeeeayy, kamu mendapatkan teman ngobrol.</strong>
🔹Gender            : {}

<strong>Pastikan obrolan tidak melanggar /rules ya.</strong>
<strong>Jika partnermu melanggar, silahkan /lapor.</strong>
    \
            """.format("Laki-Laki 👦" if identitas['jeniskelamin_user'] == 'L' else "Perempuan 👧"), parse_mode='HTML')
    # print(conn.execute(query).fetchone())
    else :
        # print(loopnya)
        # 1800 artinya 30 menit 
        if loopnya < 1800 and r.exists("inchat_{}".format(identitas['id_user'])) == 0 and r.exists("antrian_{}".format(identitas['id_user'])):
            loopnya+=1
            time.sleep(1)
            cariPartner(id, mssge_id, msg, loopnya)
        elif loopnya == 1800:
            # print("batassss")
            now = datetime.now()
            iddle = {
                'status': False,
                'mssg_id': None,
                'updated_at': now.strftime("%Y/%m/%d %H:%M:%S")
            }
            updateDataIddle(iddle, id)
            id_antrian = "antrian_{}".format(identitas['id_user'])
            r.delete(id_antrian)
            bot.send_message(msg.chat.id,"""\
⚠️<strong>Upsss, sepertinya proses terlalu lama.</strong>⚠️

<strong>Silahkan mulai ulang lagi /start.</strong>
\
            """, parse_mode='HTML')
        else:
            return

def pisahPartner(id, mssge_id):
    satu = "inchat_"+str(mssge_id)
    dua = "inchat_"+r.hget("inchat_{}".format(mssge_id), mssge_id).decode("utf8")
    now = datetime.now()
    iddle = {
        'status': False,
        'mssg_id': None,
        'updated_at': now.strftime("%Y/%m/%d %H:%M:%S")
    }
    updateDataIddle(iddle, id)
    iddle = {
        'status': False,
        'mssg_id': None,
        'updated_at': now.strftime("%Y/%m/%d %H:%M:%S")
    }
    updateDataIddle(iddle, r.hget("inchat_{}".format(mssge_id), mssge_id).decode("utf8"))
    
    r.delete(satu)
    r.delete(dua)
    
# Ini tambah laporan
def tambahLaporan(data):
    query = plprn.insert().values(data)
    conn.execute(query)
