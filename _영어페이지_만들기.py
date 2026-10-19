# -*- coding: utf-8 -*-
r"""culturepick.co.kr 영어 페이지 만들기(10/19 · 영어판) — index.html(한국어)을 바탕으로 en/index.html 을 만든다

  python 웹사이트/_영어페이지_만들기.py   → 웹사이트/en/index.html  (+ 한국어 페이지에 English 링크)

- 한국어 index.html 을 고치면 이걸 다시 돌린다 · 바꿀 글을 못 찾으면 「못 찾은 바꿀 글」로 알린다(그 줄을 여기서 고친다)
- 영어 개인정보처리방침(en/privacy.html)은 앱/방침_올리기.py 가 web/privacy_en.js 로 만든다
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
R = [
    ('<html lang="ko">', '<html lang="en">'),
    ('<title>컬처픽 — 우리 동네 강좌·축제를 지도에서</title>', '<title>CulturePick — Local classes and festivals in Korea</title>'),
    ('content="컬처픽은 주민센터·도서관·체육센터·문화센터가 공개한 강좌와 전국 축제를 지도 한 장에 모아 보여 주는 앱입니다. 신청과 결제는 각 기관 누리집에서 합니다."',
     'content="CulturePick gathers public classes from community centers, libraries, sports centers and culture centers, plus exhibitions and festivals across Korea, on one map."'),
    ('<meta property="og:title" content="컬처픽 — 우리 동네 강좌·축제를 지도에서">', '<meta property="og:title" content="CulturePick — Local classes and festivals in Korea">'),
    ('<meta property="og:description" content="공공·도서관·문화센터 강좌와 전국 축제를 지도에서 한 번에 찾는 앱">', '<meta property="og:description" content="Find public, library and culture-center classes and festivals in Korea on one map">'),
    ('href="img/icon.png"', 'href="/img/icon.png"'), ('src="img/', 'src="/img/'),
    ('<a class="brand" href="#"><img src="/img/icon.png" alt="">컬처픽</a>', '<a class="brand" href="/en/"><img src="/img/icon.png" alt="">CulturePick</a>'),
    ('<a href="#menus">화면 둘러보기</a><a href="#login">로그인과 개인정보</a><a href="#rules">운영 원칙</a><a href="#contact">문의</a>',
     '<a href="#menus">Screens</a><a href="#login">Sign-in &amp; privacy</a><a href="#rules">Principles</a><a href="#contact">Contact</a>'),
    ('<a href="/en/">English</a>', '<a href="/">한국어</a>'),
    ('<span class="kicker">강좌·축제 지도 앱</span>', '<span class="kicker">Classes &amp; festivals map</span>'),
    ('<h1>우리 동네 <em>강좌와 축제</em>를<br>지도 한 장에서</h1>', '<h1>Local <em>classes and festivals</em><br>on one map</h1>'),
    ('주민센터·평생학습관·체육센터·도서관, 백화점과 마트 문화센터가 공개한 강좌, 그리고 전국 축제를 매일 모아 지도에 보여 드려요. 마음에 드는 강좌는 찜해 두고, 접수 날짜가 오면 알림을 받아요.',
     'Every day we gather classes published by community centers, lifelong learning centers, sports centers, libraries and department store culture centers, plus exhibitions and festivals across Korea, and show them on a map. Save the classes you like and get an alert when sign-up opens.'),
    ('<li>전국 강좌 <b>5만 개</b> 넘게</li>', '<li><b>50,000+</b> classes</li>'), ('<li>강좌 여는 곳 <b>4,899</b>곳</li>', '<li><b>4,899</b> places</li>'),
    ('<li>진행 중·예정 축제 <b>171</b>개</li>', '<li><b>171</b> festivals</li>'), ('<li>매일 새벽 새로 모음</li>', '<li>Updated every morning</li>'),
    ('2026년 10월 기준 숫자예요. 안드로이드 앱은 구글 플레이 비공개 시험을 준비하고 있고, 아이폰 앱도 함께 만들고 있어요.',
     'Numbers as of October 2026. The Android app is preparing for a closed test on Google Play, and an iPhone app is in the works. The app can be used in English; class names stay in Korean as published.'),
    ('alt="컬처픽 지도 화면: 동네 강좌가 말풍선으로 보인다"', 'alt="CulturePick map with nearby classes"'),
    ('<h2>컬처픽은 이런 서비스예요</h2>', '<h2>What CulturePick is</h2>'),
    ('흩어져 있는 공공·민간 강좌 정보를 한곳에서 찾게 해 주는 <b>정보 안내 앱</b>이에요. 신청과 결제는 컬처픽이 하지 않고, 각 기관 누리집으로 연결해 드려요.',
     'An <b>information app</b> that brings scattered public and private class listings into one place. CulturePick does not handle sign-ups or payments; it links you to each organization’s website.'),
    ('<tr><th>서비스 종류</th><td>강좌·문화행사 정보 검색과 지도 안내(무료)</td></tr>', '<tr><th>Service</th><td>Search and map guide for classes and cultural events (free)</td></tr>'),
    ('<tr><th>보여 주는 정보</th><td>기관이 누구나 볼 수 있게 공개한 강좌 목록(강좌 이름·대상·요일·시간·수강료·접수 기간·남은 자리), 한국관광공사 축제 정보</td></tr>',
     '<tr><th>Information</th><td>Class listings organizations publish for everyone (name, audience, days, time, fee, sign-up period, seats left), exhibitions, and Korea Tourism Organization festival data</td></tr>'),
    ('<tr><th>신청·결제</th><td>하지 않아요. [신청하러 가기]를 누르면 그 기관 누리집이 열려요</td></tr>', '<tr><th>Sign-up &amp; payment</th><td>Not handled by us. Tapping [Sign up] opens the organization’s website</td></tr>'),
    ('<tr><th>회원 가입</th><td>없어도 모든 기능을 쓸 수 있어요. 로그인은 찜·알림을 폰을 바꿔도 이어 쓰고 싶을 때만 골라서 해요</td></tr>',
     '<tr><th>Account</th><td>Not required. Sign in only if you want to keep saved items and alerts across phones</td></tr>'),
    ('<tr><th>돈 버는 방법</th><td>앱 화면 아래 배너 광고(구글 애드몹). 유료 결제·사행성 기능은 없어요</td></tr>', '<tr><th>Revenue</th><td>A banner ad at the bottom of the app (Google AdMob). No paid features or gambling</td></tr>'),
    ('<b>이런 분께 필요해요</b>', '<b>Made for</b>'),
    ('<li>퇴근 후 다닐 요가·수영 강좌를 집 근처에서 찾는 직장인</li>', '<li>Workers looking for yoga or swimming near home after work</li>'),
    ('<li>아이와 갈 만한 주말 체험·그림책 강좌를 찾는 부모</li>', '<li>Parents looking for weekend programs to enjoy with kids</li>'),
    ('<li>부모님 댁 근처 시니어 강좌를 대신 찾아 드리는 자녀</li>', '<li>Adult children finding senior classes near their parents’ home</li>'),
    ('<li>이번 주말 가까운 축제를 찾는 분</li>', '<li>Anyone looking for a festival this weekend</li>'),
    ('<h2>메뉴별 화면</h2>', '<h2>Screens</h2>'),
    ('앱 아래쪽에 <b>지도 · 축제 · 찜 · 내 정보</b> 네 개 메뉴가 있어요. 실제 앱 화면이에요.', 'The app has four menus at the bottom: <b>Map · Events · Saved · Me</b>. These are real app screens (shown in Korean).'),
    ('<span class="n">지도</span>', '<span class="n">Map</span>'), ('alt="지도 화면"', 'alt="Map"'), ('<h3>지도에서 찾기</h3>', '<h3>Find on the map</h3>'),
    ('지금 있는 곳 주변의 강좌 여는 곳이 말풍선으로 보여요. 숫자는 지금 신청할 수 있는 강좌 수예요. 위쪽 칸으로 접수중·문화센터·전시·도서관·축제를 골라 볼 수 있어요.',
     'Places near you appear as bubbles. The number is how many classes are open for sign-up now. Filter by open now, culture centers, museums, libraries and festivals.'),
    ('<span class="n">지도 › 장소</span>', '<span class="n">Map › Place</span>'), ('alt="센터 강좌 목록 화면"', 'alt="Place class list"'), ('<h3>장소별 강좌 목록</h3>', '<h3>Classes by place</h3>'),
    ('말풍선을 누르면 그곳 강좌가 지금 신청 가능 → 곧 접수 → 진행 중 순서로 나와요. 전화·길찾기·기관 누리집 단추가 있어요.',
     'Tap a bubble to see its classes: open now, opening soon, then ongoing. Call, directions and website buttons included.'),
    ('<span class="n">지도 › 강좌</span>', '<span class="n">Map › Class</span>'), ('alt="강좌 상세 화면"', 'alt="Class details"'), ('<h3>강좌 자세히</h3>', '<h3>Class details</h3>'),
    ('대상·요일·시간·수강료·접수 기간·남은 자리와 자료 출처를 보여 줘요. [신청하러 가기]는 기관 신청 화면으로 넘어가요.',
     'Audience, days, time, fee, sign-up period, seats left and the source. [Sign up] takes you to the organization’s page.'),
    ('<span class="n">지도 › 상황 칸</span>', '<span class="n">Map › Filters</span>'), ('alt="아이와 함께 강좌 화면"', 'alt="With kids filter"'), ('<h3>상황별로 고르기</h3>', '<h3>Filter by situation</h3>'),
    ('이번 주말 · 아이와 함께 · 퇴근 후 · 시니어처럼 상황에 맞는 강좌만 골라 보여 줘요.', 'This weekend, with kids, after work or seniors — see only the classes that fit.'),
    ('<span class="n">축제</span>', '<span class="n">Events</span>'), ('alt="축제 목록 화면"', 'alt="Festivals"'), ('<h3>전국 축제</h3>', '<h3>Festivals across Korea</h3>'),
    ('진행 중·이번 주말·무료 축제를 날짜 순이나 가까운 순으로 볼 수 있어요. 끝난 축제는 저절로 빠져요.', 'See ongoing, this-weekend and free festivals by date or distance. Finished festivals drop off automatically.'),
    ('<span class="n">찜</span>', '<span class="n">Saved</span>'), ('alt="찜 화면"', 'alt="Saved"'), ('<h3>찜과 접수일 알림</h3>', '<h3>Saved &amp; sign-up alerts</h3>'),
    ('하트를 누른 강좌·축제가 모여요. 접수 알림을 켜면 접수 전날 저녁 8시와 접수 30분쯤 전에 알려 드려요. 가입 없이 폰 안에 저장돼요.',
     'Hearted classes and festivals gather here. Turn on an alert to be reminded at 8 pm the day before and about 30 minutes before sign-up opens. Saved on your phone without an account.'),
    ('<h2>로그인과 개인정보</h2>', '<h2>Sign-in &amp; privacy</h2>'),
    ('로그인은 <b>골라서</b> 하는 기능이에요. 로그인하지 않아도 지도·검색·찜·알림을 모두 쓸 수 있어요.', 'Sign-in is <b>optional</b>. Map, search, saved items and alerts all work without it.'),
    ('<tr><th>로그인 방법</th><td>카카오 로그인, 네이버 로그인(내 정보 메뉴)</td></tr>', '<tr><th>Sign-in</th><td>Kakao or NAVER (Me menu)</td></tr>'),
    ('<tr><th>로그인하는 이유</th><td>찜·접수일 알림·부모님 동네를 계정에 저장해서, 폰을 바꾸거나 앱을 다시 깔아도 이어 쓰기 위해서예요</td></tr>',
     '<tr><th>Why sign in</th><td>To keep saved items, alerts and parents’ neighborhoods when you change phones or reinstall</td></tr>'),
    ('<tr><th>네이버에서 받는 정보</th><td><b>회원 식별 번호와 별명</b>만 받아요. 이름·전화번호·이메일·생년월일은 받지 않아요</td></tr>',
     '<tr><th>Data from NAVER</th><td>Only the <b>member ID and nickname</b>. No name, phone, email or birthday</td></tr>'),
    ('<tr><th>정보를 쓰는 곳</th><td>회원 구분(식별 번호)과 내 정보 화면의 인사말(별명)에만 써요. 광고·마케팅에 쓰지 않아요</td></tr>',
     '<tr><th>Used for</th><td>Telling members apart (ID) and the greeting on the Me screen (nickname). Never for ads or marketing</td></tr>'),
    ('<tr><th>가입 나이</th><td>만 14세 이상만 가입할 수 있어요(로그인 단추 위 확인 칸)</td></tr>', '<tr><th>Age</th><td>14 or older (checkbox above the sign-in buttons)</td></tr>'),
    ('<tr><th>탈퇴</th><td>내 정보 › 계정 삭제를 누르면 계정과 찜이 바로 지워지고, 네이버·카카오 연결도 함께 끊어요</td></tr>',
     '<tr><th>Delete</th><td>Me › Delete account removes your account and saved items right away and disconnects NAVER or Kakao</td></tr>'),
    ('<tr><th>위치</th><td>지도 가운데를 정하는 데만 폰 안에서 쓰고, 서버로 보내지 않아요</td></tr>', '<tr><th>Location</th><td>Used only on your phone, never sent to a server</td></tr>'),
    ('<a href="/privacy.html">개인정보처리방침 전문</a> · <a href="/delete.html">계정 삭제 안내</a>', '<a href="/en/privacy.html">Full privacy policy</a> · <a href="/delete.html">Account deletion (Korean)</a>'),
    ('alt="내 정보 메뉴의 로그인 화면"', 'alt="Sign-in screen"'), ('내 정보 메뉴: 만 14세 확인 후 카카오·네이버 로그인', 'Me menu: confirm age 14+, then Kakao or NAVER'),
    ('alt="네이버 로그인 동의 화면"', 'alt="NAVER consent screen"'), ('네이버 동의 화면: 이용자 식별자·별명만 요청', 'NAVER consent: only member ID and nickname'),
    ('<h2>운영 원칙</h2>', '<h2>Principles</h2>'),
    ('기관이 <b>누구나 볼 수 있게 공개한 정보</b>만 모으고, 강좌마다 출처와 원문 링크를 함께 보여 줘요.', 'We collect only <b>information organizations publish for everyone</b>, and show the source and original link for every class.'),
    ('기관 누리집에는 사람이 보는 속도로, 하루에 정해진 횟수만 접속해요. 수집을 거절한 곳은 받지 않아요.', 'We visit websites at human speed, a limited number of times a day, and skip sites that refuse collection.'),
    ('자리·날짜는 모은 뒤 바뀔 수 있어서, 신청 전에 기관 화면을 한 번 더 확인하도록 안내해요.', 'Seats and dates can change after collection, so we ask you to double-check on the organization’s page.'),
    ('축제 정보는 한국관광공사 관광정보(TourAPI)를 쓰고, 사진에 출처를 적어요.', 'Festival data comes from Korea Tourism Organization (TourAPI), with photo credits.'),
    ('기관별 자료 출처 전체 목록은 <a href="/sources.html">자료 출처 페이지</a>에서 볼 수 있어요. 정보가 틀렸거나 빼 달라는 요청은 아래 메일로 보내 주세요.',
     'The full source list is on the <a href="/sources.html">sources page</a> (Korean). To report an error or ask us to remove information, email us below.'),
    ('<h2>문의</h2>', '<h2>Contact</h2>'), ('<tr><th>운영</th><td>컬처픽 (개인 개발)</td></tr>', '<tr><th>Operator</th><td>CulturePick (independent developer)</td></tr>'),
    ('<tr><th>메일</th><td>', '<tr><th>Email</th><td>'),
    ('<a href="/privacy.html">개인정보처리방침</a><a href="/delete.html">계정 삭제 안내</a><a href="/sources.html">자료 출처</a>',
     '<a href="/en/privacy.html">Privacy policy</a><a href="/delete.html">Account deletion</a><a href="/sources.html">Sources</a>'),
    ('© 2026 컬처픽 · 강좌 정보는 각 기관, 축제 정보는 한국관광공사 관광정보(TourAPI)에서 받아요.',
     '© 2026 CulturePick · Class information from each organization, festival information from Korea Tourism Organization (TourAPI).'),
]

# 한국어 페이지에 English 링크(없을 때만)
k = s
if '<a href="/en/">English</a>' not in k:
    k = k.replace('<a href="#contact">문의</a></nav>', '<a href="#contact">문의</a><a href="/en/">English</a></nav>', 1)
    k = k.replace('<a href="/sources.html">자료 출처</a></div>', '<a href="/sources.html">자료 출처</a><a href="/en/">English</a></div>', 1)
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(k)
e = k
miss = [a[:40] for a, b in R if a not in e]
for a, b in R:
    e = e.replace(a, b)
os.makedirs(os.path.join(HERE, "en"), exist_ok=True)
open(os.path.join(HERE, "en", "index.html"), "w", encoding="utf-8").write(e)
left = [x for x in re.findall(r">[^<]*[가-힣][^<]*<", e) if "한국어" not in x]
print("못 찾은 바꿀 글:", miss)
print("영어 페이지에 남은 한국어:", left[:10])
