#!/usr/bin/env python3
"""Build the bilingual static site. No runtime dependency on Python."""

from pathlib import Path
from html import escape
from urllib.parse import quote_plus
from format_html import format_html

ROOT = Path(__file__).resolve().parents[1]

COPY = {
    "uk": {
        "locale": "uk_UA", "label": "UA", "skip": "Перейти до вмісту",
        "nav": {"about": "Про майстра", "services": "Напрямки", "portfolio": "Портфоліо", "process": "Процес", "contact": "Контакти", "cta": "Обговорити проєкт"},
        "home": "Головна", "all_services": "Усі напрямки", "view": "Переглянути",
        "privacy": "Політика конфіденційності", "rights": "Усі права захищено.",
        "footer_text": "Мистецтво, ремесло й сучасні технології для індивідуальних проєктів.",
        "discuss": "Обговорити проєкт", "more": "Дізнатися більше", "works": "Переглянути роботи",
    },
    "en": {
        "locale": "en_US", "label": "EN", "skip": "Skip to content",
        "nav": {"about": "About", "services": "Disciplines", "portfolio": "Portfolio", "process": "Process", "contact": "Contact", "cta": "Discuss a project"},
        "home": "Home", "all_services": "All disciplines", "view": "View",
        "privacy": "Privacy policy", "rights": "All rights reserved.",
        "footer_text": "Art, craft and contemporary technology for individual projects.",
        "discuss": "Discuss a project", "more": "Learn more", "works": "View selected work",
    },
}

SERVICES = {
    "jewelry": {
        "image": "/assets/img/projects/jewelry-ear.webp",
        "card_image": "/assets/img/projects/jewelry-accent.webp",
        "uk": {
            "name": "Ювелірні вироби", "short": "Авторські прикраси, виразні форми та індивідуальний дизайн.",
            "intro": "Створення індивідуальних прикрас — від першої ідеї та ескізу до точної 3D-моделі й завершеного виробу.",
            "offers": [("Індивідуальний дизайн", "Прикраса розробляється навколо вашої ідеї, образу або символу."), ("Складні форми", "Опрацювання пластики, конструкції та дрібних деталей майбутнього виробу."), ("Поєднання матеріалів", "Метали, камені та інші акценти добираються відповідно до концепції."), ("Повний цикл", "Ескіз, 3D-модель, підготовка до виготовлення та фінішна обробка.")],
            "faq": [("Чи можна замовити прикрасу за власним ескізом?", "Так. Ескіз, референс або опис ідеї стане відправною точкою для обговорення."), ("Чи можна повторити показану роботу?", "Портфоліо демонструє підхід і можливості. Новий виріб узгоджується індивідуально з повагою до авторського задуму."), ("Як визначається вартість?", "Після уточнення матеріалів, конструкції, складності та обсягу робіт.")],
        },
        "en": {
            "name": "Jewellery", "short": "Signature jewellery, expressive forms and individual design.",
            "intro": "Individual jewellery created from an initial idea and sketch through a precise 3D model to a finished piece.",
            "offers": [("Individual design", "Each piece is developed around your idea, image or personal symbol."), ("Complex forms", "Careful development of form, construction and small details."), ("Material combinations", "Metals, stones and other accents are selected to serve the concept."), ("Complete process", "Sketching, 3D modelling, production preparation and finishing.")],
            "faq": [("Can I commission a piece from my own sketch?", "Yes. A sketch, reference or written idea can begin the discussion."), ("Can an existing work be reproduced?", "The portfolio demonstrates an approach and capabilities. Each new piece is discussed individually with respect for the original concept."), ("How is the price determined?", "After the materials, construction, complexity and scope have been clarified.")],
        },
    },
    "metal-casting": {
        "image": "/assets/img/process/process-cast.webp", "card_image": "/assets/img/projects/casting-boar.webp",
        "uk": {"name": "Лиття металів", "short": "Професійне лиття для прикрас, скульптур і декоративних елементів.", "intro": "Лиття художніх і функціональних об’єктів зі збереженням характеру форми та опрацьованих деталей.", "offers": [("Ювелірне лиття", "Підготовка та відливання деталей для індивідуальних прикрас."), ("Художні об’єкти", "Втілення скульптурних і декоративних форм у металі."), ("Майстер-моделі", "Робота з підготовленою моделлю або створення цифрової основи."), ("Фінішна обробка", "Шліфування, полірування та ручне доопрацювання за завданням.")], "faq": [("Які метали доступні?", "Перелік матеріалів уточнюється для конкретного проєкту."), ("Чи працюєте з одиничними виробами?", "Формат і доцільність виробництва визначаються після перегляду моделі та вимог."), ("Які потрібні файли?", "Надішліть наявні матеріали — вимоги до моделі узгодимо після оцінювання.")]},
        "en": {"name": "Metal casting", "short": "Professional casting for jewellery, sculpture and decorative elements.", "intro": "Casting artistic and functional objects while preserving the character of the form and its considered details.", "offers": [("Jewellery casting", "Preparation and casting of components for individual jewellery."), ("Art objects", "Realisation of sculptural and decorative forms in metal."), ("Master models", "Working from a prepared model or creating the digital foundation."), ("Finishing", "Grinding, polishing and manual refinement as required.")], "faq": [("Which metals are available?", "The material list is confirmed for each individual project."), ("Do you produce one-off pieces?", "The production format is determined after the model and requirements are reviewed."), ("Which files are required?", "Send the materials you have; model requirements will be agreed after assessment.")]},
    },
    "3d-printing": {
        "image": "/assets/img/process/process-print.webp", "card_image": "/assets/img/process/process-print.webp",
        "uk": {"name": "3D-друк", "short": "Майстер-моделі, прототипи, художні та технічні деталі.", "intro": "3D-друк допомагає перевірити форму, підготувати майстер-модель або виготовити деталь перед наступним виробничим етапом.", "offers": [("Прототипи", "Фізична перевірка масштабу, пропорцій і загальної конструкції."), ("Майстер-моделі", "Підготовка моделей для подальших виробничих процесів."), ("Художні форми", "Друк скульптурних, декоративних і складних геометричних об’єктів."), ("Технічні деталі", "Виготовлення деталей відповідно до погодженої цифрової моделі.")], "faq": [("Яку технологію друку ви використовуєте?", "Технологію та матеріал підбираємо після оцінювання моделі й призначення деталі."), ("Чи можна надрукувати готовий файл?", "Так, після перевірки геометрії та придатності файлу до друку."), ("Які максимальні розміри?", "Допустимий розмір і поділ моделі уточнюються для конкретного завдання.")]},
        "en": {"name": "3D printing", "short": "Master models, prototypes, artistic and technical parts.", "intro": "3D printing can test a form, produce a master model or create a part before the next production stage.", "offers": [("Prototypes", "Physical evaluation of scale, proportion and overall construction."), ("Master models", "Preparing models for subsequent production processes."), ("Artistic forms", "Printing sculptural, decorative and complex geometric objects."), ("Technical parts", "Producing parts from an approved digital model.")], "faq": [("Which printing technology do you use?", "Technology and material are selected after the model and intended use are assessed."), ("Can you print an existing file?", "Yes, after its geometry and print readiness have been checked."), ("What are the maximum dimensions?", "Size limits and possible model segmentation are discussed for each project.")]},
    },
    "3d-modeling": {
        "image": "/assets/img/process/process-model.webp", "card_image": "/assets/img/process/process-model.webp",
        "uk": {"name": "3D-моделювання", "short": "Цифрові моделі для прикрас, скульптур, деталей і макетів.", "intro": "Точне цифрове опрацювання форми для візуалізації, перевірки конструкції та підготовки до виробництва.", "offers": [("Ювелірні моделі", "Деталізована геометрія та посадкові місця відповідно до задуму."), ("Скульптурні форми", "Цифрова підготовка органічних і складних художніх об’єктів."), ("Архітектурні макети", "Опрацювання елементів споруд та масштабних композицій."), ("Підготовка до виробництва", "Перевірка геометрії з урахуванням обраного наступного процесу.")], "faq": [("Чи достатньо ескізу для початку?", "Так. Також корисні розміри, фотографії та референси бажаної форми."), ("У яких форматах передаєте модель?", "Формат погоджується відповідно до подальшого використання."), ("Чи можна замовити лише моделювання?", "Так, обсяг робіт і склад фінальних матеріалів узгоджуються перед початком.")]},
        "en": {"name": "3D modelling", "short": "Digital models for jewellery, sculpture, parts and scale models.", "intro": "Precise digital development for visualisation, construction review and production preparation.", "offers": [("Jewellery models", "Detailed geometry and stone settings developed around the concept."), ("Sculptural forms", "Digital preparation of organic and complex artistic objects."), ("Architectural models", "Developing structural elements and scaled compositions."), ("Production preparation", "Geometry reviewed for the selected next-stage process.")], "faq": [("Is a sketch enough to begin?", "Yes. Dimensions, photographs and references for the intended form are also useful."), ("Which file formats are supplied?", "The format is agreed according to its subsequent use."), ("Can I commission modelling only?", "Yes. The scope and final deliverables are agreed before work begins.")]},
    },
    "cnc-laser": {
        "image": "/assets/img/process/process-cnc.webp", "card_image": "/assets/img/projects/pavilion.webp",
        "uk": {"name": "ЧПК та лазерне гравіювання", "short": "Дерев’яні, інтер’єрні та декоративні елементи зі складним рисунком.", "intro": "Цифрова точність для декоративних панелей, деталей інтер’єру, меблевих елементів і авторських конструкцій.", "offers": [("ЧПК-обробка", "Фрезерування підготовлених форм і декоративних елементів."), ("Декоративні панелі", "Складні орнаменти та повторювані елементи для простору."), ("Інтер’єрні компоненти", "Індивідуальні деталі, фурнітура та авторські рішення."), ("Лазерне гравіювання", "Нанесення узгодженого рисунка або маркування на придатну поверхню.")], "faq": [("З якими матеріалами ви працюєте?", "Матеріал і його придатність потрібно підтвердити до розрахунку."), ("Чи підготуєте файл для ЧПК?", "Так, 3D-моделювання й виробнича підготовка можуть бути частиною проєкту."), ("Чи можливі великі конструкції?", "Конструкцію, розбиття на частини та монтаж потрібно оцінити індивідуально.")]},
        "en": {"name": "CNC & laser engraving", "short": "Wooden, interior and decorative elements with intricate patterns.", "intro": "Digital precision for decorative panels, interior details, furniture elements and custom structures.", "offers": [("CNC machining", "Milling prepared forms and decorative elements."), ("Decorative panels", "Intricate ornament and repeatable components for interiors."), ("Interior components", "Individual details, fittings and custom solutions."), ("Laser engraving", "Applying an agreed design or marking to a suitable surface.")], "faq": [("Which materials can you process?", "The material and its suitability must be confirmed before estimating."), ("Can you prepare the CNC file?", "Yes. 3D modelling and production preparation can be included in the project."), ("Are large structures possible?", "Construction, segmentation and installation must be assessed individually.")]},
    },
    "sculpture": {
        "image": "/assets/img/projects/mcgregor-sculpture.webp", "card_image": "/assets/img/projects/modern-object.webp",
        "uk": {"name": "Скульптури та художні об’єкти", "short": "Скульптура, авторські об’єкти, статуї та архітектурні моделі.", "intro": "Індивідуальні художні роботи — від камерного об’єкта до масштабної скульптури або моделі.", "offers": [("Портретна скульптура", "Опрацювання образу, характеру та пластики в обраному матеріалі."), ("Авторські об’єкти", "Унікальні форми для приватних колекцій, інтер’єрів і публічних просторів."), ("Моделі й макети", "Масштабні моделі транспорту, споруд та інших складних об’єктів."), ("Комбіновані техніки", "Поєднання ремесла, 3D-технологій і ручної фінішної роботи.")], "faq": [("Чи створюєте роботи за фотографіями?", "Вихідні матеріали й потрібна точність образу обговорюються до початку."), ("Чи працюєте з каменем і мармуром?", "Такі проєкти представлені в портфоліо; конкретний матеріал узгоджується окремо."), ("Чи можливий міжнародний проєкт?", "Так. Логістику, комунікацію та формат передачі роботи плануємо індивідуально.")]},
        "en": {"name": "Sculpture & art objects", "short": "Sculpture, commissioned art objects, statues and architectural models.", "intro": "Individual artworks ranging from intimate objects to large-scale sculpture or models.", "offers": [("Portrait sculpture", "Developing likeness, character and form in the selected material."), ("Original art objects", "Unique forms for private collections, interiors and public spaces."), ("Models and maquettes", "Scale models of vehicles, buildings and other complex objects."), ("Combined techniques", "Bringing together craft, 3D technology and manual finishing.")], "faq": [("Can you work from photographs?", "Source materials and the required level of likeness are discussed before work begins."), ("Do you work in stone and marble?", "Such projects are represented in the portfolio; the exact material is agreed separately."), ("Can you work internationally?", "Yes. Logistics, communication and delivery format are planned individually.")]},
    },
}

