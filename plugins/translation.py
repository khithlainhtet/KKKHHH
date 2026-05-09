from pyrogram import Client, filters
from googletrans import Translator


translator = Translator()

@Client.on_message(filters.command("tr") & filters.reply)
async def translate_reply(client, message):
    # Reply ပြန်ထားတဲ့ စာကို ယူမယ်
    target_message = message.reply_to_message
    
    if not target_message.text:
        await message.reply_text("❌ စာသား (Text) ပါတဲ့ Message ကိုပဲ Reply ပြန်ပြီး ဘာသာပြန်ပေးပါဗျာ။")
        return

    # ခေတ္တစောင့်ရန် အကြောင်းကြားမယ်
    status_msg = await message.reply_text("⌛️ ဘာသာပြန်ဆိုနေပါသည်...")

    try:
        # ဘာသာစကားကို Auto Detect လုပ်ပြီး မြန်မာလို (my) ပြန်မယ်
        result = translator.translate(target_message.text, dest='my')
        
        # မူရင်းဘာသာစကား အမည်ကို ယူမယ် (ဥပမာ- English, Thai)
        src_lang = result.src.upper()
        
        response_text = (
            f"🇲🇲 **ဘာသာပြန်ဆိုချက်** ({src_lang} -> MY)\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"{result.text}"
        )
        
        await status_msg.edit_text(response_text)
        
    except Exception as e:
        print(f"Translation Error: {e}")
        await status_msg.edit_text("❌ ဘာသာပြန်နေစဉ် Error တက်သွားပါတယ်။ ခဏနေမှ ပြန်ကြိုးစားကြည့်ပါဗျာ။")

# Command အသုံးပြုပုံ ရှင်းပြချက် (Reply မပါဘဲ /tr ရိုက်ရင် ပြမယ့်စာ)
@Client.on_message(filters.command("tr") & ~filters.reply)
async def tr_help(client, message):
    await message.reply_text(
        "💡 **အသုံးပြုနည်း:**\n"
        "ဘာသာပြန်ချင်တဲ့ စာကို **Reply** ပြန်ပြီး `/tr` လို့ ရိုက်လိုက်ပါဗျာ။"
    )
