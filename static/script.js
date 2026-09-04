const input = document.querySelector('#message-input');
const sendButton = document.querySelector('#send-button');
const feed = document.querySelector('#message-feed');
const status = document.querySelector('#connection-status');
const statusLight = document.querySelector('.status i');
const count = document.querySelector('#message-count');
const charCount = document.querySelector('#char-count');
let messageTotal = 0;
let socket;
let reconnectTimer;
let deferredInstall;

const protocol = location.protocol === 'https:' ? 'wss' : 'ws';

function connect() {
  status.textContent = 'connecting'; statusLight.style.background = '#ffca5f';
  socket = new WebSocket(`${protocol}://${location.host}/ws`);
  socket.addEventListener('open', () => { status.textContent = 'connected'; statusLight.style.background = '#5ff3ff'; });
  socket.addEventListener('close', () => { status.textContent = 'reconnecting'; statusLight.style.background = '#ff607d'; reconnectTimer = setTimeout(connect, 1500); });
  socket.addEventListener('message', ({ data }) => {
    const event = JSON.parse(data);
    if (event.type === 'message') addMessage(event);
    if (event.type === 'decoded') {
      const card = document.querySelector(`[data-id="${event.message_id}"]`);
      if (card) { card.querySelector('.decoded').textContent = event.text; card.querySelector('.decoded').hidden = false; card.querySelector('.decode').textContent = 'PLAINTEXT REVEALED'; }
    }
    if (event.type === 'error') showToast(event.message);
  });
}
connect();

if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(() => {});

const installCard = document.querySelector('#install-card');
const installButton = document.querySelector('#install-button');
const installHelp = document.querySelector('#install-help');
const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;
window.addEventListener('beforeinstallprompt', event => { event.preventDefault(); deferredInstall = event; if (!isStandalone) installCard.hidden = false; });
if (isIOS && !isStandalone) { installCard.hidden = false; installButton.hidden = true; installHelp.textContent = 'In Safari, tap Share, then “Add to Home Screen”.'; }
installButton.addEventListener('click', async () => { if (!deferredInstall) return; deferredInstall.prompt(); await deferredInstall.userChoice; deferredInstall = null; installCard.hidden = true; });

function addMessage(event) {
  document.querySelector('.empty-state')?.remove();
  messageTotal += 1;
  count.textContent = `${String(messageTotal).padStart(2, '0')} messages`;
  const card = document.createElement('article');
  card.className = 'message-card'; card.dataset.id = event.message_id;
  card.innerHTML = `<div class="card-top"><div class="signal">⌁</div><div class="card-info"><p class="card-title">Morse audio transmission</p><p class="card-meta">ID ${event.message_id} · STORED WAV SIGNAL</p></div></div><div class="signal-bars" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><button class="play">▶ PLAY MORSE SIGNAL</button><button class="decode">REVEAL TEXT AFTER LISTENING →</button><div class="decoded" hidden></div>`;
  const audio = new Audio(event.audio_url);
  card.querySelector('.play').addEventListener('click', async () => { try { await audio.play(); card.querySelector('.play').textContent = '▮▮ PLAYING MORSE SIGNAL'; } catch { showToast('Audio could not start. Try Play again.'); } });
  audio.addEventListener('ended', () => { card.querySelector('.play').textContent = '▶ PLAY MORSE SIGNAL'; });
  card.querySelector('.decode').addEventListener('click', () => { if (socket.readyState !== WebSocket.OPEN) return showToast('Reconnecting…'); socket.send(JSON.stringify({ type:'decode', message_id:event.message_id })); });
  feed.prepend(card);
}

function sendMessage() { const text = input.value.trim(); if (!text) return; if (!socket || socket.readyState !== WebSocket.OPEN) return showToast('Still connecting…'); socket.send(JSON.stringify({ type:'send_message', text })); input.value=''; updateCount(); input.focus(); }
function updateCount() { charCount.textContent = `${input.value.length} / 500`; }
function showToast(message) { status.textContent = message; setTimeout(() => { if (socket?.readyState === WebSocket.OPEN) status.textContent = 'connected'; }, 2200); }
sendButton.addEventListener('click', sendMessage); input.addEventListener('input', updateCount); input.addEventListener('keydown', event => { if (event.key === 'Enter') sendMessage(); });
