# -*- coding: utf-8 -*-
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json, os, re, html, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS = os.path.join(ROOT, 'data', 'uploads')
os.makedirs(UPLOADS, exist_ok=True)

EMPLOYEES = {
    '1001': {'tab':'1001','email':'work@portal-test.1221systems.ru','name':'Алексей Рабочев','role':'Сотрудник','department':'Производственный блок','position':'Специалист производственного блока','manager':'Мария Директорова','phone':'+7 900 122-10-01','location':'Производственная площадка','schedule':'5/2, 09:00–18:00','hire_date':'12.02.2024','inspector':'Анна HR','vacation_days':14,'nearest_vacation':'15.07.2026 — 28.07.2026','birthday':'18 октября','benefits':'ДМС базовый пакет, мерч-магазин, реферальная программа'},
    '2001': {'tab':'2001','email':'dir@portal-test.1221systems.ru','name':'Мария Директорова','role':'Руководитель','department':'Операционный департамент','position':'Руководитель операционного департамента','manager':'Анна HR','phone':'+7 900 122-20-01','location':'Главный офис','schedule':'5/2, гибкий график','hire_date':'04.09.2021','inspector':'Анна HR','vacation_days':21,'nearest_vacation':'03.08.2026 — 16.08.2026','birthday':'7 мая','benefits':'ДМС расширенный пакет, кадровые заявки, отчеты по команде'},
    '3001': {'tab':'3001','email':'hr@portal-test.1221systems.ru','name':'Анна HR','role':'HR','department':'HR-департамент','position':'HR-специалист','manager':'Директор по персоналу','phone':'+7 900 122-30-01','location':'HR-департамент','schedule':'5/2, 09:00–18:00','hire_date':'18.01.2022','inspector':'Директор по персоналу','vacation_days':18,'nearest_vacation':'10.09.2026 — 23.09.2026','birthday':'12 марта','benefits':'Администрирование HR-процессов, база знаний, обращения сотрудников'},
}
EMAIL_INDEX = {v['email'].lower(): k for k, v in EMPLOYEES.items()}
BIRTHDAYS = {'иванова':'12 марта','иванов':'18 октября','петров':'24 ноября','сидоров':'5 февраля','рабочев':'18 октября','директорова':'7 мая'}
STOP = set('и в во на по к ко о об от для что как где когда сколько у меня мой моя мои мне или а не из за ли с со'.split())
SYN = {
    'зп':'зарплата', 'зарплат':'зарплата', 'оплат':'зарплата', 'аванс':'аванс',
    'расчет':'расчетный лист', 'расчёт':'расчетный лист', 'лист':'расчетный лист',
    'больнич':'больничный', 'справк':'справка', 'элн':'больничный',
    'дмс':'дмс', 'медицин':'дмс', 'льгот':'льготы',
    'отпуск':'отпуск', 'перен':'перенос отпуска', 'остаток':'остаток отпуска',
    'мерч':'мерч', 'магазин':'мерч', 'заказ':'заказ',
    'друг':'реферальная программа', 'ваканси':'реферальная программа', 'рекоменд':'реферальная программа',
    'стажиров':'стажировка', 'материальн':'материальная ответственность', 'команда':'команда', 'заявк':'заявка',
    'профиль':'профиль', 'карточка':'профиль'
}

