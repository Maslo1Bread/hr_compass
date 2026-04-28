const $ = id => document.getElementById(id);
const logo = 'assets/robot-logo.svg';
const defaultUsers = [
    {
        id: '101',
        tab: '101',
        email: 'work@portal-test.1221systems.ru',
        password: 'password123',
        role: 'employee',
        fullName: 'Иван Иванов',
        firstName: 'Иван',
        lastName: 'Иванов',
        aliases: ['иван', 'ивана', 'ивану', 'иванов', 'иванова', 'иванову', 'ивановым', 'иванове'],
        vacationDays: 21,
        vacationTotalDays: 28,
        vacationStart: '03.08.2026',
        vacationEnd: '16.08.2026',
        birthday: null,
        children: null,
        isHR: false
    },
    {
        id: '102',
        tab: '102',
        email: 'hr@portal-test.1221systems.ru',
        password: 'password123',
        role: 'hr',
        fullName: 'Мария Директорова',
        firstName: 'Мария',
        lastName: 'Директорова',
        aliases: ['мария', 'марии', 'марию', 'директорова', 'директоровой', 'директорову', 'директоровым', 'директорове'],
        vacationDays: 14,
        vacationTotalDays: 28,
        vacationStart: '',
        vacationEnd: '',
        birthday: '12.05',
        children: null,
        isHR: true
    },
    {
        id: '103',
        tab: '103',
        email: 'petrov@portal-test.1221systems.ru',
        password: 'password123',
        role: 'employee',
        fullName: 'Андрей Петров',
        firstName: 'Андрей',
        lastName: 'Петров',
        aliases: ['андрей', 'андрея', 'андрею', 'петров', 'петрова', 'петрову', 'петровым', 'петрове'],
        vacationDays: 0,
        vacationTotalDays: 28,
        vacationStart: '',
        vacationEnd: '',
        birthday: null,
        children: '3 ребенка (8, 12, 15 лет)',
        isHR: false
    },
    {
        id: '900',
        tab: '900',
        email: 'dir@portal-test.1221systems.ru',
        password: 'password123',
        role: 'manager',
        fullName: 'Ольга Руководитель',
        firstName: 'Ольга',
        lastName: 'Руководитель',
        aliases: ['ольга', 'руководитель', 'руководителя'],
        vacationDays: 28,
        vacationTotalDays: 28,
        vacationStart: '',
        vacationEnd: '',
        birthday: null,
        children: null,
        isHR: false
    }
];
const knowledgeBase = {
    vacation: {
        title: 'График отпусков 2026',
        summary: 'Персональный остаток отпуска и даты ближайшего отпуска.',
        path: '/docs/vacation-2026.pdf',
        example: 'Сколько у меня осталось дней отпуска?'
    },
    vacationTransfer: {
        title: 'ПВТР п.4.2 – перенос отпуска',
        summary: 'Перенос оформляется заявлением после согласования с руководителем и HR.',
        path: '/docs/pvtr.pdf#p4.2',
        example: 'Как перенести отпуск?'
    },
    sickLeave: {
        title: 'Положение об оплате больничных п.3.1',
        summary: 'Больничный оплачивается по электронному листку нетрудоспособности.',
        path: '/docs/sick-leave.docx#p3.1',
        example: 'Как оплачивается больничный?'
    },
    payslip: {
        title: 'Инструкция «Расчётный лист» п.2.1',
        summary: 'Расчётный лист скачивается в личном кабинете в разделе «Зарплата».',
        path: '/portal/payroll/payslip',
        example: 'Где скачать расчетный лист?'
    },
    merch: {
        title: 'Инструкция по мерчу – /merch',
        summary: 'Заказ мерча оформляется через раздел /merch с выбором товара и размера.',
        path: '/merch',
        example: 'Как заказать мерч?'
    },
    dms: {
        title: 'Положение о ДМС п.1.2 – 2 программы',
        summary: 'Доступны базовая и расширенная программы ДМС.',
        path: '/benefits/dms',
        example: 'Какие программы ДМС есть?'
    },
    referral: {
        title: 'Реферальная форма – /referral',
        summary: 'Рекомендация кандидата оформляется через форму /referral.',
        path: '/referral',
        example: 'Как порекомендовать друга?'
    },
    advance: {
        title: 'Положение об оплате труда п.5.1',
        summary: 'Аванс выплачивается 27 числа, зарплата — 12 числа следующего месяца.',
        path: '/docs/payroll-policy.docx#p5.1',
        example: 'Сколько дней до аванса?'
    },
    certificate: {
        title: 'Инструкция HR-отдела по кадровым документам п.2.3',
        summary: 'Справки передаются в HR лично, сканом или через внутреннюю форму.',
        path: '/docs/hr-documents.docx#p2.3',
        example: 'Куда нести справку?'
    },
    birthday: {
        title: 'Персональная карточка сотрудника',
        summary: 'Даты рождения берутся из карточек сотрудников локальной базы.',
        path: '/local/employees',
        example: 'Когда день рождения Директоровой?'
    },
    children: {
        title: 'Персональная карточка сотрудника',
        summary: 'Данные о детях берутся только из карточек сотрудников локальной базы.',
        path: '/local/employees',
        example: 'Сколько детей у Петрова?'
    },
    kedo: {
        title: 'Регламент КЭДО п.1.4',
        summary: 'Работник отправляет заявление, руководитель подписывает его в локальном кабинете.',
        path: '/docs/kedo-regulation.docx#p1.4',
        example: 'Отправить заявление на отпуск'
    },
    fallback: {
        title: 'Контакт HR-поддержки',
        summary: 'Если ответа нет в базе, вопрос передаётся HR.',
        path: 'mailto:hr@1221systems.ru',
        example: 'Написать в HR'
    }
};
const sourceKeys = ['vacation', 'vacationTransfer', 'dms', 'merch', 'referral', 'advance', 'certificate', 'kedo'];
const hrContact = 'hr@1221systems.ru';
let state, currentUser, selectedHrChat = null, currentTab = '';

function loadState() {
    try {
        state = JSON.parse(localStorage.getItem('hr1221State') || 'null')
    } catch (e) {
    }
    if (!state) {
        state = {users: defaultUsers, hrChats: {}, requests: {}, applications: [], botMessages: {}};
        saveState()
    }
    ensureState()
}