PROJECTS = {
    "wolf-pendant": {"image": "/assets/img/brand/hero-wolf.webp", "category": "jewelry", "gallery": ["/assets/img/brand/hero-wolf.webp", "/assets/img/projects/symbol-pendant.webp"], "uk": {"name": "Підвіс «Вовк»", "category_name": "Ювелірні вироби", "summary": "Складна ажурна форма з виразною пластикою та високою деталізацією.", "concept": "Образ вовка побудований на поєднанні впізнаваного силуету, наскрізної структури й ретельно опрацьованої поверхні.", "materials": "Метал; точний склад потребує уточнення", "technology": "Моделювання, лиття, ручна фінішна обробка"}, "en": {"name": "Wolf pendant", "category_name": "Jewellery", "summary": "An intricate openwork form with expressive modelling and fine detail.", "concept": "The wolf motif combines a recognisable silhouette, open structure and a carefully articulated surface.", "materials": "Metal; exact composition to be confirmed", "technology": "Modelling, casting and hand finishing"}},
    "expressive-jewelry": {"image": "/assets/img/projects/jewelry-ear.webp", "category": "jewelry", "gallery": ["/assets/img/projects/jewelry-ear.webp", "/assets/img/projects/jewelry-accent.webp", "/assets/img/projects/jewelry-minimal.webp"], "uk": {"name": "Виразні форми", "category_name": "Ювелірні вироби", "summary": "Серія прикрас, у яких смілива пластика формує впізнаваний образ.", "concept": "Скульптурний підхід перетворює прикрасу на самостійний акцент, зберігаючи увагу до посадки та деталей.", "materials": "Метал; окремі матеріали уточнюються", "technology": "Дизайн, 3D-моделювання та фінішна обробка"}, "en": {"name": "Expressive forms", "category_name": "Jewellery", "summary": "A series of pieces where bold sculptural form creates a distinctive image.", "concept": "A sculptural approach turns jewellery into a strong visual accent while retaining attention to fit and detail.", "materials": "Metal; individual materials to be confirmed", "technology": "Design, 3D modelling and finishing"}},
    "mcgregor-sculpture": {"image": "/assets/img/projects/mcgregor-sculpture.webp", "category": "sculpture", "gallery": ["/assets/img/projects/mcgregor-sculpture.webp", "/assets/img/projects/modern-object.webp"], "uk": {"name": "Скульптура Конора Макгрегора", "category_name": "Скульптура", "summary": "Кам’яна скульптура відомого MMA-бійця Конора Макгрегора.", "concept": "Монументальний образ поєднує портретну впізнаваність, опрацювання анатомії та деталі сценічного образу.", "materials": "Натуральний камінь", "technology": "Скульптурне моделювання та обробка каменю"}, "en": {"name": "Conor McGregor sculpture", "category_name": "Sculpture", "summary": "A stone sculpture of MMA fighter Conor McGregor.", "concept": "The monumental portrait combines recognisable likeness, anatomical study and detailed elements of the subject’s public image.", "materials": "Natural stone", "technology": "Sculptural modelling and stone work"}},
    "hammond-bust": {"image": "/assets/img/projects/hammond-bust.webp", "category": "sculpture", "gallery": ["/assets/img/projects/hammond-bust.webp", "/assets/img/projects/queen-bust.webp"], "uk": {"name": "Бюст Річарда Гаммонда", "category_name": "Портретна скульптура", "summary": "Бюст у камені для ведучого Top Gear Річарда Гаммонда.", "concept": "Портретна робота зосереджена на впізнаваності, характері та природній пластиці образу.", "materials": "Камінь", "technology": "Портретне моделювання та скульптурна обробка"}, "en": {"name": "Richard Hammond bust", "category_name": "Portrait sculpture", "summary": "A stone bust for Top Gear presenter Richard Hammond.", "concept": "The portrait focuses on likeness, character and natural sculptural modelling.", "materials": "Stone", "technology": "Portrait modelling and sculptural work"}},
    "architecture-model": {"image": "/assets/img/projects/architecture-model.webp", "category": "modeling", "gallery": ["/assets/img/projects/architecture-model.webp", "/assets/img/projects/marble-car.webp"], "uk": {"name": "Архітектурна модель", "category_name": "Моделі та макети", "summary": "Деталізований архітектурний макет зі складною вертикальною структурою.", "concept": "Масштабна модель передає пропорції споруди, ритм архітектурних елементів і декоративні акценти.", "materials": "Комбіновані матеріали", "technology": "3D-моделювання, виготовлення деталей і ручне складання"}, "en": {"name": "Architectural model", "category_name": "Models and maquettes", "summary": "A detailed architectural model with a complex vertical structure.", "concept": "The scale model conveys the building’s proportions, architectural rhythm and decorative accents.", "materials": "Combined materials", "technology": "3D modelling, component production and hand assembly"}},
    "decorative-pavilion": {"image": "/assets/img/projects/pavilion.webp", "category": "cnc", "gallery": ["/assets/img/projects/pavilion.webp", "/assets/img/projects/interior-detail.webp"], "uk": {"name": "Декоративний павільйон", "category_name": "ЧПК та декоративні конструкції", "summary": "Великоформатна конструкція зі складним наскрізним орнаментом.", "concept": "Архітектурна форма побудована на ритмі повторюваних декоративних елементів і тонкій деталізації панелей.", "materials": "Комбіновані матеріали", "technology": "Цифрова підготовка, ЧПК-обробка та складання"}, "en": {"name": "Decorative pavilion", "category_name": "CNC and decorative structures", "summary": "A large-scale structure with intricate openwork ornament.", "concept": "The architectural form is built around repeating decorative elements and finely detailed panels.", "materials": "Combined materials", "technology": "Digital preparation, CNC machining and assembly"}},
}

