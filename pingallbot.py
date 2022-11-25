#Copyright ©️ 2022 TeLe TiPs. All Rights Reserved
#You are free to use this code in any of your project, but you MUST include the following in your README.md (Copy & paste)
# ##Credits - [Ping All Telegram bot by TeLe TiPs] (https://github.com/teletips/PingAllBot-teletips)

# Changing the code is not allowed! Read GNU AFFERO GENERAL PUBLIC LICENSE: https://github.com/teletips/PingAllBot-teletips/blob/main/LICENSE

from pyrogram import Client, filters
from pyrogram.types import Message
import os
import asyncio
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

teletips=Client(
    "PingAllBot",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"]
)

chatQueue = []

stopProcess = False

@teletips.on_message(filters.command(["all"]))
async def everyone(client, message):
  global stopProcess
  try: 
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 5:
        await message.reply("⛔️ Şuanda aktif çalışıyorum daha sonra tekrar deneyin.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("🚫 Bu sohbette çalışıyorum yeni bir etiketleme işlemi başlatmak icin /stop komutunu kullanın.")
        else:  
          chatQueue.append(message.chat.id)
          if len(message.command) > 1:
            inputText = message.command[1]
          elif len(message.command) == 1:
            usrtxt = ""    
          membersList = []
          async for member in teletips.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"text = f" **{reason}** {usrtxt}""
            try:    
              while j < 6:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"{user.mention} "
                  j+=1
                else:
                  text1 += f"@{user.username} "
                  j+=1
              try:     
                await teletips.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(3) 
              i+=3
            except IndexError:
              try:
                await teletips.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"✅  Başarılı etiket **Toplam sayı {i} kullanıcı**.\n❌ Botlar ve silinen hesaplar iptal edildi.") 
          else:
            await message.reply(f"✅  Başarılı etiket **{i} kullanıcı.**\n❌  Botlar ve silinen hesaplar iptal edildi.")    
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮 Üzgünüm, **Sadece yöneticiler** Bu komutu kullanabilir.")  
  except FloodWait as e:
    await asyncio.sleep(e.value) 

@teletips.on_message(filters.command(["remove","clean"]))
async def remove(client, message):
  global stopProcess
  try: 
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      bot = await teletips.get_chat_member(message.chat.id, "self")
      if bot.status == ChatMemberStatus.MEMBER:
        await message.reply("🕹 Silinen hesapları kaldırabilmem için bazı yetkilere ihtiyacım var.")  
      else:  
        if len(chatQueue) > 5 :
          await message.reply("⛔️ Şuanda aktif çalışıyorum daha sonra tekrar deneyin")
        else:  
          if message.chat.id in chatQueue:
            await message.reply("🚫 Bu sohbette çalışıyorum yeni bir işleme başlamak icin /stop komutunu kullanın.")
          else:  
            chatQueue.append(message.chat.id)  
            deletedList = []
            async for member in teletips.get_chat_members(message.chat.id):
              if member.user.is_deleted == True:
                deletedList.append(member.user)
              else:
                pass
            lenDeletedList = len(deletedList)  
            if lenDeletedList == 0:
              await message.reply("👻 sohbette ki hesaplar silindi.")
              chatQueue.remove(message.chat.id)
            else:
              k = 0
              processTime = lenDeletedList*10
              temp = await teletips.send_message(message.chat.id, f"🚨 Toplamı {lenDeletedList} Silinen hesaplar tespit edildi.\n⏳  Tahmini süre: {processTime} Saniye sonra.")
              if stopProcess: stopProcess = False
              while len(deletedList) > 0 and not stopProcess:   
                deletedAccount = deletedList.pop(0)
                try:
                  await teletips.ban_chat_member(message.chat.id, deletedAccount.id)
                except Exception:
                  pass  
                k+=1
                await asyncio.sleep(10)
              if k == lenDeletedList:  
                await message.reply(f"✅  silinen tüm hesaplar bu sohbetten kaldırıldı.")  
                await temp.delete()
              else:
                await message.reply(f"✅  Başarıyla kaldırıldı {k} Hesaplar bu sohbetten kaldırıldı.")  
                await temp.delete()  
              chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮 Üzgünüm, **sadece yöneticiler** bu komutu kullanabilir.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                               
        
@teletips.on_message(filters.command(["stop","cancel"]))
async def stop(client, message):
  global stopProcess
  try:
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("🤷 Durmak icin devam eden bir işlem bulunamadı.")
      else:
        stopProcess = True
        await message.reply("🛑 Durduruldu.")
    else:
      await message.reply("👮 Üzgünüm, **Sadece yöneticiler** bu komutu kullanabilir.")
  except FloodWait as e:
    await asyncio.sleep(e.value)

@teletips.on_message(filters.command(["admins","staff"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in teletips.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**Yöneticiler - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 Kurucu\n└ {owner.mention}\n\n👮🏻 adminler\n"
      else:
        text2 += f"👑 Kurucu\n└ @{owner.username}\n\n👮🏻 adminler\n"
    except:
      text2 += f"👑 Kurucu\n└ <i>anonim</i>\n\n👮🏻 adminler\n"
    if len(adminList) == 0:
      text2 += "└ <i>Gizli Yöneticiler</i>"  
      await teletips.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅  **Toplam  yönetici sayısı**: {lenAdminList}\n❌  Botlar ve gizli Yöneticiler"  
      await teletips.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       

@teletips.on_message(filters.command("bots"))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in teletips.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"**Botlar - {message.chat.title}**\n\n🤖 Botlar\n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"├ @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅  **  Toplam bot sayısı**: {lenBotList}"  
      await teletips.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)

@teletips.on_message(filters.command("start") & filters.private)
async def start(client, message):
  text = f'''
Merhaba {message.from_user.mention},
Benim adım **Samil Etiket**. Sohbetinizde tüm üyelerden bahsederek herkesin dikkatini çekmenize yardımcı olmak için buradayım.

Bazı ek harika özelliklerim var ve ayrıca kanallarda çalışabilirim.

Son guncellemelerden haberdar olmak icin [kanala](http://t.me/Samilbots) bakabilirsiniz

Komutlarımı ve bunların kullanımını öğrenmek için /help tuşuna basın.
'''
  await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)


@teletips.on_message(filters.command("help"))
async def help(client, message):
  text = '''
Hadi, komutlarıma kısaca göz atalım.

**Komutlar**:
- /all : <i>Tüm kullanıcılardan bahsedin.</i>
- /remove: <i>Silinen hesapları kaldırın.</i>
- /admins: <i>Adminlere gözat.</i>
- /bots: <i>Botları listele.</i>
- /stop: <i>İşlemi iptal eder.</i>

Beni nasıl kullanacağınızla ilgili herhangi bir sorunuz varsa, [destek grubuma](https://t.me/Developersohbet) bekliyorum .
'''
  await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)

print("PingAll is alive!")  
teletips.run()
 
#Copyright ©️ 2021 TeLe TiPs. All Rights Reserved 