function ensureState() {
    state.users = state.users || [];
    state.hrChats = state.hrChats || {};
    state.requests = state.requests || {};
    state.applications = state.applications || [];
    state.botMessages = state.botMessages || {};
    // Мягкая миграция демо-пользователей: сохраняет созданных пользователей, но чинит обязательные демо-аккаунты.
    defaultUsers.forEach(seed => {
        let u = state.users.find(x => String(x.tab) === String(seed.tab) || normalize(x.email) === normalize(seed.email) || String(x.id) === String(seed.id));
        if (!u) {
            state.users.push({...seed});
            return;
        }
        Object.assign(u, {
            id: seed.id,
            tab: seed.tab,
            email: seed.email,
            password: seed.password,
            role: seed.role,
            isHR: seed.isHR,
            firstName: seed.firstName,
            lastName: seed.lastName
        });
        if (!u.fullName) u.fullName = seed.fullName;
        if (u.vacationDays === undefined || u.vacationDays === null) u.vacationDays = seed.vacationDays;
        if (!u.vacationTotalDays) u.vacationTotalDays = seed.vacationTotalDays;
        if (!u.vacationStart) u.vacationStart = seed.vacationStart;
        if (!u.vacationEnd) u.vacationEnd = seed.vacationEnd;
        if (!u.aliases || !u.aliases.length) u.aliases = seed.aliases;
        if (!u.birthday) u.birthday = seed.birthday;
        if (!u.children) u.children = seed.children;
    });
    state.users.forEach(u => {
        if (!u.id) u.id = u.tab;
        if (u.role === 'hr') u.isHR = true;
        if (!u.password) u.password = 'password123';
        if (!u.vacationTotalDays) u.vacationTotalDays = 28;
        if (!u.aliases) u.aliases = makeAliases(u.fullName || '');
        const info = getVacationInfo(u);
        if (info.start && info.end) {
            u.vacationDays = info.remainingDays;
        }
    });
    saveState();
}

function saveState() {
    localStorage.setItem('hr1221State', JSON.stringify(state))
}

function initials(n) {
    return (n || '??').split(' ').filter(Boolean).slice(0, 2).map(x => x[0]).join('').toUpperCase()
}

function normalize(t) {
    return String(t || '').toLowerCase().replace(/ё/g, 'е').replace(/[.,!?;:()«»"']/g, ' ').replace(/\s+/g, ' ').trim()
}

function makeAliases(name) {
    const n = normalize(name).split(' ');
    const arr = [...n];
    n.forEach(x => {
        arr.push(x + 'а', x + 'у', x + 'ой', x + 'ым', x + 'е')
    });
    return [...new Set(arr.filter(Boolean))]
}

function roleName(r) {
    return r === 'manager' ? 'Руководитель' : r === 'hr' ? 'HR' : 'Работник'
}

function roleHint() {
    return currentUser ? `${roleName(currentUser.role)} • локальный режим` : 'работает локально'
}

function dayWord(n) {
    n = Math.abs(Number(n));
    const last = n % 10;
    const lastTwo = n % 100;
    if (last === 1 && lastTwo !== 11) return 'день';
    if ([2, 3, 4].includes(last) && ![12, 13, 14].includes(lastTwo)) return 'дня';
    return 'дней';
}

function formatDateRu(date) {
    return date.toLocaleDateString('ru-RU', {day: '2-digit', month: '2-digit', year: 'numeric'});
}

function startOfDay(date) {
    return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

function diffDaysInclusive(start, end) {
    return Math.floor((startOfDay(end) - startOfDay(start)) / (1000 * 60 * 60 * 24)) + 1;
}

function daysBetween(from, to) {
    return Math.ceil((startOfDay(to) - startOfDay(from)) / (1000 * 60 * 60 * 24));
}

function parseVacationDate(value, fallbackYear) {
    const text = String(value || '').trim();
    if (!text) return null;
    const match = text.match(/^(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?$/);
    if (!match) return null;
    const day = Number(match[1]);
    const month = Number(match[2]) - 1;
    const year = Number(match[3]) || fallbackYear;
    const date = new Date(year, month, day);
    if (
        Number.isNaN(date.getTime()) ||
        date.getDate() !== day ||
        date.getMonth() !== month ||
        date.getFullYear() !== year
    ) return null;
    return startOfDay(date);
}

function getVacationPeriod(user) {
    if (!user?.vacationStart || !user?.vacationEnd) return null;
    const currentYear = new Date().getFullYear();
    let start = parseVacationDate(user.vacationStart, currentYear);
    if (!start) return null;
    let end = parseVacationDate(user.vacationEnd, start.getFullYear());
    if (!end) return null;
    if (!/\.\d{4}$/.test(String(user.vacationEnd || '').trim()) && end < start) {
        end = parseVacationDate(user.vacationEnd, start.getFullYear() + 1);
    }
    if (!end || end < start) return null;
    return {start, end};
}

function getVacationInfo(user, today = new Date()) {
    const period = getVacationPeriod(user);
    const totalDays = Number(user?.vacationTotalDays) || 28;
    const normalizedToday = startOfDay(today);
    if (!period) {
        return {
            totalDays,
            plannedDays: 0,
            remainingDays: Math.max(0, Number(user?.vacationDays) || totalDays),
            status: 'notScheduled',
            start: null,
            end: null
        };
    }
    const plannedDays = diffDaysInclusive(period.start, period.end);
    const remainingDays = Math.max(0, totalDays - plannedDays);
    if (normalizedToday < period.start) {
        return {
            totalDays,
            plannedDays,
            remainingDays,
            status: 'upcoming',
            daysUntilStart: daysBetween(normalizedToday, period.start),
            start: period.start,
            end: period.end
        };
    }
    if (normalizedToday > period.end) {
        return {
            totalDays,
            plannedDays,
            remainingDays,
            status: 'finished',
            daysAfterEnd: daysBetween(period.end, normalizedToday),
            start: period.start,
            end: period.end
        };
    }
    return {
        totalDays,
        plannedDays,
        remainingDays,
        status: 'active',
        dayNumber: diffDaysInclusive(period.start, normalizedToday),
        daysLeftIncludingToday: diffDaysInclusive(normalizedToday, period.end),
        start: period.start,
        end: period.end
    };
}

function adjustWeekendPayment(date) {
    const adjusted = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    if (adjusted.getDay() === 6) adjusted.setDate(adjusted.getDate() - 1);
    if (adjusted.getDay() === 0) adjusted.setDate(adjusted.getDate() - 2);
    return adjusted;
}

function getPaymentSchedule(fromDate = new Date()) {
    const base = startOfDay(fromDate);
    const candidates = [
        {type: 'salary', date: adjustWeekendPayment(new Date(base.getFullYear(), base.getMonth(), 12))},
        {type: 'advance', date: adjustWeekendPayment(new Date(base.getFullYear(), base.getMonth(), 27))},
        {type: 'salary', date: adjustWeekendPayment(new Date(base.getFullYear(), base.getMonth() + 1, 12))},
        {type: 'advance', date: adjustWeekendPayment(new Date(base.getFullYear(), base.getMonth() + 1, 27))},
        {type: 'salary', date: adjustWeekendPayment(new Date(base.getFullYear(), base.getMonth() + 2, 12))}
    ].sort((a, b) => a.date - b.date);
    const next = candidates.find(item => item.date >= base) || candidates[0];
    const days = Math.max(0, daysBetween(base, next.date));
    return {
        nextType: next.type,
        nextDate: next.date,
        daysUntilNext: days,
        advanceDate: candidates.find(item => item.type === 'advance' && item.date >= base)?.date || candidates[0].date,
        salaryDate: candidates.find(item => item.type === 'salary' && item.date >= base)?.date || candidates[candidates.length - 1].date
    };
}

function setProfile() {
    const shown = !!currentUser;
    $('profileCard').style.display = shown ? 'block' : 'none';
    if (!shown) return;
    $('profileAvatar').textContent = initials(currentUser.fullName);
    $('profileName').textContent = currentUser.fullName;
    $('profileMeta').textContent = `${currentUser.email} • таб. № ${currentUser.tab}`;
    $('profileRole').textContent = roleName(currentUser.role);
    $('profileVacation').textContent = getVacationInfo(currentUser).remainingDays ?? '—';
    $('profileTab').textContent = currentUser.tab;
    $('workspaceStatus').textContent = roleHint()
}

function renderSources() {
    const box = $('sourceTags');
    box.innerHTML = '';
    sourceKeys.forEach(k => {
        const b = document.createElement('button');
        b.className = 'tag';
        b.type = 'button';
        b.textContent = knowledgeBase[k].title.replace(' – ', ' — ');
        b.onclick = () => openSource(k);
        box.appendChild(b)
    })
}

function openSource(k) {
    const s = knowledgeBase[k];
    const d = $('sourceDetails');
    d.style.display = 'block';
    d.innerHTML = `<b>${s.title}</b><div>${s.summary}</div><div style="margin-top:8px">Путь: <a href="#">${s.path}</a></div><div style="margin-top:8px">Пример: «${s.example}»</div>`;
    if (currentUser?.role === 'employee') botReply(`Открываю локальный источник: ${s.title}\n\n${s.summary}\n\nПуть в демо-базе: ${s.path}\n\nМожете спросить: «${s.example}».`, s.title)
}

function login() {
    const login = normalize($('loginInput').value);
    const pass = $('passwordInput').value || '';
    const u = state.users.find(x => normalize(x.tab) === login || normalize(x.email) === login);
    if (!u || u.password !== pass) {
        $('loginError').textContent = 'Пользователь не найден или пароль неверный.';
        return
    }
    $('loginError').textContent = '';
    currentUser = u;
    setProfile();
    renderApp()
}

function logout() {
    currentUser = null;
    selectedHrChat = null;
    setProfile();
    $('content').innerHTML = '<div class="notice">Введите табельный номер или корпоративную почту слева, чтобы открыть нужную роль: работник, HR или руководитель.</div>';
    $('workspaceTitle').textContent = 'HR‑Ассистент 1221';
    $('workspaceStatus').textContent = 'работает локально'
}

$('loginBtn').onclick = login;
$('passwordInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') login()
});
$('loginInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') login()
});
$('logoutBtn').onclick = logout;
$('demoBtn').onclick = () => {
    $('loginInput').value = 'work@portal-test.1221systems.ru';
    $('passwordInput').value = 'password123'
};