PROCESS_IMAGES = [
    ("process-sketch", "Ескіз", "Sketch"), ("process-model", "3D-модель", "3D model"),
    ("process-print", "3D-друк", "3D printing"), ("process-cast", "Відливання", "Casting"),
    ("process-hand", "Ручна обробка", "Hand finishing"), ("process-polish", "Полірування", "Polishing"),
]

def path_for(lang, section="", slug=""):
    parts = [lang]
    if section: parts.append(section)
    if slug: parts.append(slug)
    return "/" + "/".join(parts) + "/"

def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix == ".html":
        content = format_html(content)
    target.write_text(content, encoding="utf-8")

def contact_icon(kind):
    paths = {
        "email": '<path d="M3 6.5h18v12H3z"/><path d="m4 7 8 6 8-6"/>',
        "phone": '<path d="M8.1 3.5 5.6 4.7c-.8.4-1.2 1.3-1 2.2 1.4 6.2 6.3 11.1 12.5 12.5.9.2 1.8-.2 2.2-1l1.2-2.5-4.3-2-1.4 2c-3-1.2-5.5-3.6-6.7-6.7l2-1.4-2-4.3Z"/>',
        "telegram": '<path d="m3 11 18-7-4 16-6-5-3 3 .7-4.8L17 7l-10 5.2L3 11Z"/>',
    }
    return f'<svg class="contact-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</svg>'

def service_links(lang):
    return "".join(f'<a href="{path_for(lang, "services", slug)}">{escape(item[lang]["name"])}</a>' for slug, item in SERVICES.items())

def header(lang, alternate):
    c = COPY[lang]
    language_switch = (f'<span class="active">UA</span><span>/</span><a href="{alternate}">EN</a>' if lang == "uk"
                       else f'<a href="{alternate}">UA</a><span>/</span><span class="active">EN</span>')
    return f'''<a class="skip-link" href="#main">{c["skip"]}</a>
<header class="site-header"><div class="container nav">
  <a class="brand" href="/{lang}/" aria-label="Yevhenii Muradov — {c['home']}"><strong>YEVHENII MURADOV</strong><span>ART · CRAFT · DESIGN</span></a>
  <nav class="nav-links" id="site-nav" aria-label="Main navigation">
    <a href="/{lang}/">{c['home']}</a>
    <a href="/{lang}/about/">{c['nav']['about']}</a>
    <div class="dropdown"><button type="button" aria-expanded="false">{c['nav']['services']}</button><div class="dropdown-menu"><a href="/{lang}/services/"><strong>{c['all_services']}</strong></a>{service_links(lang)}</div></div>
    <a href="/{lang}/portfolio/">{c['nav']['portfolio']}</a><a href="/{lang}/process/">{c['nav']['process']}</a><a href="/{lang}/#contact">{c['nav']['contact']}</a>
    <div class="lang-switch" aria-label="Language">{language_switch}</div>
  </nav>
  <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Menu"><span></span><span></span></button>
</div></header>'''

def footer(lang):
    c = COPY[lang]
    return f'''<footer class="site-footer"><div class="container">
  <div class="footer-top"><div class="footer-brand"><a class="brand" href="/{lang}/"><strong>YEVHENII MURADOV</strong><span>ART · CRAFT · DESIGN</span></a><p>{c['footer_text']}</p></div>
  <nav class="footer-nav" aria-label="Footer"><a href="/{lang}/about/">{c['nav']['about']}</a><a href="/{lang}/services/">{c['nav']['services']}</a><a href="/{lang}/portfolio/">{c['nav']['portfolio']}</a><a href="/{lang}/process/">{c['nav']['process']}</a><a href="/{lang}/#contact">{c['nav']['contact']}</a><a href="/{lang}/privacy/">{c['privacy']}</a></nav>
  <div class="footer-contact"><a href="mailto:muradov.workk@gmail.com">{contact_icon('email')}<span>muradov.workk@gmail.com</span></a><a href="tel:+380994891881">{contact_icon('phone')}<span>+380 99 489 18 81</span></a><a href="https://t.me/Yevhenii_Muradov" rel="noopener" aria-label="Telegram @Yevhenii_Muradov">{contact_icon('telegram')}<span>@Yevhenii_Muradov</span></a></div></div>
  <div class="footer-bottom"><span>© <span data-year>2026</span> Yevhenii Muradov. {c['rights']}</span><span>ART · CRAFT · DESIGN</span></div>
</div></footer>'''

