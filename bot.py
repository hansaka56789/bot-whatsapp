import os
import yt_dlp

from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv
from neonize.utils.message import extract_text


# =========================================================
# SETTINGS
# =========================================================

PHONE_NUMBER = "947XXXXXXXX"   # මෙතන ඔයාගේ WhatsApp number එක දාන්න
SESSION_FILE = "auth.db"


# =========================================================
# CLIENT
# =========================================================

client = NewClient(SESSION_FILE)


# =========================================================
# CONNECTED EVENT
# =========================================================

@client.event(ConnectedEv)
def on_connected(client, event):
    print("================================")
    print("✅ WhatsApp Bot Connected!")
    print("================================")


# =========================================================
# DOWNLOAD FUNCTION
# =========================================================

def download_and_send(chat, url, caption):

    client.send_message(
        chat,
        f"⏳ {caption} download කරනවා..."
    )

    filename = None

    try:

        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "format": "best",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )

            filename = ydl.prepare_filename(info)

        print(f"Downloaded: {filename}")

        # Video එක WhatsApp එකට යවන්න
        client.send_video(
            chat,
            filename,
            caption=f"✅ {caption} Done"
        )

        print("✅ Video sent")

    except Exception as e:

        print("❌ Download error:")
        print(e)

        client.send_message(
            chat,
            f"❌ Download fail.\n\n{e}"
        )

    finally:

        # Download කරපු file එක delete කරන්න
        if filename and os.path.exists(filename):

            try:
                os.remove(filename)
                print("🗑️ Temporary file deleted")

            except Exception as e:
                print(f"File delete error: {e}")


# =========================================================
# MESSAGE EVENT
# =========================================================

@client.event(MessageEv)
def on_message(client, message):

    try:

        text = extract_text(message.Message)
        chat = message.Info.MessageSource.Chat

        print(f"📩 Message: {text}")

        if not text:
            return

        text = text.strip()

        # =================================================
        # HELP
        # =================================================

        if text == ".help":

            client.send_message(
                chat,
                """
🤖 *WA DOWNLOADER BOT*

Commands:

.fb <link>
Facebook video download

.tt <link>
TikTok video download

.ig <link>
Instagram video download

.help
Show this menu
"""
            )

            return

        # =================================================
        # FACEBOOK
        # =================================================

        if text.startswith(".fb "):

            link = text[4:].strip()

            if not link:
                client.send_message(
                    chat,
                    "❌ Facebook link එකක් දාන්න."
                )
                return

            download_and_send(
                chat,
                link,
                "Facebook Video"
            )

            return

        # =================================================
        # TIKTOK
        # =================================================

        if text.startswith(".tt "):

            link = text[4:].strip()

            if not link:
                client.send_message(
                    chat,
                    "❌ TikTok link එකක් දාන්න."
                )
                return

            download_and_send(
                chat,
                link,
                "TikTok Video"
            )

            return

        # =================================================
        # INSTAGRAM
        # =================================================

        if text.startswith(".ig "):

            link = text[4:].strip()

            if not link:
                client.send_message(
                    chat,
                    "❌ Instagram link එකක් දාන්න."
                )
                return

            download_and_send(
                chat,
                link,
                "Instagram Video"
            )

            return

    except Exception as e:

        print("❌ Message handler error:")
        print(e)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("================================")
    print("🤖 WA BOT STARTING...")
    print("================================")

    # -----------------------------------------------------
    # First run = Pairing
    # Existing auth.db = reconnect
    # -----------------------------------------------------

    print("Connecting to WhatsApp...")

    client.connect()
