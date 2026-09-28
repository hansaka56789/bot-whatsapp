import os
import yt_dlp
from neonize.client import NewClient
from neonize.utils import log

# Pair Code එක ගන්න number එක - 94 එක්ක දාන්න
PHONE_NUMBER = "94762320234"  # <--- මෙතන උඹේ number එක දාන්න

client = NewClient("auth.db")

@client.event
def on_connected():
    print("✅ Bot Connected!")

@client.event
def on_message(message):
    chat = message.chat
    text = message.text or ""
    
    print(f"Message: {text}")

    if not text.startswith("."):
        return

    # link එක අරන් download කරන function එක
    def download_and_send(url, caption):
        client.send_message(chat, f"⏳ {caption} download කරනවා...")
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': 'best',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            client.send_video(chat, filename, caption=f"✅ {caption} Done")
            os.remove(filename)
        except Exception as e:
            print(e)
            client.send_message(chat, f"❌ Download fail. Link එක වැරදියි\n{e}")

    if text.startswith(".fb "):
        link = text.replace(".fb ", "").strip()
        download_and_send(link, "FB Video")

    elif text.startswith(".tt "):
        link = text.replace(".tt ", "").strip()
        download_and_send(link, "TikTok Video")

    elif text.startswith(".ig "):
        link = text.replace(".ig ", "").strip()
        download_and_send(link, "IG Video")

# Pair code එකෙන් login වෙන විදිය
if not client.is_logged_in:
    print(f"Pair Code ඉල්ලනවා {PHONE_NUMBER} ට...")
    client.request_pairing_code(PHONE_NUMBER)
    code = input("WhatsApp එකේ Linked Devices > Link with phone number වල ගහන්න ඕන Code එක උඩ print වෙලා තියෙනවා. Code එක බලලා enter කරන්න: ")
    print(f"Code එක: {code}")

client.connect()