def project_modal(lang):
    uk = lang == "uk"
    return f'''<div class="project-modal" data-project-modal hidden>
  <div class="project-modal__backdrop" data-modal-close></div>
  <section class="project-modal__dialog" id="project-modal" role="dialog" aria-modal="true" aria-labelledby="project-modal-title" tabindex="-1">
    <button class="project-modal__close" type="button" data-modal-close aria-label="{'Закрити вікно' if uk else 'Close dialog'}">×</button>
    <div class="project-modal__heading"><p class="eyebrow">{'Обговорити проєкт' if uk else 'Discuss a project'}</p><h2 id="project-modal-title">{'Розкажіть про вашу ідею' if uk else 'Tell us about your idea'}</h2><p>{'Залиште контакти й коротко опишіть запит — ми зв’яжемося з вами для обговорення деталей.' if uk else 'Leave your details and briefly describe the enquiry — we will contact you to discuss the next steps.'}</p></div>
    <div class="project-modal__grid">
      <div class="project-modal__contacts"><h3>{'Контакти' if uk else 'Contact'}</h3><div class="contact-list"><a href="mailto:muradov.workk@gmail.com">{contact_icon('email')}<span>muradov.workk@gmail.com</span></a><a href="tel:+380994891881">{contact_icon('phone')}<span>+380 99 489 18 81</span></a><a href="https://t.me/Yevhenii_Muradov" rel="noopener" aria-label="Telegram @Yevhenii_Muradov">{contact_icon('telegram')}<span>@Yevhenii_Muradov</span></a></div></div>
      <form class="form-grid contact-form modal-form" action="/api/contact.php" method="post" data-contact-form novalidate>
        <div class="field field--full"><label class="visually-hidden" for="modal-name">{'Ім’я' if uk else 'Name'} *</label><input id="modal-name" name="name" required maxlength="80" autocomplete="name" placeholder="{'Ім’я' if uk else 'Name'}"></div>
        <div class="field field--full"><label class="visually-hidden" for="modal-phone">{'Телефон' if uk else 'Phone'} *</label><input id="modal-phone" name="contact" type="tel" required minlength="7" maxlength="24" inputmode="tel" autocomplete="tel" placeholder="{'Телефон' if uk else 'Phone'}"></div>
        <div class="field field--full"><label class="visually-hidden" for="modal-message">{'Ваше запитання' if uk else 'Your enquiry'} *</label><textarea id="modal-message" name="message" required minlength="10" maxlength="3000" placeholder="{'Ваше запитання' if uk else 'Your enquiry'}"></textarea></div>
        <div class="honeypot" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
        <div class="field field--full"><label class="checkbox"><input type="checkbox" name="consent" value="yes" required><span>{'Я погоджуюся на оброблення даних відповідно до' if uk else 'I agree to the processing of my data under the'} <a href="/{lang}/privacy/"><u>{COPY[lang]['privacy'].lower()}</u></a>.</span></label></div>
        <div class="field field--full form-actions"><button class="button button--dark contact-submit" type="submit"><span>{'Відправити' if uk else 'Send'}</span><span aria-hidden="true">→</span></button><p class="form-status" data-form-status role="status" aria-live="polite"></p></div>
      </form>
    </div>
  </section>
</div>'''

def layout(lang, title, description, content, alternate, scripts=None, body_class=""):
    scripts = scripts or []
    script_sources = list(dict.fromkeys(["/assets/js/main.js", "/assets/js/form.js", "/assets/js/modal.js", *scripts]))
    js = "".join(f'<script src="{src}" defer></script>' for src in script_sources)
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}"><meta name="theme-color" content="#111113">
<meta property="og:type" content="website"><meta property="og:locale" content="{COPY[lang]['locale']}"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:image" content="/assets/img/brand/hero-wolf.webp">
<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/css/styles.css">{js}</head><body class="{body_class}">{header(lang, alternate)}{content}{footer(lang)}{project_modal(lang)}</body></html>'''

def breadcrumb(lang, current):
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/{lang}/">{COPY[lang]["home"]}</a><span>•</span>{escape(current)}</nav>'

def cta(lang):
    title = "Маєте ідею? Перетворімо її на форму." if lang == "uk" else "Have an idea? Let’s give it form."
    text = "Розкажіть про задум, бажаний матеріал і контекст майбутнього виробу." if lang == "uk" else "Tell us about the idea, intended material and context for the future piece."
    return f'''<section class="section section--dark"><div class="container cta-panel reveal"><div><p class="eyebrow">YEVHENII MURADOV</p><h2>{title}</h2><p>{text}</p></div><a class="button" href="/{lang}/#contact" data-modal-open aria-haspopup="dialog" aria-controls="project-modal">{COPY[lang]['discuss']}</a></div></section>'''

def service_cards(lang):
    cards = []
    for i, (slug, item) in enumerate(SERVICES.items(), 1):
        d = item[lang]
        cards.append(f'''<a class="service-card reveal" href="{path_for(lang, 'services', slug)}"><img src="{item['card_image']}" alt="" loading="lazy"><div class="service-card-content"><span class="number">0{i}</span><h3>{d['name']}</h3><p>{d['short']}</p></div></a>''')
    return "".join(cards)

def project_cards(lang, limit=None):
    cards = []
    for i, (slug, item) in enumerate(PROJECTS.items()):
        if limit and i >= limit: break
        d = item[lang]; wide = " project-card--wide" if i in (0, 3) else ""
        cards.append(f'''<article class="project-card{wide} reveal" data-category="{item['category']}"><a href="{path_for(lang, 'portfolio', slug)}"><div class="project-card-media"><img src="{item['image']}" alt="{escape(d['name'])}" loading="lazy"></div><div class="project-card-meta"><div><small>{escape(d['category_name'])}</small><h3>{escape(d['name'])}</h3></div><span aria-hidden="true">↗</span></div></a></article>''')
    return "".join(cards)

