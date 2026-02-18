const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const { spawn } = require('child_process');
const path = require('path');

// === CONFIGURATION ===
// Set your WhatsApp number (with country code, no + or spaces)
// Example: '491234567890' for a German number
// Leave empty to allow any number (NOT recommended)
const AUTHORIZED_NUMBERS = process.env.WA_AUTHORIZED_NUMBERS
    ? process.env.WA_AUTHORIZED_NUMBERS.split(',').map(n => n.trim())
    : [];

// Working directory for Claude Code commands
const WORK_DIR = process.env.WA_WORK_DIR || path.resolve(__dirname, '..');

// Max response length for WhatsApp (messages get truncated beyond ~65000 chars)
const MAX_RESPONSE_LENGTH = 4000;

// Timeout for Claude commands (5 minutes)
const CLAUDE_TIMEOUT_MS = 5 * 60 * 1000;

// === STATE ===
const activeSessions = new Map(); // number -> { busy: boolean }

// === WHATSAPP CLIENT ===
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', (qr) => {
    console.log('\n📱 Scan this QR code with WhatsApp:\n');
    qrcode.generate(qr, { small: true });
    console.log('\nOpen WhatsApp → Settings → Linked Devices → Link a Device\n');
});

client.on('ready', () => {
    console.log('✅ WhatsApp bridge is ready!');
    console.log(`📂 Working directory: ${WORK_DIR}`);
    if (AUTHORIZED_NUMBERS.length > 0) {
        console.log(`🔒 Authorized numbers: ${AUTHORIZED_NUMBERS.join(', ')}`);
    } else {
        console.log('⚠️  No authorized numbers set — will reject all messages.');
        console.log('   Set WA_AUTHORIZED_NUMBERS env var (e.g., "491234567890")');
    }
});

client.on('authenticated', () => {
    console.log('🔑 Authenticated with WhatsApp');
});

client.on('auth_failure', (msg) => {
    console.error('❌ Authentication failed:', msg);
});

client.on('disconnected', (reason) => {
    console.log('🔌 Disconnected:', reason);
});

// === MESSAGE HANDLER ===
client.on('message', async (message) => {
    // Ignore group messages, status updates, and media-only messages
    if (message.isGroupMsg || message.isStatus || !message.body) return;

    const sender = message.from.replace('@c.us', '');

    // Security: only respond to authorized numbers
    if (AUTHORIZED_NUMBERS.length === 0 || !AUTHORIZED_NUMBERS.includes(sender)) {
        console.log(`🚫 Unauthorized message from ${sender}: "${message.body.substring(0, 50)}"`);
        return;
    }

    const text = message.body.trim();
    console.log(`\n📨 Message from ${sender}: "${text.substring(0, 100)}${text.length > 100 ? '...' : ''}"`);

    // Handle built-in commands
    if (text.toLowerCase() === '/help') {
        await message.reply(
            '🤖 *Mission Control WhatsApp Bridge*\n\n' +
            'Send any message and Claude will process it.\n\n' +
            '*Commands:*\n' +
            '`/help` — Show this help\n' +
            '`/status` — Check bridge status\n' +
            '`/tasks` — List current tasks\n\n' +
            '*Examples:*\n' +
            '• "Show me the current tasks"\n' +
            '• "Create a new task: Fix login bug"\n' +
            '• "What files were changed recently?"\n' +
            '• "Run the tests"\n\n' +
            'Everything else is sent directly to Claude Code.'
        );
        return;
    }

    if (text.toLowerCase() === '/status') {
        const session = activeSessions.get(sender);
        await message.reply(
            `🟢 *Bridge Status*\n\n` +
            `Working directory: \`${WORK_DIR}\`\n` +
            `Session active: ${session?.busy ? 'Yes (processing...)' : 'Idle'}`
        );
        return;
    }

    if (text.toLowerCase() === '/tasks') {
        try {
            const result = await runClaude('List all tasks from data/tasks.json with their status. Be concise.', WORK_DIR);
            await sendLongMessage(message, result);
        } catch (err) {
            await message.reply(`❌ Error: ${err.message}`);
        }
        return;
    }

    // Check if already processing a command
    const session = activeSessions.get(sender);
    if (session?.busy) {
        await message.reply('⏳ Still processing your previous command. Please wait...');
        return;
    }

    // Forward to Claude
    activeSessions.set(sender, { busy: true });

    try {
        await message.reply('🔄 Processing...');
        const result = await runClaude(text, WORK_DIR);
        await sendLongMessage(message, result);
    } catch (err) {
        console.error('❌ Claude error:', err.message);
        await message.reply(`❌ Error: ${err.message}`);
    } finally {
        activeSessions.set(sender, { busy: false });
    }
});

// === CLAUDE EXECUTION ===
function runClaude(prompt, cwd) {
    return new Promise((resolve, reject) => {
        let output = '';
        let errorOutput = '';

        const proc = spawn('claude', [
            '--print',
            '--max-turns', '3',
            prompt
        ], {
            cwd,
            env: { ...process.env, NO_COLOR: '1' },
            timeout: CLAUDE_TIMEOUT_MS
        });

        proc.stdout.on('data', (data) => {
            output += data.toString();
        });

        proc.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        proc.on('close', (code) => {
            if (code === 0 || output.length > 0) {
                resolve(output.trim() || '(No output)');
            } else {
                reject(new Error(errorOutput.trim() || `Claude exited with code ${code}`));
            }
        });

        proc.on('error', (err) => {
            reject(new Error(`Failed to run Claude: ${err.message}`));
        });

        // Timeout handling
        setTimeout(() => {
            proc.kill('SIGTERM');
            reject(new Error('Command timed out after 5 minutes'));
        }, CLAUDE_TIMEOUT_MS);
    });
}

// === HELPERS ===
async function sendLongMessage(message, text) {
    if (text.length <= MAX_RESPONSE_LENGTH) {
        await message.reply(text);
        return;
    }

    // Split into chunks at line boundaries
    const lines = text.split('\n');
    let chunk = '';
    let part = 1;

    for (const line of lines) {
        if (chunk.length + line.length + 1 > MAX_RESPONSE_LENGTH) {
            await message.reply(`📄 *Part ${part}:*\n\n${chunk}`);
            chunk = '';
            part++;
            // Small delay to avoid rate limiting
            await new Promise(r => setTimeout(r, 500));
        }
        chunk += line + '\n';
    }

    if (chunk.trim()) {
        await message.reply(part > 1 ? `📄 *Part ${part}:*\n\n${chunk}` : chunk);
    }
}

// === START ===
console.log('🚀 Starting Mission Control WhatsApp Bridge...');
console.log('   Connecting to WhatsApp Web...\n');
client.initialize();