function renderApp() {
    if (!currentUser) return logout();
    if (currentUser.role === 'manager') renderManager(); else if (currentUser.role === 'hr') renderHR(); else renderEmployee()
}

function setWorkspace(title) {
    $('workspaceTitle').textContent = title;
    $('workspaceStatus').textContent = roleHint()
}

function employeeTabs(active = 'bot') {
    currentTab = active;
    return `<div class="tabs"><button class="tab ${active === 'bot' ? 'active' : ''}" onclick="renderEmployee('bot')">HR‑бот</button><button class="tab ${active === 'hrchat' ? 'active' : ''}" onclick="renderEmployee('hrchat')">Чат с HR</button><button class="tab ${active === 'kedo' ? 'active' : ''}" onclick="renderEmployee('kedo')">КЭДО</button></div>`
}

function managerTabs(active = 'users') {
    return `<div class="tabs"><button class="tab ${active === 'users' ? 'active' : ''}" onclick="renderManager('users')">Работники</button><button class="tab ${active === 'register' ? 'active' : ''}" onclick="renderManager('register')">Регистрация</button><button class="tab ${active === 'docs' ? 'active' : ''}" onclick="renderManager('docs')">Подписание документов</button></div>`
}

function hrTabs(active = 'chats') {
    return `<div class="tabs"><button class="tab ${active === 'chats' ? 'active' : ''}" onclick="renderHR('chats')">Переписка</button><button class="tab ${active === 'users' ? 'active' : ''}" onclick="renderHR('users')">Работники</button><button class="tab ${active === 'register' ? 'active' : ''}" onclick="renderHR('register')">Регистрация</button></div>`
}

function renderEmployee(tab = 'bot') {
    setWorkspace('Кабинет работника');
    if (tab === 'bot') return renderEmployeeBot();
    if (tab === 'hrchat') return renderWorkerHrChat();
    if (tab === 'kedo') return renderWorkerKedo()
}

function renderEmployeeBot() {
    const messages = state.botMessages[currentUser.id] || [];
    let html = `${employeeTabs('bot')}<div class="chat-layout"><div class="messages" id="messages"></div><div class="quick" id="quick"></div><form class="composer" id="composer"><input class="field" id="questionInput" placeholder="Напишите вопрос HR‑Ассистенту 1221" autocomplete="off"><button class="btn send-btn" aria-label="Отправить"><span class="pixel-arrow"><i></i><i></i><i class="on"></i><i></i><i></i><i></i><i></i><i></i><i class="on"></i><i></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i><i></i><i class="on"></i><i></i><i></i><i></i><i class="on"></i><i></i><i></i></span></button></form></div>`;
    $('content').innerHTML = html;
    const box = $('messages');
    if (!messages.length) {
        botReply(`👋 Здравствуйте, ${currentUser.fullName}!\nЯ HR‑Ассистент 1221. Работаю локально и отвечаю по базе знаний HR.\nЧем могу помочь?\nНапример, вы можете спросить:\n• Сколько у меня дней отпуска?\n• Хочу в отпуск летом\n• Куда нести справку?\n• Сколько дней до аванса?\n• Как порекомендовать друга?`, 'Локальная база сотрудников 1221', false)
    } else messages.forEach(m => addChatBubble(box, m.role, m.text, m.source, false));
    renderQuick();
    $('composer').onsubmit = e => {
        e.preventDefault();
        askBot()
    };
    setTimeout(() => box.scrollTop = box.scrollHeight, 0)
}

