import express from 'express';
import QRCode from 'qrcode'
import makeWASocket, { DisconnectReason, useMultiFileAuthState } from "baileys";

const app = express()

let latestQRCode = null;

const start = async() => {
    const { state, saveCreds } = await useMultiFileAuthState('sessions')
    const sock = makeWASocket({ auth: state, })

    sock.ev.on('connection.update', async (update) => {
        const {connection, lastDisconnect, qr } = update
      
        if (qr) {
          latestQRCode = qr
          console.log(await QRCode.toString(qr, {type:'terminal', small: true}))
        }

        if (connection === 'open') {
            console.log("Whatsapp conectado!")
        }

        if (connection === 'close') {
            const reason = lastDisconnect?.error?.output?.statusCode
            
            if (reason != DisconnectReason.loggedOut) {
                console.log('Reconectando...')
                start()
            } else {
                console.log("Desconectado manualmente.")
            }
        }
      })

      sock.ev.on('messages.upsert', async (m) => {
        if (m.type === 'notify') {
            const msg = m.messages[0]
            
            if (!msg.key.fromMe && !msg.key.remoteJid.includes('@g.us') || !msg.key.remoteJid === 'status@broadcast') {
                const phone = msg.key.remoteJid
                const textMessage = msg.message.conversation

                console.log('Mensagem recebida: "' + textMessage + '"')

                await sock.sendPresenceUpdate('composing', phone)
                await new Promise(r => setTimeout(r, 3000))

                await sock.sendMessage(phone, { text: "Mensagem recebida de '" + phone + "'."})
            }

        }
      })

      sock.ev.on('creds.update', saveCreds)
}

app.get('/qr', async (req, res) => {
    if (!latestQRCode) {
        return res.status(404).send('O QRCode ainda não foi gerado. Por favor aguarde...')
    }

    try {
        const svgString = await QRCode.toString(latestQRCode, {type: 'svg'})

        const html = `
        <html>
            <head><title>Automação Proway WhatsApp QRCode</title></head>
            <body style="display: flex; justify-content: center; align-items: center, height: 100vh, flex-direction: column;">
            <h1>Escaneie o seguinte código para conectar o seu whatsapp</h1>
            ${svgString}
        
        `

        res.setHeader('Content-type', 'text/html')
        res.send(html)
    } catch (err) {
        res.status(500).send('Erro ao gerar o QRCode: ' + err.text)
    }
})

app.listen(3000, () => {
    console.log('Servidor iniciado!')
    start().catch(console.error)
})

// start().catch(console.error)