from bots import (
    bot,
    telebot
)
import controller.pengguna as pengguna
import uuid
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.message_handler(commands=['start','cari_partner'])
def start(message):
    cek = pengguna.getData(message.from_user.id)
    # print(cek)
    if cek == None:
        bot.send_message(message.chat.id,"""\
Upss, nampaknya anda pengguna baru.
Silahkan lengkapi data di menu /pengaturan
\
""")
    elif cek['ketertarikan_user'] == None or cek['umur_user'] == None:
        bot.send_message(message.chat.id,"""\
Upss, nampaknya ada beberapa pengaturan yang belum lengkap.
Silahkan lengkapi di menu /pengaturan
\
""")
    else:
        bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['pengaturan','settings'])
def pengaturan(message):
    global idnya_user
    idnya_user = message.from_user.id
    cek = pengguna.getData(message.from_user.id)
    if cek == None:
        now = datetime.now()
        data = {
            'user_uuid': uuid.uuid4(),
            'id_user': message.from_user.id,
            'username_user': message.from_user.username,
            'firstname_user': message.from_user.first_name,
            'lastname_user': message.from_user.last_name,
            'joined_at': now.strftime("%d/%m/%Y %H:%M:%S")
        }
        pengguna.insertData(data)
        data = {
            'iddle_uuid': uuid.uuid4(),
            'id_user': message.from_user.id,
            'status': False
        }
        pengguna.insertDataIddle(data)
    
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
            telebot.types.InlineKeyboardButton('🥰 Umur', callback_data='set-umur'),
        )
    keyboard.row(
            telebot.types.InlineKeyboardButton('💕 Ketertarikan Gender', callback_data='set-gender')
        )
    keyboard.row(
            telebot.types.InlineKeyboardButton('❌ Batal', callback_data='set-batal')
        )
    if cek['umur_user'] is not None and cek['ketertarikan_user'] is None:
        bot.send_message(message.chat.id, """\
⚙️ <em><strong>Pengaturan</strong></em>
Pada menu ini adalah halaman untuk mengubah beberapa identitas.
Silahkan ubah sesuai kondisi yang kamu inginkan.
Agar nantinya sistem akan mencocokan orang yang tepat buatmu.😋

Pengaturan yang sudah tersimpan:
Umur: {}
\
""".format(cek['umur_user']), parse_mode="HTML" ,reply_markup=keyboard)
    elif cek['ketertarikan_user'] is not None and cek['umur_user'] is not None:
        bot.send_message(message.chat.id, """\
⚙️ <em><strong>Pengaturan</strong></em>
Pada menu ini adalah halaman untuk mengubah beberapa identitas.
Silahkan ubah sesuai kondisi yang kamu inginkan.
Agar nantinya sistem akan mencocokan orang yang tepat buatmu.😋

Pengaturan yang sudah tersimpan:🚻
Umur {} Tahun
Ketertarikan pada {}
\
""".format(cek['umur_user'], "Laki-Laki" if cek['ketertarikan_user'] == 'L' else "Perempuan" ), parse_mode="HTML" ,reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, """\
⚙️ <em><strong>Pengaturan</strong></em>
Pada menu ini adalah halaman untuk mengubah beberapa identitas.
Silahkan ubah sesuai kondisi yang kamu inginkan.
Agar nantinya sistem akan mencocokan orang yang tepat buatmu.😋
    \
    """, parse_mode="HTML" ,reply_markup=keyboard)
    # bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    global chat_ids, msg_id
    chat_ids = message.chat.id
    msg_id = message.id