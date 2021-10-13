from bots import (
    bot,
    telebot,
    menu
)
import controller.pengguna as pengguna
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


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
        
    elif call.data.startswith('gender-l'):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        data = {
            "ketertarikan_user": "L"
        }
        pengguna.updateData(data,menu.idnya_user)
        bot.send_message(call.message.chat.id,"""\
Data telah tersimpan kedalam sistem. 📋📌
\
        """)
    elif call.data.startswith('gender-p'):
        print(call.message.from_user.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        data = {
            "ketertarikan_user": "P"
        }
        pengguna.updateData(data,menu.idnya_user)
        bot.send_message(call.message.chat.id,"""\
Data telah tersimpan kedalam sistem. 📋📌
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
Data telah tersimpan kedalam sistem. 📋📌
\
""")
    except Exception as e:
        bot.reply_to(message, 'oooops')