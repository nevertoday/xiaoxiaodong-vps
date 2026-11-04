# XXD VPS

[中文](./README.md) · [English](./README.en.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [العربية](./README.ar.md) · [Español](./README.es.md) · [Français](./README.fr.md) · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · **Português**

Vai viajar para um país onde é difícil usar a internet? Continue usando os sites e as ferramentas de IA de sempre.

Site com o tutorial passo a passo (em inglês e chinês): <https://vps.xiaoxiaodong.ai/en/> (versão em chinês: <https://vps.xiaoxiaodong.ai>; espelho: <https://nevertoday.github.io/xiaoxiaodong-vps/en/>)

Como funciona: você instala o Codex no seu próprio computador, compra um servidor no exterior, deixa o Codex configurá-lo remotamente com este projeto e importa uma assinatura no celular e no computador. **Você não instala nada no servidor nem precisa entrar nele.** A conexão é só sua; você não a divide com desconhecidos.

## O que você ganha

- **Sua própria conexão** para computador, celular e roteador. Há um nó principal e um de reserva: se um falhar, a conexão passa para o outro automaticamente.
- **Funciona assim que importar.** As regras para sites e ferramentas de IA comuns já vêm prontas. Sites da China continental conectam direto; todo o resto passa pelo seu servidor.
- **CLIProxyAPI**: seu próprio acesso à API e painel de administração, atualizado automaticamente para a versão mais recente.
  - ⚠️ **Não conecte uma conta do Claude ao CLIProxyAPI**: a política da Anthropic não permite. A OpenAI disse que contas do ChatGPT podem ser usadas assim — eu, pessoalmente, adoro usar para criar imagens.
- **Seguro**: o servidor só aceita a chave do seu computador e usa um certificado HTTPS de verdade, então o navegador nunca mostra "não seguro".
- **Quase sem manutenção**: certificados, regras e CLIProxyAPI se atualizam sozinhos, e a configuração tem backup todos os dias.

## Quatro passos

### 1. Instale o Codex no computador

O Codex é o app de IA da OpenAI; você entra com um plano pago do ChatGPT. Ele vai no **seu próprio computador**, não no servidor.

- **Iniciantes**: instale o app para desktop. No Windows, procure **Codex** na Microsoft Store e instale; no Mac, baixe no [site do Codex](https://openai.com/codex/). Abra e entre com sua conta do ChatGPT.
- **Quem já tem experiência**: use o [Codex](https://github.com/openai/codex) na linha de comando. Já instalou? Rode `codex` no terminal e é só conversar com ele.

Não tem plano do ChatGPT? O passo 3 do [site do tutorial](https://vps.xiaoxiaodong.ai/en/guide/3-deploy/) tem um caminho "Type it yourself" (digitar tudo você mesmo).

### 2. Compre um servidor

No momento, vá de **BandwagonHost**; é o que eu mesmo uso.

Recomendo esse tipo de servidor porque é **uma lição que paguei do meu bolso e aprendi da forma mais dura**: as rotas são otimizadas para conexões a partir da China continental, e são tão estáveis que virei fã de carteirinha.

**[Comprar BandwagonHost](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=88&billingcycle=quarterly&configoption%5B17%5D=55)**

O plano deste link inclui **2 TB de tráfego por mês** e 2 GB de RAM, em um data center CN2 GIA de Los Angeles — mais do que suficiente para você e sua família.

O ~~[plano de 1 TB](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)~~ que eu recomendava antes está sem estoque e não dá para comprar agora.

[DMIT](https://www.dmit.io/aff.php?aff=23544) é outro que eu gosto muito de usar, mas infelizmente está sem estoque agora. Não precisa esperar.

> Todos são meus links de indicação. Posso receber uma comissão se você comprar por eles, e vou usar essa renda em trabalhos de caridade. Preços e estoque conforme os sites oficiais.

Escolha **Ubuntu 24.04** como sistema. Quando o servidor estiver pronto, anote três coisas do painel: **IP do servidor, senha de root (ou arquivo de chave) e porta SSH**. No BandwagonHost, anote também o **VEID e a API Key** (página “API” no menu esquerdo do KiwiVM, [como encontrar](https://vps.xiaoxiaodong.ai/en/howto/traffic-and-ip/)) para que o tráfego mostrado nos apps bata com o painel.

Depois da compra, você não entra no servidor nem instala nada nele — o próximo passo é com o Codex.

### 3. Deixe o Codex configurar

Abra o Codex do passo 1 (qualquer outra ferramenta de IA que consiga executar comandos no seu computador também serve). Copie o texto abaixo, preencha e envie:

```text
Por favor, configure meu servidor novo com o plano "XXD VPS".

Plano: https://github.com/nevertoday/xiaoxiaodong-vps
Primeiro baixe este projeto no meu computador e leia por inteiro
skills/xiaoxiaodong-vps/SKILL.md. Siga exatamente os passos e as regras
de lá e use os scripts do projeto para configurar e verificar.
Fale comigo em português, por favor.

Meu servidor:
- IP:
- Acesso: senha inicial (deixe que eu mesmo digite; não me peça para mandá-la no chat)
- Usuário e porta SSH: padrão
- Nome que quero usar para entrar: bwg
- VEID e API Key do BandwagonHost (para o uso oficial de tráfego; apague esta linha se não for BandwagonHost):
```

O que preencher:

- **IP**: o IP do servidor que aparece no painel.
- **Acesso**: se o provedor deu um arquivo de chave, troque por `arquivo de chave: caminho do arquivo` (zip também serve).
- **Nome**: troque `bwg` pelo nome que quiser. Depois, basta digitar `ssh esse-nome` para entrar no servidor.
- **BandwagonHost**: preencha o VEID e a API Key na última linha. Assim os apps leem a cota de tráfego, o uso e o dia de reinício direto do BandwagonHost, e batem tanto no plano de 1 TB quanto no de 2 TB. **Não é BandwagonHost? Apague essa linha**; o uso aparece sobre 1000 GB por mês.

Se o usuário e a porta não forem root / 22, troque "padrão" pelos valores reais.

Aí é só esperar a IA terminar, normalmente de 10 a 20 minutos. Em algum momento vai aparecer uma janela de senha no seu computador; digite nela a senha do servidor uma vez. **Nunca cole a senha no chat.** Ao final, o acesso por senha é desligado e só este computador consegue entrar.

Se a IA não conseguir baixar o projeto, [baixe o ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) você mesmo, descompacte e acrescente uma linha ao texto: "O projeto já está em: caminho da pasta".

No final, aparece na sua área de trabalho o arquivo `my-server-seu-nome-subscriptions-and-accounts-pt.md` com:

- a **URL de assinatura do Clash** para computador e roteador, e a **URL de assinatura do Shadowrocket** para iPhone;
- endereço, usuário e senha do painel 3x-ui;
- endereço do painel do CLIProxyAPI, a chave de acesso dele, o endereço da API e a chave de API.

<details>
<summary>Configura servidores com frequência? Instale como skill e chame com uma frase</summary>

Rode uma vez no terminal:

```bash
git clone https://github.com/nevertoday/xiaoxiaodong-vps.git
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.claude/skills/
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.codex/skills/
```

Depois disso, basta dizer à IA "use xiaoxiaodong-vps para configurar meu servidor novo" e ela pergunta os dados.

</details>

### 4. Importe a assinatura

- **Computador (recomendado: Clash Verge Rev)**: instale o [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), importe a URL de assinatura do Clash, escolha o modo **Regra (Rule)** e ligue o **modo TUN** (placa de rede virtual; instale o serviço quando solicitado). Só com o proxy do sistema, o WebRTC do navegador pode revelar seu IP real — veja o [guia de correção de vazamento de WebRTC](./docs/Clash-Verge-WebRTC泄露修复手册.md) (em chinês, escrito para que um assistente de IA possa segui-lo passo a passo).
- **iPhone**: importe a URL de assinatura do Shadowrocket no Shadowrocket.
- **Roteador (OpenClash)**: a mesma URL de assinatura do Clash funciona, e todos os aparelhos de casa usam a linha. Adicione-a na assinatura de configuração (não envie o arquivo YAML, senão o uso de dados não aparece e as regras não se atualizam sozinhas), desative a conversão de assinatura online e use o núcleo Meta.
- **Já usa o v2rayN (Windows / Mac / Linux)**: funciona, mas só como alternativa. Importe a URL da linha "Shadowrocket (iPhone)" (não a do Clash), escolha o roteamento "ignorar China continental" e ative o TUN contra vazamentos de WebRTC. Essa assinatura traz só os nós, sem as regras de IA nem de WeChat direto, por isso no computador continuamos recomendando o Clash Verge Rev. Veja o [guia do v2rayN](https://vps.xiaoxiaodong.ai/en/howto/v2rayn/) (em inglês).

Depois abra <https://ip.net.coffee/claude/>. Se aparecer o IP do seu servidor, você está conectado.

## Antes de viajar

- **Configure e teste tudo antes de sair.** Numa rede restrita, baixar o projeto ou até abrir ferramentas de IA pode ficar bem mais difícil.
- Instale os clientes e importe as assinaturas no celular e no computador, e confira se os dois nós conectam.
- Se alguma rede local não alcançar seu servidor, tente outra primeiro (Wi-Fi do hotel, dados móveis, outra operadora). Se nenhuma funcionar, o IP do servidor provavelmente está bloqueado lá. Nenhuma configuração resolve isso: peça um IP novo ao provedor.
- Use a conexão só você e sua família. Não compartilhe.

## Verificar o servidor depois

Envie isto para a IA (troque `bwg` pelo seu nome):

```text
Por favor, verifique meu servidor com o plano "XXD VPS": ssh bwg

Plano: https://github.com/nevertoday/xiaoxiaodong-vps
Baixe o projeto e leia a parte "以后的复核和维护" (verificação e
manutenção posteriores) de skills/xiaoxiaodong-vps/SKILL.md.
Primeiro só verifique, diga o que falhou e por quê, e não corrija nada sem eu concordar.
Não mostre senhas, URLs de assinatura nem chaves no chat. Fale comigo em português.
```

A documentação detalhada ([solução de problemas](./skills/xiaoxiaodong-vps/references/troubleshooting.md), [notas de projeto](./skills/xiaoxiaodong-vps/references/design.md)) por enquanto só existe em chinês; sua IA pode ler por você.

## Comentários e sugestões

Tem uma sugestão, ou algo não está claro ou não funciona como descrito? [Abra uma issue no GitHub](https://github.com/nevertoday/xiaoxiaodong-vps/issues), [me mande uma mensagem no X](https://x.com/xiaoxiaodong) (@xiaoxiaodong) ou me adicione no WeChat (Xiaoxiaodong, 小小东). Vou incluir no guia.

<img src="https://vip.xiaoxiaodong.ai/site-assets/wechat-qr.png" width="160" alt="QR code do WeChat de Xiaoxiaodong">

## Privacidade

- Este projeto não contém informação de nenhum servidor real.
- Senhas, chaves, URLs de assinatura e chaves de API de cada servidor são geradas do zero na configuração e ficam só no servidor e no seu computador. A IA não as mostra no chat.
- Não publique em lugar nenhum o seu arquivo de acesso, as URLs de assinatura ou as chaves, nem tire print deles.
- Para relatar um problema de segurança, veja [SECURITY.md](./SECURITY.md).

Conseguir conectar, e com que velocidade, também depende da rede local e da rota até o servidor. Este projeto garante que o servidor fique bem configurado, mas não que um mesmo IP seja alcançável de todos os países e operadoras.

## Licença

[MIT](./LICENSE)
