from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.server import MANIFEST
from backend.auth.jwt import create_access_token, verify_password
from backend.config import settings
from backend.database import Base, SessionLocal, engine, get_db
from backend.models.db import DocumentChunk, Employee
from backend.models.schemas import ChatRequest
from backend.routes.admin import router as admin_router
from backend.routes.auth import router as auth_router
from backend.routes.chat import router as chat_router
from backend.routes.hr_chat import router as hr_chat_router
from backend.routes.users import router as users_router
from backend.rag.ingest import ingest_file
from backend.services.bootstrap import seed_employees
from backend.services.chat_service import ask_hr_assistant
from backend.services.logging_service import save_chat_log

EXTRA_UI_SCRIPT = """
<script>
(function () {
  let auth = { email: '', password: '', token: '', role: '' };

  function authHeaders() {
    return auth.token ? { Authorization: 'Bearer ' + auth.token } : {};
  }

  async function authed(path, options) {
    const opts = options || {};
    opts.headers = Object.assign({}, opts.headers || {}, authHeaders());
    const r = await fetch(path, opts);
    return r.json();
  }

  function ensureUiBlocks() {
    if (document.getElementById('password')) return;
    const loginInput = document.getElementById('login');
    const pass = document.createElement('input');
    pass.id = 'password';
    pass.className = 'field';
    pass.placeholder = 'Пароль';
    pass.type = 'password';
    pass.style.marginTop = '10px';
    loginInput.insertAdjacentElement('afterend', pass);

    const inputWrap = document.querySelector('.input');
    if (inputWrap && !document.getElementById('callHrBtn')) {
      const btn = document.createElement('button');
      btn.id = 'callHrBtn';
      btn.className = 'btn secondary';
      btn.textContent = 'Вызвать HR';
      btn.style.display = 'none';
      btn.onclick = window.callHr;
      inputWrap.appendChild(btn);
    }

    const nav = document.querySelector('.nav');
    if (nav && !document.getElementById('nav-hr')) {
      const hrBtn = document.createElement('button');
      hrBtn.id = 'nav-hr';
      hrBtn.className = 'navBtn';
      hrBtn.style.display = 'none';
      hrBtn.textContent = 'HR чаты';
      hrBtn.onclick = function () { showView('hr', hrBtn); loadHrTickets(); };
      nav.appendChild(hrBtn);

      const manageBtn = document.createElement('button');
      manageBtn.id = 'nav-manage';
      manageBtn.className = 'navBtn';
      manageBtn.style.display = 'none';
      manageBtn.textContent = 'Управление';
      manageBtn.onclick = function () { showView('manage', manageBtn); loadUsers(); };
      nav.appendChild(manageBtn);
    }

    const main = document.querySelector('main.main');
    if (main && !document.getElementById('view-hr')) {
      const hrView = document.createElement('div');
      hrView.id = 'view-hr';
      hrView.className = 'view';
      hrView.innerHTML = '<div class="docList"><div class="docCard"><h2 id="hrTitle">HR чаты</h2><div id="hrTicketList"></div></div><div class="docCard"><h3>Сообщения</h3><div id="hrMessages" class="msgs" style="height:280px"></div><div class="input"><input id="hrReply" class="field" placeholder="Сообщение"><button class="btn secondary" onclick="sendHrReply()">Отправить</button><button id="clearHrBtn" class="btn secondary" style="display:none" onclick="clearHrChat()">Очистить чат</button></div></div></div>';
      main.appendChild(hrView);

      const mView = document.createElement('div');
      mView.id = 'view-manage';
      mView.className = 'view';
      mView.innerHTML = '<div class="docList"><div class="docCard"><h2>Пользователи</h2><div id="usersList"></div></div><div class="docCard"><h3>Создать работника</h3><input id="newMail" class="field" placeholder="Email"><input id="newTab" class="field" placeholder="Табельный номер" style="margin-top:8px"><input id="newName" class="field" placeholder="ФИО" style="margin-top:8px"><input id="newPos" class="field" placeholder="Должность" style="margin-top:8px"><input id="newPass" class="field" type="password" placeholder="Пароль" style="margin-top:8px"><button class="btn secondary" style="margin-top:10px" onclick="createWorker()">Создать</button><div id="manageStatus" class="hint"></div></div></div>';
      main.appendChild(mView);
    }
  }

  function applyRoleUi() {
    const role = (auth.role || '').toLowerCase();
    const callBtn = document.getElementById('callHrBtn');
    const navHr = document.getElementById('nav-hr');
    const navManage = document.getElementById('nav-manage');
    const navChat = document.querySelector('.nav .navBtn');
    const upload = document.querySelector('.upload');
    const chatActionBtns = document.querySelector('.top .row');
    const hrTitle = document.getElementById('hrTitle');
    const clearBtn = document.getElementById('clearHrBtn');
    if (callBtn) callBtn.style.display = role === 'worker' || role === 'employee' ? '' : 'none';
    if (navHr) navHr.style.display = role === 'hr_manager' || role === 'worker' || role === 'employee' ? '' : 'none';
    if (navManage) navManage.style.display = role === 'manager' || role === 'hr_manager' ? '' : 'none';
    if (upload) upload.style.display = role === 'manager' ? '' : 'none';
    if (navChat) navChat.style.display = role === 'worker' || role === 'employee' ? '' : 'none';
    if (chatActionBtns && !(role === 'worker' || role === 'employee')) {
      chatActionBtns.style.display = 'none';
      if (typeof showView === 'function' && navManage && navManage.style.display !== 'none') showView('manage', navManage);
    }
    if (chatActionBtns && (role === 'worker' || role === 'employee')) chatActionBtns.style.display = '';
    if (hrTitle) hrTitle.textContent = role === 'hr_manager' ? 'Чаты с работниками' : 'Мой HR чат';
    if (clearBtn) clearBtn.style.display = role === 'worker' || role === 'employee' ? '' : 'none';
  }

  function mapEmployee(e) {
    return {
      id: e.id,
      email: e.email,
      tab: e.tab_number || '-',
      name: e.full_name || e.name || '',
      role: e.role || 'worker',
      department: e.department || '',
      position: e.position || '',
      manager: e.manager || '',
      vacation_days: e.vacation_days || 0,
      nearest_vacation: e.nearest_vacation || '',
      birthday: e.birthday || '',
      phone: e.phone || '-',
      hire_date: e.hire_date || '-',
      inspector: e.inspector || '-',
      benefits: e.benefits || '-'
    };
  }

  window.doLogin = async function () {
    ensureUiBlocks();
    const quickNode = document.getElementById('quick');
    const email = (document.getElementById('login').value || '').trim();
    const password = (document.getElementById('password').value || '').trim();
    const loginErrNode = document.getElementById('loginErr');
    if (!email || !password) {
      if (loginErrNode) loginErrNode.textContent = 'Введите email и пароль';
      return;
    }
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, password: password })
    }).then(r => r.json());

    if (!res.ok) {
      if (loginErrNode) loginErrNode.textContent = res.error || 'Ошибка входа';
      return;
    }
    const employee = mapEmployee(res.employee || {});
    auth = { email: email, password: password, token: res.access_token || '', role: employee.role || '' };
    window.current = employee;
    try { current = employee; } catch (e) {}
    landing.style.display = 'none';
    app.style.display = 'grid';
    pname.textContent = employee.name || '';
    prole.textContent = (employee.role || '') + ' • ' + (employee.department || '');
    vacDays.textContent = String(employee.vacation_days || 0);
    tabNo.textContent = employee.tab || '-';
    nearest.textContent = 'Ближайший отпуск: ' + (employee.nearest_vacation || '-');
    if (quickNode) {
      quickNode.innerHTML = '';
      if (typeof quickEl === 'function') quickEl();
    }
    if (typeof renderProfile === 'function') renderProfile();
    await loadDocs();
    applyRoleUi();
    msgs.innerHTML = '';
    bot('Здравствуйте, ' + (employee.name || 'сотрудник') + '! Вы вошли как: ' + (employee.role || 'worker') + '.');
  };

  window.send = async function () {
    const text = (q.value || '').trim();
    if (!text || !window.current) return;
    user(text);
    q.value = '';
    const res = await fetch('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ login: auth.email, question: text })
    }).then(r => r.json());
    setTimeout(function () { bot(res.answer || 'Нет ответа', res); }, 180);
  };

  window.uploadFile = async function () {
    const f = file.files[0];
    if (!f) { uploadStatus.textContent = 'Выберите файл'; return; }
    const fd = new FormData();
    fd.append('file', f);
    fd.append('email', auth.email);
    fd.append('password', auth.password);
    const j = await fetch('/api/upload', { method: 'POST', body: fd }).then(r => r.json());
    uploadStatus.textContent = j.message || 'Готово';
    await loadDocs();
  };

  window.callHr = async function () {
    const text = prompt('Опишите вопрос для HR:');
    if (!text) return;
    const data = await authed('/hr-chat/call', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    bot(data.ok ? 'HR вызван. Номер тикета: ' + data.ticket_id : (data.detail || 'Ошибка вызова HR'));
    if (data.ok) {
      window.__activeTicket = data.ticket_id;
      await loadHrTickets();
      await openHrTicket(data.ticket_id);
    }
  };

  window.loadHrTickets = async function () {
    const data = await authed('/hr-chat/my');
    const box = document.getElementById('hrTicketList');
    if (!box) return;
    const tickets = data.tickets || [];
    const role = (auth.role || '').toLowerCase();
    box.innerHTML = tickets.map(function (t) {
      const who = role === 'hr_manager' ? ('worker: ' + t.worker_id) : ('HR: ' + t.hr_manager_id);
      return '<div class="source"><b>Тикет #' + t.id + '</b> (' + who + ') <button class="btn secondary" onclick="openHrTicket(' + t.id + ')">Открыть</button></div>';
    }).join('') || '<div class="hint">Нет чатов</div>';
    if (tickets.length && !window.__activeTicket) {
      window.__activeTicket = tickets[0].id;
      await openHrTicket(window.__activeTicket);
    }
  };

  window.openHrTicket = async function (ticketId) {
    window.__activeTicket = ticketId;
    const data = await authed('/hr-chat/' + ticketId + '/messages');
    const box = document.getElementById('hrMessages');
    const messages = data.messages || [];
    box.innerHTML = messages.map(function (m) {
      return '<div class="msg bot"><b>' + m.sender_id + ':</b> ' + (m.message || '') + '</div>';
    }).join('');
  };

  window.sendHrReply = async function () {
    const input = document.getElementById('hrReply');
    const text = (input.value || '').trim();
    if (!text || !window.__activeTicket) return;
    await authed('/hr-chat/' + window.__activeTicket + '/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    input.value = '';
    await openHrTicket(window.__activeTicket);
  };

  window.clearHrChat = async function () {
    if (!window.__activeTicket) return;
    const ok = confirm('Очистить всю историю этого HR-чата?');
    if (!ok) return;
    const data = await authed('/hr-chat/' + window.__activeTicket + '/clear', { method: 'DELETE' });
    if (data.ok) {
      document.getElementById('hrMessages').innerHTML = '<div class="hint">Чат очищен</div>';
      window.__activeTicket = null;
      await loadHrTickets();
    }
  };

  window.loadUsers = async function () {
    const users = await authed('/users/');
    const list = document.getElementById('usersList');
    if (!Array.isArray(users)) { list.innerHTML = '<div class="hint">Недостаточно прав</div>'; return; }
    const role = (auth.role || '').toLowerCase();
    list.innerHTML = users.map(function (u) {
      const assign = role === 'manager' ? ' <button class="btn secondary" onclick="assignHr(' + u.id + ')">Назначить HR</button>' : '';
      const edit = ' <button class="btn secondary" onclick="quickVacation(' + u.id + ')">Изменить отпуск</button>';
      return '<div class="source"><b>' + u.full_name + '</b> (' + u.role + ') - ' + u.email + assign + edit + '</div>';
    }).join('');
  };

  window.createWorker = async function () {
    const payload = {
      email: (document.getElementById('newMail').value || '').trim(),
      tab_number: (document.getElementById('newTab').value || '').trim(),
      full_name: (document.getElementById('newName').value || '').trim(),
      position: (document.getElementById('newPos').value || '').trim(),
      department: '',
      manager: '',
      vacation_days: 0,
      nearest_vacation: '',
      birthday: '',
      role: 'worker',
      password: (document.getElementById('newPass').value || '').trim()
    };
    const data = await authed('/users/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    document.getElementById('manageStatus').textContent = data.id ? 'Пользователь создан' : (data.detail || 'Ошибка');
    await loadUsers();
  };

  window.assignHr = async function (userId) {
    const data = await authed('/users/' + userId + '/assign-hr', { method: 'POST' });
    document.getElementById('manageStatus').textContent = data.message || data.detail || '';
    await loadUsers();
  };

  window.quickVacation = async function (userId) {
    const days = prompt('Введите количество дней отпуска:');
    if (days === null) return;
    const nearest = prompt('Введите период ближайшего отпуска:');
    const data = await authed('/users/' + userId, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ vacation_days: Number(days), nearest_vacation: nearest || '' })
    });
    document.getElementById('manageStatus').textContent = data.id ? 'Данные обновлены' : (data.detail || 'Ошибка');
    await loadUsers();
  };

  window.addEventListener('load', ensureUiBlocks);
})();
</script>
"""


