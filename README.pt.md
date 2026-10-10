# XXD VPS

[中文](./README.md) · [English](./README.en.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [العربية](./README.ar.md) · [Español](./README.es.md) · [Français](./README.fr.md) · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · **Português**

Vai viajar para um país onde é difícil usar a internet? Continue usando os sites e as ferramentas de IA de sempre.

Como funciona: você compra seu próprio servidor no exterior, deixa uma IA configurá-lo com este projeto e importa uma assinatura no celular e no computador. A conexão é só sua; você não a divide com desconhecidos.

## O que você ganha

- **Sua própria conexão** para computador, celular e roteador. Há um nó principal e um de reserva: se um falhar, a conexão passa para o outro automaticamente.
- **Funciona assim que importar.** As regras para sites e ferramentas de IA comuns já vêm prontas. Sites da China continental conectam direto; todo o resto passa pelo seu servidor.
- **CLIProxyAPI**: seu próprio acesso à API e painel de administração, atualizado automaticamente para a versão mais recente.
- **Seguro**: o servidor só aceita a chave do seu computador e usa um certificado HTTPS de verdade, então o navegador nunca mostra "não seguro".
- **Quase sem manutenção**: certificados, regras e CLIProxyAPI se atualizam sozinhos, e a configuração tem backup todos os dias.

## Três passos

### 1. Compre um servidor

No momento, vá de **BandwagonHost**. A rede é estável e é o que eu mesmo uso:

**[Comprar BandwagonHost](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)**

[DMIT](https://www.dmit.io/aff.php?aff=23544) também é bom, mas está sem estoque agora. Não precisa esperar.

> Os dois são meus links de indicação. Posso receber uma comissão se você comprar por eles, e vou usar essa renda em trabalhos de caridade. Preços e estoque conforme os sites oficiais.

Escolha **Ubuntu 24.04** como sistema. Quando o servidor estiver pronto, anote três coisas do painel: **IP do servidor, senha de root (ou arquivo de chave) e porta SSH**.

### 2. Deixe uma IA configurar

Abra uma ferramenta de IA que consiga executar comandos no seu computador, como o [Codex](https://github.com/openai/codex) ou o [Claude Code](https://claude.com/claude-code) (no Windows, use dentro do WSL). Copie o texto abaixo, preencha e envie:

```text
Por favor, configure meu servidor novo com o plano "XXD VPS".

Plano: https://github.com/nevertoday/xiaoxiaodong-vps
Primeiro baixe este projeto no meu computador e leia por inteiro
skills/xiaoxiaodong-vps/SKILL.md. Siga exatamente os passos e as regras
de lá e use os scripts do projeto para configurar e verificar.
Fale comigo em português, por favor.

Meu servidor:
- IP:
- Acesso: senha inicial (deixe que eu mesmo digite no terminal)
- Usuário e porta SSH: padrão
- Nome que quero usar para entrar: bwg
```

Só três coisas mudam:

- **IP**: o IP do servidor que aparece no painel.
- **Acesso**: se o provedor deu um arquivo de chave, troque por `arquivo de chave: caminho do arquivo` (zip também serve).
- **Nome**: troque `bwg` pelo nome que quiser. Depois, basta digitar `ssh esse-nome` para entrar no servidor.

Se o usuário e a porta não forem root / 22, troque "padrão" pelos valores reais.

Aí é só esperar a IA terminar, normalmente de 10 a 20 minutos. Em algum momento ela vai pedir que você digite a senha do servidor no terminal. **Nunca cole a senha no chat.** Ao final, o acesso por senha é desligado e só este computador consegue entrar.

Se a IA não conseguir baixar o projeto, [baixe o ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) você mesmo, descompacte e acrescente uma linha ao texto: "O projeto já está em: caminho da pasta".

No final, aparece na sua área de trabalho o arquivo `XXD-VPS-seu-nome-login-pt.md` com:

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

### 3. Importe a assinatura

- **Computador**: instale o [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), importe a URL de assinatura do Clash, escolha o modo **Regra (Rule)** e ligue o **proxy do sistema**.
- **iPhone**: importe a URL de assinatura do Shadowrocket no Shadowrocket.
- **Roteador**: importe a URL de assinatura do Clash no OpenClash.

Depois abra <https://ipinfo.io>. Se aparecer o IP do seu servidor, você está conectado.

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

## Privacidade

- Este projeto não contém informação de nenhum servidor real.
- Senhas, chaves, URLs de assinatura e chaves de API de cada servidor são geradas do zero na configuração e ficam só no servidor e no seu computador. A IA não as mostra no chat.
- Não publique em lugar nenhum o seu arquivo de acesso, as URLs de assinatura ou as chaves, nem tire print deles.
- Para relatar um problema de segurança, veja [SECURITY.md](./SECURITY.md).

Conseguir conectar, e com que velocidade, também depende da rede local e da rota até o servidor. Este projeto garante que o servidor fique bem configurado, mas não que um mesmo IP seja alcançável de todos os países e operadoras.

## Licença

[MIT](./LICENSE)
