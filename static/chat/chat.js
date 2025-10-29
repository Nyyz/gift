function getCookie(name){let v=document.cookie.match('(^|;) ?'+name+'=([^;]*)(;|$)');return v?v[2]:null}

function initChat(conversationId){
  const form = document.getElementById('msg-form') || document.getElementById('message-form')
  const box = document.getElementById('messages') || document.querySelector('.chat-messages')
  if(!form) return
  const input = form.querySelector('input[name="text"]')
  const btn = form.querySelector('button[type="submit"]')
  if(input) input.focus()

  // disable send if empty
  const toggleButton = ()=>{ if(btn) btn.disabled = !input || !input.value.trim() }
  if(input){ input.addEventListener('input', toggleButton); toggleButton() }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    const data = new FormData(this)
    if(btn) btn.textContent = 'Відправлення...'
    fetch(`/chat/conversation/${conversationId}/send/`, {method:'POST', body: data, headers: {'X-CSRFToken': getCookie('csrftoken')}, credentials:'same-origin'})
      .then(r=>r.json()).then(d=>{
        if(d.status==='ok'){
          const div = document.createElement('div')
          div.className = 'msg me'
          div.textContent = d.text
          if(box) box.appendChild(div)
          form.reset()
          if(input) input.focus()
          box.scrollTop = box.scrollHeight
        }
      }).finally(()=>{ if(btn) btn.textContent = 'Відправити'; toggleButton() })
  })
  if(box) box.scrollTop = box.scrollHeight
}

document.addEventListener('DOMContentLoaded', ()=>{
  const el = document.getElementById('chat-root')
  if(el && el.dataset.convId) initChat(el.dataset.convId)
})
