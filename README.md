# 🏛️ Alcalde Digital

Videojuego educativo sobre el uso responsable de las redes sociales.
Universidad del Norte — Estructura de Datos II — Laboratorio.

Ciudad Nova está en campaña electoral. En la red social **Civitas** circulan
noticias verdaderas, opiniones, rumores y mentiras. Cada publicación que llega
a tu feed te obliga a decidir: ¿verificar, compartir, reportar o ignorar?
Al final se elige alcalde, y quién gana depende del estado en que ustedes
dejaron la conversación pública.

---

## Estado: Primera entrega

Esta entrega cubre lo que evalúa el rubro de la semana 8:
árboles, pertinencia de la estructura, operaciones y recorridos, interfaz
gráfica preliminar y relación del árbol con la lógica del juego.

Los grafos, el multijugador y la arquitectura cliente‑servidor corresponden a
la segunda entrega y a la final; todavía no están implementados.

---

## Cómo ejecutarlo

Requiere el SDK de Ren'Py 8.5.3 o superior.

```bash
/ruta/al/renpy-8.5.3-sdk/renpy.sh /ruta/a/Alcalde-Digital
```

Para comprobar el proyecto sin abrir ventana:

```bash
/ruta/al/renpy-8.5.3-sdk/renpy.sh /ruta/a/Alcalde-Digital lint
```

La lógica es Python puro y se puede ejercitar sin el motor:

```bash
cd game && python3 -c "
from clases.partida import Partida
p = Partida('Tu', 'PERIODISTA', semilla=42)
while p.hay_turnos() and p.siguiente_publicacion():
    p.decidir('VERIFICAR' if p.jugador.puede_verificar() else 'REPORTAR')
print(p.resultado_final())
"
```

---

## Arquitectura

El enunciado exige Java o Python. Toda la lógica del juego vive en **módulos
Python puros** bajo `game/clases/`, sin ninguna dependencia de Ren'Py: se
pueden importar, probar y defender por separado. Los archivos `.rpy` solo
dibujan la interfaz y encadenan pantallas.

```
game/
├── clases/                  ← lógica, Python puro
│   ├── nodo_avl.py          nodo del AVL
│   ├── arbol_avl.py         AVL: inserción, borrado, rotaciones, recorridos
│   ├── arbol_decisiones.py  árbol n-ario de decisión y sus consecuencias
│   ├── publicacion.py       modelo de publicación
│   ├── ciudad.py            los seis indicadores de Ciudad Nova
│   ├── jugador.py           jugador y habilidades por rol
│   ├── datos.py             contenido inicial y de eventos
│   └── partida.py           orquestador de la partida
├── definiciones.rpy         paleta, imágenes, estilos
├── pantallas_juego.rpy      pantallas propias (HUD, feed, visor del árbol…)
├── script.rpy               flujo de la partida
└── images/                  arte generado proceduralmente
```

---

## Las dos estructuras de árbol

Cada árbol resuelve un problema distinto. Ninguno está puesto para cumplir el
requisito: si se quitan, el juego deja de funcionar.

### 1. Árbol AVL — clasificación del feed

**Qué problema resuelve.** El feed debe recorrerse ordenado por nivel de
riesgo, y además cambia durante la partida: los eventos aleatorios insertan
publicaciones nuevas y cada decisión elimina la que se acaba de atender.

**Por qué esta estructura.** Una lista ordenada costaría O(n) por inserción.
Un BST simple degenera a lista enlazada cuando las publicaciones llegan casi
ordenadas por riesgo —justo lo que ocurre con una racha de rumores— y las
operaciones caen a O(n).

**Qué variante.** AVL: BST con autobalanceo por altura. Tras cada alta o baja
se recalcula el factor de equilibrio y se rota si |FE| > 1, garantizando
altura O(log n).

**Inserción y eliminación.** Inserción recursiva con rebalanceo en los cuatro
casos (II, DD, ID, DI). Eliminación con los tres casos clásicos; con dos hijos
se sustituye por el sucesor inorden y se rebalancea al regresar.

**Recorridos.** Preorden, inorden y posorden (recursivos e iterativos con
pila) y por niveles (BFS con cola). El inorden define el orden real del feed.

