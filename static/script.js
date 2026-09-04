const input = document.querySelector('#message-input');
const sendButton = document.querySelector('#send-button');
const feed = document.querySelector('#message-feed');
const status = document.querySelector('#connection-status');
const count = document.querySelector('#message-count');
const charCount = document.querySelector('#char-count');
let messageTotal = 0;

const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
const socket = new WebSocket(`${protocol}://${location.host}/ws`);

socket.addEventListener('open', () => { status.textContent = 'connected'; document.querySelector('.status i').style.color = '#5ff3ff'; });
socket.addEventListener('close', () => { status.textContent = 'offline'; document.querySelector('.status i').style.background = '#ff607d'; });
socket.addEventListener('message', ({ data }) => {
  const event = JSON.parse(data);
  if (event.type === 'message') addMessage(event);
  if (event.type === 'decoded') {
    const card = document.querySelector(`[data-id="${event.message_id}"]`);
    if (card) { card.querySelector('.decoded').textContent = event.text; card.querySelector('.decoded').hidden = false; }
  }
});

function addMessage(event) {
  document.querySelector('.empty-state')?.remove();
  messageTotal += 1;
  count.textContent = `${String(messageTotal).padStart(2, '0')} messages`;
  const card = document.createElement('article');
  card.className = 'message-card'; card.dataset.id = event.message_id;
  card.innerHTML = `<div class="signal">⌁</div><div class="card-info"><p class="card-title">Incoming audio transmission</p><p class="card-meta">ID ${event.message_id} · MORSE WAV</p></div><div class="card-actions"><button class="play">▶ PLAY</button><button class="decode">DECODE</button></div><div class="decoded" hidden></div>`;
  card.querySelector('.play').addEventListener('click', () => new Audio(event.audio_url).play());
  card.querySelector('.decode').addEventListener('click', () => socket.send(JSON.stringify({ type:'decode', message_id:event.message_id })));
  feed.prepend(card);
}

function sendMessage() { const text = input.value.trim(); if (!text || socket.readyState !== WebSocket.OPEN) return; socket.send(JSON.stringify({ type:'send_message', text })); input.value=''; updateCount(); input.focus(); }
function updateCount() { charCount.textContent = `${input.value.length} / 500`; }
sendButton.addEventListener('click', sendMessage); input.addEventListener('input', updateCount); input.addEventListener('keydown', event => { if (event.key === 'Enter') sendMessage(); });
