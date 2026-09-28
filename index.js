const { default: makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys")
const axios = require("axios")
const P = require("pino")

async function start() {
    const { state, saveCreds } = await useMultiFileAuthState('auth')
    
    const sock = makeWASocket({
        auth: state,
        logger: P({ level: 'silent' }),
        printQRInTerminal: false
    })

    // PAIR CODE එක ගන්න - මෙතන number එක වෙනස් කරපන්
    if (!sock.authState.creds.registered) {
        const phoneNumber = "94762320234" // <---number එක 94 එක්ක දාන්න
        const code = await sock.requestPairingCode(phoneNumber)
        console.log(`\n\n================\nPAIR CODE: ${code}\n================\n\n`)
    }

    sock.ev.on('creds.update', saveCreds)

    sock.ev.on('messages.upsert', async m => {
        const msg = m.messages[0]
        if (!msg.message || msg.key.fromMe) return
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text || ""
        const jid = msg.key.remoteJid

        console.log("Message:", text)

        // .fb command
        if (text.startsWith(".fb ")) {
            const link = text.replace(".fb ", "").trim()
            await sock.sendMessage(jid, { text: "⏳ FB video download කරනවා..." })
            try {
                const api = `https://www.tikwm.com/api/?url=${link}`
                const res = await axios.get(api)
                // fb එකටත් tikwm වැඩ කරනවා සමහර වෙලාවට
                if(res.data.data && res.data.data.play) {
                   await sock.sendMessage(jid, { video: { url: res.data.data.play }, caption: "✅ FB Video Done" })
                } else {
                   throw new Error()
                }
            } catch {
                await sock.sendMessage(jid, { text: "❌ FB download fail. වෙන link එකක් try කරපන්" })
            }
        }

        // .tt command
        if (text.startsWith(".tt ")) {
            const link = text.replace(".tt ", "").trim()
            await sock.sendMessage(jid, { text: "⏳ TikTok download කරනවා..." })
            try {
                const res = await axios.get(`https://www.tikwm.com/api/?url=${link}`)
                const videoUrl = res.data.data.play
                await sock.sendMessage(jid, { video: { url: videoUrl }, caption: "✅ TikTok Done" })
            } catch {
                await sock.sendMessage(jid, { text: "❌ TT link වැරදියි" })
            }
        }

        // .ig command
        if (text.startsWith(".ig ")) {
            const link = text.replace(".ig ", "").trim()
            await sock.sendMessage(jid, { text: "⏳ IG video download කරනවා..." })
            try {
                const res = await axios.get(`https://www.tikwm.com/api/?url=${link}`)
                const videoUrl = res.data.data.play || res.data.data.images
                await sock.sendMessage(jid, { video: { url: videoUrl }, caption: "✅ IG Done" })
            } catch {
                await sock.sendMessage(jid, { text: "❌ IG link වැරදියි" })
            }
        }
    })
}

start()
