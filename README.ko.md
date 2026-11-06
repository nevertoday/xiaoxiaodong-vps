# XXD VPS

[中文](./README.md) · [English](./README.en.md) · **한국어** · [日本語](./README.ja.md) · [العربية](./README.ar.md) · [Español](./README.es.md) · [Français](./README.fr.md) · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · [Português](./README.pt.md)

인터넷 사용이 어려운 나라로 출장을 가도, 평소 쓰던 웹사이트와 AI 도구를 그대로 쓸 수 있습니다.

<a href="https://vps.xiaoxiaodong.ai/en/"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/readme/button-ko-dark.svg"><img src="docs/readme/button-ko-light.svg" alt="단계별 가이드 열기 · vps.xiaoxiaodong.ai/en"></picture></a>

단계별 튜토리얼 웹사이트(영어·중국어): <https://vps.xiaoxiaodong.ai/en/> (중국어판: <https://vps.xiaoxiaodong.ai>, 미러: <https://nevertoday.github.io/xiaoxiaodong-vps/en/>)

방법은 간단합니다. 내 컴퓨터에 Codex를 설치하고, 해외 서버를 한 대 사서, 이 프로젝트대로 Codex가 원격으로 설정하게 한 뒤, 휴대폰과 컴퓨터에 구독을 가져오면 됩니다. **서버에는 아무것도 설치하지 않고, 서버에 로그인할 필요도 없습니다.** 회선은 나만 쓰고, 모르는 사람과 공유하지 않습니다.

## 설정이 끝나면

- **나만의 회선**: 컴퓨터, 휴대폰, 공유기 모두 사용 가능. 주 노드와 예비 노드가 있어서 하나가 끊기면 자동으로 다른 쪽으로 바뀝니다.
- **가져오면 바로 사용**: 자주 쓰는 웹사이트와 AI 도구의 라우팅 규칙이 이미 설정되어 있습니다. 중국 본토 웹사이트는 직접 연결되고, 나머지는 내 서버를 거칩니다.
- **CLIProxyAPI**: 나만의 API 주소와 관리 화면. 최신 버전으로 자동 업데이트됩니다.
  - ⚠️ **Claude 계정을 CLIProxyAPI에 연결하지 마세요**: Anthropic 정책상 허용되지 않습니다. ChatGPT 등은 OpenAI가 공식적으로 괜찮다고 밝혔고, 저는 이미지 만들 때 즐겨 씁니다.
- **보안**: 서버는 내 컴퓨터의 키로만 로그인할 수 있고, 정식 HTTPS 인증서를 써서 "안전하지 않음" 경고가 뜨지 않습니다.
- **관리가 거의 필요 없음**: 인증서, 규칙, CLIProxyAPI가 스스로 업데이트되고, 설정은 매일 자동 백업됩니다.

## 네 단계로 시작

### 1. 컴퓨터에 Codex 설치

Codex는 OpenAI의 AI 앱으로, 유료 ChatGPT 요금제로 로그인합니다. 서버가 아니라 **내 컴퓨터**에 설치합니다.