function addChatBubble(box, role, text, source, store = true) {
    const row = document.createElement('div');
    row.className = `msg-row ${role}`;
    const av = document.createElement('div');
    av.className = 'msg-avatar';
    if (role === 'bot') {
        av.innerHTML = `<img src="${logo}" alt="бот">`
    } else av.textContent = initials(currentUser?.fullName || 'Я');
    const b = document.createElement('div');
    b.className = 'bubble';
    b.textContent = text;
    if (source) {
        const s = document.createElement('span');
        s.className = 'source';
        s.textContent = `Основание: ${source}`;
        b.appendChild(s)
    }
    row.append(av, b);
    box.appendChild(row);
    box.scrollTop = box.scrollHeight;
    if (store && currentUser?.role === 'employee') {
        state.botMessages[currentUser.id] = state.botMessages[currentUser.id] || [];
        state.botMessages[currentUser.id].push({role, text, source});
        saveState()
    }
}

function botReply(text, source, store = true) {
    const box = $('messages');
    if (!box) return;
    const typing = document.createElement('div');
    typing.className = 'msg-row bot';
    typing.innerHTML = `<div class="msg-avatar"><img src="${logo}" alt="бот"></div><div class="bubble"><span class="typing"><span></span><span></span><span></span></span></div>`;
    box.appendChild(typing);
    box.scrollTop = box.scrollHeight;
    setTimeout(() => {
        typing.remove();
        addChatBubble(box, 'bot', text, source, store)
    }, 220)
}

function renderQuick() {
    const q = ['Сколько у меня дней отпуска?', 'Остаток отпуска', 'Сколько дней до аванса?', 'Как оплачивается больничный?', 'Где скачать расчетный лист?', 'Вызвать HR'];
    const quick = $('quick');
    quick.innerHTML = '';
    q.forEach(x => {
        const b = document.createElement('button');
        b.type = 'button';
        b.textContent = x;
        b.onclick = () => {
            if (x === 'Вызвать HR') callHR(); else askBot(x)
        };
        quick.appendChild(b)
    });
    const hr = document.createElement('button');
    hr.className = 'btn dark small call-hr-btn';
    hr.textContent = 'Вызвать HR';
    hr.onclick = callHR;
    quick.appendChild(hr)
}

function askBot(text) {
    const input = $('questionInput');
    const q = (text || input.value).trim();
    if (!q) return;
    addChatBubble($('messages'), 'user', q, '');
    if (input) input.value = '';
    const r = answerQuestion(q);
    botReply(r.text, r.source, true);
    if (r.hrButton) {
        setTimeout(() => {
            const btn = document.createElement('button');
            btn.className = 'btn dark small call-hr-btn';
            btn.textContent = 'Вызвать HR';
            btn.onclick = callHR;
            const box = $('messages');
            const row = document.createElement('div');
            row.className = 'msg-row bot';
            row.innerHTML = `<div class="msg-avatar"><img src="${logo}"></div>`;
            const bub = document.createElement('div');
            bub.className = 'bubble';
            bub.textContent = 'Могу передать вопрос HR.';
            bub.appendChild(document.createElement('br'));
            bub.appendChild(btn);
            row.appendChild(bub);
            box.appendChild(row);
            box.scrollTop = box.scrollHeight
        }, 260)
    }
}

function findMentioned(text) {
    const n = normalize(text);
    return state.users.find(u => (u.aliases || []).some(a => a && n.includes(normalize(a))))
}

function has(t, arr) {
    return arr.some(x => t.includes(x))
}

function detectIntent(raw) {
    const t = normalize(raw);
    const hasVacation = t.includes('отпуск');
    const asksDays = /сколько|остат|остал|дн(ей|я|и)|мой/.test(t);
    if (/правил|порядок|срок|регламент|как выплачивается/.test(t) && /(аванс|зарплат|зп)/.test(t)) return 'advanceRules';
    if (has(t, ['сколько дней до аванс', 'сколько до аванс', 'через сколько аванс', 'до аванса', 'когда аванс', 'когда будет аванс', 'аванс', 'когда зарплата', 'когда зп', 'когда будет зарплата', 'когда будет зп', 'до зарплаты', 'через сколько зарплата', 'через сколько зп', 'зарплата', 'зп'])) return 'advanceDays';
    if (hasVacation && /всего|положено|за год|годовой/.test(t)) return 'vacationTotal';
    if (hasVacation && has(t, ['когда отпуск', 'когда у меня отпуск', 'я в отпуске', 'у меня сейчас отпуск', 'идет отпуск', 'иду в отпуск'])) return 'vacationStatus';
    if (hasVacation && asksDays) return 'vacationBalance';
    if (has(t, ['сколько у меня дней отпуска', 'сколько дней отпуска', 'остаток отпуска', 'сколько осталось отпуска', 'сколько отпуска', 'мой отпуск', 'дни отпуска'])) return 'vacationBalance';
    if (has(t, ['хочу в отпуск', 'летом в отпуск', 'отпуск летом'])) return 'vacationPlan';
    if (has(t, ['перенести отпуск', 'перенос отпуска'])) return 'transfer';
    if (has(t, ['день рождения', 'др коллег'])) return 'birthday';
    if (has(t, ['сколько детей', 'дети у', 'ребенок', 'ребенка', 'детей'])) return 'children';
    if (has(t, ['мерч', 'магазин мерча', 'заказать мерч'])) return 'merch';
    if (has(t, ['дмс', 'страховк', 'медицинск'])) return 'dms';
    if (has(t, ['порекомендовать друга', 'рефераль', 'рекомендовать друга', 'друга на вакансию'])) return 'referral';
    if (has(t, ['больничн', 'лист нетрудоспособности'])) return 'sickLeave';
    if (has(t, ['расчетный лист', 'расчетный листок', 'расчётный лист', 'где скачать'])) return 'payslip';
    if (has(t, ['справк', 'куда нести'])) return 'certificate';
    if (has(t, ['адаптац', 'новичк'])) return 'adaptation';
    if (has(t, ['реквизит'])) return 'requisites';
    if (has(t, ['график работ', 'режим работ'])) return 'schedule';
    if (has(t, ['оформить сотрудника', 'прием сотрудника', 'приём сотрудника'])) return 'hiring';
    if (has(t, ['стажировк'])) return 'internship';
    if (has(t, ['материальн'])) return 'liability';
    if (has(t, ['преми'])) return 'bonus';
    return 'unknown'
}

