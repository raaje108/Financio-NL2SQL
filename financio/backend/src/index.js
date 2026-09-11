require('dotenv').config();
const app = require('./app');
const { spawn } = require('child_process');
const path = require('path');

const PORT = process.env.PORT || 8000;

const server = app.listen(PORT, () => {
    console.log(`Server is running at port : ${PORT}`);
});

// Spawn the Python NLP server process
const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
const nlpServerPath = path.join(__dirname, 'nlp', 'nlp_server.py');

console.log(`[NLP Server] Starting Python NLP server: ${nlpServerPath}...`);
const nlpProcess = spawn(pythonPath, [nlpServerPath], {
    stdio: 'inherit',
    detached: false,
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
});

nlpProcess.on('error', (err) => {
    console.error('[NLP Server] Failed to start Python NLP process. Make sure python is in your PATH.', err);
});

// Handle cleanup when Node process exits
process.on('SIGINT', () => {
    console.log('[Server] Shutting down Node and Python NLP server...');
    nlpProcess.kill();
    server.close(() => {
        process.exit(0);
    });
});

process.on('SIGTERM', () => {
    console.log('[Server] Shutting down Node and Python NLP server...');
    nlpProcess.kill();
    server.close(() => {
        process.exit(0);
    });
});