- **처음이라면**: 데스크톱 앱을 설치하세요. Windows는 Microsoft Store에서 **Codex**를 검색해 설치하고, Mac은 [Codex 웹사이트](https://openai.com/codex/)에서 내려받으세요. 앱을 열고 ChatGPT 계정으로 로그인하면 됩니다.
- **익숙한 분이라면**: [Codex](https://github.com/openai/codex) 명령줄 버전을 쓰세요. 이미 설치했다면 터미널에서 `codex`를 실행하고 그대로 대화하면 됩니다.

ChatGPT 요금제가 없다면 [튜토리얼 웹사이트](https://vps.xiaoxiaodong.ai/en/guide/3-deploy/) 3단계의 "Type it yourself"(직접 입력) 방법을 따르세요.

### 2. 서버 구매

지금은 **BandwagonHost**를 바로 사는 것을 추천합니다. 저도 계속 쓰고 있습니다.

이런 서버를 추천하는 건 **제 돈을 쏟아붓고 호되게 당하면서 얻은 교훈**이기 때문입니다. 회선이 중국 본토에서의 연결에 맞춰 최적화되어 있고, 너무 안정적이라 저는 열성 팬이 되었습니다.

**[BandwagonHost 구매하기](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=88&billingcycle=quarterly&configoption%5B17%5D=55)**

이 링크의 요금제는 **매월 2TB 트래픽**, 메모리 2GB, 로스앤젤레스 CN2 GIA 데이터센터로 가족이 함께 써도 넉넉합니다.

전에 추천했던 ~~[1TB 요금제](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)~~는 현재 품절이라 구매할 수 없습니다.

[DMIT](https://www.dmit.io/aff.php?aff=23544)도 제가 즐겨 쓰는 서버지만, 아쉽게도 현재 품절입니다. 기다릴 필요는 없습니다.

**왜 이 두 곳만 추천할까요?** BandwagonHost와 DMIT는 제가 여러 번 테스트한 끝에 남긴 두 곳이고, 지금 마음 놓고 추천할 수 있는 유일한 곳입니다. 위 링크의 요금제는 두 곳에서 현재 재고가 있는 유일한 입문용 요금제이기도 합니다. 다른 곳의 서버는 겉보기엔 괜찮아도 실제로는 함정이 많습니다. 평소엔 쓸 만하다가 상황이 민감해지면 버티지 못하고 끊기거나 아예 연결되지 않으며, AI 서비스를 쓰다가 계정에까지 문제가 생길 수 있습니다. 저는 이런 일로 몇 번이나 고생해서 이제 정말 지쳤습니다. 그래서 제가 겪은 시행착오를 반복하지 않도록 여기서 바로 구매하시길 권합니다.

> 모두 제 추천 링크입니다. 이 링크로 구매하면 제가 수수료를 받을 수 있으며, 그 수입은 자선 활동에 쓰겠습니다. 가격과 재고는 공식 사이트 기준입니다.

운영체제는 **Ubuntu 24.04**를 선택하세요. 개통되면 관리 화면에서 세 가지를 적어 두세요: **서버 IP, root 비밀번호(또는 키 파일), SSH 포트**. BandwagonHost라면 **VEID와 API Key**도 적어 두세요(KiwiVM 왼쪽 메뉴의 「API」 페이지, [찾는 방법](https://vps.xiaoxiaodong.ai/en/howto/traffic-and-ip/)). 그래야 클라이언트에 표시되는 트래픽이 관리 화면과 일치합니다.

구매한 뒤에는 서버에 로그인하거나 무언가를 설치할 필요가 없습니다. 다음 단계는 Codex가 맡습니다.

### 3. Codex에게 설정 맡기기

1단계에서 설치한 Codex를 여세요(내 컴퓨터에서 명령을 실행할 수 있는 다른 AI 도구도 됩니다). 아래 문구를 복사해 채운 뒤 보내세요.

```text
「XXD VPS」 방식으로 새로 산 서버를 설정해 주세요.

방식 주소: https://github.com/nevertoday/xiaoxiaodong-vps
먼저 이 프로젝트를 내 컴퓨터에 내려받고 skills/xiaoxiaodong-vps/SKILL.md를
끝까지 읽은 뒤, 그 단계와 규칙을 그대로 따라 프로젝트의 스크립트로
설정과 검증을 마쳐 주세요. 대화는 한국어로 해 주세요.

내 서버:
- IP:
- 로그인 방식: 초기 비밀번호 (제가 직접 입력하게 해 주세요. 채팅으로 보내라고 하지 마세요)
- SSH 사용자와 포트: 기본값
- 앞으로 로그인할 때 쓸 이름: bwg
- BandwagonHost VEID와 API Key (공식 트래픽 사용량용. BandwagonHost가 아니면 이 줄을 지우세요):
```

채울 곳은 다음과 같습니다.

- **IP**: 관리 화면에 보이는 서버 IP.
- **로그인 방식**: 업체가 키 파일을 줬다면 `키 파일: 파일 경로`로 바꾸세요 (zip도 됩니다).
- **이름**: `bwg`를 원하는 이름으로 바꾸세요. 이후 `ssh 그이름`만 입력하면 서버에 로그인됩니다.
- **BandwagonHost**: 마지막 줄에 VEID와 API Key를 채우세요. 클라이언트의 트래픽 한도·사용량·초기화일을 BandwagonHost 관리 화면에서 바로 읽어 와 1TB·2TB 요금제 모두 맞게 표시됩니다. **BandwagonHost가 아니면 그 줄을 지우세요.** 그때는 매월 1000GB 기준으로 표시됩니다.

사용자와 포트가 root / 22가 아니라면 "기본값"을 실제 값으로 바꾸세요.

그다음 AI가 끝낼 때까지 기다리면 됩니다. 보통 10~20분 걸립니다. 중간에 컴퓨터에 비밀번호 입력 창이 뜨면 서버 비밀번호를 한 번 입력하세요. **비밀번호를 채팅에 붙여 넣지 마세요.** 설정이 끝나면 비밀번호 로그인이 꺼지고, 이 컴퓨터에서만 로그인할 수 있습니다.

AI가 프로젝트를 내려받지 못하면 직접 [ZIP을 내려받아](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) 압축을 풀고, 위 문구에 "프로젝트는 이미 여기 있습니다: 폴더 경로"라고 한 줄 추가하세요.

완료되면 바탕화면에 `my-server-이름-subscriptions-and-accounts-ko.md` 파일이 생깁니다. 안에는:

- 컴퓨터·공유기용 **Clash 구독 주소**, iPhone용 **Shadowrocket 구독 주소**
- 3x-ui 패널 주소, 사용자 이름, 비밀번호
- CLIProxyAPI 관리 화면 주소, 관리 로그인 키, API 주소, API 키

<details>
<summary>서버를 자주 설정하나요? skill로 설치하면 한 문장으로 부를 수 있습니다</summary>

터미널에서 한 번 실행하세요.

```bash
git clone https://github.com/nevertoday/xiaoxiaodong-vps.git
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.claude/skills/
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.codex/skills/
```

이후 AI에게 "xiaoxiaodong-vps로 새 서버를 설정해 줘"라고만 하면, 필요한 서버 정보를 AI가 물어봅니다.

</details>

### 4. 구독 가져오기

- **컴퓨터 (Clash Verge Rev 권장)**: [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases)를 설치하고 Clash 구독 주소를 가져온 뒤, **규칙(Rule)** 모드를 고르고 **TUN 모드**(가상 네트워크 어댑터, 안내가 나오면 서비스 설치)를 켜세요. 시스템 프록시만 켜면 브라우저의 WebRTC로 실제 IP가 드러날 수 있습니다. [WebRTC 유출 해결 가이드](./docs/Clash-Verge-WebRTC泄露修复手册.md)(중국어, AI 도우미가 단계별로 따라 할 수 있게 작성됨)를 참고하세요.
- **iPhone**: Shadowrocket에서 Shadowrocket 구독 주소를 가져오세요.
- **공유기(OpenClash)**: 같은 Clash 구독 주소를 그대로 쓸 수 있어 집 안의 모든 기기가 이 회선을 씁니다. '구성 구독'에 주소를 추가하세요(YAML 파일을 업로드하면 사용량이 표시되지 않고 규칙도 자동 업데이트되지 않습니다). '온라인 구독 변환'은 끄고 코어는 Meta를 고르세요.
- **이미 v2rayN을 쓰고 있다면 (Windows / Mac / Linux)**: 사용할 수 있지만 대안일 뿐입니다. "Shadowrocket (iPhone)" 줄의 구독 주소를 가져오고(Clash 줄이 아님), 라우팅은 "중국 본토 우회"를 고르고, WebRTC 유출을 막도록 TUN을 켜세요. 이 구독에는 노드만 있고 AI 분류나 WeChat 직결 규칙이 없으므로, 컴퓨터에서는 계속 Clash Verge Rev를 권장합니다. 자세한 내용은 [v2rayN 가이드](https://vps.xiaoxiaodong.ai/en/howto/v2rayn/)(영어).

그다음 <https://ip.net.coffee/claude/>를 열어 내 서버의 IP가 보이면 연결된 것입니다.

## 출장 전에

- **떠나기 전에 설정하고 한 번 테스트하세요.** 제한된 네트워크에 도착하면 프로젝트를 내려받거나 AI 도구를 여는 것조차 어려워질 수 있습니다.
- 휴대폰과 컴퓨터 모두 클라이언트를 설치하고 구독을 가져와서, 두 노드가 모두 연결되는지 확인하세요.
- 현지의 어떤 네트워크에서 서버에 연결되지 않으면 먼저 다른 네트워크로 바꿔 보세요 (호텔 Wi-Fi, 모바일 데이터, 다른 통신사). 모두 안 되면 그 지역에서 서버 IP가 막혔을 가능성이 큽니다. 설정으로는 해결되지 않으니 업체에 IP 교체를 요청하세요.
- 회선은 본인과 가족만 쓰고, 다른 사람과 공유하지 마세요.

## 나중에 서버 점검하기

아래 문구를 AI에게 보내세요 (`bwg`는 내 이름으로 바꾸기).

```text
「XXD VPS」 방식으로 내 서버를 점검해 주세요: ssh bwg

방식 주소: https://github.com/nevertoday/xiaoxiaodong-vps
프로젝트를 내려받아 skills/xiaoxiaodong-vps/SKILL.md의
"以后的复核和维护"(이후 점검과 유지보수) 부분을 읽어 주세요.
먼저 점검만 하고, 실패한 항목과 이유를 알려 준 뒤 제가 동의하면 고쳐 주세요.
비밀번호, 구독 주소, 키는 채팅에 표시하지 마세요. 대화는 한국어로 해 주세요.
```

자세한 문서([문제 해결](./skills/xiaoxiaodong-vps/references/troubleshooting.md), [설계 설명](./skills/xiaoxiaodong-vps/references/design.md))는 현재 중국어로만 있습니다. AI가 대신 읽어 줄 수 있습니다.

## 피드백과 제안

제안이 있거나 설명이 불분명한 곳, 그대로 따라 해도 안 되는 부분을 발견하면 [GitHub에 Issue를 남겨 주세요](https://github.com/nevertoday/xiaoxiaodong-vps/issues). [X로 DM](https://x.com/xiaoxiaodong)(@xiaoxiaodong)을 보내거나 위챗(WeChat)으로 저(Xiaoxiaodong, 小小东)를 추가해 알려 주셔도 됩니다. 가이드에 반영하겠습니다.

<img src="https://vip.xiaoxiaodong.ai/site-assets/wechat-qr.png" width="160" alt="Xiaoxiaodong의 위챗 QR 코드">

## 개인정보

- 이 프로젝트에는 실제 서버 정보가 전혀 들어 있지 않습니다.
- 서버마다 비밀번호, 키, 구독 주소, API 키를 설정할 때 새로 만들고, 서버와 내 컴퓨터에만 저장합니다. AI는 이것들을 채팅에 보여 주지 않습니다.
- 로그인 정보 파일, 구독 주소, 키는 어디에도 올리거나 캡처하지 마세요.
- 보안 문제는 [SECURITY.md](./SECURITY.md)를 참고하세요.

연결이 되는지, 속도가 어떤지는 현지 네트워크와 서버 회선에도 달려 있습니다. 이 프로젝트는 서버가 올바르게 설정되도록 보장하지만, 모든 나라와 통신사에서 같은 IP에 연결된다고 보장할 수는 없습니다.

## 라이선스

[MIT](./LICENSE)
