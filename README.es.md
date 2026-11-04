# XXD VPS

[中文](./README.md) · [English](./README.en.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [العربية](./README.ar.md) · **Español** · [Français](./README.fr.md) · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · [Português](./README.pt.md)

¿Viajas a un país donde usar internet es complicado? Sigue usando las webs y herramientas de IA de siempre.

Sitio web con el tutorial paso a paso (en inglés y chino): <https://vps.xiaoxiaodong.ai/en/> (versión en chino: <https://vps.xiaoxiaodong.ai>; espejo: <https://nevertoday.github.io/xiaoxiaodong-vps/en/>)

Cómo funciona: instalas Codex en tu propio ordenador, compras un servidor en el extranjero, dejas que Codex lo configure a distancia con este proyecto e importas una suscripción en tu móvil y tu ordenador. **No instalas nada en el servidor ni tienes que entrar en él.** La conexión es solo tuya; no la compartes con desconocidos.

## Qué obtienes

- **Tu propia conexión** para ordenador, móvil y router. Hay un nodo principal y uno de respaldo: si uno falla, cambia al otro automáticamente.
- **Funciona nada más importarla.** Las reglas para las webs y herramientas de IA más comunes ya vienen configuradas. Las webs de China continental se conectan directamente; todo lo demás pasa por tu servidor.
- **CLIProxyAPI**: tu propio punto de acceso a la API y panel de administración, que se actualiza solo a la última versión.
  - ⚠️ **No conectes una cuenta de Claude a CLIProxyAPI**: la política de Anthropic no lo permite. OpenAI ha dicho que las cuentas de ChatGPT sí se pueden usar así; a mí me encanta usarlo para crear imágenes.
- **Seguro**: el servidor solo acepta la clave de tu ordenador y usa un certificado HTTPS de verdad, así que el navegador nunca avisa de "no seguro".
- **Casi sin mantenimiento**: los certificados, las reglas y CLIProxyAPI se actualizan solos, y la configuración se copia cada día.

## Cuatro pasos

### 1. Instala Codex en tu ordenador

Codex es la app de IA de OpenAI; se entra con un plan de pago de ChatGPT. Se instala en **tu propio ordenador**, no en el servidor.

- **Si empiezas de cero**: instala la app de escritorio. En Windows, busca **Codex** en Microsoft Store e instálala; en Mac, descárgala desde la [web de Codex](https://openai.com/codex/). Ábrela e inicia sesión con tu cuenta de ChatGPT.
- **Si tienes experiencia**: usa [Codex](https://github.com/openai/codex) en la línea de comandos. ¿Ya lo tienes instalado? Ejecuta `codex` en la terminal y háblale directamente.

¿No tienes plan de ChatGPT? En el paso 3 del [sitio web del tutorial](https://vps.xiaoxiaodong.ai/en/guide/3-deploy/) hay una vía "Type it yourself" (escribirlo todo tú).

### 2. Compra un servidor

Ahora mismo, elige **BandwagonHost**; es el que uso yo.

Recomiendo este tipo de servidor porque es **una lección que pagué con mi dinero y aprendí a base de golpes**: sus rutas están optimizadas para conectarse desde China continental y son tan estables que me he vuelto fan incondicional.

**[Comprar BandwagonHost](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=88&billingcycle=quarterly&configoption%5B17%5D=55)**

El plan de este enlace incluye **2 TB de tráfico al mes** y 2 GB de RAM, en un centro de datos CN2 GIA de Los Ángeles: de sobra para ti y tu familia.

El ~~[plan de 1 TB](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)~~ que recomendaba antes está agotado y ahora no se puede comprar.

[DMIT](https://www.dmit.io/aff.php?aff=23544) es otro que me encanta usar, pero por desgracia ahora está agotado. No hace falta esperar.

**¿Por qué solo recomiendo estos dos?** BandwagonHost y DMIT son los dos con los que me quedé después de muchas pruebas, y los únicos que hoy puedo recomendar con tranquilidad. El plan del enlace de arriba es, además, el único plan de entrada que tienen disponible ahora mismo. Muchos otros proveedores parecen buenos al principio, pero tienen muchas trampas: funcionan los días normales y, cuando la situación se complica, no aguantan; la conexión se cae o no llega a conectar, y con servicios de IA eso puede incluso poner en riesgo tu cuenta. Me he llevado tantos disgustos con esto que ya estoy cansado, así que te recomiendo comprar aquí y ahorrarte los rodeos que yo tuve que dar.

> Todos son enlaces de referido míos. Puede que reciba una comisión si compras a través de ellos, y destinaré ese dinero a labores benéficas. Precios y disponibilidad según las webs oficiales.

Elige **Ubuntu 24.04** como sistema. Cuando el servidor esté listo, apunta tres datos del panel: **IP del servidor, contraseña de root (o archivo de clave) y puerto SSH**. Si es BandwagonHost, apunta también el **VEID y la API Key** (página «API» del menú izquierdo de KiwiVM, [cómo encontrarlos](https://vps.xiaoxiaodong.ai/en/howto/traffic-and-ip/)) para que el tráfico que muestran las apps coincida con el panel.

Después de comprarlo no tienes que entrar en el servidor ni instalar nada en él: el siguiente paso es cosa de Codex.

### 3. Deja que Codex lo configure

Abre el Codex del paso 1 (también vale cualquier otra herramienta de IA que pueda ejecutar comandos en tu ordenador). Copia el texto de abajo, rellénalo y envíalo:

```text
Configura mi nuevo servidor con el plan "XXD VPS", por favor.

Plan: https://github.com/nevertoday/xiaoxiaodong-vps
Primero descarga este proyecto en mi ordenador y lee entero
skills/xiaoxiaodong-vps/SKILL.md. Sigue sus pasos y reglas al pie de la letra
y usa los scripts del proyecto para configurar y verificar.
Háblame en español, por favor.

Mi servidor:
- IP:
- Acceso: contraseña inicial (déjame escribirla yo; no me pidas que la envíe por el chat)
- Usuario y puerto SSH: por defecto
- Nombre con el que quiero entrar: bwg
- VEID y API Key de BandwagonHost (para el consumo oficial de tráfico; borra esta línea si no es BandwagonHost):
```

Qué rellenar:

- **IP**: la IP del servidor que aparece en el panel.
- **Acceso**: si tu proveedor te dio un archivo de clave, cámbialo por `archivo de clave: ruta del archivo` (un zip vale).
- **Nombre**: cambia `bwg` por el nombre que quieras. Después, con escribir `ssh ese-nombre` entrarás en el servidor.
- **BandwagonHost**: rellena el VEID y la API Key en la última línea. Así las apps leen el cupo de tráfico, el consumo y el día de reinicio directamente de BandwagonHost, y cuadran tanto en el plan de 1 TB como en el de 2 TB. **¿No es BandwagonHost? Borra esa línea**; entonces se muestra sobre 1000 GB al mes.

Si el usuario y el puerto no son root / 22, cambia "por defecto" por los valores reales.

Luego espera a que la IA termine, normalmente entre 10 y 20 minutos. En algún momento aparecerá en tu ordenador una ventana para la contraseña; escribe ahí la contraseña del servidor una vez. **No pegues nunca la contraseña en el chat.** Al terminar, el acceso con contraseña queda desactivado y solo este ordenador puede entrar.

Si la IA no puede descargar el proyecto, [descarga el ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) tú mismo, descomprímelo y añade una línea al texto: "El proyecto ya está en: ruta de la carpeta".

Al terminar aparecerá en tu escritorio el archivo `my-server-tu-nombre-subscriptions-and-accounts-es.md` con:

- la **URL de suscripción de Clash** para ordenador y router, y la **URL de suscripción de Shadowrocket** para iPhone;
- la dirección, el usuario y la contraseña del panel 3x-ui;
- la dirección del panel de CLIProxyAPI, su clave de acceso, la dirección de la API y la clave de API.

<details>
<summary>¿Configuras servidores a menudo? Instálalo como skill y llámalo con una frase</summary>

Ejecútalo una vez en la terminal:

```bash
git clone https://github.com/nevertoday/xiaoxiaodong-vps.git
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.claude/skills/
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.codex/skills/
```

A partir de ahí, basta con decirle a la IA "usa xiaoxiaodong-vps para configurar mi nuevo servidor" y ella te pedirá los datos.

</details>

### 4. Importa la suscripción

- **Ordenador (recomendado: Clash Verge Rev)**: instala [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), importa la URL de suscripción de Clash, elige el modo **Regla (Rule)** y activa el **modo TUN** (tarjeta de red virtual; instala el servicio cuando lo pida). Con solo el proxy del sistema, el WebRTC del navegador puede revelar tu IP real: consulta la [guía para corregir fugas de WebRTC](./docs/Clash-Verge-WebRTC泄露修复手册.md) (en chino, escrita para que un asistente de IA pueda seguirla paso a paso).
- **iPhone**: importa la URL de suscripción de Shadowrocket en Shadowrocket.
- **Router (OpenClash)**: la misma URL de suscripción de Clash funciona, así todos los dispositivos de casa usan la línea. Añádela en la suscripción de configuración (no subas el archivo YAML, o no verás el uso de datos y las reglas no se actualizarán solas), desactiva la conversión de suscripción en línea y usa el núcleo Meta.
- **Si ya usas v2rayN (Windows / Mac / Linux)**: funciona, pero solo como alternativa. Importa la URL de la fila «Shadowrocket (iPhone)» (no la de Clash), elige el enrutamiento «evitar China continental» y activa TUN contra las fugas de WebRTC. Esa suscripción solo trae los nodos, sin las reglas de IA ni de WeChat directo, así que en el ordenador seguimos recomendando Clash Verge Rev. Consulta la [guía de v2rayN](https://vps.xiaoxiaodong.ai/en/howto/v2rayn/) (en inglés).

Después abre <https://ip.net.coffee/claude/>. Si muestra la IP de tu servidor, ya estás conectado.

## Antes de viajar

- **Déjalo todo configurado y probado antes de salir.** En una red restringida, descargar el proyecto o incluso abrir herramientas de IA puede volverse mucho más difícil.
- Instala los clientes e importa las suscripciones en el móvil y en el ordenador, y comprueba que los dos nodos conectan.
- Si alguna red local no llega a tu servidor, prueba primero otra (wifi del hotel, datos móviles, otro operador). Si no funciona ninguna, lo más probable es que la IP del servidor esté bloqueada allí. Ningún cambio de configuración lo arregla: pide a tu proveedor una IP nueva.
- Usa la conexión solo tú y tu familia. No la compartas.

## Revisar el servidor más adelante

Envía esto a la IA (cambia `bwg` por tu nombre):

```text
Revisa mi servidor con el plan "XXD VPS", por favor: ssh bwg

Plan: https://github.com/nevertoday/xiaoxiaodong-vps
Descarga el proyecto y lee la parte "以后的复核和维护" (revisiones y
mantenimiento posteriores) de skills/xiaoxiaodong-vps/SKILL.md.
Primero solo revisa, dime qué falló y por qué, y no arregles nada hasta que yo diga que sí.
No muestres contraseñas, URLs de suscripción ni claves en el chat. Háblame en español.
```

La documentación detallada ([solución de problemas](./skills/xiaoxiaodong-vps/references/troubleshooting.md), [notas de diseño](./skills/xiaoxiaodong-vps/references/design.md)) de momento solo está en chino; tu IA puede leerla por ti.

## Comentarios y sugerencias

¿Tienes una sugerencia, o algo no está claro o no funciona como se describe? [Abre un issue en GitHub](https://github.com/nevertoday/xiaoxiaodong-vps/issues), [escríbeme por X](https://x.com/xiaoxiaodong) (@xiaoxiaodong) o agrégame en WeChat (Xiaoxiaodong, 小小东). Lo incorporaré a la guía.

<img src="https://vip.xiaoxiaodong.ai/site-assets/wechat-qr.png" width="160" alt="Código QR de WeChat de Xiaoxiaodong">

## Privacidad

- Este proyecto no contiene información de ningún servidor real.
- Las contraseñas, claves, URLs de suscripción y claves de API de cada servidor se generan de nuevo durante la configuración y solo se guardan en el servidor y en tu ordenador. La IA no las muestra en el chat.
- No publiques en ningún sitio tu archivo de acceso, las URLs de suscripción ni las claves, ni les hagas capturas.
- Para informar de un problema de seguridad, consulta [SECURITY.md](./SECURITY.md).

Que puedas conectarte, y a qué velocidad, también depende de la red local y de la ruta del servidor. Este proyecto se asegura de que el servidor quede bien configurado, pero no puede garantizar que una misma IP sea accesible desde todos los países y operadores.

## Licencia

[MIT](./LICENSE)
