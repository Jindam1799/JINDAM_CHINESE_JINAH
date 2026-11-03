# 반별 오락실 만들기: python3 tools/make_editions.py
# 본판 index.html(1:1 학생용)을 바탕으로 반별 페이지를 만듦 → hanja/ · adult-high/ · adult-basic/
# 본판 디자인이나 게임 정보를 고친 뒤 다시 실행. 반별 게임 목록은 아래 EDITIONS 에서 고침
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 본판에는 없지만 반별 오락실에 쓰는 게임
EXTRA = """
    { zone: 'sent', name: '速成 덩어리 툭!', url: 'https://jindam1799.github.io/jindam_sucheng_tuk/', icon: 'sucheng', steps: ['tuk', 'mine'], retry: true, who: ['성인'], exam: [], topic: ['회화', '汉语口语速成'], min: 10, desc: '교재 16~30과 표현을 덩어리로 익히고 1초 안에 툭! 말해요.' },
    { zone: 'sent', name: '덩어리 툭 고급회화', url: 'https://jindam1799.github.io/jindam_gogeup/', icon: 'gogeup', steps: ['mine', 'tuk'], retry: true, who: ['성인'], exam: [], topic: ['고급회화'], min: 10, desc: '고급반 교재 표현으로 내 문장을 만들고 바로 반응해요.' },
"""

EDITIONS = {
  'hanja': {
    'title': '한자어로 시작하는 중국어', 'short': '한자어 오락실',
    'h1': '한자어로 시작하는 중국어 <span class="zh">오락실</span>',
    'zones': "    { id: 'gh', name: '우리 반 게임', note: '수업에서 배운 중국어로 놀아요 · 1번부터 차례로 해 봐요', icon: 'all', color: '#2f9a7a' },",
    'games': """
    { zone: 'gh', name: '1. 덩어리 숲속의 모험', url: 'https://jindamchineseadventure.vercel.app/kids', icon: 'adventure', steps: ['see', 'link'], retry: true, who: ['초등'], exam: [], topic: ['한자어 중국어'], min: 10, desc: '수업에서 배운 한자어 중국어를 찾아 대나무숲을 달려요.' },
    { zone: 'gh', name: '2. 블록퍼즐', url: 'https://jindamblockpuzzle.vercel.app/grandhills/', icon: 'puzzle', steps: ['link'], retry: true, who: ['초등'], exam: [], topic: ['활동지 4장', '퍼즐'], min: 10, desc: '우리 학교 · 내 생일 · 우리 동네 · 지금 몇 시? 단어로 퀴즈를 풀고 블록 퍼즐을 맞춰요.' },
    { zone: 'gh', name: '3. 진담점프', url: 'https://jindamjump.vercel.app/granhills/', icon: 'jump', steps: ['tuk', 'see'], retry: false, who: ['초등'], exam: [], topic: ['듣기'], min: 5, desc: '활동지(학교·달력·동네 간판·시계)의 중국어를 듣고 뜻을 골라 용암을 피해 점프!' },
""",
    'hide': '.map, #rooms, #filters',
  },
  'adult-high': {
    'title': '성인 중급~고급반', 'short': '성인 고급 오락실',
    'h1': '성인 중급~고급반 <span class="zh">오락실</span>',
    'pick': ['진담 HSK4 한자톡', '진담 테트리스', '진담 블록퍼즐', '진담점프', '천하통일 중국어', '진담 도시 탐정 런', '덩어리 툭 고급회화'],
    'hide': '#filters',
  },
  'adult-basic': {
    'title': '성인 입문~초급반', 'short': '성인 초급 오락실',
    'h1': '성인 입문~초급반 <span class="zh">오락실</span>',
    'pick': ['진담한자톡', '덩어리 숲', '速成 덩어리 툭!', '덩어리 숲속의 모험'],
    'hide': '#filters',
  },
}

base = open(os.path.join(ROOT, 'index.html')).read()
games_block = re.search(r'  var GAMES = \[\n(.*?)\n  \];', base, re.S).group(1) + EXTRA
lines = {re.search(r"name: '([^']+)'", l).group(1): l for l in games_block.split('\n') if "name: '" in l}
zones_block = re.search(r'  var ZONES = \[\n(.*?)\n  \];', base, re.S).group(1)

for slug, E in EDITIONS.items():
    h = base

    def sub(pat, rep):
        global h
        h2, n = re.subn(pat, lambda m: rep, h, count=1, flags=re.S)
        assert n == 1, (slug, pat)
        h = h2

    if 'pick' in E:
        games = '\n'.join(lines[n] for n in E['pick'])
        used = {re.search(r"zone: '(\w+)'", lines[n]).group(1) for n in E['pick']}
        zones = '\n'.join(l for l in zones_block.split('\n') if "id: '" in l and re.search(r"id: '(\w+)'", l).group(1) in used)
    else:
        games, zones = E['games'].strip('\n'), E['zones']
    sub(r'  var ZONES = \[\n.*?\n  \];', '  var ZONES = [\n' + zones + '\n  ];')
    sub(r'  var GAMES = \[\n.*?\n  \];', '  var GAMES = [\n' + games + '\n  ];')
    sub(r'<title>.*?</title>', '<title>%s · 진담 중국어 오락실</title>' % E['title'])
    sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="진담중국어 %s 게임 모음">' % E['title'])
    sub(r'<meta name="apple-mobile-web-app-title" content="[^"]*">', '<meta name="apple-mobile-web-app-title" content="%s">' % E['short'])
    sub(r'<link rel="manifest" href="[^"]*">', '<link rel="manifest" href="app.webmanifest">')
    h = h.replace('href="icons/', 'href="../icons/').replace('src="icons/', 'src="../icons/').replace('href="apple-touch-icon.png"', 'href="../apple-touch-icon.png"')
    sub(r'<h1>.*?</h1>', '<h1>%s</h1>' % E['h1'])
    # 안내 팝업은 1:1 오락실용이라 반별 페이지에서는 숨김
    sub(r'</style>', '  %s, .about-btn { display: none !important; }\n  h1 .zh { white-space: nowrap; }\n</style>' % E['hide'])
    sub(r'    if \(!seen\) show\(\);\n', '')
    h = h.replace('<!doctype html>', '<!doctype html>\n<!-- 반별 오락실(%s): tools/make_editions.py 로 만든 파일이에요. 직접 고치지 말고 스크립트를 고쳐서 다시 실행하세요. -->' % slug, 1)
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    open(os.path.join(ROOT, slug, 'index.html'), 'w').write(h)
    man = json.load(open(os.path.join(ROOT, 'app.webmanifest')))
    man.update({'name': '%s · 진담 중국어 오락실' % E['title'], 'short_name': E['short'], 'start_url': './index.html', 'scope': './', 'id': './'})
    for ic in man['icons']:
        ic['src'] = '../' + ic['src']
    json.dump(man, open(os.path.join(ROOT, slug, 'app.webmanifest'), 'w'), ensure_ascii=False, indent=2)
    print(slug, 'ok')