KB = [
    {'id':'kb-1','title':'Правила внутреннего трудового распорядка','section':'п. 4.2','text':'Сотрудник может перенести отпуск по согласованию с руководителем. Для переноса отпуска нужно подать заявление через HR-портал не позднее чем за 14 календарных дней до начала отпуска. Если перенос связан с больничным или производственной необходимостью, сотрудник обращается к кадровому инспектору.'},
    {'id':'kb-2','title':'График отпусков 2026','section':'раздел 2','text':'Остаток отпуска сотрудника отображается в карточке сотрудника и рассчитывается по графику отпусков. Ближайший отпуск показывается по персональному графику сотрудника.'},
    {'id':'kb-3','title':'Положение об оплате труда','section':'п. 3.1','text':'Аванс выплачивается 25 числа текущего месяца. Окончательный расчет заработной платы производится 10 числа следующего месяца. Если дата выплаты приходится на выходной, выплата производится накануне.'},
    {'id':'kb-4','title':'Инструкция по расчетным листам','section':'п. 2.3','text':'Расчетный лист доступен в HR-портале в разделе Мои документы — Расчетные листы. Сотрудник может выбрать месяц и скачать расчетный лист в формате PDF.'},
    {'id':'kb-5','title':'Положение о больничных листах','section':'п. 5.1','text':'Для оформления больничного сотрудник должен сообщить руководителю и загрузить электронный лист нетрудоспособности или номер ЭЛН в HR-портал. Бумажные подтверждающие документы передаются через раздел Документы или кадровому инспектору.'},
    {'id':'kb-6','title':'Кафетерий льгот — ДМС','section':'раздел Программа ДМС','text':'Программа ДМС доступна сотрудникам после завершения испытательного срока. В личном кабинете сотрудник видит доступный пакет. В компании предусмотрены базовый и расширенный пакеты ДМС в зависимости от категории сотрудника.'},
    {'id':'kb-7','title':'Магазин мерча','section':'инструкция, раздел 1','text':'Заказ корпоративного мерча оформляется через раздел Магазин мерча HR-портала. В карточке товара сотрудник выбирает размер, количество и подтверждает заказ.'},
    {'id':'kb-8','title':'Реферальная программа','section':'п. 1.4','text':'Чтобы порекомендовать друга на вакансию, сотрудник заполняет форму рекомендации на HR-портале. После отправки формы HR связывается с кандидатом и сообщает статус рассмотрения.'},
    {'id':'kb-9','title':'Инструкция руководителя','section':'п. 6.2','text':'Руководитель может оформить стажировку, кадровую заявку или материальную ответственность через раздел Команда в HR-портале. В заявке указывается сотрудник, период, подразделение и основание.'},
    {'id':'kb-10','title':'Карточка сотрудника','section':'профиль сотрудника','text':'Карточка сотрудника содержит табельный номер, корпоративную почту, должность, подразделение, руководителя, график работы, кадрового инспектора, отпуск и доступные льготы.'},
    {'id':'kb-11','title':'Контакты HR-поддержки','section':'раздел Поддержка','text':'Если информация не найдена в документах, сотрудник создает обращение в HR-поддержку. В обращении нужно указать тему, описание вопроса и при необходимости приложить документ.'},
]

def employee_by_login(login):
    key=(login or '').strip().lower()
    if key in EMPLOYEES: return EMPLOYEES[key]
    if key in EMAIL_INDEX: return EMPLOYEES[EMAIL_INDEX[key]]
    return None

def tokenize(text):
    words = re.findall(r'[а-яА-Яa-zA-Z0-9]+', (text or '').lower())
    out=[]
    for w in words:
        if w in STOP or len(w)<2: continue
        out.append(w)
        for k,v in SYN.items():
            if k in w: out += re.findall(r'[а-яa-z0-9]+', v.lower())
    return out

def split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def uploaded_docs():
    docs=[]
    for name in sorted(os.listdir(UPLOADS)):
        path=os.path.join(UPLOADS,name)
        if not os.path.isfile(path): continue
        text=''
        ext=os.path.splitext(name)[1].lower()
        if ext in ['.txt','.md','.csv','.html','.json']:
            for enc in ['utf-8','cp1251','latin-1']:
                try:
                    with open(path,'r',encoding=enc,errors='ignore') as f: text=f.read()
                    break
                except Exception: pass
        if not text:
            text=f'Файл {name} загружен в локальное хранилище. Для глубокого поиска по PDF/DOCX в промышленной версии подключается локальный парсер документов.'
        docs.append({'id':'upl-'+name,'title':name,'section':'загруженный документ','text':text[:5000]})
    return docs

def all_docs(): return KB + uploaded_docs()

def search_context(question, limit=3):
    qtokens=tokenize(question)
    if not qtokens: return []
    scored=[]
    for doc in all_docs():
        dtokens=tokenize(doc['title']+' '+doc['section']+' '+doc['text'])
        overlap=sum(1 for t in qtokens if t in dtokens)
        # substring boosts for Russian stems
        boost=0
        low=(doc['title']+' '+doc['text']).lower()
        for t in set(qtokens):
            if len(t)>3 and t in low: boost+=2
        score=overlap+boost
        if score>0:
            scored.append((score,doc))
    scored.sort(key=lambda x:x[0], reverse=True)
    return [d for s,d in scored[:limit] if s>=2]