**Clave.** La tupla `(nivel_riesgo, id)` en vez del riesgo solo, para
garantizar unicidad: con clave simple, dos publicaciones del mismo riesgo
obligarían a descartar una y se perdería información.

### 2. Árbol de decisiones — consecuencias de cada acción

**Qué problema resuelve.** Las consecuencias dependen del camino recorrido:
verificar y luego compartir algo falso no es lo mismo que compartirlo de
entrada. El árbol guarda ese encadenamiento.

**Por qué esta estructura.** El flujo es jerárquico y finito, y ningún camino
vuelve atrás. Con condicionales sueltos sería inmantenible y no se podría
recorrer ni mostrar gráficamente.

**Qué variante.** Árbol n-ario de decisión, de 0 a 3 hijos etiquetados. No
necesita balanceo: su forma la define el diseño del juego, no el orden de
llegada de los datos.

**Inserción y eliminación.** Inserción por ruta de etiquetas desde la raíz;
eliminación por poda de la rama completa que cuelga de una etiqueta.

**Recorridos.** Preorden y por niveles para dibujarlo; durante la partida se
desciende etiqueta a etiqueta con `avanzar()`.

**Detalle de diseño.** Al elegir VERIFICAR, la rama siguiente no la elige el
jugador: la determina el dato real de la publicación. Eso es exactamente lo
que significa verificar, y hace que el recorrido dependa a la vez de la
decisión y de la información.

---

## Mecánica

Ocho turnos. Cada turno aparece la publicación de mayor riesgo viva en el
feed (el máximo del AVL) y se elige una acción.

**Las verificaciones son limitadas** y dependen del rol. Esa escasez es lo que
convierte el turno en una decisión real: verificar siempre es lo más seguro,
pero no alcanza para todo, así que hay que gastar las verificaciones en lo que
más riesgo tiene y arriesgarse en el resto.

| Rol | Verificaciones | Habilidad |
|---|---|---|
| Ciudadano | 3 | Equilibrado |
| Periodista | 5 | Verificar rinde un 50% más |
| Influencer | 2 | Compartir tiene el doble de impacto, para bien y para mal |
| Candidato | 3 | Más reputación al verificar |

Las cuatro acciones mueven los seis indicadores de Ciudad Nova. El estado
inicial da una salud de 67: un punto neutro, de modo que mantenerlo ya cuesta.

Cuatro estrategias dan cuatro finales distintos:

| Estrategia | Salud final | Alcalde electo |
|---|---|---|
| Verificar y luego actuar | 82–88 | Sofía Restrepo |
| Reportar todo | 75 | Marco Duarte |
| Ignorar todo | 59 | Tomás Iriarte |
| Compartir sin verificar | 32 | Lucas Vergara |

Reportar todo acierta el 100% de las veces pero **no** alcanza el mejor final:
bloquear a ciegas tampoco es uso responsable de una red social.

---

## Interfaz

- **Indicadores de Ciudad Nova** en la barra superior, con salud global.
- **Panel del jugador**: avatar del rol, puntos, reputación, precisión,
  verificaciones restantes y turno.
- **Tarjeta de la publicación**: autor, texto y nivel de riesgo.
- **Acciones disponibles**, tomadas del primer nivel del árbol de decisiones.
- **Resultado de la acción**: camino recorrido en el árbol, tipo real de la
  publicación y efecto sobre cada indicador.
- **Visor del AVL**: dibuja el árbol con el factor de equilibrio de cada nodo
  y muestra los cuatro recorridos en vivo.
- **Ayuda** con objetivo, reglas, botones, roles e indicadores.

El arte se genera proceduralmente con Pillow, sin dependencias de licencia.

**Accesibilidad.** El nivel de riesgo nunca se comunica solo con color: cada
publicación muestra siempre el número y la etiqueta ALTO, MEDIO o BAJO, de
modo que el juego es legible sin distinguir rojo de verde.

---

## Pendiente para las siguientes entregas

- Grafo social y de la ciudad, y propagación de publicaciones por el grafo.
- Multijugador local de 2 a 4 jugadores con arquitectura cliente‑servidor.
- Sonido, animaciones y logros.
