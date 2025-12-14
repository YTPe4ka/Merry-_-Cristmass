// admin.js — CRUD client for /api/* endpoints
(function(){
  const API = {
    home: '/api/home/',
    about: '/api/about/',
    resume: '/api/resume/',
    portfolio: '/api/portfolio/',
    services: '/api/services/',
    skills: '/api/skills/',
    contact: '/api/contact/'
  };

  // client-side defaults used when DB is empty (mirror of configapp/defaults.py)
  const DEFAULTS = {
    ABOUT_DESC: 'Magnam dolores commodi suscipit. Necessitatibus eius consequatur ex aliquid fuga eum quidem. Sit sint consectetur velit. Quisquam quos quisquam cupiditate. Et nemo qui impedit suscipit alias ea. Quia fugiat sit in iste officiis commodi quidem hic quas.',
    HERO_ROLES: 'Designer, Developer, Freelancer, Photographer'
  };

  // util: get csrftoken
  function getCookie(name) {
    let v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
  }
  const csrftoken = getCookie('csrftoken');

  function fetchWithCreds(url, opts){
    opts = opts || {};
    if(!opts.credentials) opts.credentials = 'same-origin';
    return fetch(url, opts);
  }

  // DOM
  const sidebarLinks = document.querySelectorAll('.admin-sidebar .nav-link');
  const sectionTitle = document.getElementById('section-title');
  const btnAdd = document.getElementById('btn-add');
  const btnRefresh = document.getElementById('btn-refresh');
  const listPanel = document.getElementById('list-panel');
  const homePanel = document.getElementById('home-panel');
  const aboutPanel = document.getElementById('about-panel');
  const adminTableHead = document.getElementById('table-head');
  const adminTableBody = document.getElementById('table-body');
  const modal = new bootstrap.Modal(document.getElementById('modal-edit'), {});

  // confirm modal helper (promise-based)
  const confirmModalEl = document.getElementById('modal-confirm');
  let _confirmResolve = null;
  let _confirmModal = null;
  if(confirmModalEl){
    _confirmModal = new bootstrap.Modal(confirmModalEl, {});
    const btnConfirm = confirmModalEl.querySelector('.btn-confirm');
    const btnCancel = confirmModalEl.querySelector('.btn-cancel');
    if(btnConfirm) btnConfirm.addEventListener('click', ()=>{ if(_confirmResolve) { _confirmResolve(true); _confirmResolve = null; } _confirmModal.hide(); });
    if(btnCancel) btnCancel.addEventListener('click', ()=>{ if(_confirmResolve) { _confirmResolve(false); _confirmResolve = null; } _confirmModal.hide(); });
  }

  function confirmAction(msg){
    if(!confirmModalEl) return Promise.resolve(window.confirm(msg));
    return new Promise(resolve=>{
      const msgEl = confirmModalEl.querySelector('.confirm-message');
      if(msgEl) msgEl.textContent = msg;
      _confirmResolve = resolve;
      _confirmModal.show();
    });
  }

  // home preview handler: show selected background before upload
  const homeFormEl = document.getElementById('home-form');
  if(homeFormEl){
    const bgInput = homeFormEl.querySelector('input[name=background]');
    const previewWrapper = document.querySelector('.preview-wrapper');
    const bgPreview = document.getElementById('home-bg-preview');
    if(bgInput){
      bgInput.addEventListener('change', function(){
        const f = this.files && this.files[0];
        if(f){
          try{ bgPreview.src = URL.createObjectURL(f); }catch(e){}
          previewWrapper && previewWrapper.classList.remove('d-none');
        } else {
          previewWrapper && previewWrapper.classList.add('d-none');
        }
      });
    }
  }

  // current section
  let current = 'home';
  function setActiveSection(name){
    current = name;
    sectionTitle.textContent = name.charAt(0).toUpperCase() + name.slice(1);
    document.querySelectorAll('.admin-sidebar .nav-link').forEach(n=>n.classList.remove('active'));
    document.querySelector(`.admin-sidebar .nav-link[data-section="${name}"]`)?.classList.add('active');

    // show/hide panels
    homePanel.classList.add('d-none');
    listPanel.classList.add('d-none');
    if(aboutPanel) aboutPanel.classList.add('d-none');

    if(name === 'home'){
      homePanel.classList.remove('d-none');
      btnAdd.classList.add('d-none'); // home is single resource
    } else if(name === 'about'){
      if(aboutPanel) aboutPanel.classList.remove('d-none');
      btnAdd.classList.add('d-none');
    } else {
      listPanel.classList.remove('d-none');
      btnAdd.classList.remove('d-none');
    }

    loadSection(name);
  }

  // attach sidebar clicks
  sidebarLinks.forEach(link=>{
    link.addEventListener('click', e=>{
      e.preventDefault();
      const s = link.dataset.section;
      setActiveSection(s);
    });
  });

  // refresh button
  btnRefresh.addEventListener('click', ()=> loadSection(current));

  const adminNotice = document.getElementById('admin-notice');
  function showNotice(msg, type='info', timeout=4000){
    if(!adminNotice) return;
    adminNotice.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
    if(timeout) setTimeout(()=>{ if(adminNotice) adminNotice.innerHTML = ''; }, timeout);
  }

  function setLoading(on){
    // disable buttons and show small spinner
    const allBtns = document.querySelectorAll('#admin-content button, #admin-content input');
    allBtns.forEach(b=>{ b.disabled = !!on; });
    if(on) showNotice('Loading…', 'secondary', 0);
    else adminNotice && (adminNotice.innerHTML = '');
  }

  // add button -> open modal for new
  btnAdd.addEventListener('click', ()=>{
    openModalForNew(current);
  });

  // initial load
  setActiveSection('home');

  /* ---------- LOADS ---------- */
  function loadSection(name, suppressLoading=false){
    if(name === 'home') return loadHome(suppressLoading);
    if(name === 'about') return loadAbout(suppressLoading);
    // list endpoints
    const url = API[name];
    if(!suppressLoading) setLoading(true);
    fetchWithCreds(url)
      .then(r => r.json())
      .then(data => { renderTable(name, data); if(!suppressLoading) setLoading(false); })
      .catch(err => { console.error(err); showErrorTable(err); if(!suppressLoading) setLoading(false); showNotice('Error loading data', 'danger'); });
  }

  function loadAbout(suppressLoading=false){
    if(!suppressLoading) setLoading(true);
    fetchWithCreds(API.about)
      .then(r=>r.json())
      .then(data=>{
        const form = document.getElementById('about-form');
        if(!data || data.length === 0){
          // prefill with sensible defaults when empty
          form.reset();
          form.querySelector('input[name=id]').value = '';
          form.title.value = '';
          form.description.value = DEFAULTS.ABOUT_DESC;
          form.phone.value = '';
          form.email.value = '';
          document.querySelector('.about-preview')?.classList.add('d-none');
        } else {
          const item = data[0];
          form.title.value = item.title || '';
          form.description.value = item.description || '';
          form.phone.value = item.phone || '';
          form.email.value = item.email || '';
          form.querySelector('input[name=id]').value = item.id || '';
          if(item.profile_image){
            document.querySelector('.about-preview')?.classList.remove('d-none');
            document.getElementById('about-img-preview').src = item.profile_image;
          }
        }
        if(!suppressLoading) setLoading(false);
      }).catch(err=>{ console.error(err); setLoading(false); showNotice('Error loading about', 'danger'); });
  }

  function loadHome(suppressLoading=false){
    if(!suppressLoading) setLoading(true);
    fetchWithCreds(API.home)
      .then(r=>r.json())
      .then(data=>{
        const form = document.getElementById('home-form');
        if(!data || data.length === 0){
          // empty form for new
          form.reset();
          form.querySelector('input[name=id]').value = '';
          document.querySelector('.preview-wrapper').classList.add('d-none');
        } else {
          const item = data[0];
          form.name.value = item.name || '';
          form.roles.value = item.roles || '';
          form.querySelector('input[name=id]').value = item.id || '';
          if(item.background){
            document.querySelector('.preview-wrapper').classList.remove('d-none');
            document.getElementById('home-bg-preview').src = item.background;
          }
        }
        if(!suppressLoading) setLoading(false);
      }).catch(err=>{ console.error(err); setLoading(false); showNotice('Error loading home', 'danger'); });
  }

  /* ---------- HOME FORM (single) ---------- */
  document.getElementById('home-form').addEventListener('submit', function(e){
    e.preventDefault();
    const form = e.target;
    const id = form.querySelector('input[name=id]').value;
    const name = form.name.value;
    const roles = form.roles.value;
    const file = form.background.files[0];

    if(file){
      // upload via FormData (create or update)
      const fd = new FormData();
      fd.append('name', name);
      fd.append('roles', roles);
      fd.append('background', file);
      const method = id ? 'PATCH' : 'POST';
      const url = id ? (API.home + id + '/') : API.home;
      fetchWithCreds(url, {
        method,
        headers: { 'X-CSRFToken': csrftoken },
        body: fd
      }).then(r=>{ if(!r.ok) throw r; return r.json(); }).then(()=>{ loadHome(true); showNotice('Saved', 'success'); }).catch(err=>{ console.error(err); showNotice('Save failed', 'danger'); });
    } else {
      // JSON update/create without file
      const payload = { name, roles };
      const method = id ? 'PUT' : 'POST';
      const url = id ? (API.home + id + '/') : API.home;
      fetchWithCreds(url, {
        method, headers: {
          'Content-Type':'application/json', 'X-CSRFToken': csrftoken
        }, body: JSON.stringify(payload)
      }).then(r=>{ if(!r.ok) throw r; return r.json(); }).then(()=>{ loadHome(true); showNotice('Saved', 'success'); }).catch(err=>{ console.error(err); showNotice('Save failed', 'danger'); });
    }
  });

  // home delete
  document.getElementById('home-delete').addEventListener('click', function(){
    const id = document.getElementById('home-form').querySelector('input[name=id]').value;
    if(!id) return showNotice('Nothing to delete', 'warning');
    confirmAction('Delete home entry?').then(confirm => {
      if(!confirm) return;
      fetchWithCreds(API.home + id + '/', { method:'DELETE', headers:{ 'X-CSRFToken': csrftoken }})
        .then(r=>{
          if(r.ok) { showNotice('Deleted', 'success'); loadHome(); } else { showNotice('Delete failed', 'danger'); }
        }).catch(err=>{ console.error(err); showNotice('Delete failed', 'danger'); });
    });
  });

  /* ---------- ABOUT FORM (single) ---------- */
  const aboutFormEl = document.getElementById('about-form');
  if(aboutFormEl){
    aboutFormEl.addEventListener('submit', function(e){
      e.preventDefault();
      const form = e.target;
      const id = form.querySelector('input[name=id]').value;
      const fd = new FormData(form);
      const url = id ? (API.about + id + '/') : API.about;
      const method = id ? 'PATCH' : 'POST';
      fetchWithCreds(url, { method, headers:{ 'X-CSRFToken': csrftoken }, body: fd })
        .then(r=>{ if(!r.ok) throw r; return r.json(); }).then(()=>{ loadAbout(true); showNotice('Saved', 'success'); }).catch(err=>{ console.error(err); showNotice('Save failed', 'danger'); });
    });

    document.getElementById('about-delete').addEventListener('click', function(){
      const id = aboutFormEl.querySelector('input[name=id]').value;
      if(!id) return showNotice('Nothing to delete', 'warning');
      confirmAction('Delete about entry?').then(confirm => {
        if(!confirm) return;
        fetchWithCreds(API.about + id + '/', { method:'DELETE', headers:{ 'X-CSRFToken': csrftoken }})
          .then(r=>{ if(r.ok){ showNotice('Deleted', 'success'); loadAbout(); } else { showNotice('Delete failed', 'danger'); } }).catch(err=>{ console.error(err); showNotice('Delete failed', 'danger'); });
      });
    });
  }

  // about image preview on change
  if(aboutFormEl){
    const aboutFile = aboutFormEl.querySelector('input[name=profile_image]');
    const aboutPreviewWrap = document.querySelector('.about-preview');
    const aboutImg = document.getElementById('about-img-preview');
    if(aboutFile){
      aboutFile.addEventListener('change', function(){
        const f = this.files && this.files[0];
        if(f){
          try{ aboutImg.src = URL.createObjectURL(f); }catch(e){}
          aboutPreviewWrap && aboutPreviewWrap.classList.remove('d-none');
        } else {
          aboutPreviewWrap && aboutPreviewWrap.classList.add('d-none');
        }
      });
    }
  }

  /* ---------- TABLE RENDER ---------- */
  function renderTable(section, items){
    // set headers depending on section
    let headers = [];
    if(section === 'resume'){
      headers = ['ID','Section','Title','Dates','Company','Actions'];
    } else if(section === 'portfolio'){
      headers = ['ID','Title','Category','Image','Actions'];
    } else if(section === 'services'){
      headers = ['ID','Title','Description','Actions'];
    } else if(section === 'skills'){
      headers = ['ID','Name','Level','Actions'];
    } else if(section === 'contact'){
      headers = ['ID','Name','Email','Subject','Message','Actions'];
    } else {
      headers = Object.keys(items[0]||{}).map(k=>k);
    }

    adminTableHead.innerHTML = '';
    headers.forEach(h=>{
      const th = document.createElement('th'); th.textContent = h; adminTableHead.appendChild(th);
    });

    adminTableBody.innerHTML = '';
    items.forEach(it=>{
      const tr = document.createElement('tr');
      if(section === 'resume'){
        tr.innerHTML = `
            <td>${it.id}</td>
            <td>${it.section}</td>
            <td>${escapeHtml(it.title)}</td>
            <td>${it.date_from || ''} - ${it.date_to || ''}</td>
            <td>${escapeHtml(it.company||'')}</td>
            <td style="text-align:right">
              <button class="btn btn-sm btn-outline-secondary btn-up" data-id="${it.id}">⬆</button>
              <button class="btn btn-sm btn-outline-secondary btn-down ms-1" data-id="${it.id}">⬇</button>
              <button class="btn btn-sm btn-outline-primary btn-edit ms-2" data-id="${it.id}">Edit</button>
              <button class="btn btn-sm btn-danger btn-delete ms-1" data-id="${it.id}">Delete</button>
            </td>`;
      } else if(section === 'portfolio'){
        tr.innerHTML = `
          <td>${it.id}</td>
          <td>${escapeHtml(it.title)}</td>
            <td>${escapeHtml(it.category||'')}</td>
            <td><img src="${it.image||'/static/img/placeholder.png'}" style="height:40px;border-radius:4px"></td>
            <td>
              <a href="${it.details_url || '/swagger/'}" target="_blank" class="btn btn-sm btn-outline-info me-1">Open</a>
              <button class="btn btn-sm btn-outline-primary btn-edit" data-id="${it.id}">Edit</button>
              <button class="btn btn-sm btn-danger btn-delete" data-id="${it.id}">Delete</button>
            </td>`;
      } else if(section === 'services'){
        tr.innerHTML = `
          <td>${it.id}</td>
          <td>${escapeHtml(it.title)}</td>
          <td>${escapeHtml(it.description||'')}</td>
          <td>
            <button class="btn btn-sm btn-outline-primary btn-edit" data-id="${it.id}">Edit</button>
            <button class="btn btn-sm btn-danger btn-delete" data-id="${it.id}">Delete</button>
          </td>`;
          } else if(section === 'skills'){
            tr.innerHTML = `
              <td>${it.id}</td>
              <td>${escapeHtml(it.name)}</td>
              <td>
                <div class="skill-slider" data-id="${it.id}" data-level="${it.level}">
                  <div class="skill-fill" style="width:${it.level}%;"></div>
                  <div class="skill-handle" style="left:calc(${it.level}% - 8px);"></div>
                  <div class="skill-value">${it.level}%</div>
                </div>
              </td>
              <td>
                <button class="btn btn-sm btn-outline-primary btn-edit" data-id="${it.id}">Edit</button>
                <button class="btn btn-sm btn-danger btn-delete" data-id="${it.id}">Delete</button>
              </td>`;
      } else if(section === 'contact'){
        tr.innerHTML = `
          <td>${it.id}</td>
          <td>${escapeHtml(it.name)}</td>
          <td>${escapeHtml(it.email)}</td>
          <td>${escapeHtml(it.subject||'')}</td>
          <td>${escapeHtml(it.message||'')}</td>
          <td>
            <button class="btn btn-sm btn-danger btn-delete" data-id="${it.id}">Delete</button>
          </td>`;
      } else {
        tr.textContent = JSON.stringify(it);
      }
      adminTableBody.appendChild(tr);
    });
    // after rows rendered, bind skill sliders
    if(section === 'skills') bindSkillSliders();
    // attach edit/delete handlers
    adminTableBody.querySelectorAll('.btn-edit').forEach(b=>{
      b.addEventListener('click', e=>{
        const id = b.dataset.id;
        openModalForEdit(current, id);
      });
    });
    adminTableBody.querySelectorAll('.btn-delete').forEach(b=>{
      b.addEventListener('click', e=>{
        const id = b.dataset.id;
        confirmAction('Delete item?').then(confirm => {
          if(!confirm) return;
          fetchWithCreds(API[current] + id + '/', { method:'DELETE', headers:{ 'X-CSRFToken': csrftoken }})
            .then(r=>{ if(r.ok) loadSection(current); else showNotice('Delete failed', 'danger'); })
            .catch(err=>{ console.error(err); showNotice('Delete failed', 'danger'); });
        });
      });
    });

    // resume up/down handlers
    adminTableBody.querySelectorAll('.btn-up').forEach(b=>{
      b.addEventListener('click', e=>{
        const id = b.dataset.id;
        // decrease order (move earlier)
        fetchWithCreds(API.resume + id + '/').then(r=>r.json()).then(item=>{
          const newOrder = (item.order || 0) - 10;
          fetchWithCreds(API.resume + id + '/', { method:'PATCH', headers:{ 'Content-Type':'application/json','X-CSRFToken': csrftoken }, body: JSON.stringify({ order: newOrder }) }).then(r=>{ if(r.ok) loadSection('resume'); else showNotice('Reorder failed','danger'); }).catch(err=>{ console.error(err); showNotice('Reorder failed','danger'); });
        }).catch(console.error);
      });
    });
    adminTableBody.querySelectorAll('.btn-down').forEach(b=>{
      b.addEventListener('click', e=>{
        const id = b.dataset.id;
        // increase order (move later)
        fetchWithCreds(API.resume + id + '/').then(r=>r.json()).then(item=>{
          const newOrder = (item.order || 0) + 10;
          fetchWithCreds(API.resume + id + '/', { method:'PATCH', headers:{ 'Content-Type':'application/json','X-CSRFToken': csrftoken }, body: JSON.stringify({ order: newOrder }) }).then(r=>{ if(r.ok) loadSection('resume'); else showNotice('Reorder failed','danger'); }).catch(err=>{ console.error(err); showNotice('Reorder failed','danger'); });
        }).catch(console.error);
      });
    });
  }

  function showErrorTable(err){
    adminTableBody.innerHTML = `<tr><td colspan="6" class="text-danger">Error loading data</td></tr>`;
  }

  /* ---------- SKILL SLIDER BINDING ---------- */
  function bindSkillSliders(){
    const sliders = document.querySelectorAll('.skill-slider');
    sliders.forEach(slider => {
      if(slider._bound) return;
      slider._bound = true;
      const id = slider.dataset.id;
      const fill = slider.querySelector('.skill-fill');
      const handle = slider.querySelector('.skill-handle');
      const valueEl = slider.querySelector('.skill-value');

      let dragging = false;
      let lastShift = false; // whether user held shift (fine mode)
      const rect = ()=> slider.getBoundingClientRect();

      function updateFromClient(clientX){
        const r = rect();
        let pct = Math.round(((clientX - r.left) / r.width) * 100);
        if(pct < 0) pct = 0; if(pct > 100) pct = 100;
        fill.style.width = pct + '%';
        handle.style.left = `calc(${pct}% - 8px)`;
        valueEl.textContent = pct + '%';
        slider.dataset.level = pct;
        return pct;
      }

      function saveLevel(level){
        // PATCH level
        fetchWithCreds(API.skills + id + '/', {
          method: 'PATCH',
          headers: { 'Content-Type':'application/json', 'X-CSRFToken': csrftoken },
          body: JSON.stringify({ level })
        }).then(r=>{ if(!r.ok) throw r; return r.json(); }).then(()=>{ showNotice('Skill updated', 'success'); }).catch(err=>{ console.error(err); showNotice('Save failed', 'danger'); });
      }

      // mouse / touch
      const onPointerDown = (e)=>{
        e.preventDefault(); dragging = true; slider.classList.add('dragging');
        lastShift = !!(e.shiftKey);
        const clientX = (e.touches ? e.touches[0].clientX : e.clientX);
        updateFromClient(clientX);
      };
      const onPointerMove = (e)=>{
        if(!dragging) return;
        lastShift = !!(e.shiftKey || false);
        const clientX = (e.touches ? e.touches[0].clientX : e.clientX);
        updateFromClient(clientX);
      };
      const onPointerUp = (e)=>{
        if(!dragging) return; dragging = false; slider.classList.remove('dragging');
        // snap to step unless user held shift (fine control)
        const levelRaw = parseInt(slider.dataset.level || '0', 10);
        const step = lastShift ? 1 : 5;
        const snapped = Math.min(100, Math.max(0, Math.round(levelRaw / step) * step));
        // animate to snapped value (transitions enabled when not dragging)
        fill.style.width = snapped + '%';
        handle.style.left = `calc(${snapped}% - 8px)`;
        valueEl.textContent = snapped + '%';
        slider.dataset.level = snapped;
        saveLevel(snapped);
      };

      handle.addEventListener('mousedown', onPointerDown);
      handle.addEventListener('touchstart', onPointerDown, {passive:true});
      window.addEventListener('mousemove', onPointerMove);
      window.addEventListener('touchmove', onPointerMove, {passive:true});
      window.addEventListener('mouseup', onPointerUp);
      window.addEventListener('touchend', onPointerUp);
    });
  }

  /* ---------- MODAL / EDIT ---------- */
  function openModalForNew(section){
    document.getElementById('modal-body').innerHTML = renderFormFields(section, null);
    document.getElementById('modal-form').querySelector('input[name=id]').value = '';
    document.getElementById('modal-form').onsubmit = handleModalSubmit;
    // setup modal file previews for newly created form
    bindModalFilePreviews();
    modal.show();
  }

  function openModalForEdit(section, id){
    fetchWithCreds(API[section] + id + '/').then(r=>{ if(!r.ok) throw r; return r.json(); }).then(data=>{
      document.getElementById('modal-body').innerHTML = renderFormFields(section, data);
      document.getElementById('modal-form').querySelector('input[name=id]').value = id;
      document.getElementById('modal-form').onsubmit = handleModalSubmit;
      // setup modal file previews and, if portfolio, show existing image
      bindModalFilePreviews();
      if(section === 'portfolio' && data && data.image){
        const img = document.getElementById('modal-image-preview');
        if(img){ img.src = data.image; img.closest('.modal-image-preview')?.classList.remove('d-none'); }
      }
      modal.show();
    }).catch(console.error);
  }

  function renderFormFields(section, data){
    data = data || {};
    if(section === 'resume'){
      return `
        <div class="mb-3"><label>Section</label><input name="section" class="form-control" value="${escapeHtml(data.section||'education')}" /></div>
        <div class="mb-3"><label>Title</label><input name="title" class="form-control" value="${escapeHtml(data.title||'')}" /></div>
        <div class="row">
          <div class="col"><div class="mb-3"><label>Date from</label><input name="date_from" class="form-control" value="${escapeHtml(data.date_from||'')}" /></div></div>
          <div class="col"><div class="mb-3"><label>Date to</label><input name="date_to" class="form-control" value="${escapeHtml(data.date_to||'')}" /></div></div>
        </div>
        <div class="mb-3"><label>Company</label><input name="company" class="form-control" value="${escapeHtml(data.company||'')}" /></div>
        <div class="mb-3"><label>Description</label><textarea name="description" class="form-control">${escapeHtml(data.description||'')}</textarea></div>
        <div class="mb-3"><label>Order</label><input name="order" type="number" class="form-control" value="${escapeHtml(data.order||'0')}" /></div>
      `;
    }
    if(section === 'portfolio'){
      return `
        <div class="mb-3"><label>Title</label><input name="title" class="form-control" value="${escapeHtml(data.title||'')}" /></div>
        <div class="mb-3"><label>Category</label><input name="category" class="form-control" value="${escapeHtml(data.category||'')}" /></div>
        <div class="mb-3"><label>Image (choose to upload)</label><input type="file" name="image" class="form-control" /></div>
        <div class="mb-3 modal-image-preview d-none"><img id="modal-image-preview" src="" style="max-height:140px;border-radius:6px;display:block;"/></div>
        <div class="mb-3"><label>Description</label><textarea name="description" class="form-control">${escapeHtml(data.description||'')}</textarea></div>
        <div class="mb-3"><label>Details URL</label><input name="details_url" class="form-control" value="${escapeHtml(data.details_url||'')}" /></div>
      `;
    }
    if(section === 'services'){
      return `
        <div class="mb-3"><label>Title</label><input name="title" class="form-control" value="${escapeHtml(data.title||'')}" /></div>
        <div class="mb-3"><label>Description</label><textarea name="description" class="form-control">${escapeHtml(data.description||'')}</textarea></div>
        <div class="mb-3"><label>Icon class</label><input name="icon_class" class="form-control" value="${escapeHtml(data.icon_class||'')}" /></div>
      `;
    }
    if(section === 'skills'){
      return `
        <div class="mb-3"><label>Name</label><input name="name" class="form-control" value="${escapeHtml(data.name||'')}" /></div>
        <div class="mb-3"><label>Level (0-100)</label><input name="level" type="number" min="0" max="100" class="form-control" value="${escapeHtml(data.level||'50')}" /></div>
        <div class="mb-3"><label>Order</label><input name="order" type="number" class="form-control" value="${escapeHtml(data.order||'0')}" /></div>
      `;
    }
    if(section === 'contact'){
      return `
        <div class="mb-3"><label>Name</label><input name="name" class="form-control" value="${escapeHtml(data.name||'')}" /></div>
        <div class="mb-3"><label>Email</label><input name="email" class="form-control" value="${escapeHtml(data.email||'')}" /></div>
        <div class="mb-3"><label>Subject</label><input name="subject" class="form-control" value="${escapeHtml(data.subject||'')}" /></div>
        <div class="mb-3"><label>Message</label><textarea name="message" class="form-control">${escapeHtml(data.message||'')}</textarea></div>
      `;
    }
    return `<div class="mb-3">No form for this section</div>`;
  }

  function handleModalSubmit(e){
    e.preventDefault();
    const form = e.target;
    const id = form.querySelector('input[name=id]').value;
    const fd = new FormData(form);
    const hasFile = Array.from(fd.values()).some(v=> v instanceof File && v.size > 0);

    const url = API[current] + (id ? id + '/' : '');
    const method = id ? 'PUT' : 'POST';

    if(hasFile){
      // send FormData (PATCH preferred for partial updates but using POST/PUT works if backend accepts)
      fetchWithCreds(url, { method: id ? 'PATCH' : 'POST', headers:{ 'X-CSRFToken': csrftoken }, body: fd })
        .then(async r=>{
          if(!r.ok){ const text = await r.text().catch(()=>null); console.error('Save failed', r.status, text); showNotice('Save failed: '+(text||r.status), 'danger', 7000); throw new Error(text||r.status); }
          return r.json().catch(()=>null);
        }).then(()=>{ modal.hide(); loadSection(current, true); showNotice('Saved', 'success'); })
        .catch(err=>{ console.error(err); });
    } else {
      const obj = {};
      for(const [k,v] of fd.entries()){ if(k!=='id') obj[k]=v; }
      fetchWithCreds(url, { method, headers:{ 'Content-Type':'application/json', 'X-CSRFToken': csrftoken }, body: JSON.stringify(obj) })
        .then(async r=>{
          if(!r.ok){ const text = await r.text().catch(()=>null); console.error('Save failed', r.status, text); showNotice('Save failed: '+(text||r.status), 'danger', 7000); throw new Error(text||r.status); }
          return r.json().catch(()=>null);
        }).then(()=>{ modal.hide(); loadSection(current, true); showNotice('Saved', 'success'); })
        .catch(err=>{ console.error(err); });
    }
  }

  // bind modal file input previews (for portfolio image etc.)
  function bindModalFilePreviews(){
    const modalBody = document.getElementById('modal-body');
    if(!modalBody) return;
    const fileInputs = modalBody.querySelectorAll('input[type=file]');
    fileInputs.forEach(inp=>{
      inp.addEventListener('change', function(){
        const f = this.files && this.files[0];
        const previewImg = modalBody.querySelector('#modal-image-preview');
        const previewWrap = modalBody.querySelector('.modal-image-preview');
        if(f && previewImg){
          try{ previewImg.src = URL.createObjectURL(f); }catch(e){}
          previewWrap && previewWrap.classList.remove('d-none');
        } else {
          previewWrap && previewWrap.classList.add('d-none');
        }
      });
    });
  }

  /* ---------- helpers ---------- */
  function escapeHtml(s){
    if(!s) return '';
    return String(s)
      .replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')
      .replaceAll('"','&quot;').replaceAll("'",'&#039;');
  }

})();