def detect_personal(question):
    q=(question or '').lower()
    if any(x in q for x in ['профиль','карточка','мои данные','личные данные']): return 'profile'
    if any(x in q for x in ['сколько', 'остаток', 'дней отпуска', 'мой отпуск', 'отпуск осталось']): return 'vacation'
    if 'день рождения' in q or 'др ' in q or 'birthday' in q: return 'birthday'
    return None

def portal_action(doc_title):
    t=doc_title.lower()
    if 'отпуск' in t: return {'label':'Открыть локальный раздел «Мой отпуск»','url':'/portal/vacation'}
    if 'расчет' in t: return {'label':'Открыть локальный раздел «Расчетные листы»','url':'/portal/payslips'}
    if 'больнич' in t: return {'label':'Открыть локальный раздел «Загрузить документ»','url':'/portal/documents'}
    if 'дмс' in t or 'льгот' in t: return {'label':'Открыть локальный раздел «ДМС»','url':'/portal/dms'}
    if 'мерч' in t: return {'label':'Открыть локальный раздел «Магазин мерча»','url':'/portal/merch'}
    if 'рефераль' in t: return {'label':'Открыть локальную форму рекомендации','url':'/portal/referral'}
    if 'руковод' in t: return {'label':'Открыть локальный раздел «Команда»','url':'/portal/team'}
    return None

def generate_answer(emp, question, contexts):
    personal = detect_personal(question)
    q=(question or '').lower()
    if personal=='profile':
        text=(f'Ваш профиль: {emp["name"]}, {emp["position"]}. Табельный номер — {emp["tab"]}. '
              f'Почта — {emp["email"]}. Подразделение — {emp["department"]}. Руководитель — {emp["manager"]}. '
              f'График — {emp["schedule"]}. Кадровый инспектор — {emp["inspector"]}. Остаток отпуска — {emp["vacation_days"]} дней.')
        return text, [{'title':'Карточка сотрудника','section':'профиль сотрудника'}], [{'label':'Открыть локальный профиль сотрудника','url':'/portal/profile'}]
    if personal=='vacation':
        return (f'{emp["name"]}, у вас осталось {emp["vacation_days"]} календарных дней отпуска. '
                f'Ближайший отпуск запланирован на период: {emp["nearest_vacation"]}. '
                'Я использовал персональную карточку сотрудника и график отпусков.'), [{'title':'График отпусков 2026','section':'раздел 2'}, {'title':'Карточка сотрудника','section':'профиль сотрудника'}], [{'label':'Открыть локальный раздел «Мой отпуск»','url':'/portal/vacation'}]
    if personal=='birthday':
        for name, bd in BIRTHDAYS.items():
            if name in q:
                return f'День рождения сотрудника: {bd}. Данные найдены в карточке сотрудника.', [{'title':'Карточка сотрудника','section':'профиль сотрудника'}], []
        return 'Уточните фамилию коллеги. Например: «Когда день рождения Иванова?»', [{'title':'Карточка сотрудника','section':'профиль сотрудника'}], []

    # role gate for manager questions
    if any(w in q for w in ['стажиров','оформить сотруд','материальн','команда','заявк']) and not emp['role'].lower().startswith('руковод'):
        return ('Этот процесс доступен руководителям. Если вам нужно оформить кадровую заявку, обратитесь к руководителю или кадровому инспектору. ' 
                f'Ваш кадровый инспектор: {emp["inspector"]}.'), [{'title':'Инструкция руководителя','section':'п. 6.2'}], [{'label':'Создать локальное обращение в HR','url':'/portal/support'}]

    if not contexts:
        return (f'В локальной базе знаний нет подтвержденного правила по этому вопросу. Я не буду выдумывать ответ.\n\n'
                f'Что можно сделать дальше:\n1. Создать обращение в HR-поддержку.\n2. Написать кадровому инспектору: {emp["inspector"]}.\n3. Загрузить документ или регламент в раздел «Документы», чтобы я смог использовать его как источник.'), [{'title':'Контакты HR-поддержки','section':'раздел Поддержка'}], [{'label':'Создать локальное обращение в HR','url':'/portal/support'}]

    best=contexts[0]
    sentences=split_sentences(best['text'])[:3]
    body=' '.join(sentences) if sentences else best['text'][:500]
    prefix='По найденному документу: '
    # make answer naturally adapted
    if 'куда' in q and ('справк' in q or 'больнич' in q): prefix='По документам по больничным и справкам: '
    elif 'как' in q: prefix='Порядок такой: '
    elif 'когда' in q: prefix='Сроки такие: '
    elif 'где' in q: prefix='Найденный раздел: '
    answer = prefix + body
    portals=[]
    for d in contexts:
        a=portal_action(d['title'])
        if a and a not in portals: portals.append(a)
    sources=[{'title':d['title'], 'section':d['section']} for d in contexts[:2]]
    return answer, sources, portals[:2]

