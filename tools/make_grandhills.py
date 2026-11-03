# 그랑힐스 전용 오락실 만들기: python3 tools/make_grandhills.py
# 본판 index.html 을 바탕으로 grandhills/index.html 을 만듦 (본판 디자인을 고친 뒤 다시 실행)
# 그랑힐스 게임을 바꾸려면 아래 GH_GAMES 를 고치고 다시 실행
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GH_ZONES = """  var ZONES = [
    { id: 'gh', name: '우리 반 게임', note: '수업에서 배운 중국어로 놀아요 · 1번부터 차례로 해 봐요', icon: 'all', color: '#2f9a7a' },
  ];"""
GH_GAMES = """  var GAMES = [
    { zone: 'gh', name: '1. 덩어리 숲속의 모험', url: 'https://jindamchineseadventure.vercel.app/kids', icon: 'adventure', steps: ['see', 'link'], retry: true, who: ['초등'], exam: [], topic: ['한자어 중국어'], min: 10, desc: '수업에서 배운 한자어 중국어를 찾아 대나무숲을 달려요.' },
    { zone: 'gh', name: '2. 블록퍼즐', url: 'https://jindamblockpuzzle.vercel.app/grandhills/', icon: 'puzzle', steps: ['link'], retry: true, who: ['초등'], exam: [], topic: ['활동지 4장', '퍼즐'], min: 10, desc: '우리 학교 · 내 생일 · 우리 동네 · 지금 몇 시? 단어로 퀴즈를 풀고 블록 퍼즐을 맞춰요.' },
    { zone: 'gh', name: '3. 진담점프', url: 'https://jindamjump.vercel.app/granhills/', icon: 'jump', steps: ['tuk', 'see'], retry: false, who: ['초등'], exam: [], topic: ['듣기'], min: 5, desc: '활동지(학교·달력·동네 간판·시계)의 중국어를 듣고 뜻을 골라 용암을 피해 점프!' },
  ];"""
h = open(os.path.join(ROOT, 'index.html')).read()
def sub(pat, rep, flags=re.S):
    global h
    h2, n = re.subn(pat, lambda m: rep, h, count=1, flags=flags)
    assert n == 1, pat
    h = h2
sub(r'  var ZONES = \[.*?\n  \];', GH_ZONES)
sub(r'  var GAMES = \[.*?\n  \];', GH_GAMES)
sub(r'<title>.*?</title>', '<title>그랑힐스 중국어 오락실</title>')
sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="그랑힐스 반 친구들을 위한 진담중국어 게임 모음">')
sub(r'<meta name="apple-mobile-web-app-title" content="[^"]*">', '<meta name="apple-mobile-web-app-title" content="그랑힐스 오락실">')
sub(r'<link rel="manifest" href="[^"]*">', '<link rel="manifest" href="app.webmanifest">')
h = h.replace('href="icons/', 'href="../icons/').replace('src="icons/', 'src="../icons/').replace('href="apple-touch-icon.png"', 'href="../apple-touch-icon.png"')
sub(r'<h1>.*?</h1>', '<h1>그랑힐스 <span class="zh">중국어 오락실</span></h1>')
# 훈련 지도·존 메뉴·필터·안내 팝업은 숨김 (게임 3개라 필요 없음)
sub(r'</style>', '  .map, #rooms, #filters, .about-btn { display: none !important; }\n</style>')
sub(r'    if \(!seen\) show\(\);\n', '')
h = h.replace('<!doctype html>', '<!doctype html>\n<!-- 그랑힐스 전용 오락실: tools/make_grandhills.py 로 만든 파일이에요. 직접 고치지 말고 스크립트를 고쳐서 다시 실행하세요. -->', 1)
open(os.path.join(ROOT, 'grandhills', 'index.html'), 'w').write(h)
man = json.load(open(os.path.join(ROOT, 'app.webmanifest')))
man.update({'name': '그랑힐스 중국어 오락실', 'short_name': '그랑힐스 오락실', 'start_url': './index.html', 'scope': './', 'id': './'})
for ic in man['icons']: ic['src'] = '../' + ic['src']
json.dump(man, open(os.path.join(ROOT, 'grandhills', 'app.webmanifest'), 'w'), ensure_ascii=False, indent=2)
print('ok')