function answerQuestion(q) {
    const intent = detectIntent(q);
    const m = findMentioned(q);
    const src = k => knowledgeBase[k].title;
    switch (intent) {
        case'vacationTotal':
            {
                const info = getVacationInfo(currentUser);
                return {
                    text: `Всего по стандартному графику вам положено ${info.totalDays} календарных ${dayWord(info.totalDays)} отпуска в год.\nПо текущим датам отпуска остаток составляет ${info.remainingDays} ${dayWord(info.remainingDays)}.`,
                    source: src('vacation')
                };
            }
        case'vacationBalance':
            {
                const info = getVacationInfo(currentUser);
                let details = '';
                if (info.start && info.end) {
                    details = `\nЗапланированный отпуск: ${formatDateRu(info.start)} — ${formatDateRu(info.end)} (${info.plannedDays} ${dayWord(info.plannedDays)}).`;
                    if (info.status === 'active') {
                        details += `\nВы уже в отпуске. Сегодня ${info.dayNumber}-й день, осталось ${info.daysLeftIncludingToday} ${dayWord(info.daysLeftIncludingToday)} вместе с текущим днём.`;
                    } else if (info.status === 'upcoming') {
                        details += `\nДо начала отпуска осталось ${info.daysUntilStart} ${dayWord(info.daysUntilStart)}.`;
                    } else if (info.status === 'finished') {
                        details += '\nЭтот отпуск уже завершился.';
                    }
                }
                return {text: `У вас осталось ${info.remainingDays} ${dayWord(info.remainingDays)} отпуска.` + details, source: src('vacation')};
            }
        case'vacationStatus':
            {
                const info = getVacationInfo(currentUser);
                if (!info.start || !info.end) {
                    return {
                        text: 'В системе пока не указаны даты вашего отпуска. Если подскажете период или оформите его через HR/КЭДО, я смогу определить статус автоматически.',
                        source: src('vacation')
                    };
                }
                if (info.status === 'active') {
                    return {
                        text: `Вы уже в отпуске: ${formatDateRu(info.start)} — ${formatDateRu(info.end)}.\nСегодня ${info.dayNumber}-й день отпуска, осталось ${info.daysLeftIncludingToday} ${dayWord(info.daysLeftIncludingToday)} вместе с текущим днём.\nПосле этого периода у вас останется ${info.remainingDays} ${dayWord(info.remainingDays)}.`,
                        source: src('vacation')
                    };
                }
                if (info.status === 'upcoming') {
                    return {
                        text: `Ваш отпуск запланирован на ${formatDateRu(info.start)} — ${formatDateRu(info.end)}.\nДо начала осталось ${info.daysUntilStart} ${dayWord(info.daysUntilStart)}.\nПосле этого периода у вас останется ${info.remainingDays} ${dayWord(info.remainingDays)}.`,
                        source: src('vacation')
                    };
                }
                return {
                    text: `Последний указанный отпуск был на ${formatDateRu(info.start)} — ${formatDateRu(info.end)} и уже завершился.\nТекущий остаток отпуска: ${info.remainingDays} ${dayWord(info.remainingDays)}.`,
                    source: src('vacation')
                };
            }
        case'vacationPlan':
            return {
                text: 'Для отпуска летом нужно проверить доступные даты в графике и согласовать период с руководителем. Затем подайте заявление на перенос/планирование отпуска через КЭДО в этом кабинете. Если даты конфликтуют с графиком, вопрос согласует HR.',
                source: src('vacationTransfer')
            };
        case'transfer':
            return {
                text: 'Чтобы перенести отпуск: 1) согласуйте новые даты с руководителем; 2) подайте заявление через КЭДО; 3) дождитесь подписания руководителем и подтверждения HR. Если по документам нельзя ответить однозначно, обратитесь к инспектору по кадрам.',
                source: src('vacationTransfer')
            };
        case'birthday':
            if (!m) return {
                text: 'Уточните, пожалуйста, фамилию или имя коллеги. Например: «Когда день рождения Директоровой?»',
                source: src('birthday')
            };
            return {
                text: m.birthday ? `День рождения сотрудника ${m.fullName}: ${m.birthday}.` : `В локальной карточке сотрудника ${m.fullName} дата рождения не указана.`,
                source: src('birthday')
            };
        case'children':
            if (!m) return {
                text: 'Уточните, пожалуйста, фамилию сотрудника. Например: «Сколько детей у Петрова?»',
                source: src('children')
            };
            return {
                text: m.children ? `У сотрудника ${m.fullName}: ${m.children}.` : `В локальной базе нет подтверждённых данных о детях сотрудника ${m.fullName}. Я не буду подставлять данные из отпусков, зарплаты или карточек других сотрудников.`,
                source: src('children')
            };
        case'merch':
            return {
                text: 'Оформить заказ в магазине мерча можно в разделе /merch. Выберите товар, размер и количество, заполните форму заказа и отправьте заявку. После подтверждения HR сообщит статус, наличие и способ получения.',
                source: src('merch')
            };
        case'dms':
            return {
                text: 'Доступны 2 программы ДМС: базовая и расширенная. Базовая включает основные медицинские услуги, расширенная — увеличенный перечень клиник и дополнительных опций. Детали: «Кафетерий льгот» → «Программа ДМС».',
                source: src('dms')
            };
        case'referral':
            return {
                text: `Чтобы порекомендовать друга на вакансию, заполните форму /referral. Укажите ФИО и контакты кандидата, вакансию и короткий комментарий. Для дополнительных вопросов: ${hrContact}.`,
                source: src('referral')
            };
        case'advanceDays': {
            const info = getPaymentSchedule();
            const label = info.nextType === 'advance' ? 'аванс' : 'зарплата';
            return {
                text: `${info.daysUntilNext === 0 ? `${label === 'аванс' ? 'Аванс' : 'Зарплата'} сегодня.` : `До ближайшей выплаты (${label}) осталось ${info.daysUntilNext} ${dayWord(info.daysUntilNext)}.`}\nБлижайшая выплата: ${label} ${formatDateRu(info.nextDate)}.\nСледующий аванс: ${formatDateRu(info.advanceDate)}. Следующая зарплата: ${formatDateRu(info.salaryDate)}.\nЕсли дата выплаты выпадает на выходной, выплата переносится на предыдущий рабочий день.`,
                source: src('advance')
            }
        }
        case'advanceRules':
            return {
                text: 'По правилам аванс выплачивается 27 числа текущего месяца.\nЕсли дата выплаты приходится на выходной, выплата производится накануне.\nОкончательный расчёт заработной платы производится 12 числа следующего месяца.',
                source: src('advance')
            };
        case'sickLeave':
            return {
                text: 'Больничный оплачивается на основании электронного листка нетрудоспособности. Сообщите номер ЭЛН HR/бухгалтерии, чтобы данные проверили и передали в расчёт. Размер оплаты зависит от страхового стажа и действующего положения.',
                source: src('sickLeave')
            };
        case'payslip':
            return {
                text: 'Расчётный лист можно скачать во внутреннем личном кабинете в разделе «Зарплата» → «Расчётные листы». Выберите месяц и нажмите «Скачать PDF».',
                source: src('payslip')
            };
        case'certificate':
            return {
                text: `Справку или кадровый документ нужно передать в HR-отдел: лично, сканом или через внутреннюю форму обращения. Укажите табельный номер и тип документа. Для нестандартных справок напишите HR: ${hrContact}.`,
                source: src('certificate')
            };
        case'adaptation':
            return {
                text: 'Для адаптации нового сотрудника используйте памятку новичка: контакты HR, базовая информация о компании, график работы, реквизиты и внутренние разделы. Начните с проверки доступа к почте, порталу и личному кабинету.',
                source: 'Памятка нового сотрудника п.1.1'
            };
        case'requisites':
            return {
                text: 'Реквизиты компании размещены в карточке организации на внутреннем портале: юридический адрес, ИНН/КПП и банковские реквизиты.',
                source: 'Карточка организации на внутреннем портале'
            };
        case'schedule':
            return {
                text: 'Режим работы определяется ПВТР. Индивидуальные режимы и сменность фиксируются в трудовом договоре или дополнительном соглашении.',
                source: 'ПВТР п.3.1'
            };
        case'hiring':
            return {
                text: 'Для оформления сотрудника руководитель передаёт HR заявку на приём, данные кандидата, дату выхода и условия работы. HR проверяет документы, готовит трудовой договор и организует онбординг.',
                source: 'Регламент оформления сотрудников п.2.1'
            };
        case'internship':
            return {
                text: 'Стажировка оформляется через HR: руководитель согласует наставника, срок, задачи и критерии прохождения. По итогам фиксируется решение о дальнейшем оформлении или завершении стажировки.',
                source: 'Положение о стажировке п.1.3'
            };
        case'liability':
            return {
                text: 'Материальная ответственность оформляется только для ролей и задач, где это предусмотрено локальными документами. Нужен перечень имущества и договор/акт, подготовленный HR или ответственным подразделением.',
                source: 'Положение о материальной ответственности п.2.4'
            };
        case'bonus':
            return {
                text: 'Условия премирования зависят от роли, KPI и действующего положения о премировании. Для конкретной выплаты уточните период и тип премии.',
                source: 'Положение о премировании п.1.1'
            };
        default:
            return {
                text: `Я не нашёл точный ответ в локальной базе знаний и не буду выдумывать факты. Можно передать вопрос в HR: ${hrContact}.`,
                source: src('fallback'),
                hrButton: true
            }
    }
}

