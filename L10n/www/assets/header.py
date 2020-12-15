from browser import bind, console, html, window, document, alert
import browser.widgets.menu as menu

href = document.location.href
protocol, rest = href.split("://")
host, addr = rest.split("/", 1)

# automatic redirection from http to https for brython.info
if protocol == "http" and host.endswith("brython.info"):
    document.location.href = f"https://{rest}"

Menu = menu.Menu

languages = ["zh-hant"]
languages_options = [["zh-hant", "繁體中文"]]

trans_menu = {
    "menu_console": {"zh-hant": "控制台"},
    "menu_editor": {"zh-hant": "編輯器"},
    "menu_demo": {"zh-hant": "演示"},
    "menu_gallery": {"zh-hant": "Gallery"},
    "menu_doc": {"zh-hant": "文檔"},
    "menu_download": {"zh-hant": "下載"},
    "menu_dev": {"zh-hant": "開發"},
    "menu_ex": {"zh-hant": "範例"},
    "menu_groups": {"zh-hant": "社群"},
    "menu_ref": {"zh-hant": "參考"},
    "menu_resources": {"zh-hant": "資源"},
    "menu_tutorial": {"zh-hant": "教學"},
}
links = {
    "home": "/index.html",
    "console": "https://www.brython.info/tests/console.html",  # official
    "demo": "https://www.brython.info/demo.html",  # official
    "editor": "https://www.brython.info/tests/editor.html",  # official
    "gallery": "https://www.brython.info/gallery/gallery_en.html",  # official
    "doc": "/static_doc/{language}/intro.html",
    "download": "https://github.com/brython-dev/brython/releases",
    "dev": "https://github.com/brython-dev/brython",
    "groups": "/groups.html",
    "tutorial": "/static_tutorial/{language}/index.html",
}


def show(language=None):
    """Detect language, either from the key "lang" in the query string or
    from the browser settings."""
    has_req = False
    qs_lang = None

    prefix = "/"

    if language is None:
        qs_lang = document.query.getfirst("lang")  # query string
        if qs_lang and qs_lang in languages:
            has_req = True
            language = qs_lang
        else:
            lang = __BRYTHON__.language  # browser setting
            if lang[:2] == "zh":
                language = "zh-hant"

    language = language or "zh-hant"

    _banner = document["banner_row"]

    loc = window.location.href
    current = None
    for key in ["home", "console", "demo", "editor", "groups"]:
        if links[key] in loc:
            current = key
            break

    if current is None:
        if "gallery" in loc:
            current = "gallery"
        elif "static_doc" in loc:
            current = "doc"

    def load_page(key):
        officials = ["console", "demo", "editor", "gallery"]

        def f(e):
            href = links[key].format(language=language)
            if key in officials:
                window.location.href = href
            else:
                window.location.href = href + f"?lang={language}"

        return f

    menu = Menu(_banner, default_css=False)

    menu.add_item(trans_menu["menu_tutorial"][language], callback=load_page("tutorial"))

    menu.add_item(trans_menu["menu_demo"][language], callback=load_page("demo"))

    menu.add_item(trans_menu["menu_doc"][language], callback=load_page("doc"))

    menu.add_item(trans_menu["menu_console"][language], callback=load_page("console"))

    menu.add_item(trans_menu["menu_editor"][language], callback=load_page("editor"))

    menu.add_item(trans_menu["menu_gallery"][language], callback=load_page("gallery"))

    ex_resources = menu.add_menu(trans_menu["menu_resources"][language])
    ex_resources.add_item(
        trans_menu["menu_download"][language], callback=load_page("download")
    )
    ex_resources.add_item(trans_menu["menu_dev"][language], callback=load_page("dev"))
    ex_resources.add_item(trans_menu["menu_groups"][language], callback=load_page("groups"))

    # insert language selection menu
    sel_lang = html.DIV(Class="sel_lang")

    document.body.insertBefore(sel_lang, _banner.nextElementSibling)
    select = html.SELECT(Class="language")
    sel_lang <= select
    for lang1, lang2 in languages_options:
        select <= html.OPTION(lang2, value=lang1, selected=lang1 == language)

    @bind(select, "change")
    # If user changes the language in the select box, reload the page.
    def change_language(ev):
        sel = ev.target
        new_lang = sel.options[sel.selectedIndex].value
        head = f"{protocol}://{host}"
        new_href = href
        if addr == "" or addr.startswith("index.html"):
            new_href = f"{head}/index.html?lang={new_lang}"
        elif addr.startswith(("static_tutorial", "static_doc")):
            elts = addr.split("/")
            page = elts[-1].split("?")[0]
            elts[1] = new_lang
            new_href = f"{head}/{elts[0]}/{new_lang}/{page}"
        elif addr.startswith(("demo.html", "tests/console.html", "tests/editor.html")):
            elts = addr.split("?")
            new_href = f"{head}/{elts[0]}?lang={new_lang}"
        document.location.href = new_href

    return qs_lang, language