def home(lang):
    uk = lang == "uk"
    title = "Мистецтво, що набуває форми" if uk else "Art, given form"
    content = f'''<main id="main">
<section class="hero"><div class="hero-media"><img src="/assets/img/brand/hero-wolf.webp" alt="{'Ажурний металевий підвіс у формі голови вовка' if uk else 'Openwork metal wolf-head pendant'}" fetchpriority="high"></div><div class="container"><div class="hero-content"><p class="eyebrow">ART · CRAFT · DESIGN</p><h1>{title}</h1><p class="hero-copy">{'Від авторської прикраси до масштабного арт-об’єкта — поєднуємо ремесло, точність і сучасні технології.' if uk else 'From signature jewellery to large-scale art objects — bringing together craft, precision and contemporary technology.'}</p><div class="hero-actions"><a class="button" href="/{lang}/portfolio/">{COPY[lang]['works']}</a><a class="button button--ghost" href="/{lang}/#contact" data-modal-open aria-haspopup="dialog" aria-controls="project-modal">{COPY[lang]['discuss']}</a></div></div></div><span class="hero-mark">YM</span></section>
<section class="section"><div class="container intro-grid reveal"><div><p class="eyebrow">{'Майстерня' if uk else 'The studio'}</p><p class="display">{'Ідея. Матеріал. Майстерність.' if uk else 'Idea. Material. Mastery.'}</p></div><div class="intro-copy"><p class="lede">{'Yevhenii Muradov створює унікальні прикраси, скульптури, моделі та художні об’єкти, поєднуючи ручну працю з цифровим проєктуванням.' if uk else 'Yevhenii Muradov creates unique jewellery, sculpture, models and art objects, combining hand craft with digital design.'}</p><p>{'Кожен проєкт починається з розуміння задуму. Форма, матеріал і технологія працюють разом, щоб результат мав власний характер.' if uk else 'Every project begins with understanding the idea. Form, material and technology work together so the result has a character of its own.'}</p><div class="fact-row"><div class="fact"><strong>01</strong><span>{'Індивідуальний підхід' if uk else 'Individual approach'}</span></div><div class="fact"><strong>02</strong><span>{'Ремесло й технології' if uk else 'Craft and technology'}</span></div><div class="fact"><strong>03</strong><span>{'Проєкти без шаблонів' if uk else 'Projects without templates'}</span></div></div></div></div></section>
<section class="section section--dark"><div class="container"><div class="section-heading"><div><p class="eyebrow">{'Напрямки' if uk else 'Disciplines'}</p><h2>{'Від ювелірної точності до монументальної форми' if uk else 'From jewellery precision to monumental form'}</h2></div><p class="lede">{'Один простір для дизайну, моделювання, виробництва та ручного завершення.' if uk else 'One studio for design, modelling, production and hand finishing.'}</p></div><div class="services-grid">{service_cards(lang)}</div></div></section>
<section class="section"><div class="container"><div class="section-heading"><div><p class="eyebrow">{'Вибрані роботи' if uk else 'Selected work'}</p><h2>{'Матеріал як мова' if uk else 'Material as a language'}</h2></div><p>{'Реальні проєкти різного масштабу: прикраси, портретна скульптура та архітектурні об’єкти.' if uk else 'Real projects at different scales: jewellery, portrait sculpture and architectural objects.'}</p></div><div class="project-grid">{project_cards(lang, 4)}</div><p style="margin-top:50px"><a class="button button--dark" href="/{lang}/portfolio/">{COPY[lang]['works']}</a></p></div></section>
<section class="section section--dark"><div class="container"><div class="section-heading"><div><p class="eyebrow">{'Від ідеї до реалізації' if uk else 'From idea to realisation'}</p><h2>{'Три стани однієї форми' if uk else 'Three states of one form'}</h2></div><p>{'Ескіз задає напрям. 3D-модель уточнює конструкцію. Матеріал завершує задум.' if uk else 'A sketch sets the direction. A 3D model resolves the construction. Material completes the idea.'}</p></div><div class="triptych"><article class="step"><div class="step-media"><img src="/assets/img/process/process-sketch.webp" alt="{'Ескіз ювелірної каблучки' if uk else 'Jewellery ring sketch'}" loading="lazy"></div><div class="step-copy"><span class="step-index">01</span><h3>{'Ескіз та ідея' if uk else 'Sketch & idea'}</h3><p>{'Концепція, пропорції та характер.' if uk else 'Concept, proportion and character.'}</p></div></article><article class="step"><div class="step-media"><img src="/assets/img/process/process-model.webp" alt="{'Тривимірна модель каблучки' if uk else 'Three-dimensional ring model'}" loading="lazy"></div><div class="step-copy"><span class="step-index">02</span><h3>{'3D-модель' if uk else '3D model'}</h3><p>{'Точність геометрії й виробнича логіка.' if uk else 'Geometric precision and production logic.'}</p></div></article><article class="step"><div class="step-media"><img src="/assets/img/process/process-result.webp" alt="{'Готова золота каблучка' if uk else 'Finished gold ring'}" loading="lazy"></div><div class="step-copy"><span class="step-index">03</span><h3>{'Реалізація' if uk else 'Realisation'}</h3><p>{'Виготовлення та фінішна робота.' if uk else 'Making and finishing.'}</p></div></article></div></div></section>
<section class="split"><div class="split-media"><img src="/assets/img/projects/hammond-bust.webp" alt="{'Річард Гаммонд поруч зі скульптурним бюстом' if uk else 'Richard Hammond beside a sculptural bust'}" loading="lazy"></div><div class="split-copy"><p class="eyebrow">{'Міжнародна співпраця' if uk else 'International collaboration'}</p><h2>{'Ідеї, що виходять за межі масштабу й кордонів' if uk else 'Ideas beyond scale and borders'}</h2><p>{'У портфоліо — портретні та скульптурні проєкти для відомих людей, зокрема кам’яна скульптура Конора Макгрегора та бюст Річарда Гаммонда.' if uk else 'The portfolio includes portrait and sculptural projects for public figures, including a stone sculpture of Conor McGregor and a bust for Richard Hammond.'}</p><a class="button button--dark" href="/{lang}/portfolio/">{COPY[lang]['works']}</a></div></section>
<section class="section"><div class="container"><div class="section-heading"><div><p class="eyebrow">{'Матеріали' if uk else 'Materials'}</p><h2>{'Форма починається з властивостей матеріалу' if uk else 'Form begins with the nature of material'}</h2></div><p>{'Точний вибір залежить від задуму, масштабу й способу виготовлення.' if uk else 'The exact choice depends on concept, scale and production method.'}</p></div><div class="materials"><div class="material"><span>01</span><strong>{'Метали' if uk else 'Metals'}</strong></div><div class="material"><span>02</span><strong>{'Камінь' if uk else 'Stone'}</strong></div><div class="material"><span>03</span><strong>{'Дерево' if uk else 'Wood'}</strong></div><div class="material"><span>04</span><strong>{'Полімери' if uk else 'Polymers'}</strong></div><div class="material"><span>05</span><strong>{'Комбінації' if uk else 'Combinations'}</strong></div></div></div></section>{cta(lang)}{contact_section(lang)}</main>'''
    return layout(lang, f"Yevhenii Muradov — {title}", "Авторські прикраси, скульптура, 3D-моделювання, лиття та художні об’єкти." if uk else "Signature jewellery, sculpture, 3D modelling, casting and art objects.", content, f"/{'en' if uk else 'uk'}/", ["/assets/js/form.js"])

def services_overview(lang):
    uk = lang == "uk"; name = "Напрямки" if uk else "Disciplines"
    content = f'''<main id="main"><section class="page-hero"><img src="/assets/img/projects/pavilion.webp" alt="" fetchpriority="high"><div class="container">{breadcrumb(lang, name)}<p class="eyebrow">ART · CRAFT · DESIGN</p><h1>{'Можливості майстерні' if uk else 'Studio capabilities'}</h1><p>{'Від цифрової моделі до матеріального об’єкта — обираємо процес навколо задуму, а не навпаки.' if uk else 'From digital model to physical object — the process is chosen around the idea, not the other way around.'}</p></div></section><section class="section section--dark"><div class="container"><div class="section-heading"><h2>{'Шість напрямів. Один цілісний процес.' if uk else 'Six disciplines. One coherent process.'}</h2><p>{'Напрями можуть працювати окремо або поєднуватися в межах складного індивідуального проєкту.' if uk else 'Disciplines can stand alone or combine within a complex individual project.'}</p></div><div class="services-grid">{service_cards(lang)}</div></div></section>{cta(lang)}</main>'''
    return layout(lang, f"{name} — Yevhenii Muradov", "Послуги творчої майстерні Yevhenii Muradov." if uk else "Creative studio services by Yevhenii Muradov.", content, f"/{'en' if uk else 'uk'}/services/")