function callHR() {
    state.requests[currentUser.id] = {
        workerId: currentUser.id,
        createdAt: new Date().toISOString(),
        status: 'open'
    };
    state.hrChats[currentUser.id] = state.hrChats[currentUser.id] || [];
    state.hrChats[currentUser.id].push({
        from: 'system',
        text: `${currentUser.fullName} вызвал HR из кабинета работника.`,
        time: new Date().toISOString()
    });
    saveState();
    botReply('HR вызван. Я открыл отдельный чат с HR — история переписки будет сохранена локально.', 'Контакт HR-поддержки', true);
    setTimeout(() => renderEmployee('hrchat'), 500)
}

function renderWorkerHrChat() {
    setWorkspace('Чат с HR');
    $('content').innerHTML = `${employeeTabs('hrchat')}<div class="module" style="margin-top:16px;height:calc(100% - 58px);display:grid;grid-template-rows:auto 1fr auto"><div class="item-head"><div><h3>Переписка с HR</h3><div class="muted">История сохраняется в localStorage браузера.</div></div><div><button class="btn dark small call-hr-btn" onclick="callHRFromChat()">Вызвать HR</button> <button class="btn danger small call-hr-btn" onclick="clearWorkerHrChat()">Очистить чат с HR</button></div></div><div class="hr-messages" id="workerHrMessages"></div><form class="hr-composer" id="workerHrForm"><input class="field" id="workerHrInput" placeholder="Сообщение HR"><button class="btn">Отправить</button></form></div>`;
    renderWorkerHrMessages();
    $('workerHrForm').onsubmit = e => {
        e.preventDefault();
        const inp = $('workerHrInput');
        const text = inp.value.trim();
        if (!text) return;
        state.hrChats[currentUser.id] = state.hrChats[currentUser.id] || [];
        state.hrChats[currentUser.id].push({from: 'worker', text, time: new Date().toISOString()});
        state.requests[currentUser.id] = {
            workerId: currentUser.id,
            createdAt: new Date().toISOString(),
            status: 'open'
        };
        saveState();
        inp.value = '';
        renderWorkerHrMessages()
    }
}

function callHRFromChat() {
    state.requests[currentUser.id] = {
        workerId: currentUser.id,
        createdAt: new Date().toISOString(),
        status: 'open'
    };
    state.hrChats[currentUser.id] = state.hrChats[currentUser.id] || [];
    state.hrChats[currentUser.id].push({
        from: 'system',
        text: `${currentUser.fullName} повторно вызвал HR.`,
        time: new Date().toISOString()
    });
    saveState();
    renderWorkerHrMessages()
}

function renderWorkerHrMessages() {
    const box = $('workerHrMessages');
    if (!box) return;
    const arr = state.hrChats[currentUser.id] || [];
    box.innerHTML = arr.length ? '' : '<div class="notice">Пока сообщений нет. Нажмите «Вызвать HR» или напишите сообщение.</div>';
    arr.forEach(m => {
        const div = document.createElement('div');
        div.className = 'hr-msg ' + (m.from === 'worker' ? 'me' : 'them');
        div.textContent = (m.from === 'hr' ? 'HR: ' : m.from === 'system' ? 'Система: ' : 'Вы: ') + m.text;
        box.appendChild(div)
    });
    box.scrollTop = box.scrollHeight
}

function clearWorkerHrChat() {
    if (!confirm('Очистить историю чата с HR для этого работника?')) return;
    state.hrChats[currentUser.id] = [];
    state.requests[currentUser.id] = {
        workerId: currentUser.id,
        createdAt: new Date().toISOString(),
        status: 'open'
    };
    saveState();
    renderWorkerHrMessages()
}

