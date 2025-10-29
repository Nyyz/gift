document.addEventListener('click', function(e){
  if(e.target.matches('.like-btn')){
    const id = e.target.dataset.id
  fetch(`/gift/${id}/like/`, {method:'POST', headers:{'X-CSRFToken': getCookie('csrftoken')}, credentials: 'same-origin'})
      .then(r=>r.json()).then(d=>{
        const btns = document.querySelectorAll(`.like-btn[data-id="${id}"]`)
        btns.forEach(b=>{
          const span = b.querySelector('span')
          if(span) span.textContent = d.likes_count
        })
        const detailCount = document.getElementById('likes-count')
        if(detailCount) detailCount.textContent = d.likes_count
      })
  }
  if(e.target.matches('.save-btn')){
    const id = e.target.dataset.id
  fetch(`/gift/${id}/save/`, {method:'POST', headers:{'X-CSRFToken': getCookie('csrftoken')}, credentials: 'same-origin'})
      .then(r=>r.json()).then(d=>{
        e.target.textContent = d.status
      })
  }
})

const commentForm = document.getElementById('comment-form')
if(commentForm){
  commentForm.addEventListener('submit', function(ev){
    ev.preventDefault()
    const data = new FormData(commentForm)
    const giftId = location.pathname.split('/').filter(Boolean).pop()
  fetch(`/gift/${giftId}/comment/`, {method:'POST', body: data, headers:{'X-CSRFToken': getCookie('csrftoken')}, credentials: 'same-origin'})
      .then(r=>r.json()).then(d=>{
        if(d.status === 'ok') location.reload()
      })
  })
}

function getCookie(name){
  let v=document.cookie.match('(^|;) ?'+name+'=([^;]*)(;|$)');
  return v?v[2]:null
}

// Load more / infinite scroll
const loadMore = document.getElementById('load-more')
if(loadMore){
  loadMore.addEventListener('click', function(){
    const next = this.dataset.next
    fetch(`/?page=${next}`, {credentials:'same-origin'}).then(r=>r.text()).then(html=>{
      // cheaply parse returned html and append posts
      const tmp = document.createElement('div')
      tmp.innerHTML = html
      const newPosts = tmp.querySelectorAll('#feed .post')
      newPosts.forEach(n=>document.getElementById('feed').appendChild(n))
      // update next button
      const newBtn = tmp.querySelector('#load-more')
      if(newBtn) loadMore.dataset.next = newBtn.dataset.next
      else loadMore.remove()
    })
  })
}