def service_page(lang, slug, item):
    d = item[lang]; uk = lang == "uk"
    offers = "".join(f'<article class="offer"><span class="index">0{i}</span><h3>{escape(title)}</h3><p>{escape(text)}</p></article>' for i, (title, text) in enumerate(d['offers'], 1))
    faq = "".join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in d['faq'])
    related = [p for p in PROJECTS.items() if p[1]['category'] in ({"jewelry"} if slug == "jewelry" else {"sculpture"} if slug == "sculpture" else {"cnc"} if slug == "cnc-laser" else {"modeling"} if slug in ("3d-modeling", "3d-printing") else {"jewelry"})][:3]
    related_html = "".join(f'<article class="project-card"><a href="{path_for(lang,"portfolio",pslug)}"><div class="project-card-media"><img src="{p["image"]}" alt="{escape(p[lang]["name"])}" loading="lazy"></div><div class="project-card-meta"><div><small>{escape(p[lang]["category_name"])}</small><h3>{escape(p[lang]["name"])}</h3></div><span>↗</span></div></a></article>' for pslug, p in related)
    content = f'''<main id="main"><section class="page-hero"><img src="{item['image']}" alt="" fetchpriority="high"><div class="container">{breadcrumb(lang, d['name'])}<p class="eyebrow">{COPY[lang]['nav']['services']}</p><h1>{escape(d['name'])}</h1><p>{escape(d['intro'])}</p></div></section><section class="section"><div class="container content-grid"><aside class="side-title"><p>{'Можливості' if uk else 'Capabilities'}</p><h3>{escape(d['short'])}</h3></aside><div class="offer-grid">{offers}</div></div></section><section class="section section--dark"><div class="container"><div class="section-heading"><div><p class="eyebrow">{'Процес' if uk else 'Process'}</p><h2>{'Зрозумілий шлях від задуму до результату' if uk else 'A clear path from idea to result'}</h2></div><p>{'Після першої розмови визначаємо завдання, матеріал, потрібні етапи та спосіб взаємодії.' if uk else 'After the first conversation, we define the brief, material, stages and way of working.'}</p></div><div class="triptych"><div class="step"><div class="step-copy"><span class="step-index">01</span><h3>{'Обговорення' if uk else 'Discovery'}</h3><p>{'Ідея, референси, масштаб і призначення.' if uk else 'Idea, references, scale and intended use.'}</p></div></div><div class="step"><div class="step-copy"><span class="step-index">02</span><h3>{'Проєктування' if uk else 'Development'}</h3><p>{'Ескіз, цифрова модель і погодження форми.' if uk else 'Sketch, digital model and form approval.'}</p></div></div><div class="step"><div class="step-copy"><span class="step-index">03</span><h3>{'Виготовлення' if uk else 'Making'}</h3><p>{'Матеріалізація та фінальне доопрацювання.' if uk else 'Production and final refinement.'}</p></div></div></div></div></section><section class="section"><div class="container"><div class="section-heading"><h2>{'Пов’язані роботи' if uk else 'Related work'}</h2><a href="/{lang}/portfolio/">{COPY[lang]['works']} →</a></div><div class="project-grid">{related_html}</div></div></section><section class="section section--tight"><div class="container content-grid"><aside class="side-title"><p>FAQ</p><h3>{'Перед початком' if uk else 'Before we begin'}</h3></aside><div class="faq">{faq}</div></div></section>{cta(lang)}</main>'''
    return layout(lang, f"{d['name']} — Yevhenii Muradov", d['intro'], content, path_for("en" if lang == "uk" else "uk", "services", slug))

def portfolio(lang):
    uk = lang == "uk"; name = "Портфоліо" if uk else "Portfolio"
    labels = [("all", "Усі" if uk else "All"), ("jewelry", "Ювелірні" if uk else "Jewellery"), ("sculpture", "Скульптура" if uk else "Sculpture"), ("modeling", "Моделі" if uk else "Models"), ("cnc", "ЧПК" if uk else "CNC")]
    filters = "".join(f'<button class="filter-button{" active" if i == 0 else ""}" type="button" data-filter="{key}" aria-pressed="{"true" if i == 0 else "false"}">{label}</button>' for i, (key, label) in enumerate(labels))
    content = f'''<main id="main"><section class="page-hero"><img src="/assets/img/projects/jewelry-minimal.webp" alt="" fetchpriority="high"><div class="container">{breadcrumb(lang, name)}<p class="eyebrow">ART · CRAFT · DESIGN</p><h1>{name}</h1><p>{'Реальні роботи в металі, камені та комбінованих матеріалах — від прикраси до масштабного об’єкта.' if uk else 'Real work in metal, stone and combined materials — from jewellery to large-scale objects.'}</p></div></section><section class="section"><div class="container"><div class="filters" data-portfolio-filters aria-label="{'Фільтр категорій' if uk else 'Category filter'}">{filters}</div><div class="project-grid">{project_cards(lang)}</div></div></section>{cta(lang)}</main>'''
    return layout(lang, f"{name} — Yevhenii Muradov", "Портфоліо ювелірних, скульптурних і технологічних проєктів." if uk else "A portfolio of jewellery, sculpture and technology-led projects.", content, f"/{'en' if uk else 'uk'}/portfolio/", ["/assets/js/portfolio.js"])

def project_page(lang, slug, item):
    d = item[lang]; uk = lang == "uk"
    facts = [("Категорія" if uk else "Category", d['category_name']), ("Матеріали" if uk else "Materials", d['materials']), ("Технології" if uk else "Techniques", d['technology'])]
    facts_html = "".join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in facts)
    gallery = "".join(f'<figure><img src="{img}" alt="{escape(d["name"])} — {i+1}" loading="lazy"></figure>' for i, img in enumerate(item['gallery']))
    content = f'''<main id="main"><section class="page-hero project-detail-hero"><img src="{item['image']}" alt="{escape(d['name'])}" fetchpriority="high"><div class="container">{breadcrumb(lang, d['name'])}<p class="eyebrow">{escape(d['category_name'])}</p><h1>{escape(d['name'])}</h1><p>{escape(d['summary'])}</p></div></section><section class="section"><div class="container project-overview"><div><p class="eyebrow">{'Про проєкт' if uk else 'About the project'}</p><h2>{'Концепція та форма' if uk else 'Concept and form'}</h2></div><div><p class="lede">{escape(d['concept'])}</p><dl class="project-facts">{facts_html}</dl></div></div></section><section class="section--tight"><div class="container gallery">{gallery}</div></section><section class="section"><div class="container"><div class="section-heading"><h2>{'Від задуму до матеріалу' if uk else 'From idea to material'}</h2><p>{'Для кожної роботи послідовність етапів визначається окремо: ескіз, моделювання, підготовка, виготовлення та фініш.' if uk else 'The sequence is defined for each work: sketching, modelling, preparation, making and finishing.'}</p></div><a class="button button--dark" href="/{lang}/#contact">{'Замовити подібний проєкт' if uk else 'Commission a related project'}</a></div></section>{cta(lang)}</main>'''
    return layout(lang, f"{d['name']} — Yevhenii Muradov", d['summary'], content, path_for("en" if lang == "uk" else "uk", "portfolio", slug))