function renderWorkerKedo() {
    setWorkspace('КЭДО работника');
    const apps = state.applications.filter(a => a.workerId === currentUser.id).sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    $('content').innerHTML = `${employeeTabs('kedo')}<div class="module-grid" style="margin-top:16px"><div class="module"><h3>Отправить заявление</h3><form class="kedo-form" id="kedoForm"><select class="field" id="kedoType"><option>Заявление на отпуск</option><option>Заявление на перенос отпуска</option><option>Заявление на справку</option><option>Заявление на увольнение</option><option>Другое заявление</option></select><textarea class="field" id="kedoText" placeholder="Текст заявления"></textarea><button class="btn">Отправить руководителю на подпись</button></form><div class="hint">Подписать заявление может только руководитель.</div></div><div class="module"><h3>Мои заявления</h3><div class="list">${apps.map(appCard).join('') || '<div class="notice">Заявлений пока нет.</div>'}</div></div></div>`;
    $('kedoForm').onsubmit = e => {
        e.preventDefault();
        const type = $('kedoType').value;
        const text = $('kedoText').value.trim();
        if (!text) return alert('Введите текст заявления');
        state.applications.push({
            id: 'app' + Date.now(),
            workerId: currentUser.id,
            workerName: currentUser.fullName,
            type,
            text,
            status: 'pending',
            createdAt: new Date().toISOString(),
            signedAt: null,
            signedBy: null
        });
        saveState();
        renderWorkerKedo()
    }
}

function appCard(a) {
    return `<div class="item"><div class="item-head"><b>${a.type}</b><span class="status ${a.status === 'signed' ? 'signed' : 'pending'}">${a.status === 'signed' ? 'подписано' : 'ожидает подписи'}</span></div><div style="margin-top:8px;white-space:pre-wrap">${escapeHtml(a.text)}</div><div class="muted" style="margin-top:8px">Отправлено: ${new Date(a.createdAt).toLocaleString('ru-RU')}${a.signedAt ? ` • Подписал: ${a.signedBy}, ${new Date(a.signedAt).toLocaleString('ru-RU')}` : ''}</div><span class="source">Основание: ${knowledgeBase.kedo.title}</span></div>`
}

function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, m => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }[m]))
}

function renderManager(tab = 'users') {
    setWorkspace('Кабинет руководителя');
    if (tab === 'users') return renderUsersPage('manager', 'users');
    if (tab === 'register') return renderRegisterPage('manager');
    if (tab === 'docs') return renderManagerDocs()
}

function renderHR(tab = 'chats') {
    setWorkspace('Кабинет HR');
    if (tab === 'chats') return renderHrChats();
    if (tab === 'users') return renderUsersPage('hr', 'users');
    if (tab === 'register') return renderRegisterPage('hr')
}

function renderUsersPage(role, tab) {
    const tabs = role === 'manager' ? managerTabs('users') : hrTabs('users');
    const rows = state.users.map(u => `<tr><td>${u.tab}</td><td>${escapeHtml(u.fullName)}<br><span class="muted">${roleName(u.role)}</span></td><td>${escapeHtml(u.email)}</td><td>${u.vacationDays}/${u.vacationTotalDays}</td><td>${u.vacationStart || '—'} — ${u.vacationEnd || '—'}</td><td>${u.role === 'hr' ? 'да' : 'нет'}</td><td><button class="btn small secondary" onclick="editUser('${u.id}','${role}')">Редактировать</button></td></tr>`).join('');
    $('content').innerHTML = `${tabs}<div class="module" style="margin-top:16px"><h3>Данные работников${role === 'manager' ? ' и HR' : ''}</h3><div class="table-wrap"><table class="data-table"><thead><tr><th>Таб.</th><th>ФИО / роль</th><th>Почта</th><th>Отпуск</th><th>Даты отпуска</th><th>HR</th><th></th></tr></thead><tbody>${rows}</tbody></table></div><div id="editBox" style="margin-top:16px"></div></div>`
}

function editUser(id, viewerRole) {
    const u = state.users.find(x => x.id === id);
    const canAssign = viewerRole === 'manager';
    $('editBox').innerHTML = `<div class="card"><h3>Редактирование: ${escapeHtml(u.fullName)}</h3><div class="form-grid"><input class="field" id="editFull" value="${escapeHtml(u.fullName)}" placeholder="ФИО"><input class="field" id="editEmail" value="${escapeHtml(u.email)}" placeholder="Почта"><input class="field" id="editPass" value="${escapeHtml(u.password)}" placeholder="Пароль"><input class="field" id="editVac" type="number" value="${u.vacationDays}" placeholder="Дни отпуска"><input class="field" id="editStart" value="${escapeHtml(u.vacationStart || '')}" placeholder="Дата начала отпуска"><input class="field" id="editEnd" value="${escapeHtml(u.vacationEnd || '')}" placeholder="Дата окончания отпуска">${canAssign ? `<select class="field full" id="editRole"><option value="employee" ${u.role === 'employee' ? 'selected' : ''}>Работник</option><option value="hr" ${u.role === 'hr' ? 'selected' : ''}>HR</option><option value="manager" ${u.role === 'manager' ? 'selected' : ''}>Руководитель</option></select>` : '<div class="notice full">HR может менять данные работников, но не может назначать HR или менять роль.</div>'}</div><div style="margin-top:12px"><button class="btn" onclick="saveUserEdit('${id}','${viewerRole}')">Сохранить</button></div></div>`
}

function saveUserEdit(id, viewerRole) {
    const u = state.users.find(x => x.id === id);
    u.fullName = $('editFull').value.trim();
    u.email = $('editEmail').value.trim();
    u.password = $('editPass').value.trim();
    u.vacationDays = Number($('editVac').value || 0);
    u.vacationStart = $('editStart').value.trim();
    u.vacationEnd = $('editEnd').value.trim();
    u.aliases = makeAliases(u.fullName);
    if (viewerRole === 'manager') {
        u.role = $('editRole').value;
        u.isHR = u.role === 'hr'
    }
    saveState();
    if (currentUser.id === u.id) currentUser = u;
    setProfile();
    viewerRole === 'manager' ? renderManager('users') : renderHR('users')
}

