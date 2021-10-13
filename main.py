from alembic.op import f
from fastapi import FastAPI, Request
from config.db import database, conn, config
import controller.pengguna as pengguna
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid
from datetime import datetime
from config.redis import r
from config.bot import bot, TOKEN
import uvicorn


config.read('konfig.ini')

app = FastAPI()

@app.on_event("startup")
async def startup():
    bot.set_webhook(url=config.get('BotKu', 'URL_WEBSITE') + TOKEN)
    await database.connect()    

@app.on_event("shutdown")
async def shutdown():
    bot.remove_webhook()
    await database.disconnect()

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
    elif cek['ketertarikan_user'] == None or cek['umur_user'] == None or cek['jeniskelamin_user'] == None:
        bot.send_message(message.chat.id,"""\
Upss, nampaknya ada beberapa pengaturan yang belum lengkap.
Silahkan lengkapi di menu /pengaturan
\
""")
    elif r.exists("inchat_{}".format(message.from_user.id)):
        bot.send_message(message.chat.id,"""\
⚠️ <em><b>Anda sedang didalam chat bersama partnermu</b></em> ⚠️
Jika kamu ingin mencari yang lain silahkan tekan /lewati .
Atau jika ingin berhenti tekan /berhenti
\
""", parse_mode='HTML')
    else:
    # print(r.exists("inchat_{}".format(message.from_user.id)))
        bot.send_message(message.chat.id, """\
<em><strong>Sedang mencari partner ngobrol</strong></em>⌛
    \
    """, parse_mode="HTML")
        pengguna.cariPartner(message.from_user.id, message.chat.id, message)

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
            telebot.types.InlineKeyboardButton('🥰 Umur {}'.format("❗" if pengguna.cekUmur(message.from_user.id) is None else "✅"), callback_data='set-umur'),
        )
    keyboard.row(
            telebot.types.InlineKeyboardButton('🚻 Jenis Kelamin {}'.format("❗" if pengguna.cekJenKel(message.from_user.id) is None else "✅"), callback_data='set-jenkel'),
        )
    keyboard.row(
            telebot.types.InlineKeyboardButton('💕 Ketertarikan Gender {}'.format("❗" if pengguna.cekKetertarikan(message.from_user.id) is None else "✅"), callback_data='set-gender')
        )
    keyboard.row(
            telebot.types.InlineKeyboardButton('❌ Batal', callback_data='set-batal')
        )
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


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith('set-umur'):
        bot.answer_callback_query(call.id, "Silahkan ketik umur kamu berupa digit angka.")
        # bot.edit_message_text(text="szxcasdasdasdasd", chat_id=chat_ids, message_id=msg_id)
        msg = bot.edit_message_text(text="Berapa umurmu sekarang? 🔢", chat_id=call.message.chat.id, message_id=call.message.id)
        global chat_ids, msg_id
        chat_ids = call.message.chat.id
        msg_id = call.message.id
        bot.register_next_step_handler(msg, proses_umur)
        # bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None)
    
    elif call.data.startswith('set-jenkel'):
        
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Aku adalah Laki-laki 🚹', callback_data='jenkel-l'),
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Aku adalah Perempuan 🚺', callback_data='jenkel-p')
        )
        bot.edit_message_text("""
\
Silahkan pilih identitasmu🚻.
\
        """, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)
        
    elif call.data.startswith('set-gender'):
        
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Laki-laki 🚹', callback_data='gender-l'),
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Perempuan 🚺', callback_data='gender-p')
        )
        bot.edit_message_text("""
\
Silahkan pilih gender pasanganmu.
Agar nantinya sistem akan mencocokan orang yang tepat buatmu.😋
\
        """, chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)
        
    elif call.data.startswith('set-batal'):
        bot.edit_message_text("""
\
<strong>Perintah dibatalkan.</strong>
\
        """, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode="HTML")
    
    elif call.data.startswith('jenkel-l'):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        data = {
            "jeniskelamin_user": "L"
        }
        pengguna.updateData(data,idnya_user)
        bot.send_message(call.message.chat.id,"""\
Pengaturan gender telah disimpan. 📋📌
\
        """)
    elif call.data.startswith('jenkel-p'):
        print(call.message.from_user.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        data = {
            "jeniskelamin_user": "P"
        }
        pengguna.updateData(data,idnya_user)
        bot.send_message(call.message.chat.id,"""\
Pengaturan gender telah disimpan. 📋📌
\
        """)
    
        
    elif call.data.startswith('gender-l'):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        data = {
            "ketertarikan_user": "L"
        }
        pengguna.updateData(data,idnya_user)
        bot.send_message(call.message.chat.id,"""\
Pengaturan ketertarikan gender telah disimpan. 📋📌
\
        """)
    elif call.data.startswith('gender-p'):
        print(call.message.from_user.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        data = {
            "ketertarikan_user": "P"
        }
        pengguna.updateData(data,idnya_user)
        bot.send_message(call.message.chat.id,"""\
Pengaturan ketertarikan gender telah disimpan. 📋📌
\
        """)
        
def proses_umur(message):
    try:
        umur = message.text
        if not umur.isdigit():
            msg = bot.reply_to(message, 'Inputan umur haruslah berupa angka🔢.\nBerapa umurmu sekarang?')
            bot.register_next_step_handler(msg, proses_umur)
            return
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        bot.delete_message(chat_id=chat_ids, message_id=msg_id)
        data = {
            "umur_user": umur
        }
        pengguna.updateData(data,message.from_user.id)
        bot.send_message(message.chat.id,"""\
Pengaturan umur telah disimpan. 📋📌
\
""")
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['stop','berhenti'])
def stop(message: telebot.types.Message):
    if r.exists("inchat_{}".format(message.from_user.id)):
        bot.send_message(message.chat.id, "<em><strong>Kamu telah menyudahi obrolan bersama partnermu.</strong></em>😐", parse_mode="HTML")
        bot.send_message(r.hget("inchat_{}".format(message.chat.id), message.chat.id).decode("utf8"), "<em><strong>Duhhh, sayang sekali partnermu telah menyudahi obrolan bersamamu.</strong></em>😔", parse_mode="HTML")
        pengguna.pisahPartner(message.chat.id, message.chat.id)
    else:
        bot.send_message(message.chat.id, "<strong>Lohh, kok dihentikan sih😔😔. Hmmm, baiklah kalo begitu.</strong>😐", parse_mode="HTML")
        iddle = {
            'status': False,
            'mssg_id': None
        }
        pengguna.updateDataIddle(iddle, message.chat.id)

@bot.message_handler(commands=['skip','lewati'])
def lewati(message: telebot.types.Message):
    if r.exists("inchat_{}".format(message.from_user.id)):
        # bot.send_message(message.chat.id, "<em><strong>Sedang mencari partner ngobrol</strong></em>", parse_mode="HTML")
        bot.send_message(r.hget("inchat_{}".format(message.chat.id), message.chat.id).decode("utf8"), """\
<em><strong>Duhhh, sayang sekali partnermu telah menyudahi obrolan bersamamu.</strong></em>😔
Yukkk cari lagi /cari_partner
    \
    """, parse_mode="HTML")
        pengguna.pisahPartner(message.chat.id, message.chat.id)
        bot.send_message(message.chat.id, """\
<em><strong>Sedang mencari partner ngobrol</strong></em>⌛
    \
    """, parse_mode="HTML")
        pengguna.cariPartner(message.from_user.id, message.chat.id, message)
    else:
        bot.send_message(message.chat.id, 
                         """
<strong>Upsss, nampaknya kamu belum memiliki partner ngobrol.</strong>
Daripada gabut, silahkan tekan /cari_partner untuk mencari partner ngobrolmu.                         
                         """, parse_mode="HTML")

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     bot.reply_to(message, message.text)
# message handler for conversation
#
# That handler needed to send message from one opponent to another
# If you are not in `users`, you will recieve a message 'No one can hear you...'
# Otherwise all your messages are sent to your opponent
# @bot.message_handler(content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
@bot.message_handler(content_types=['animation', 'audio', 'contact', 'photo', 'sticker', 'text', 'venue', 'voice'])
def chatting(message: telebot.types.Message):
    # print(r.hget("inchat_{}".format(message.chat.id), 'user_1').decode("utf8"))
    # print("ini\n",message.chat.id, '\n', r.hget("inchat_{}".format(message.chat.id), message.chat.id).decode("utf8"),'\nhoppp')
    if r.exists("inchat_{}".format(message.from_user.id)):
        bot.copy_message(r.hget("inchat_{}".format(message.chat.id), message.chat.id).decode("utf8"),message.chat.id , message.id)
    else:
        bot.send_message(message.chat.id, 
                         """
<strong>Upsss, nampaknya kamu belum memiliki partner ngobrol.</strong>
Daripada gabut, silahkan tekan /cari_partner untuk mencari partner ngobrolmu.                         
                         """, parse_mode="HTML")



@app.post('/' + TOKEN)
async def getMessage(request: Request):
    dt = await request.body()
    json_string = dt.decode("utf8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.get("/")
def root():
    # print(r.keys())
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)