def about(lang):
    uk = lang == "uk"; name = "Про майстра" if uk else "About"
    content = f'''<main id="main"><section class="page-hero"><img src="/assets/img/process/process-consult.webp" alt="" fetchpriority="high"><div class="container">{breadcrumb(lang, name)}<p class="eyebrow">YEVHENII MURADOV</p><h1>{'Між ремеслом і технологією' if uk else 'Between craft and technology'}</h1><p>{'Авторський підхід до прикрас, скульптури та об’єктів, у яких ідея проходить повний шлях до матеріальної форми.' if uk else 'An original approach to jewellery, sculpture and objects where an idea travels the full path into physical form.'}</p></div></section><section class="section"><div class="container intro-grid"><div><p class="eyebrow">{'Підхід' if uk else 'Approach'}</p><p class="display">{'Точність не виключає характер.' if uk else 'Precision does not exclude character.'}</p></div><div class="intro-copy"><p class="lede">{'Євгеній Мурадов працює на перетині художньої пластики, традиційного ремесла та сучасного цифрового виробництва.' if uk else 'Yevhenii Muradov works where artistic form, traditional craft and contemporary digital production meet.'}</p><p>{'Робота може починатися з ручного ескізу, фотографії, короткого опису або вже готової 3D-моделі. Важливо не нав’язати матеріалу форму, а знайти спосіб, у якому задум, конструкція і технологія підтримують одне одного.' if uk else 'A project may begin with a hand sketch, photograph, short description or an existing 3D model. The aim is not to impose a form on the material, but to find a method in which concept, construction and technology support one another.'}</p></div></div></section><section class="split"><div class="split-media"><img src="/assets/img/projects/mcgregor-sculpture.webp" alt="{'Кам’яна скульптура Конора Макгрегора' if uk else 'Stone sculpture of Conor McGregor'}" loading="lazy"></div><div class="split-copy"><p class="eyebrow">{'Міжнародні проєкти' if uk else 'International projects'}</p><h2>{'Робота з впізнаваними образами' if uk else 'Working with recognisable subjects'}</h2><p>{'Серед реалізованих робіт — кам’яна скульптура Конора Макгрегора, портретний бюст для Річарда Гаммонда, масштабні моделі та авторські об’єкти.' if uk else 'Completed work includes a stone sculpture of Conor McGregor, a portrait bust for Richard Hammond, scale models and original art objects.'}</p><a class="button button--dark" href="/{lang}/portfolio/">{COPY[lang]['works']}</a></div></section><section class="section"><div class="container"><div class="section-heading"><h2>{'Принципи роботи' if uk else 'Working principles'}</h2><p>{'Без універсальних шаблонів і непотрібних обіцянок — рішення формується навколо конкретного завдання.' if uk else 'No universal templates or unnecessary promises — the solution is formed around the actual brief.'}</p></div><div class="offer-grid"><article class="offer"><span class="index">01</span><h3>{'Індивідуальність' if uk else 'Individuality'}</h3><p>{'Власний характер кожної форми.' if uk else 'A distinct character for every form.'}</p></article><article class="offer"><span class="index">02</span><h3>{'Виробнича логіка' if uk else 'Production logic'}</h3><p>{'Краса, яку підтримує продумана конструкція.' if uk else 'Beauty supported by considered construction.'}</p></article><article class="offer"><span class="index">03</span><h3>{'Діалог' if uk else 'Dialogue'}</h3><p>{'Погодження ключових рішень на шляху до результату.' if uk else 'Key decisions agreed throughout the process.'}</p></article><article class="offer"><span class="index">04</span><h3>{'Завершеність' if uk else 'Resolution'}</h3><p>{'Увага до поверхні, деталей і фінального враження.' if uk else 'Attention to surface, detail and final impression.'}</p></article></div></div></section>{cta(lang)}</main>'''
    return layout(lang, f"{name} — Yevhenii Muradov", "Про творчий і виробничий підхід Yevhenii Muradov." if uk else "The creative and production approach of Yevhenii Muradov.", content, f"/{'en' if uk else 'uk'}/about/")

def process_page(lang):
    uk = lang == "uk"; name = "Процес роботи" if uk else "Process"
    descriptions_uk = ["Пошук силуету, пропорцій і характеру.", "Точна геометрія та перевірка конструкції.", "Створення прототипу або майстер-моделі.", "Перенесення форми в матеріал.", "Уточнення деталей і поверхні вручну.", "Фінальний блиск, фактура й контроль результату."]
    descriptions_en = ["Exploring silhouette, proportion and character.", "Precise geometry and construction review.", "Creating a prototype or master model.", "Translating form into material.", "Refining details and surfaces by hand.", "Final polish, texture and result review."]
    cards = "".join(f'<article class="process-card reveal"><img src="/assets/img/process/{img}.webp" alt="{en if not uk else ua}" loading="lazy"><div><small>0{i}</small><h3>{ua if uk else en}</h3><p>{(descriptions_uk if uk else descriptions_en)[i-1]}</p></div></article>' for i, (img, ua, en) in enumerate(PROCESS_IMAGES, 1))
    content = f'''<main id="main"><section class="page-hero"><img src="/assets/img/process/process-hand.webp" alt="" fetchpriority="high"><div class="container">{breadcrumb(lang, name)}<p class="eyebrow">{'Як ми працюємо' if uk else 'How we work'}</p><h1>{'Від першої лінії до останнього дотику' if uk else 'From the first line to the final touch'}</h1><p>{'Послідовність адаптується до проєкту, але кожен етап має зрозумілу мету.' if uk else 'The sequence adapts to the project, but every stage has a clear purpose.'}</p></div></section><section class="section"><div class="container"><div class="section-heading"><h2>{'Шість ключових етапів' if uk else 'Six key stages'}</h2><p>{'Не всі проєкти потребують кожного процесу. Остаточний маршрут визначаємо після оцінювання задуму.' if uk else 'Not every project needs every process. The final route is defined after the concept is assessed.'}</p></div><div class="process-grid">{cards}</div></div></section><section class="section section--dark"><div class="container content-grid"><aside class="side-title"><p>{'Співпраця' if uk else 'Collaboration'}</p><h3>{'Що підготувати до першої розмови' if uk else 'What to prepare for the first conversation'}</h3></aside><div class="prose"><h2>{'Достатньо самої ідеї' if uk else 'An idea is enough to begin'}</h2><p class="lede">{'Корисно надіслати короткий опис, референси, приблизний масштаб і бажаний контекст використання.' if uk else 'A short description, references, approximate scale and intended context are useful.'}</p><p>{'Якщо частини інформації ще немає, ми визначимо, що потрібно уточнити перед ескізом, моделюванням або розрахунком.' if uk else 'If some information is not yet available, we will identify what needs clarification before sketching, modelling or estimating.'}</p></div></div></section>{cta(lang)}</main>'''
    return layout(lang, f"{name} — Yevhenii Muradov", "Етапи роботи над індивідуальними прикрасами, скульптурою та об’єктами." if uk else "The process behind individual jewellery, sculpture and art objects.", content, f"/{'en' if uk else 'uk'}/process/")

