# XXD VPS

[中文](./README.md) · [English](./README.en.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [العربية](./README.ar.md) · **Español** · [Français](./README.fr.md) · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · [Português](./README.pt.md)

¿Viajas a un país donde usar internet es complicado? Sigue usando las webs y herramientas de IA de siempre.

Cómo funciona: compras tu propio servidor en el extranjero, dejas que una IA lo configure con este proyecto e importas una suscripción en tu móvil y tu ordenador. La conexión es solo tuya; no la compartes con desconocidos.

## Qué obtienes

- **Tu propia conexión** para ordenador, móvil y router. Hay un nodo principal y uno de respaldo: si uno falla, cambia al otro automáticamente.
- **Funciona nada más importarla.** Las reglas para las webs y herramientas de IA más comunes ya vienen configuradas. Las webs de China continental se conectan directamente; todo lo demás pasa por tu servidor.
- **CLIProxyAPI**: tu propio punto de acceso a la API y panel de administración, que se actualiza solo a la última versión.
- **Seguro**: el servidor solo acepta la clave de tu ordenador y usa un certificado HTTPS de verdad, así que el navegador nunca avisa de "no seguro".
- **Casi sin mantenimiento**: los certificados, las reglas y CLIProxyAPI se actualizan solos, y la configuración se copia cada día.

## Tres pasos

### 1. Compra un servidor

Ahora mismo, elige **BandwagonHost**. La red es estable y es el que uso yo:

**[Comprar BandwagonHost](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)**

[DMIT](https://www.dmit.io/aff.php?aff=23544) también es bueno, pero ahora está agotado. No hace falta esperar.

> Los dos son enlaces de referido míos. Puede que reciba una comisión si compras a través de ellos, y destinaré ese dinero a labores benéficas. Precios y disponibilidad según las webs oficiales.

Elige **Ubuntu 24.04** como sistema. Cuando el servidor esté listo, apunta tres datos del panel: **IP del servidor, contraseña de root (o archivo de clave) y puerto SSH**.

### 2. Deja que una IA lo configure

Abre una herramienta de IA que pueda ejecutar comandos en tu ordenador, como [Codex](https://github.com/openai/codex) o [Claude Code](https://claude.com/claude-code) (en Windows, úsala dentro de WSL). Copia el texto de abajo, rellénalo y envíalo:

```text
Configura mi nuevo servidor con el plan "XXD VPS", por favor.

Plan: https://github.com/nevertoday/xiaoxiaodong-vps
Primero descarga este proyecto en mi ordenador y lee entero
skills/xiaoxiaodong-vps/SKILL.md. Sigue sus pasos y reglas al pie de la letra
y usa los scripts del proyecto para configurar y verificar.
Háblame en español, por favor.

Mi servidor:
- IP:
- Acceso: contraseña inicial (déjame escribirla yo en la terminal)
- Usuario y puerto SSH: por defecto
- Nombre con el que quiero entrar: bwg
```

Solo tienes que cambiar tres cosas:

- **IP**: la IP del servidor que aparece en el panel.
- **Acceso**: si tu proveedor te dio un archivo de clave, cámbialo por `archivo de clave: ruta del archivo` (un zip vale).
- **Nombre**: cambia `bwg` por el nombre que quieras. Después, con escribir `ssh ese-nombre` entrarás en el servidor.

Si el usuario y el puerto no son root / 22, cambia "por defecto" por los valores reales.

Luego espera a que la IA termine, normalmente entre 10 y 20 minutos. En algún momento te pedirá que escribas la contraseña del servidor en la terminal. **No pegues nunca la contraseña en el chat.** Al terminar, el acceso con contraseña queda desactivado y solo este ordenador puede entrar.

Si la IA no puede descargar el proyecto, [descarga el ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) tú mismo, descomprímelo y añade una línea al texto: "El proyecto ya está en: ruta de la carpeta".

Al terminar aparecerá en tu escritorio el archivo `XXD-VPS-tu-nombre-login-es.md` con:

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

### 3. Importa la suscripción

- **Ordenador**: instala [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), importa la URL de suscripción de Clash, elige el modo **Regla (Rule)** y activa el **proxy del sistema**.
- **iPhone**: importa la URL de suscripción de Shadowrocket en Shadowrocket.
- **Router**: importa la URL de suscripción de Clash en OpenClash.

Después abre <https://ipinfo.io>. Si muestra la IP de tu servidor, ya estás conectado.

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

## Privacidad

- Este proyecto no contiene información de ningún servidor real.
- Las contraseñas, claves, URLs de suscripción y claves de API de cada servidor se generan de nuevo durante la configuración y solo se guardan en el servidor y en tu ordenador. La IA no las muestra en el chat.
- No publiques en ningún sitio tu archivo de acceso, las URLs de suscripción ni las claves, ni les hagas capturas.
- Para informar de un problema de seguridad, consulta [SECURITY.md](./SECURITY.md).

Que puedas conectarte, y a qué velocidad, también depende de la red local y de la ruta del servidor. Este proyecto se asegura de que el servidor quede bien configurado, pero no puede garantizar que una misma IP sea accesible desde todos los países y operadores.

## Licencia

[MIT](./LICENSE)
