# 진담 중국어 오락실

진담중국어 게임을 한곳에 모아 아이들이 골라서 할 수 있는 페이지예요.

- `index.html` 한 장짜리 페이지 (빌드 없음)
- 게임 카드는 각 게임의 원래 주소로 연결돼요 (아이들 기록이 그대로 이어지게)
- 분류(「진담오락실 분류 구조 기획」 2026-10-28): 존(한자·단어·문장) / 덩어리훈련 4단계 배지(보고·연결·내 문장·1초 툭!, 게임당 최대 2개) / 꼬리표(시험·대상·주제) + 소요시간 / 다시 도전 표시
- 새 게임 추가: `index.html` 아래쪽 `GAMES` 목록에 한 줄(zone·name·url·icon·steps·retry·who·exam·topic·min·desc), 아이콘은 `icons/`

## 그랑힐스 전용 오락실 `/grandhills/`
- 주소: https://jindam1799.github.io/JINDAM_CHINESE_JINAH/grandhills/ (비밀번호 없음, 반에만 따로 알려 줌)
- 게임 3개: 덩어리 숲속의 모험(/kids) · 블록퍼즐(/grandhills/) · 진담점프(/granhills/)
- `python3 tools/make_grandhills.py` 로 만듦: 본판 index.html 디자인 + 스크립트 안 `GH_GAMES` 목록. 본판을 고친 뒤에도 다시 실행

© 2026 진담중국어. All rights reserved.
