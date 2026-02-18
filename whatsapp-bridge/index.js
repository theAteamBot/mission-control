const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, makeCacheableSignalKeyStore } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const pino = require('pino');
const { spawn } = require('child_process');
const path = require('path');

const logger = pino({ level: 'silent' });

// === CONFIGURATION ===
// Set your WhatsApp number (with country code, no + or spaces)
// Example: '13057207870' for a US number
const AUTHORIZED_NUMBERS = process.env.WA_AUTHORIZED_NUMBERS
    ? process.env.WA_AUTHORIZED_NUMBERS.split(',').map(n => n.trim().replace(/^\+/, ''))
    : [];

// Working directory for Claude Code commands
const WORK_DIR = process.env.WA_WORK_DIR || path.resolve(__dirname, '..');

// Max response length for WhatsApp
const MAX_RESPONSE_LENGTH = 4000;

// Timeout for Claude commands (5 minutes)
const CLAUDE_TIMEOUT_MS = 5 * 60 * 1000;

// === STATE ===
const activeSessions = new Map();

// === MAIN ===
async function startBridge() {
    const { state, saveCreds } = await useMultiFileAuthState('./auth_store');

    const sock = makeWASocket({
        auth: {
            creds: state.creds,
            keys: makeCacheableSignalKeyStore(state.keys, logger)
        },
        printQRInTerminal: false,
        logger
    });

    // Save credentials on update
    sock.ev.on('creds.update', saveCreds);

    // Connection handling
    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log('\n📱 Scan this QR code with WhatsApp:\n');
            qrcode.generate(qr, { small: true });
            console.log('\nOpen WhatsApp → Settings → Linked Devices → Link a Device\n');
        }

        if (connection === 'close') {
            const statusCode = lastDisconnect?.error?.output?.statusCode;
            const shouldReconnect = statusCode !== DisconnectReason.loggedOut;

            if (shouldReconnect) {
                console.log('🔄 Reconnecting in 3 seconds...');
                setTimeout(startBridge, 3000);
            } else {
                console.log('👋 Logged out. Delete ./auth_store and restart to re-link.');
            }
        }

        if (connection === 'open') {
            console.log('✅ WhatsApp bridge is ready!');
            console.log(`📂 Working directory: ${WORK_DIR}`);
            if (AUTHORIZED_NUMBERS.length > 0) {
                console.log(`🔒 Authorized numbers: ${AUTHORIZED_NUMBERS.join(', ')}`);
            } else {
                console.log('⚠️  No authorized numbers set — will reject all messages.');
                console.log('   Set WA_AUTHORIZED_NUMBERS="13057207870" before starting');
            }
        }
    });

    // Message handling
    sock.ev.on('messages.upsert', async ({ messages }) => {
        for (const msg of messages) {
            // Skip non-personal messages
            if (!msg.message || msg.key.fromMe || msg.key.remoteJid.endsWith('@g.us') || msg.key.remoteJid === 'status@broadcast') {
                continue;
            }

            const sender = msg.key.remoteJid.replace('@s.whatsapp.net', '');
            const text = msg.message.conversation
                || msg.message.extendedTextMessage?.text
                || '';

            if (!text.trim()) continue;

            // Security: only respond to authorized numbers
            if (AUTHORIZED_NUMBERS.length === 0 || !AUTHORIZED_NUMBERS.includes(sender)) {
                console.log(`🚫 Unauthorized: ${sender}`);
                continue;
            }

            console.log(`\n📨 From ${sender}: "${text.substring(0, 100)}${text.length > 100 ? '...' : ''}"`);
            await handleMessage(sock, msg.key.remoteJid, text.trim());
        }
    });
}

// === MESSAGE HANDLER ===
async function handleMessage(sock, jid, text) {
    const sender = jid.replace('@s.whatsapp.net', '');

    // Built-in commands
    if (text.toLowerCase() === '/help') {
        await sendMessage(sock, jid,
            '🤖 *Mission Control WhatsApp Bridge*\n\n' +
            'Send any message and Claude will process it.\n\n' +
            '*Commands:*\n' +
            '/help — Show this help\n' +
            '/status — Bridge status\n' +
            '/tasks — List tasks\n\n' +
            '*Examples:*\n' +
            '• "Show me the current tasks"\n' +
            '• "Create a new task: Fix login bug"\n' +
            '• "What files changed recently?"\n' +
            '• "Run the tests"'
        );
        return;
    }

    if (text.toLowerCase() === '/status') {
        const session = activeSessions.get(sender);
        await sendMessage(sock, jid,
            `🟢 *Bridge Status*\n\n` +
            `Dir: ${WORK_DIR}\n` +
            `Busy: ${session?.busy ? 'Yes' : 'No'}`
        );
        return;
    }

    if (text.toLowerCase() === '/tasks') {
        text = 'List all tasks from data/tasks.json with their status. Be concise.';
    }

    // Check if busy
    const session = activeSessions.get(sender);
    if (session?.busy) {
        await sendMessage(sock, jid, '⏳ Still processing your previous command...');
        return;
    }

    activeSessions.set(sender, { busy: true });

    try {
        await sendMessage(sock, jid, '🔄 Processing...');
        const result = await runClaude(text, WORK_DIR);
        await sendLongMessage(sock, jid, result);
    } catch (err) {
        console.error('❌ Error:', err.message);
        await sendMessage(sock, jid, `❌ Error: ${err.message}`);
    } finally {
        activeSessions.set(sender, { busy: false });
    }
}

// === CLAUDE EXECUTION ===
function runClaude(prompt, cwd) {
    return new Promise((resolve, reject) => {
        let output = '';
        let errorOutput = '';
        let killed = false;

        const proc = spawn('claude', [
            '--print',
            '--max-turns', '3',
            prompt
        ], {
            cwd,
            env: { ...process.env, NO_COLOR: '1' }
        });

        proc.stdout.on('data', (data) => {
            output += data.toString();
        });

        proc.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        proc.on('close', (code) => {
            if (killed) return;
            if (code === 0 || output.length > 0) {
                resolve(output.trim() || '(No output)');
            } else {
                reject(new Error(errorOutput.trim() || `Claude exited with code ${code}`));
            }
        });

        proc.on('error', (err) => {
            reject(new Error(`Failed to run Claude: ${err.message}`));
        });

        setTimeout(() => {
            killed = true;
            proc.kill('SIGTERM');
            reject(new Error('Command timed out after 5 minutes'));
        }, CLAUDE_TIMEOUT_MS);
    });
}

// === HELPERS ===
async function sendMessage(sock, jid, text) {
    await sock.sendMessage(jid, { text });
}

async function sendLongMessage(sock, jid, text) {
    if (text.length <= MAX_RESPONSE_LENGTH) {
        await sendMessage(sock, jid, text);
        return;
    }

    const lines = text.split('\n');
    let chunk = '';
    let part = 1;

    for (const line of lines) {
        if (chunk.length + line.length + 1 > MAX_RESPONSE_LENGTH) {
            await sendMessage(sock, jid, `📄 *Part ${part}:*\n\n${chunk}`);
            chunk = '';
            part++;
            await new Promise(r => setTimeout(r, 500));
        }
        chunk += line + '\n';
    }

    if (chunk.trim()) {
        await sendMessage(sock, jid, part > 1 ? `📄 *Part ${part}:*\n\n${chunk}` : chunk);
    }
}

// === START ===
console.log('🚀 Starting Mission Control WhatsApp Bridge...');
console.log('   Connecting to WhatsApp...\n');
startBridge();
