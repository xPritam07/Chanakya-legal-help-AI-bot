(function () {
  const composer = document.getElementById('composer');
  const input = document.getElementById('textInput');
  const messages = document.getElementById('messages');

  // Avatar images
  const USER_AVATAR = '/static/images/bot_male.svg';
  const BOT_AVATAR = '/static/images/bot_female.svg';

  // format time with leading zeros
  function two(n) {
    return (n < 10 ? '0' + n : '' + n);
  }

  function nowTimeStr() {
    const d = new Date();
    return two(d.getHours()) + ':' + two(d.getMinutes());
  }

  // scroll messages container to bottom
  function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight;
  }

  // simple escape to avoid raw HTML injection
  function escapeHtml(s) {
    if (!s && s !== 0) return '';
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;')
      .replace(/\n/g, '<br>');
  }

  // create and append message elements
  function appendMessage(text, who) {
    const row = document.createElement('div');
    row.className = 'row ' + (who === 'user' ? 'user' : 'bot');

    const imgWrap = document.createElement('div');
    imgWrap.className = 'img-msg';
    const img = document.createElement('img');
    img.src = who === 'user' ? USER_AVATAR : BOT_AVATAR;
    img.alt = who === 'user' ? 'You' : 'Bot';
    imgWrap.appendChild(img);

    const bubble = document.createElement('div');
    bubble.className = 'bubble ' + (who === 'user' ? 'user' : 'bot');
    bubble.innerHTML = escapeHtml(text);

    const time = document.createElement('div');
    time.className = 'time';
    time.textContent = nowTimeStr();
    bubble.appendChild(time);

    row.appendChild(imgWrap);
    row.appendChild(bubble);

    messages.appendChild(row);
    scrollToBottom();
  }

  // initial greeting
//   appendMessage("Hi! I'm Chanakya. How can I help you today?", 'bot');

  // handle message submit
  composer.addEventListener('submit', function (ev) {
    ev.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    appendMessage(text, 'user');
    input.value = '';
    input.focus();

    const payload = new URLSearchParams();
    payload.append('msg', text);

    fetch('/get', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: payload.toString()
    })
      .then(async resp => {
        if (!resp.ok) {
          const errText = await resp.text().catch(() => resp.statusText);
          throw new Error(errText || 'Network response was not ok');
        }
        return resp.text();
      })
      .then(data => {
        appendMessage(data, 'bot');
      })
      .catch(err => {
        appendMessage("⚠️ Error: " + String(err.message || err), 'bot');
        console.error("Chat request failed:", err);
      });
  });

  // allow pressing Escape to clear input
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') input.value = '';
  });
})();