function renderRegisterPage(viewerRole) {
    const tabs = viewerRole === 'manager' ? managerTabs('register') : hrTabs('register');
    $('content').innerHTML = `${tabs}<div class="module" style="margin-top:16px"><h3>Регистрация пользователя</h3><div class="form-grid"><input class="field" id="regTab" placeholder="Табельный номер"><input class="field" id="regFull" placeholder="ФИО"><input class="field" id="regEmail" placeholder="Корпоративная почта"><input class="field" id="regPass" placeholder="Пароль" value="123456"><input class="field" id="regVac" type="number" placeholder="Дни отпуска" value="28"><input class="field" id="regStart" placeholder="Дата начала отпуска"><input class="field" id="regEnd" placeholder="Дата окончания отпуска">${viewerRole === 'manager' ? `<select class="field" id="regRole"><option value="employee">Работник</option><option value="hr">HR</option><option value="manager">Руководитель</option></select>` : '<div class="notice">Роль: работник. HR не может назначать HR.</div>'}</div><div style="margin-top:12px"><button class="btn" onclick="registerUser('${viewerRole}')">Зарегистрировать</button></div><div id="regMsg"></div></div>`
}

function registerUser(viewerRole) {
    const tab = $('regTab').value.trim(), full = $('regFull').value.trim(), email = $('regEmail').value.trim();
    if (!tab || !full || !email) {
        $('regMsg').innerHTML = '<div class="error">Заполните табельный номер, ФИО и почту.</div>';
        return
    }
    if (state.users.some(u => u.tab === tab || normalize(u.email) === normalize(email))) {
        $('regMsg').innerHTML = '<div class="error">Такой табельный номер или почта уже есть.</div>';
        return
    }
    const role = viewerRole === 'manager' ? $('regRole').value : 'employee';
    state.users.push({
        id: tab,
        tab,
        email,
        password: $('regPass').value || '123456',
        role,
        fullName: full,
        firstName: full.split(' ')[0] || full,
        lastName: full.split(' ')[1] || '',
        aliases: makeAliases(full),
        vacationDays: Number($('regVac').value || 0),
        vacationTotalDays: 28,
        vacationStart: $('regStart').value.trim(),
        vacationEnd: $('regEnd').value.trim(),
        birthday: null,
        children: null,
        isHR: role === 'hr'
    });
    saveState();
    $('regMsg').innerHTML = '<div class="ok">Пользователь зарегистрирован локально.</div>'
}

function renderManagerDocs() {
    const apps = state.applications.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    $('content').innerHTML = `${managerTabs('docs')}<div class="module" style="margin-top:16px"><h3>Окно подписания документов КЭДО</h3><div class="list">${apps.map(a => `<div class="item"><div class="item-head"><div><b>${escapeHtml(a.type)}</b><div class="muted">${escapeHtml(a.workerName)} • ${new Date(a.createdAt).toLocaleString('ru-RU')}</div></div><span class="status ${a.status === 'signed' ? 'signed' : 'pending'}">${a.status === 'signed' ? 'подписано' : 'ожидает подписи'}</span></div><div style="margin-top:8px;white-space:pre-wrap">${escapeHtml(a.text)}</div><span class="source">Основание: ${knowledgeBase.kedo.title}</span>${a.status !== 'signed' ? `<div style="margin-top:10px"><button class="btn small" onclick="signApp('${a.id}')">Подписать руководителем</button></div>` : `<div class="muted" style="margin-top:8px">Подписал: ${a.signedBy}, ${new Date(a.signedAt).toLocaleString('ru-RU')}</div>`}</div>`).join('') || '<div class="notice">Заявлений на подпись пока нет.</div>'}</div></div>`
}

function signApp(id) {
    const a = state.applications.find(x => x.id === id);
    a.status = 'signed';
    a.signedAt = new Date().toISOString();
    a.signedBy = currentUser.fullName;
    saveState();
    renderManager('docs')
}

function renderHrChats() {
    setWorkspace('Кабинет HR');
    const ids = Object.keys(state.requests);
    if (!selectedHrChat && ids.length) selectedHrChat = ids[0];
    $('content').innerHTML = `${hrTabs('chats')}<div class="hr-chat" style="margin-top:16px"><div class="chat-list" id="hrChatList"></div><div class="chat-panel"><div class="chat-panel-head"><div><b id="hrChatTitle">Выберите работника</b><div class="muted" id="hrChatSub"></div></div><button class="btn secondary small" onclick="closeHrRequest()">Закрыть обращение</button></div><div class="hr-messages" id="hrMessages"></div><form class="hr-composer" id="hrForm"><input class="field" id="hrInput" placeholder="Ответ работнику"><button class="btn">Отправить</button></form></div></div>`;
    renderHrChatList();
    renderHrMessages();
    $('hrForm').onsubmit = e => {
        e.preventDefault();
        if (!selectedHrChat) return;
        const inp = $('hrInput');
        const text = inp.value.trim();
        if (!text) return;
        state.hrChats[selectedHrChat] = state.hrChats[selectedHrChat] || [];
        state.hrChats[selectedHrChat].push({
            from: 'hr',
            text,
            time: new Date().toISOString(),
            hrName: currentUser.fullName
        });
        saveState();
        inp.value = '';
        renderHrMessages()
    }
}

function renderHrChatList() {
    const list = $('hrChatList');
    if (!list) return;
    const ids = Object.keys(state.requests);
    list.innerHTML = ids.length ? '' : '<div class="notice">Пока нет обращений от работников.</div>';
    ids.forEach(id => {
        const u = state.users.find(x => x.id === id);
        const b = document.createElement('button');
        b.className = 'chat-person ' + (selectedHrChat === id ? 'active' : '');
        b.innerHTML = `<b>${u ? escapeHtml(u.fullName) : id}</b><br><span class="muted">${state.hrChats[id]?.length || 0} сообщений</span>`;
        b.onclick = () => {
            selectedHrChat = id;
            renderHrChats()
        };
        list.appendChild(b)
    })
}

function renderHrMessages() {
    const box = $('hrMessages');
    if (!box) return;
    const u = state.users.find(x => x.id === selectedHrChat);
    $('hrChatTitle').textContent = u ? u.fullName : 'Выберите работника';
    $('hrChatSub').textContent = u ? `${u.email} • таб. № ${u.tab}` : '';
    const arr = state.hrChats[selectedHrChat] || [];
    box.innerHTML = selectedHrChat ? (arr.length ? '' : '<div class="notice">История пустая.</div>') : '<div class="notice">Выберите обращение слева.</div>';
    arr.forEach(m => {
        const div = document.createElement('div');
        div.className = 'hr-msg ' + (m.from === 'hr' ? 'me' : 'them');
        div.textContent = (m.from === 'hr' ? 'Вы: ' : m.from === 'worker' ? 'Работник: ' : 'Система: ') + m.text;
        box.appendChild(div)
    });
    box.scrollTop = box.scrollHeight
}

function closeHrRequest() {
    if (!selectedHrChat) return;
    delete state.requests[selectedHrChat];
    saveState();
    selectedHrChat = null;
    renderHrChats()
}

loadState();
renderSources();
logout();