def serialize_employee(employee: Employee) -> dict:
    return {
        "id": employee.id,
        "tab_number": employee.tab_number,
        "tab": employee.tab_number,
        "email": employee.email,
        "full_name": employee.full_name,
        "name": employee.full_name,
        "position": employee.position,
        "department": employee.department,
        "manager": employee.manager,
        "vacation_days": employee.vacation_days,
        "nearest_vacation": employee.nearest_vacation,
        "birthday": employee.birthday,
        "role": employee.role,
        "phone": "-",
        "hire_date": "-",
        "inspector": "HR support",
        "benefits": "-",
    }


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_employees(db)
    finally:
        db.close()
    yield


app = FastAPI(title="HR Assistant", lifespan=lifespan)
FRONTEND_INDEX_PATH = Path(__file__).resolve().parents[1] / "frontend" / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)
app.include_router(admin_router)
app.include_router(hr_chat_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def frontend_index():
    return FileResponse(FRONTEND_INDEX_PATH)


@app.get("/mobile")
def frontend_mobile():
    return FileResponse(FRONTEND_INDEX_PATH)


@app.get("/manifest.json")
def frontend_manifest():
    return MANIFEST


# Compatibility endpoints for existing frontend logic.
@app.post("/api/login")
def frontend_login(payload: dict, db: Session = Depends(get_db)):
    login = str(payload.get("email", payload.get("login", ""))).strip()
    password = str(payload.get("password", "")).strip()
    if not login or not password:
        return {"ok": False, "error": "Нужны email и пароль"}
    employee = (
        db.query(Employee)
        .filter(Employee.email == login)
        .first()
    )
    if not employee or not verify_password(password, employee.password):
        return {"ok": False, "error": "Сотрудник не найден или неверный пароль"}
    token = create_access_token(employee.email)
    return {"ok": True, "access_token": token, "employee": serialize_employee(employee)}


@app.post("/api/ask")
def frontend_ask(payload: dict, db: Session = Depends(get_db)):
    login = str(payload.get("login", "")).strip()
    question = str(payload.get("question", "")).strip()
    if not login or not question:
        return {"ok": False, "answer": "Передайте login и question", "sources": []}

    employee = (
        db.query(Employee)
        .filter((Employee.email == login) | (Employee.tab_number == login))
        .first()
    )
    if not employee:
        return {"ok": False, "answer": "Сначала войдите по табельному номеру или корпоративной почте.", "sources": []}
    if employee.role.lower() not in {"worker", "employee"}:
        return {"ok": False, "answer": "Чат-бот доступен только для работников.", "sources": []}

    answer, sources, unanswered = ask_hr_assistant(question, employee, db)
    save_chat_log(db, employee, question, answer, sources, unanswered)
    legacy_sources = [{"title": item["document"], "section": item["section"]} for item in sources]
    return {"ok": True, "answer": answer, "sources": legacy_sources, "portal": [], "unanswered": unanswered}


@app.get("/api/docs")
def frontend_docs(db: Session = Depends(get_db)):
    docs = (
        db.query(DocumentChunk.document_name, DocumentChunk.section)
        .order_by(DocumentChunk.document_name.asc(), DocumentChunk.chunk_order.asc())
        .all()
    )
    payload = [{"title": name, "section": section, "kind": "загружено локально"} for name, section in docs]
    return {"ok": True, "docs": payload}


@app.post("/api/upload")
async def frontend_upload(
    file: UploadFile = File(...),
    email: str = Form(default=""),
    password: str = Form(default=""),
    db: Session = Depends(get_db),
):
    actor = db.query(Employee).filter(Employee.email == email).first()
    if not actor or not verify_password(password, actor.password):
        return {"ok": False, "message": "Требуется вход email+пароль"}
    if actor.role.lower() != "manager":
        return {"ok": False, "message": "Загружать документы может только руководитель"}
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt", ".md"}:
        return {"ok": False, "message": "Поддерживаются PDF, DOCX, TXT, MD"}
    Path(settings.uploads_dir).mkdir(parents=True, exist_ok=True)
    target = Path(settings.uploads_dir) / file.filename
    target.write_bytes(await file.read())
    indexed = ingest_file(str(target), db)
    return {"ok": True, "message": f"Документ загружен, проиндексировано чанков: {indexed}"}