def answer(login, question):
    emp=employee_by_login(login)
    if not emp:
        return {'ok':False,'answer':'Сначала войдите по табельному номеру или корпоративной почте.','sources':[],'portal':[]}
    contexts=search_context(question)
    text, sources, portals = generate_answer(emp, question, contexts)
    return {'ok':True,'answer':text,'sources':sources,'portal':portals,'debug':{'mode':'local_rag','contexts':[c['title'] for c in contexts]}}

MANIFEST={'name':'HR Compass 1221Systems','short_name':'HR Compass','start_url':'/mobile','display':'standalone','background_color':'#09111f','theme_color':'#7c3aed','icons':[]}

INDEX_HTML = r'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HR Compass</title><link rel="manifest" href="/manifest.json"><style>
:root{--bg:#07111f;--panel:rgba(255,255,255,.08);--panel2:rgba(255,255,255,.13);--txt:#edf6ff;--muted:#9fb0ca;--accent:#7048ff;--accent2:#06b6d4;--border:rgba(255,255,255,.14);--field:rgba(0,0,0,.22);--shadow:rgba(0,0,0,.32);--source-bg:rgba(52,211,153,.13);--source-border:rgba(52,211,153,.34);--source-text:#d9fff0;--source-link:#7dd3fc;--card:#111c31;--danger:#fb7185}body.light{--bg:#f4f7fb;--panel:rgba(255,255,255,.86);--panel2:#fff;--txt:#0f172a;--muted:#526178;--border:rgba(15,23,42,.12);--field:#fff;--shadow:rgba(15,23,42,.13);--source-bg:#ecfdf8;--source-border:#8bdcc6;--source-text:#0f5f4f;--source-link:#087966;--card:#fff;--danger:#dc2626}*{box-sizing:border-box}body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;color:var(--txt);min-height:100vh;background:radial-gradient(circle at 10% 0%,rgba(112,72,255,.22),transparent 34%),radial-gradient(circle at 90% 8%,rgba(6,182,212,.18),transparent 30%),linear-gradient(135deg,var(--bg),#0b1530);transition:.25s}.wrap{max-width:1230px;margin:auto;padding:24px}.glass{background:linear-gradient(135deg,var(--panel2),var(--panel));border:1px solid var(--border);box-shadow:0 28px 80px var(--shadow);border-radius:30px;backdrop-filter:blur(18px)}.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;align-items:stretch}.heroLeft,.login{padding:30px}.brand,.mascot,.profileHero{display:flex;gap:13px;align-items:center}.logo,.botface{width:54px;height:54px;border-radius:18px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:grid;place-items:center;font-size:27px;color:#fff}.botface{background:#fff;color:#172554}.brandTitle{font-size:22px;font-weight:900}.brandSub,.hint{color:var(--muted);font-size:14px;line-height:1.45}.heroTitle{font-size:58px;line-height:1.02;margin:34px 0 18px}.heroText{font-size:21px;line-height:1.55;color:var(--muted);max-width:720px}.badges{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}.badge,.chip{padding:11px 14px;border-radius:999px;background:var(--panel);border:1px solid var(--border);color:var(--txt);font-weight:650}.tabs,.kpi{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:18px 0}.tab,.q,.navBtn{border:1px solid var(--border);border-radius:15px;background:var(--panel);color:var(--txt);padding:12px;cursor:pointer;font-weight:750}.tab.active,.navBtn.active{background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;border:0}.field{width:100%;padding:16px 18px;border-radius:18px;border:1px solid var(--border);background:var(--field);color:var(--txt);font-size:16px;outline:none}.field::placeholder{color:var(--muted)}.btn{border:0;padding:15px 18px;border-radius:18px;background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;font-weight:900;cursor:pointer}.btn.secondary{background:var(--panel);color:var(--txt);border:1px solid var(--border)}.row{display:flex;gap:10px;align-items:center}.app{display:none;margin-top:22px;grid-template-columns:330px 1fr;gap:22px}.side{padding:18px}.profileBox,.upload,.docCard,.mini{padding:16px;border-radius:22px;background:var(--panel);border:1px solid var(--border)}.avatar{width:62px;height:62px;border-radius:22px;background:linear-gradient(135deg,#10b981,#06b6d4);display:grid;place-items:center;font-size:29px;margin-bottom:10px}.kpi{grid-template-columns:1fr 1fr}.kpi div{padding:13px;border-radius:18px;background:var(--panel);border:1px solid var(--border)}.kpi b{font-size:23px}.nav{display:grid;gap:8px;margin:14px 0}.view{display:none}.view.active{display:block}.main{min-height:720px;overflow:hidden}.top{display:flex;justify-content:space-between;align-items:center;padding:17px 20px;border-bottom:1px solid var(--border)}.msgs{height:585px;overflow:auto;padding:20px;display:flex;flex-direction:column;gap:14px}.msg{max-width:82%;padding:15px 17px;border-radius:20px;line-height:1.5;white-space:pre-wrap}.user{align-self:flex-end;background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;border-bottom-right-radius:6px}.bot{align-self:flex-start;background:var(--card);border:1px solid var(--border);color:var(--txt);border-bottom-left-radius:6px}.sources{margin-top:12px;display:grid;gap:8px}.source{font-size:13px;background:var(--source-bg);border:1px solid var(--source-border);border-radius:12px;padding:9px;color:var(--source-text)}.source b{color:var(--source-text)}.source a{color:var(--source-link);font-weight:900;text-decoration:underline}.input{display:flex;gap:10px;padding:18px;border-top:1px solid var(--border)}.questions{display:grid;gap:8px;margin-top:12px}.profileGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:20px}.profileItem{padding:15px;border-radius:20px;background:var(--card);border:1px solid var(--border)}.profileItem span{display:block;color:var(--muted);font-size:12px;margin-bottom:7px}.profileItem b{color:var(--txt)}.docList{display:grid;gap:12px;padding:20px}.themeSwitch{position:fixed;right:18px;top:18px;z-index:20;display:flex;gap:8px;align-items:center;padding:9px 12px;border-radius:999px;background:var(--panel2);border:1px solid var(--border);color:var(--txt);cursor:pointer;font-weight:900;box-shadow:0 12px 30px var(--shadow)}a{color:var(--source-link)}h1,h2,h3,b,strong{color:var(--txt)}body.light{background:radial-gradient(circle at 10% 0%,rgba(112,72,255,.13),transparent 34%),radial-gradient(circle at 90% 8%,rgba(6,182,212,.11),transparent 30%),linear-gradient(135deg,#f4f7fb,#eef2ff)}body.light .botface{background:#eef2ff;color:#172554}.mobile .wrap{padding:12px}.mobile .hero{grid-template-columns:1fr}.mobile .heroLeft{display:none}.mobile .app{grid-template-columns:1fr}.mobile .side{display:none}.mobile .main{min-height:calc(100vh - 24px);border-radius:28px}.mobile .msgs{height:calc(100vh - 160px)}.mobile .msg{max-width:92%}@media(max-width:900px){.hero,.app{grid-template-columns:1fr}.heroTitle{font-size:40px}.heroText{font-size:17px}.profileGrid{grid-template-columns:1fr}.main{min-height:650px}}
</style></head><body><button class="themeSwitch" onclick="toggleTheme()"><span id="themeIcon">🌙</span><b id="themeText">Тёмная</b></button><div class="wrap"><section id="landing" class="hero"><div class="heroLeft glass"><div class="brand"><div class="logo">🧭</div><div><div class="brandTitle">HR Compass</div><div class="brandSub">Локальный HR-ассистент для 1221Systems</div></div></div><h1 class="heroTitle">Ваш HR-помощник в одном окне</h1><p class="heroText">Помогает сотрудникам быстро получать ответы по отпускам, зарплате, ДМС, кадровым вопросам и внутренним регламентам компании.</p><p class="heroText">Бот определяет сотрудника по табельному номеру или корпоративной почте, учитывает профиль и показывает источник ответа.</p><div class="badges"><span class="badge">Профиль сотрудника</span><span class="badge">Документы и источники</span><span class="badge">Web + Mobile</span><span class="badge">Локально без внешних API</span></div></div><div class="login glass"><div class="mascot"><div class="botface">🤖</div><div><h2 style="margin:0">Вход в HR Compass</h2><div class="hint">Введите табельный номер или корпоративную почту</div></div></div><div class="tabs"><button class="tab active" onclick="fillLogin('work@portal-test.1221systems.ru',this)">Сотрудник</button><button class="tab" onclick="fillLogin('dir@portal-test.1221systems.ru',this)">Руководитель</button><button class="tab" onclick="fillLogin('hr@portal-test.1221systems.ru',this)">HR</button></div><input id="login" class="field" placeholder="Табельный номер или корпоративная почта"><div class="row" style="margin-top:12px"><button class="btn" onclick="doLogin()">Войти</button><button class="btn secondary" onclick="demo()">Демо</button></div><p class="hint">Демо: 1001 / work@portal-test.1221systems.ru, 2001 / dir@portal-test.1221systems.ru, 3001 / hr@portal-test.1221systems.ru</p><div id="loginErr" class="hint" style="color:var(--danger)"></div></div></section><section id="app" class="app"><aside class="side glass"><div class="profileBox"><div class="avatar">👤</div><h2 id="pname" style="margin:0"></h2><div id="prole" class="hint"></div><div class="kpi"><div><b id="vacDays">—</b><span class="hint">дней отпуска</span></div><div><b id="tabNo">—</b><span class="hint">табельный</span></div></div><p class="hint" id="nearest"></p></div><div class="nav"><button class="navBtn active" onclick="showView('chat',this)">Чат</button><button class="navBtn" onclick="showView('profile',this)">Профиль</button><button class="navBtn" onclick="showView('docs',this)">Документы</button></div><h3>Быстрые вопросы</h3><div class="questions" id="quick"></div></aside><main class="main glass"><div class="top"><div class="mascot"><div class="botface">🧭</div><div><b>HR Compass Agent</b><div class="hint">Локальный RAG: поиск → профиль → ответ → источник</div></div></div><div class="row"><button class="btn secondary" onclick="showView('profile')">Профиль</button><button class="btn secondary" onclick="logout()">Выйти</button></div></div><div id="view-chat" class="view active"><div id="msgs" class="msgs"></div><div class="input"><input id="q" class="field" placeholder="Например: Сколько у меня дней отпуска?" onkeydown="if(event.key==='Enter')send()"><button class="btn" onclick="send()">Отправить</button></div></div><div id="view-profile" class="view"><div class="profileGrid" id="profileGrid"></div></div><div id="view-docs" class="view"><div class="docList"><div class="upload"><h2 style="margin-top:0">Локальная база знаний</h2><p class="hint">Загрузите TXT/MD/CSV/PDF/DOCX. Текстовые файлы сразу участвуют в поиске. PDF/DOCX сохраняются локально как источник, в промышленной версии подключается локальный парсер.</p><input type="file" id="file"><button class="btn secondary" style="margin-top:10px" onclick="uploadFile()">Загрузить документ</button><div id="uploadStatus" class="hint"></div></div><div id="docsList"></div></div></div></main></section></div><script>
function applyTheme(t){document.body.classList.toggle('light',t==='light');localStorage.setItem('hr_compass_theme',t);themeIcon.textContent=t==='light'?'☀️':'🌙';themeText.textContent=t==='light'?'Светлая':'Тёмная'}function toggleTheme(){applyTheme(document.body.classList.contains('light')?'dark':'light')}applyTheme(localStorage.getItem('hr_compass_theme')||'dark');let current=null;const quick=['Сколько у меня дней отпуска?','Как мне перенести отпуск?','Когда аванс?','Где скачать расчетный лист?','Куда нести справку?','Какие программы ДМС есть?','Как оформить заказ в магазине мерча?','Как порекомендовать друга на вакансию?','Когда день рождения Иванова?','Как оформить стажировку?','Можно ли взять корпоративную сим-карту?'];async function api(path,data){let r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data||{})});return await r.json()}function fillLogin(v,b){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));if(b)b.classList.add('active');login.value=v}function demo(){login.value='work@portal-test.1221systems.ru';doLogin()}async function doLogin(){let res=await api('/api/login',{login:login.value.trim()});if(!res.ok){loginErr.textContent=res.error;return}current=res.employee;landing.style.display='none';app.style.display='grid';pname.textContent=current.name;prole.textContent=current.role+' • '+current.department;vacDays.textContent=current.vacation_days;tabNo.textContent=current.tab;nearest.textContent='Ближайший отпуск: '+current.nearest_vacation;quickEl();renderProfile();await loadDocs();msgs.innerHTML='';bot('Здравствуйте, '+current.name+'! Я работаю по локальной базе знаний и вашему профилю. 💡 Напишите мне вопрос — помогу с отпуском, авансом, справками, ДМС и обращением в HR. В конце ответа покажу источник.')}function quickEl(){quick.forEach(x=>{let b=document.createElement('button');b.className='q';b.textContent=x;b.onclick=()=>ask(x);document.getElementById('quick').appendChild(b)})}function showView(name,btn){document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));document.getElementById('view-'+name).classList.add('active');document.querySelectorAll('.navBtn').forEach(b=>b.classList.remove('active'));if(btn)btn.classList.add('active')}function renderProfile(){let items=[['ФИО',current.name],['Табельный номер',current.tab],['Почта',current.email],['Телефон',current.phone],['Роль',current.role],['Должность',current.position],['Подразделение',current.department],['Руководитель',current.manager],['График',current.schedule],['Дата приема',current.hire_date],['Кадровый инспектор',current.inspector],['Остаток отпуска',current.vacation_days+' дней'],['Ближайший отпуск',current.nearest_vacation],['Льготы',current.benefits]];profileGrid.innerHTML=items.map(i=>`<div class="profileItem"><span>${esc(i[0])}</span><b>${esc(i[1])}</b></div>`).join('')}function logout(){location.reload()}function ask(t){q.value=t;send()}function esc(s){return (s||'').toString().replace(/[&<>\"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]))}function add(text,cls,meta){let box=document.createElement('div');box.className='msg '+cls;box.innerHTML=esc(text);if(meta&&meta.sources){let s=document.createElement('div');s.className='sources';s.innerHTML=(meta.sources||[]).map(x=>`<div class="source"><b>Основание:</b> ${esc(x.section)} — ${esc(x.title)}</div>`).join('')+(meta.portal||[]).map(x=>`<div class="source">🔗 <a href="${esc(x.url)}" target="_blank">${esc(x.label)}</a></div>`).join('');box.appendChild(s)}msgs.appendChild(box);box.scrollIntoView({behavior:'smooth'})}function bot(t,m){add(t,'bot',m)}function user(t){add(t,'user')}async function send(){let text=q.value.trim();if(!text||!current)return;user(text);q.value='';let res=await api('/api/ask',{login:current.email,question:text});setTimeout(()=>bot(res.answer,res),220)}async function uploadFile(){let f=file.files[0];if(!f){uploadStatus.textContent='Выберите файл';return}let fd=new FormData();fd.append('file',f);let r=await fetch('/api/upload',{method:'POST',body:fd});let j=await r.json();uploadStatus.textContent=j.message;await loadDocs()}async function loadDocs(){let r=await fetch('/api/docs');let j=await r.json();docsList.innerHTML=j.docs.map(d=>`<div class="docCard"><b>${esc(d.title)}</b><div class="hint">${esc(d.section)} • ${esc(d.kind)}</div></div>`).join('')}if(location.pathname==='/mobile')document.body.classList.add('mobile');
</script></body></html>'''

PORTAL_PAGES = {
 '/portal/support':('Создать обращение в HR','Здесь сотрудник описывает вопрос, выбирает тему и прикладывает документ. В демо это локальная страница, чтобы не отправлять пользователя на пустой внешний сайт.'),
 '/portal/vacation':('Мой отпуск','Остаток отпуска, ближайшие даты и заявление на перенос отпуска.'),
 '/portal/payslips':('Расчетные листы','Выбор месяца и скачивание расчетного листа в PDF.'),
 '/portal/documents':('Загрузить документ','Передача справки, ЭЛН или подтверждающего документа кадровому инспектору.'),
 '/portal/dms':('Кафетерий льгот — ДМС','Доступные программы ДМС, условия участия и описание пакетов.'),
 '/portal/merch':('Магазин мерча','Каталог корпоративного мерча, выбор размера и оформление заказа.'),
 '/portal/referral':('Реферальная программа','Форма рекомендации кандидата на вакансию.'),
 '/portal/team':('Команда','Кадровые заявки руководителя, стажировки и материальная ответственность.'),
 '/portal/profile':('Профиль сотрудника','Карточка сотрудника: табельный номер, почта, руководитель, график и льготы.')
}

def portal_page(title, text):
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>body{{font-family:Arial,sans-serif;background:#f4f7fb;color:#0f172a;margin:0;padding:40px}}.card{{max-width:760px;margin:auto;background:white;border:1px solid #e2e8f0;border-radius:28px;padding:30px;box-shadow:0 20px 50px rgba(15,23,42,.12)}}a{{color:#2563eb}}</style></head><body><div class="card"><h1>{html.escape(title)}</h1><p>{html.escape(text)}</p><p><b>Локальная демо-страница HR-портала.</b></p><a href="/">← Вернуться в HR Compass</a></div></body></html>'''.encode('utf-8')

class Handler(BaseHTTPRequestHandler):
    def send_json(self,obj,code=200):
        data=json.dumps(obj,ensure_ascii=False).encode('utf-8')
        self.send_response(code); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        path=urlparse(self.path).path
        if path in ['/', '/mobile']:
            data=INDEX_HTML.encode('utf-8'); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
        elif path=='/manifest.json': self.send_json(MANIFEST)
        elif path=='/api/docs':
            docs=[{'title':d['title'],'section':d['section'],'kind':'встроенная база'} for d in KB]+[{'title':d['title'],'section':d['section'],'kind':'загружено локально'} for d in uploaded_docs()]
            self.send_json({'ok':True,'docs':docs})
        elif path in PORTAL_PAGES:
            title,text=PORTAL_PAGES[path]; data=portal_page(title,text); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
        else: self.send_error(404)
    def do_POST(self):
        path=urlparse(self.path).path
        if path=='/api/upload':
            content_type=self.headers.get('content-type',''); length=int(self.headers.get('content-length','0') or 0); body=self.rfile.read(length) if length else b''
            m=re.search(r'boundary="?([^";]+)"?', content_type)
            if m and body:
                boundary=('--'+m.group(1)).encode('utf-8')
                for part in body.split(boundary):
                    if b'name="file"' not in part or b'filename=' not in part or b'\r\n\r\n' not in part: continue
                    header,payload=part.split(b'\r\n\r\n',1); payload=payload.rstrip(b'\r\n-')
                    nm=re.search(br'filename="([^"]*)"', header); filename='uploaded_document.txt'
                    if nm:
                        raw=nm.group(1)
                        for enc in ('utf-8','cp1251','latin-1'):
                            try: filename=raw.decode(enc); break
                            except Exception: pass
                    safe=re.sub(r'[^\w\.\-а-яА-Я ]+','_',filename).strip() or 'uploaded_document.txt'
                    with open(os.path.join(UPLOADS,safe),'wb') as f: f.write(payload)
                    self.send_json({'ok':True,'message':'Документ загружен локально и добавлен в базу знаний: '+safe}); return
            self.send_json({'ok':False,'message':'Файл не получен'},400); return
        length=int(self.headers.get('content-length','0') or 0); raw=self.rfile.read(length).decode('utf-8') if length else '{}'
        try: data=json.loads(raw)
        except Exception: data={}
        if path=='/api/login':
            emp=employee_by_login(data.get('login','')); self.send_json({'ok':bool(emp),'employee':emp,'error':None if emp else 'Сотрудник не найден. Введите табельный номер или корпоративную почту.'})
        elif path=='/api/ask': self.send_json(answer(data.get('login',''),data.get('question','')))
        else: self.send_error(404)

def main():
    print('HR Compass 1221Systems RAG APP запущен локально')
    print('Web:    http://127.0.0.1:8000')
    print('Mobile: http://127.0.0.1:8000/mobile')
    ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
if __name__=='__main__': main()