def contact_section(lang):
    uk = lang == "uk"
    map_query = quote_plus("вулиця Богдана Хмельницького, 16-22, Київ, 01030, Україна")
    map_address = "вул. Богдана Хмельницького, 16–22, Київ, 01030" if uk else "16–22 Bohdana Khmelnytskoho Street, Kyiv, 01030, Ukraine"
    return f'''<section class="section contact-section" id="contact"><div class="container contact-panel"><div class="contact-grid">
  <div class="contact-copy"><p class="eyebrow">{'Контакти' if uk else 'Contact'}</p><h2>{'Зручним для вас способом' if uk else 'In the way that suits you'}</h2><p>{'Напишіть або зателефонуйте — після знайомства з ідеєю ми зв’яжемося з вами та обговоримо наступний крок.' if uk else 'Write or call — after reviewing the idea, we will get in touch and discuss the next step.'}</p><div class="contact-list"><a href="mailto:muradov.workk@gmail.com">{contact_icon('email')}<span>muradov.workk@gmail.com</span></a><a href="tel:+380994891881">{contact_icon('phone')}<span>+380 99 489 18 81</span></a><a href="https://t.me/Yevhenii_Muradov" rel="noopener" aria-label="Telegram @Yevhenii_Muradov">{contact_icon('telegram')}<span>@Yevhenii_Muradov</span></a></div></div>
  <form class="form-grid contact-form" action="/api/contact.php" method="post" data-contact-form novalidate>
    <div class="field field--full"><label class="visually-hidden" for="name">{'Ім’я' if uk else 'Name'} *</label><input id="name" name="name" required maxlength="80" autocomplete="name" placeholder="{'Ім’я' if uk else 'Name'}"></div>
    <div class="field field--full"><label class="visually-hidden" for="phone">{'Телефон' if uk else 'Phone'} *</label><input id="phone" name="contact" type="tel" required minlength="7" maxlength="24" inputmode="tel" autocomplete="tel" placeholder="{'Телефон' if uk else 'Phone'}"></div>
    <div class="field field--full"><label class="visually-hidden" for="message">{'Ваше запитання' if uk else 'Your enquiry'} *</label><textarea id="message" name="message" required minlength="10" maxlength="3000" placeholder="{'Ваше запитання' if uk else 'Your enquiry'}"></textarea></div>
    <div class="honeypot" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="field field--full"><label class="checkbox"><input type="checkbox" name="consent" value="yes" required><span>{'Я погоджуюся на оброблення даних відповідно до' if uk else 'I agree to the processing of my data under the'} <a href="/{lang}/privacy/"><u>{COPY[lang]['privacy'].lower()}</u></a>.</span></label></div>
    <div class="field field--full form-actions"><button class="button button--dark contact-submit" type="submit"><span>{'Відправити' if uk else 'Send'}</span><span aria-hidden="true">→</span></button><p class="form-status" data-form-status role="status" aria-live="polite"></p></div>
  </form>
</div></div></section>
<section class="section section--tight map-section"><div class="container"><div class="map-heading"><div><p class="eyebrow">{'Локація' if uk else 'Location'}</p><h2>{'Завітайте до нас' if uk else 'Visit us'}</h2></div><address>{map_address}</address></div><div class="map-frame"><iframe src="https://www.google.com/maps?q={map_query}&amp;output=embed" title="{'Карта розташування майстерні' if uk else 'Studio location map'}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></section>
'''

def privacy(lang):
    uk = lang == "uk"; name = COPY[lang]['privacy']
    if uk:
        prose = '''<h2>Які дані надсилаються</h2><p>Форма може передавати ім’я, номер телефону, опис задуму, мову та адресу сторінки. Не надсилайте конфіденційні або надлишкові персональні дані.</p><h2>Мета оброблення</h2><p>Дані використовуються виключно для відповіді на звернення, обговорення можливого проєкту та пов’язаної комунікації.</p><h2>Передавання та зберігання</h2><p>Після налаштування форми звернення передаватиметься до приватного чату Telegram через серверний обробник. Остаточні строки зберігання та дані контролера будуть уточнені перед публічним запуском.</p><h2>Ваші права</h2><p>Ви можете звернутися з питанням про свої дані або попросити припинити комунікацію через зазначені на сайті контакти.</p><h2>Контакт</h2><p><a href="mailto:muradov.workk@gmail.com">muradov.workk@gmail.com</a></p>'''
    else:
        prose = '''<h2>Data submitted</h2><p>The form may transmit your name, phone number, project description, page language and source path. Do not submit confidential or unnecessary personal information.</p><h2>Purpose</h2><p>Data is used solely to respond to your enquiry, discuss a possible project and conduct related communication.</p><h2>Transfer and retention</h2><p>Once configured, enquiries will be sent to a private Telegram chat through a server-side handler. Final retention periods and controller information will be confirmed before public launch.</p><h2>Your rights</h2><p>You may ask about your data or request that communication cease using the contact details on this website.</p><h2>Contact</h2><p><a href="mailto:muradov.workk@gmail.com">muradov.workk@gmail.com</a></p>'''
    content = f'''<main id="main"><section class="page-hero"><div class="container">{breadcrumb(lang, name)}<p class="eyebrow">{'Інформація' if uk else 'Information'}</p><h1>{name}</h1><p>{'Чернетка для локальної версії. Юридичні реквізити потрібно завершити перед публікацією.' if uk else 'Draft for the local version. Legal details must be completed before publication.'}</p></div></section><section class="section"><div class="container content-grid"><aside class="side-title"><p>{'Оновлено' if uk else 'Updated'}</p><h3>10.10.2026</h3></aside><article class="prose">{prose}</article></div></section></main>'''
    return layout(lang, f"{name} — Yevhenii Muradov", name, content, f"/{'en' if uk else 'uk'}/privacy/")

def error_page(lang):
    uk = lang == "uk"
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>404 — Yevhenii Muradov</title><link rel="stylesheet" href="/assets/css/styles.css"></head><body><main class="not-found"><div class="container"><strong>404</strong><h1>{'Сторінку не знайдено' if uk else 'Page not found'}</h1><p>{'Можливо, адресу було змінено.' if uk else 'The address may have changed.'}</p><a class="button" href="/{lang}/">{'На головну' if uk else 'Back home'}</a></div></main></body></html>'''

def root_page():
    # The root URL opens the primary Ukrainian site immediately. Language is
    # changed later through the persistent UA / EN switch in the header.
    return home("uk")

def sitemap_template():
    paths = ["/"]
    for lang in ("uk", "en"):
        paths.extend([f"/{lang}/", f"/{lang}/about/", f"/{lang}/services/"])
        paths.extend(path_for(lang, "services", slug) for slug in SERVICES)
        paths.append(f"/{lang}/portfolio/")
        paths.extend(path_for(lang, "portfolio", slug) for slug in PROJECTS)
        paths.extend([f"/{lang}/process/", f"/{lang}/privacy/"])
    urls = "\n".join(f"  <url><loc>https://example.com{path}</loc></url>" for path in paths)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Replace example.com with the production domain and regenerate before launch. -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
'''

def build():
    write("index.html", root_page())
    for lang in ("uk", "en"):
        write(f"{lang}/index.html", home(lang))
        write(f"{lang}/about/index.html", about(lang))
        write(f"{lang}/services/index.html", services_overview(lang))
        for slug, item in SERVICES.items(): write(f"{lang}/services/{slug}/index.html", service_page(lang, slug, item))
        write(f"{lang}/portfolio/index.html", portfolio(lang))
        for slug, item in PROJECTS.items(): write(f"{lang}/portfolio/{slug}/index.html", project_page(lang, slug, item))
        write(f"{lang}/process/index.html", process_page(lang))
        write(f"{lang}/privacy/index.html", privacy(lang))
        write(f"{lang}/404.html", error_page(lang))
    write("sitemap.xml", sitemap_template())
    print("Built bilingual static site")

if __name__ == "__main__":
    build()
