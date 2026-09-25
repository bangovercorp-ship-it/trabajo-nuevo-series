// Motor de render realista de Puerto Candela.
//
// POR QUE EXISTE: la maqueta de bloques servia para verificar geometria, pero no
// sirve como imagen de referencia para generar video. Una caja gris no le dice al
// generador que material es, ni como cae la luz, ni de que pais es el pueblo. Este
// modulo agrega lo que faltaba: cielo fisico, iluminacion por imagen, texturas
// procedurales, techos a dos aguas, rejas, cables y arboles de verdad.
//
// Todo es procedural y deterministico: no hay un solo archivo de imagen. La misma
// semilla saca la misma ciudad, siempre, en cualquier maquina.
//
// MATERIALES, fijados por la biblia y no negociables:
//   bloque de cemento enlucido y pintado en colores fuertes
//   cubierta de zinc o galvalume A DOS AGUAS
//   portales sobre la vereda para la sombra
//   rejas por todos lados
//   cables cruzando la calle
//   polvo o barro segun el mes
import React, {useLayoutEffect, useMemo} from 'react';
import * as THREE from 'three';
import {useThree} from '@react-three/fiber';
import {Sky} from 'three/examples/jsm/objects/Sky.js';

// ============================================================ azar determinista
export const SEMILLA = 20260925;
export function rnd(n: number) {
  let t = (Math.floor(n) * 1103515245 + SEMILLA) >>> 0;
  t ^= t >>> 15;
  t = Math.imul(t, 2246822507) >>> 0;
  t ^= t >>> 13;
  return (t >>> 0) / 4294967296;
}
/** elige de una lista con la semilla k */
export const elige = <T,>(lista: T[], k: number) => lista[Math.floor(rnd(k) * lista.length) % lista.length];

// ============================================================ cache de texturas
// Una textura cuesta caro de generar y no cambia entre cuadros. Se genera una vez
// por clave y se reusa: sin esto, 300 casas tardan minutos en vez de segundos.
const CACHE = new Map<string, any>();
function cache<T>(clave: string, hacer: () => T): T {
  if (!CACHE.has(clave)) CACHE.set(clave, hacer());
  return CACHE.get(clave) as T;
}

/** un material por textura, no uno por casa. Sin esto la ciudad crea miles de
    materiales en cada cuadro y el render se arrastra. */
export function mat(t: THREE.Texture, rug = 0.93, emi?: THREE.Texture) {
  const k = `mat|${t.uuid}|${rug}|${emi ? emi.uuid : '-'}`;
  return cache(k, () => new THREE.MeshStandardMaterial({
    map: t, roughness: rug,
    emissiveMap: emi ?? null, emissive: new THREE.Color(emi ? "#ffffff" : "#000000"),
    emissiveIntensity: emi ? 1.8 : 0,
  }));
}

function lienzo(w: number, h: number) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return {c, g: c.getContext('2d')!};
}
/** grano fino sobre lo ya dibujado: es lo que quita el plastico */
function grano(g: CanvasRenderingContext2D, w: number, h: number, fuerza: number, k = 1) {
  const img = g.getImageData(0, 0, w, h);
  const d = img.data;
  let s = (k * 7919 + 13) % 233280;
  for (let i = 0; i < d.length; i += 4) {
    s = (s * 9301 + 49297) % 233280;
    const n = (s / 233280 - 0.5) * fuerza;
    d[i] += n; d[i + 1] += n; d[i + 2] += n;
  }
  g.putImageData(img, 0, 0);
}
/** manchas de humedad y salitre: la costa se come el enlucido desde abajo */
function manchas(g: CanvasRenderingContext2D, w: number, h: number, k: number, n = 14) {
  for (let i = 0; i < n; i++) {
    const x = rnd(k + i * 31) * w;
    const y = h - rnd(k + i * 57) * h * 0.55;
    const r = 8 + rnd(k + i * 83) * 34;
    g.fillStyle = `rgba(72,64,52,${0.05 + rnd(k + i * 97) * 0.09})`;
    g.beginPath(); g.ellipse(x, y, r, r * (0.4 + rnd(k + i * 11) * 0.7), 0, 0, 7); g.fill();
  }
}
function tex(c: HTMLCanvasElement, rx = 1, ry = 1) {
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(rx, ry);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

// ============================================================ texturas de muro
const PX = 128;   // pixeles por metro de textura, aprox

/** muro liso pintado, con zocalo sucio. Para medianeras y traseras. */
export function texMuro(col: string, k: number, alto = 1) {
  return cache(`muro|${col}|${k % 8}|${alto}`, () => {
    const W = 256, H = 256 * alto;
    const {c, g} = lienzo(W, H);
    g.fillStyle = col; g.fillRect(0, 0, W, H);
    // el enlucido nunca es de un solo tono
    for (let i = 0; i < 22; i++) {
      g.fillStyle = `rgba(255,255,255,${rnd(k + i) * 0.05})`;
      g.fillRect(rnd(k + i * 3) * W, rnd(k + i * 5) * H, 30 + rnd(k + i * 7) * 90, 20 + rnd(k + i * 9) * 70);
    }
    const gr = g.createLinearGradient(0, H, 0, H - 88);
    gr.addColorStop(0, 'rgba(58,50,40,0.42)');
    gr.addColorStop(1, 'rgba(58,50,40,0)');
    g.fillStyle = gr; g.fillRect(0, 0, W, H);
    manchas(g, W, H, k);
    grano(g, W, H, 20, k);
    return tex(c);
  });
}

/** una reja de varilla sobre la ventana: en el barrio las hay por todos lados */
function dibujaReja(g: CanvasRenderingContext2D, x: number, y: number, w: number, h: number) {
  g.strokeStyle = 'rgba(30,32,34,0.85)';
  g.lineWidth = 2.5;
  for (let i = x + 6; i < x + w; i += 9) { g.beginPath(); g.moveTo(i, y); g.lineTo(i, y + h); g.stroke(); }
  g.lineWidth = 3;
  g.beginPath(); g.moveTo(x, y + h / 2); g.lineTo(x + w, y + h / 2); g.stroke();
}

function dibujaVentana(g: CanvasRenderingContext2D, x: number, y: number, w: number, h: number,
                       k: number, conReja: boolean, luz?: string) {
  g.fillStyle = luz ?? '#26303a';                       // vidrio
  g.fillRect(x, y, w, h);
  if (!luz) {                                           // reflejo del cielo de dia
    const gr = g.createLinearGradient(x, y, x + w, y + h);
    gr.addColorStop(0, 'rgba(190,212,226,0.55)');
    gr.addColorStop(0.5, 'rgba(120,140,155,0.15)');
    gr.addColorStop(1, 'rgba(40,48,56,0.1)');
    g.fillStyle = gr; g.fillRect(x, y, w, h);
  }
  g.strokeStyle = 'rgba(20,24,28,0.6)'; g.lineWidth = 2;
  g.beginPath(); g.moveTo(x + w / 2, y); g.lineTo(x + w / 2, y + h); g.stroke();
  if (conReja) dibujaReja(g, x, y, w, h);
  g.strokeStyle = '#e8e2d4'; g.lineWidth = 4;           // marco blanco, siempre
  g.strokeRect(x - 1, y - 1, w + 2, h + 2);
  if (rnd(k) > 0.55) {                                  // alero de chapa sobre la ventana
    g.fillStyle = 'rgba(90,96,100,0.75)';
    g.fillRect(x - 7, y - 10, w + 14, 7);
  }
}

/** fachada de casa: ventanas con reja, puerta, zocalo pintado. `luz` = de noche. */
export function texFachada(col: string, pisos: number, k: number, conPuerta: boolean, noche = false) {
  return cache(`fach|${col}|${pisos}|${k % 24}|${conPuerta}|${noche}`, () => {
    const W = 256, H = 256 * pisos;
    const {c, g} = lienzo(W, H);
    g.fillStyle = col; g.fillRect(0, 0, W, H);
    for (let i = 0; i < 18; i++) {
      g.fillStyle = `rgba(255,255,255,${rnd(k + i * 13) * 0.06})`;
      g.fillRect(rnd(k + i * 3) * W, rnd(k + i * 5) * H, 40 + rnd(k + i) * 80, 24 + rnd(k + i * 7) * 60);
    }
    // zocalo pintado de otro color: se hace para que el barro no se note
    const zoc = 30 + rnd(k + 91) * 16;
    g.fillStyle = `rgba(${40 + rnd(k + 5) * 60},${38 + rnd(k + 9) * 50},${34 + rnd(k + 11) * 40},0.55)`;
    g.fillRect(0, H - zoc, W, zoc);
    const gr = g.createLinearGradient(0, H, 0, H - 92);
    gr.addColorStop(0, 'rgba(56,48,38,0.40)');
    gr.addColorStop(1, 'rgba(56,48,38,0)');
    g.fillStyle = gr; g.fillRect(0, 0, W, H);

    for (let p = 0; p < pisos; p++) {
      const base = H - (p + 1) * 256;                    // techo de ese piso
      const y = base + 62;
      const planta = p === 0;
      const encendida = noche && rnd(k + p * 7 + 3) > 0.42;
      const luz = encendida ? (rnd(k + p) > 0.7 ? '#cfe4f2' : '#ffd8a0') : undefined;
      if (planta && conPuerta) {
        dibujaVentana(g, 26, y, 74, 88, k + p, true, luz);
        // puerta: madera o chapa, con su escalon
        g.fillStyle = rnd(k + 17) > 0.5 ? '#5d4a33' : '#6a7078';
        g.fillRect(132, H - 122, 60, 122);
        g.strokeStyle = 'rgba(20,20,20,0.5)'; g.lineWidth = 3; g.strokeRect(132, H - 122, 60, 122);
        g.fillStyle = 'rgba(230,226,214,0.8)'; g.fillRect(126, H - 10, 72, 10);
      } else {
        dibujaVentana(g, 26, y, 74, 88, k + p, planta, luz);
        dibujaVentana(g, 150, y, 74, 88, k + p * 3, planta, luz);
      }
    }
    manchas(g, W, H, k);
    grano(g, W, H, 18, k);
    return tex(c);
  });
}

/** ventanas encendidas sobre negro: va como emissiveMap. Sin esto, de noche las
    ventanas pintadas en el mapa de color no iluminan nada y el barrio se apaga. */
export function texEncendidas(pisos: number, k: number, conPuerta: boolean) {
  return cache(`enc|${pisos}|${k % 24}|${conPuerta}`, () => {
    const W = 256, H = 256 * pisos;
    const {c, g} = lienzo(W, H);
    g.fillStyle = '#000000'; g.fillRect(0, 0, W, H);
    for (let p = 0; p < pisos; p++) {
      const y = H - (p + 1) * 256 + 62;
      const on = rnd(k + p * 7 + 3) > 0.42;
      if (!on) continue;
      g.fillStyle = rnd(k + p) > 0.7 ? '#9fd0f0' : '#ffbe6a';   // foco frio o foco amarillo
      if (p === 0 && conPuerta) g.fillRect(28, y + 2, 70, 84);
      else { g.fillRect(28, y + 2, 70, 84); g.fillRect(152, y + 2, 70, 84); }
    }
    return tex(c);
  });
}

/** local comercial: persiana metalica y banda de rotulo. La avenida es esto. */
export function texLocal(col: string, k: number, noche = false) {
  return cache(`local|${col}|${k % 20}|${noche}`, () => {
    const W = 256, H = 256;
    const {c, g} = lienzo(W, H);
    g.fillStyle = col; g.fillRect(0, 0, W, H);
    grano(g, W, H, 16, k);
    // banda de rotulo: color plano, sin letras. Las letras las pone la imagen final.
    const rot = elige(['#b4332b', '#1f5aa0', '#e0a92c', '#2f7d5a', '#c96f52'], k + 3);
    g.fillStyle = rot; g.fillRect(0, 26, W, 52);
    g.fillStyle = 'rgba(0,0,0,0.18)'; g.fillRect(0, 74, W, 5);
    // persiana enrollable, bajada a medias o subida
    const abierto = rnd(k + 41) > 0.45;
    const top = abierto ? 150 : 96;
    g.fillStyle = noche || !abierto ? '#8d9398' : '#1c2126';
    g.fillRect(16, top, 224, H - top);
    if (noche || !abierto) {
      for (let y = top; y < H; y += 7) {
        g.fillStyle = 'rgba(0,0,0,0.16)'; g.fillRect(16, y, 224, 3);
      }
    } else {
      g.fillStyle = noche ? '#ffd8a0' : 'rgba(210,225,235,0.22)';
      g.fillRect(24, top + 8, 208, H - top - 16);
    }
    g.fillStyle = 'rgba(90,96,100,0.9)'; g.fillRect(12, 96, 232, 10);   // cajon de la persiana
    manchas(g, W, H, k, 8);
    return tex(c);
  });
}

/** bloque sin enlucir: la cara que nadie mira, y media ciudad en construccion */
export function texBloque(k: number) {
  return cache(`bloque|${k % 6}`, () => {
    const W = 256, H = 256;
    const {c, g} = lienzo(W, H);
    g.fillStyle = '#b9b3a6'; g.fillRect(0, 0, W, H);
    for (let y = 0; y < H; y += 26) {
      const off = (y / 26) % 2 ? 26 : 0;
      for (let x = -26; x < W; x += 52) {
        g.fillStyle = `rgba(255,255,255,${0.03 + rnd(k + x + y) * 0.07})`;
        g.fillRect(x + off + 1.5, y + 1.5, 49, 23);
      }
      g.fillStyle = 'rgba(120,114,104,0.55)'; g.fillRect(0, y, W, 2);
    }
    manchas(g, W, H, k, 10);
    grano(g, W, H, 22, k);
    return tex(c);
  });
}

/** zinc acanalado con su normal: sin la onda, el techo parece carton */
export function texZinc(tono: 'nuevo' | 'viejo' | 'oxido', k = 0) {
  return cache(`zinc|${tono}|${k % 4}`, () => {
    const base = {nuevo: '#b6bec4', viejo: '#8d9398', oxido: '#8a7566'}[tono];
    const W = 256, H = 256;
    const {c, g} = lienzo(W, H);
    g.fillStyle = base; g.fillRect(0, 0, W, H);
    for (let x = 0; x < W; x += 16) {
      g.fillStyle = 'rgba(255,255,255,0.13)'; g.fillRect(x, 0, 6, H);
      g.fillStyle = 'rgba(0,0,0,0.17)'; g.fillRect(x + 9, 0, 5, H);
    }
    const nOx = tono === 'oxido' ? 46 : tono === 'viejo' ? 16 : 5;
    for (let i = 0; i < nOx; i++) {
      g.fillStyle = `rgba(${132 + rnd(k + i) * 40},${64 + rnd(k + i * 3) * 26},${28 + rnd(k + i * 5) * 20},${0.08 + rnd(k + i * 7) * 0.26})`;
      g.beginPath();
      g.ellipse(rnd(k + i * 11) * W, rnd(k + i * 13) * H, 5 + rnd(k + i * 17) * 22, 4 + rnd(k + i * 19) * 14, 0, 0, 7);
      g.fill();
    }
    grano(g, W, H, 14, k);
    const mapa = tex(c);
    const {c: cn, g: gn} = lienzo(W, H);
    const im = gn.createImageData(W, H);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const nx = Math.sin((x / 16) * Math.PI * 2) * 0.85;
      const i = (y * W + x) * 4;
      im.data[i] = (nx * 0.5 + 0.5) * 255;
      im.data[i + 1] = 128; im.data[i + 2] = 255; im.data[i + 3] = 255;
    }
    gn.putImageData(im, 0, 0);
    const normal = new THREE.CanvasTexture(cn);
    normal.wrapS = normal.wrapT = THREE.RepeatWrapping;
    return {mapa, normal};
  });
}

// ============================================================ texturas de suelo
export type Piso = 'asfalto' | 'adoquin' | 'lastre' | 'tierra' | 'vereda' | 'cesped'
                 | 'arroz' | 'seco' | 'monte' | 'camaronera' | 'losa';

export function texPiso(tipo: Piso) {
  return cache(`piso|${tipo}`, () => {
    const W = 256, H = 256;
    const {c, g} = lienzo(W, H);
    const k = tipo.length * 977;
    if (tipo === 'asfalto') {
      g.fillStyle = '#5f5b54'; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 260; i++) {
        g.fillStyle = `rgba(${170 + rnd(k + i) * 60},${168 + rnd(k + i) * 50},${160 + rnd(k + i) * 50},${rnd(k + i * 3) * 0.12})`;
        g.fillRect(rnd(k + i * 5) * W, rnd(k + i * 7) * H, 2 + rnd(k + i) * 3, 2 + rnd(k + i) * 3);
      }
      for (let i = 0; i < 4; i++) {                        // algun parche, no una piel de leopardo
        g.fillStyle = `rgba(52,50,46,${0.1 + rnd(k + i) * 0.1})`;
        g.beginPath(); g.ellipse(rnd(k + i * 11) * W, rnd(k + i * 13) * H, 16 + rnd(k + i) * 30, 12 + rnd(k + i * 3) * 20, rnd(k + i) * 3, 0, 7); g.fill();
      }

      grano(g, W, H, 26, k);
    } else if (tipo === 'adoquin') {
      g.fillStyle = '#9a9186'; g.fillRect(0, 0, W, H);
      for (let y = 0; y < H; y += 16) {
        const off = (y / 16) % 2 ? 8 : 0;
        for (let x = -16; x < W; x += 16) {
          const t = 0.5 + rnd(k + x * 3 + y * 7) * 0.5;
          g.fillStyle = `rgba(${150 * t + 40},${142 * t + 38},${128 * t + 36},1)`;
          g.fillRect(x + off + 1, y + 1, 14, 14);
        }
      }
      grano(g, W, H, 18, k);
    } else if (tipo === 'lastre') {
      g.fillStyle = '#a8a08c'; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 700; i++) {
        const t = rnd(k + i * 3);
        g.fillStyle = `rgba(${140 + t * 90},${132 + t * 84},${112 + t * 76},${0.3 + t * 0.5})`;
        g.fillRect(rnd(k + i * 5) * W, rnd(k + i * 7) * H, 1 + t * 3, 1 + t * 3);
      }
      // las dos huellas de las llantas, que es como se ve una calle sin asfaltar
      g.fillStyle = 'rgba(122,110,92,0.5)';
      g.fillRect(58, 0, 34, H); g.fillRect(166, 0, 34, H);
      grano(g, W, H, 24, k);
    } else if (tipo === 'tierra') {
      g.fillStyle = '#9c8e74'; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 40; i++) {
        g.fillStyle = `rgba(${142 + rnd(k + i) * 56},${124 + rnd(k + i * 3) * 44},${96 + rnd(k + i * 5) * 34},${0.08 + rnd(k + i) * 0.18})`;
        g.beginPath(); g.ellipse(rnd(k + i * 11) * W, rnd(k + i * 13) * H, 10 + rnd(k + i) * 40, 8 + rnd(k + i * 3) * 28, 0, 0, 7); g.fill();
      }
      grano(g, W, H, 30, k);
    } else if (tipo === 'vereda') {
      g.fillStyle = '#b3aa9c'; g.fillRect(0, 0, W, H);
      g.strokeStyle = 'rgba(110,104,94,0.8)'; g.lineWidth = 2;
      for (let x = 0; x <= W; x += 64) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); }
      for (let y = 0; y <= H; y += 64) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
      manchas(g, W, H, k, 12);
      grano(g, W, H, 20, k);
    } else if (tipo === 'cesped') {
      g.fillStyle = '#6f8a52'; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 2200; i++) {
        const t = rnd(k + i * 3);
        g.fillStyle = `rgba(${74 + t * 86},${104 + t * 74},${48 + t * 52},${0.35 + t * 0.4})`;
        g.fillRect(rnd(k + i * 5) * W, rnd(k + i * 7) * H, 1.5, 2 + t * 3);
      }
      for (let i = 0; i < 14; i++) {                       // calvas de tierra, siempre las hay
        g.fillStyle = `rgba(150,136,104,${0.12 + rnd(k + i) * 0.22})`;
        g.beginPath(); g.ellipse(rnd(k + i * 11) * W, rnd(k + i * 13) * H, 8 + rnd(k + i) * 24, 6 + rnd(k + i * 3) * 18, 0, 0, 7); g.fill();
      }
    } else if (tipo === 'losa') {
      g.fillStyle = '#93a0a8'; g.fillRect(0, 0, W, H);
      grano(g, W, H, 16, k);
    } else if (tipo === 'arroz') {
      // arrozal: el damero de piscinas con el agua reflejando. Desde el aire, esto
      // es lo que dice "llanura del Guayas" antes que cualquier otra cosa.
      g.fillStyle = '#5f8340'; g.fillRect(0, 0, W, H);
      for (let y = 0; y < H; y += 32) for (let x = 0; x < W; x += 42) {
        const t = rnd(k + x * 7 + y * 13);
        g.fillStyle = t > 0.70 ? `rgba(126,150,156,0.9)` : `rgba(${72 + t * 78},${112 + t * 64},${44 + t * 50},1)`;
        g.fillRect(x + 2, y + 2, 38, 28);
      }
      g.strokeStyle = 'rgba(150,138,110,0.9)'; g.lineWidth = 3;
      for (let y = 0; y <= H; y += 32) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
      for (let x = 0; x <= W; x += 42) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); }
      grano(g, W, H, 18, k);
    } else if (tipo === 'seco' || tipo === 'monte') {
      // Bosque seco tropical, no desierto: pasto seco con mucha mata verde oscura.
      // 'monte' es lo mismo pero cerrado, para las manchas de monte de la llanura.
      const denso = tipo === 'monte';
      g.fillStyle = denso ? '#6a7346' : '#93915f'; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 110; i++) {                      // rastrojo claro
        const t = rnd(k + i * 11);
        g.fillStyle = `rgba(${176 + t * 40},${168 + t * 34},${118 + t * 34},${0.10 + t * 0.22})`;
        g.beginPath(); g.ellipse(rnd(k + i * 5) * W, rnd(k + i * 7) * H, 9 + t * 30, 7 + t * 22, 0, 0, 7); g.fill();
      }
      for (let i = 0; i < (denso ? 620 : 330); i++) {      // matorral
        const t = rnd(k + i * 3);
        g.fillStyle = `rgba(${52 + t * 52},${72 + t * 52},${36 + t * 36},${0.35 + t * 0.45})`;
        g.beginPath(); g.ellipse(rnd(k + i * 5) * W, rnd(k + i * 7) * H, 3 + t * (denso ? 12 : 8), 3 + t * (denso ? 10 : 7), 0, 0, 7); g.fill();
      }
      grano(g, W, H, 22, k);
    } else {   // camaronera: piscinas grandes de agua quieta con sus muros de tierra
      g.fillStyle = '#7d8f8c'; g.fillRect(0, 0, W, H);
      for (let y = 0; y < H; y += 64) for (let x = 0; x < W; x += 86) {
        const t = rnd(k + x * 11 + y * 17);
        g.fillStyle = `rgba(${96 + t * 38},${118 + t * 34},${118 + t * 30},1)`;
        g.fillRect(x + 5, y + 5, 76, 54);
      }
      g.strokeStyle = 'rgba(158,146,116,1)'; g.lineWidth = 7;
      for (let y = 0; y <= H; y += 64) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
      for (let x = 0; x <= W; x += 86) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); }
      grano(g, W, H, 14, k);
    }
    return tex(c);
  });
}

/** cuanto mide de verdad una baldosa de cada textura, en metros */
const METRO: Record<Piso, number> = {
  asfalto: 6, adoquin: 3.2, lastre: 5, tierra: 8, vereda: 4, cesped: 7,
  losa: 6, arroz: 150, seco: 70, monte: 50, camaronera: 190,
};

/** la misma textura con otro mosaico. Se clona porque `repeat` es de la textura,
    no del material: si se toca la compartida, se mueve en toda la ciudad. */
export function texPisoRep(tipo: Piso, rx: number, ry: number) {
  const a = Math.max(0.25, Math.round(rx * 4) / 4);
  const b = Math.max(0.25, Math.round(ry * 4) / 4);
  return cache(`pisorep|${tipo}|${a}|${b}`, () => {
    const t = texPiso(tipo).clone();
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(a, b);
    t.needsUpdate = true;
    return t;
  });
}

/** suelo plano con textura: calzadas, veredas, parcelas del territorio */
export const Suelo: React.FC<{
  x: [number, number]; z: [number, number]; y?: number; tipo: Piso;
  /** metros por baldosa; por defecto, el de la tabla METRO */
  rep?: number;
  rug?: number; met?: number; col?: string; rot?: number;
}> = ({x, z, y = 0, tipo, rep, rug, met, col, rot = 0}) => {
  const an = Math.abs(x[1] - x[0]), fo = Math.abs(z[1] - z[0]);
  const m = rep ?? METRO[tipo];                  // `rep` = metros por baldosa
  const t = texPisoRep(tipo, an / m, fo / m);
  const agua = tipo === 'camaronera';
  return (
    <mesh position={[(x[0] + x[1]) / 2, y, (z[0] + z[1]) / 2]} rotation={[-Math.PI / 2, 0, rot]} receiveShadow>
      <planeGeometry args={[an, fo]} />
      <meshStandardMaterial map={t} color={col ?? '#ffffff'}
        roughness={rug ?? (agua ? 0.18 : 0.95)} metalness={met ?? (agua ? 0.25 : 0)} />
    </mesh>
  );
};

// ============================================================ hora y atmosfera
// El Ecuador esta sobre la linea: el sol sale a las 6:15 y se pone a las 18:20 todo
// el ano, y al mediodia cae casi vertical. Eso manda sobre la luz de la serie: el
// mediodia es duro y de cielo blanco (lo dice la biblia), y el atardecer es corto.
export type Hora = 'mediodia' | 'tarde' | 'amanecer' | 'noche';

const LUZ: Record<Hora, {
  elev: number; azim: number; turb: number; ray: number; mie: number;
  exp: number; env: number; dirI: number; dirC: string;
  amb: number; ambC: string; fog: [string, number, number];
}> = {
  // el sol de la serie: 12:30, casi vertical, sombra corta y dura, cielo lavado
  mediodia: {elev: 76, azim: 104, turb: 14, ray: 0.38, mie: 0.016,
             exp: 0.34, env: 0.20, dirI: 3.6, dirC: '#fff6e8',
             amb: 0.10, ambC: '#cfe0ea', fog: ['#d3dade', 380, 3000]},
  // 16:40: la hora de los planos de apertura. Sombra larga y color caliente.
  tarde: {elev: 20, azim: 256, turb: 5, ray: 2.2, mie: 0.006,
          exp: 0.50, env: 0.19, dirI: 3.3, dirC: '#ffd7a2',
          amb: 0.12, ambC: '#d8c9b4', fog: ['#c9c7b8', 340, 2800]},
  // 06:40: bruma sobre la llanura, todo azul frio menos el sol rasante
  amanecer: {elev: 9, azim: 88, turb: 4, ray: 3.0, mie: 0.005,
             exp: 0.62, env: 0.26, dirI: 2.4, dirC: '#ffd2b0',
             amb: 0.22, ambC: '#b9c8d4', fog: ['#c6cfd6', 180, 1700]},
  // 19:05, la hora azul. NO es noche cerrada a proposito: en negro absoluto la
  // referencia no le sirve al generador de video, que necesita ver la forma. Queda
  // cielo azul profundo, resto de luz en el horizonte, y mandan los neones.
  noche: {elev: -2.0, azim: 252, turb: 8, ray: 3.2, mie: 0.010,
          exp: 0.85, env: 1.10, dirI: 0.45, dirC: '#c99a76',
          amb: 0.42, ambC: '#415980', fog: ['#26344c', 280, 2200]},
};

function solVec(elev: number, azim: number) {
  const v = new THREE.Vector3();
  v.setFromSphericalCoords(1, THREE.MathUtils.degToRad(90 - elev), THREE.MathUtils.degToRad(azim));
  return v;
}
export const posSol = (h: Hora, d = 900): [number, number, number] =>
  solVec(Math.max(LUZ[h].elev, 6), LUZ[h].azim).multiplyScalar(d).toArray() as [number, number, number];

/** cielo fisico + iluminacion por imagen + niebla. Es lo que separa el render de la maqueta. */
export const Ambiente: React.FC<{
  hora: Hora; nieblaLejos?: number; foco?: [number, number, number]; radio?: number;
}> = ({hora, nieblaLejos, foco = [300, 0, 150], radio = 380}) => {
  const {gl, scene} = useThree();
  useLayoutEffect(() => {
    const L = LUZ[hora];
    gl.toneMapping = (THREE as any).NeutralToneMapping ?? THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = L.exp;
    gl.shadowMap.enabled = true;
    gl.shadowMap.type = THREE.PCFSoftShadowMap;

    const sky = new Sky();
    sky.scale.setScalar(60000);
    const u = (sky.material as any).uniforms;
    u.turbidity.value = L.turb;
    u.rayleigh.value = L.ray;
    u.mieCoefficient.value = L.mie;
    u.mieDirectionalG.value = 0.86;
    u.sunPosition.value.copy(solVec(L.elev, L.azim));
    scene.add(sky);

    const pmrem = new THREE.PMREMGenerator(gl);
    const env = pmrem.fromScene(sky as any, 0.04);
    scene.environment = env.texture;
    (scene as any).environmentIntensity = L.env;
    scene.background = env.texture;
    scene.fog = new THREE.Fog(new THREE.Color(L.fog[0]), L.fog[1], nieblaLejos ?? L.fog[2]);
    return () => {
      scene.remove(sky);
      (sky.material as any).dispose();
      sky.geometry.dispose();
      env.texture.dispose();
      pmrem.dispose();
    };
  }, [gl, scene, hora, nieblaLejos]);

  const L = LUZ[hora];
  const blanco = useMemo(() => {
    const o = new THREE.Object3D();
    o.position.set(foco[0], foco[1], foco[2]);
    return o;
  }, [foco]);
  const sol = solVec(Math.max(L.elev, 6), L.azim).multiplyScalar(radio * 2.6);
  return (
    <>
      <primitive object={blanco} />
      <ambientLight intensity={L.amb} color={L.ambC} />
      {/* rebote del suelo: la tierra ocre devuelve luz caliente a los muros. Sin
          esto todo lo que no da al sol se pone azul y la pintura se pierde. */}
      <hemisphereLight args={[L.ambC, hora === 'noche' ? '#241f22' : '#a08a63',
                              hora === 'noche' ? 0.42 : 0.55]} />
      <directionalLight
        position={[foco[0] + sol.x, foco[1] + sol.y, foco[2] + sol.z]}
        target={blanco as any}
        intensity={L.dirI} color={L.dirC} castShadow
        shadow-mapSize-width={4096} shadow-mapSize-height={4096}
        shadow-camera-left={-radio} shadow-camera-right={radio}
        shadow-camera-top={radio} shadow-camera-bottom={-radio}
        shadow-camera-near={radio * 0.3} shadow-camera-far={radio * 6}
        shadow-bias={-0.0004} shadow-normalBias={0.06} />
    </>
  );
};

// ============================================================ volumenes
export const Caja: React.FC<{
  x: [number, number]; y: [number, number]; z: [number, number];
  c?: string; mapa?: THREE.Texture; normal?: THREE.Texture; mats?: THREE.Material[];
  rug?: number; met?: number; e?: string; ei?: number; sombra?: boolean;
}> = ({x, y, z, c, mapa, normal, mats, rug, met, e, ei, sombra = true}) => {
  const an = Math.abs(x[1] - x[0]), al = Math.abs(y[1] - y[0]), fo = Math.abs(z[1] - z[0]);
  return (
    <mesh position={[(x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2]}
          castShadow={sombra} receiveShadow material={mats as any}>
      <boxGeometry args={[an, al, fo]} />
      {!mats && (
        <meshStandardMaterial
          color={c ?? '#ffffff'} map={mapa} normalMap={normal}
          roughness={rug ?? 0.9} metalness={met ?? 0}
          emissive={e ?? '#000000'} emissiveIntensity={e ? (ei ?? 1) : 0} />
      )}
    </mesh>
  );
};

/** perfil triangular del hastial, solido, de alero a cumbrera */
const Hastial: React.FC<{
  x: [number, number]; z: [number, number]; y: number; alto: number;
  eje: 'x' | 'z'; mapa?: THREE.Texture; c?: string;
}> = ({x, z, y, alto, eje, mapa, c}) => {
  const an = x[1] - x[0], fo = z[1] - z[0];
  const base = eje === 'x' ? fo : an;
  const largo = eje === 'x' ? an : fo;
  const geo = useMemo(() => {
    const s = new THREE.Shape();
    s.moveTo(0, 0); s.lineTo(base, 0); s.lineTo(base / 2, alto); s.closePath();
    const g = new THREE.ExtrudeGeometry(s, {depth: largo, bevelEnabled: false});
    g.computeVertexNormals();
    return g;
  }, [base, alto, largo]);
  return (
    <mesh geometry={geo} castShadow receiveShadow
          position={eje === 'x' ? [x[0], y, z[1]] : [x[0], y, z[0]]}
          rotation={eje === 'x' ? [0, Math.PI / 2, 0] : [0, 0, 0]}>
      <meshStandardMaterial map={mapa} color={mapa ? '#ffffff' : (c ?? '#d9cfbe')} roughness={0.93} />
    </mesh>
  );
};

/** cubierta de zinc a dos aguas, con alero. La biblia la exige a dos aguas. */
export const TechoDosAguas: React.FC<{
  x: [number, number]; z: [number, number]; y: number;
  pend?: number; alero?: number; eje?: 'x' | 'z'; tono?: 'nuevo' | 'viejo' | 'oxido'; k?: number;
  sinHastial?: boolean; colHastial?: string; mapaHastial?: THREE.Texture;
}> = ({x, z, y, pend = 0.22, alero = 0.55, eje = 'x', tono = 'viejo', k = 1, sinHastial, colHastial, mapaHastial}) => {
  const an = x[1] - x[0], fo = z[1] - z[0];
  const d = (eje === 'x' ? fo : an) / 2;          // media luz, del caballete al alero
  const r = d * pend;                              // altura de la cumbrera
  const th = Math.atan2(r, d);
  const Ls = (d + alero) / Math.cos(th);
  const largo = (eje === 'x' ? an : fo) + alero * 2;
  const zin = texZinc(tono, k);
  const um = (d + alero) / 2;                      // medio faldon, en horizontal
  const yc = y + r - um * (r / d);
  const xc = (x[0] + x[1]) / 2, zc = (z[0] + z[1]) / 2;
  const mat = (
    <meshStandardMaterial map={zin.mapa} normalMap={zin.normal}
      normalScale={new THREE.Vector2(1.4, 1.4)} roughness={0.42} metalness={0.62} />
  );
  return (
    <group>
      {!sinHastial && (
        <Hastial x={x} z={z} y={y} alto={r} eje={eje} c={colHastial} mapa={mapaHastial} />
      )}
      {eje === 'x' ? (
        <>
          <mesh position={[xc, yc, zc + um]} rotation={[th, 0, 0]} castShadow receiveShadow>
            <boxGeometry args={[largo, 0.11, Ls]} />{mat}
          </mesh>
          <mesh position={[xc, yc, zc - um]} rotation={[-th, 0, 0]} castShadow receiveShadow>
            <boxGeometry args={[largo, 0.11, Ls]} />{mat}
          </mesh>
        </>
      ) : (
        <>
          <mesh position={[xc + um, yc, zc]} rotation={[0, 0, -th]} castShadow receiveShadow>
            <boxGeometry args={[Ls, 0.11, largo]} />{mat}
          </mesh>
          <mesh position={[xc - um, yc, zc]} rotation={[0, 0, th]} castShadow receiveShadow>
            <boxGeometry args={[Ls, 0.11, largo]} />{mat}
          </mesh>
        </>
      )}
    </group>
  );
};

// ============================================================ vegetacion
// Especies reales de la costa del Guayas. En estacion seca el ceibo pierde la hoja
// y queda el esqueleto blanco: es el arbol que dice "llanura del Guayas" de lejos.
export type Especie = 'ceibo' | 'almendro' | 'mango' | 'palma' | 'guayacan' | 'muyuyo';
export type Estacion = 'seca' | 'lluviosa';

const ESP: Record<Especie, {h: [number, number]; r: number; ry: number; col: string[]; tronco: string; grosor: number}> = {
  ceibo:    {h: [6.0, 8.2], r: 4.2, ry: 0.55, col: ['#6d7f4e', '#5f7546', '#77855a'], tronco: '#8e9481', grosor: 0.62},
  almendro: {h: [3.8, 5.0], r: 3.0, ry: 0.42, col: ['#46683a', '#3e6136', '#4f7142'], tronco: '#6d6152', grosor: 0.42},
  mango:    {h: [4.0, 5.6], r: 2.7, ry: 0.92, col: ['#31512c', '#2b4a28', '#3a5c33'], tronco: '#6b5b47', grosor: 0.52},
  guayacan: {h: [4.2, 5.8], r: 3.0, ry: 0.72, col: ['#c9a52a', '#d8b53a', '#bd9a26'], tronco: '#8b8272', grosor: 0.40},
  muyuyo:   {h: [1.4, 2.2], r: 1.7, ry: 0.85, col: ['#5d6e44', '#6b794e'], tronco: '#7a6d58', grosor: 0.18},
  palma:    {h: [7.0, 11.0], r: 3.4, ry: 0.5, col: ['#4a6b3c', '#54743f'], tronco: '#93866c', grosor: 0.26},
};

/** copa irregular: una esfera con los vertices desplazados. Una esfera lisa se lee
    como pelota de plastico; esta se lee como copa. Se cachean 5 variantes. */
function geoCopa(v: number) {
  return cache(`copa|${v}`, () => {
    const g = new THREE.IcosahedronGeometry(1, 2);
    const p = g.attributes.position as THREE.BufferAttribute;
    for (let i = 0; i < p.count; i++) {
      const x = p.getX(i), y = p.getY(i), z = p.getZ(i);
      const n = 0.72
        + 0.26 * Math.sin(x * 2.3 + v) * Math.cos(z * 2.1 - v)
        + 0.16 * Math.sin(y * 3.7 - v * 2) + 0.1 * Math.cos(x * 5.1 + z * 4.3);
      p.setXYZ(i, x * n, y * n, z * n);
    }
    g.computeVertexNormals();
    return g;
  });
}
/** hoja de palma: un cono aplastado y curvado hacia abajo */
function geoPenca() {
  return cache('penca', () => new THREE.ConeGeometry(0.46, 4.2, 5, 1, true));
}

export const Arbol: React.FC<{
  p: [number, number]; esp: Especie; k: number; y?: number; est?: Estacion;
  /** arbol de calle: se riega, asi que en verano NO pierde la hoja */
  regado?: boolean;
}> = ({p, esp, k, y = 0, est = 'seca', regado}) => {
  const c = ESP[esp];
  const v = rnd(k), v2 = rnd(k + 733);
  const h = c.h[0] + v * (c.h[1] - c.h[0]);
  const rad = c.r * (0.82 + v2 * 0.36);
  const pelado = esp === 'ceibo' && est === 'seca' && !regado;
  const col = elige(c.col, k + 3);
  if (pelado) {
    // Un ceibo sin hoja no es una copa transparente: es un tronco de botella con
    // cinco o seis ramas gruesas abiertas. Es la silueta del verano en el Guayas.
    return (
      <group position={[p[0], y, p[1]]} rotation={[0, v * 6.28, 0]}>
        <mesh position={[0, h * 0.5, 0]} castShadow>
          <cylinderGeometry args={[c.grosor * 0.42, c.grosor * 1.25, h, 9]} />
          <meshStandardMaterial color="#b3b7a2" roughness={1} />
        </mesh>
        {Array.from({length: 6}).map((_, i) => {
          const ang = (i / 6) * 6.28 + v * 2;
          const incl = 0.5 + rnd(k + i * 37) * 0.38;
          const lr = 2.4 + rnd(k + i * 53) * 2.2;
          return (
            <mesh key={i} castShadow
                  position={[Math.cos(ang) * lr * 0.42, h + Math.cos(incl) * lr * 0.5, Math.sin(ang) * lr * 0.42]}
                  rotation={[Math.sin(ang) * incl, 0, -Math.cos(ang) * incl]}>
              <cylinderGeometry args={[0.06, 0.2, lr, 6]} />
              <meshStandardMaterial color="#adb19c" roughness={1} />
            </mesh>
          );
        })}
      </group>
    );
  }
  if (esp === 'palma') {
    return (
      <group position={[p[0], y, p[1]]} rotation={[0, v * 6.28, 0]}>
        <mesh position={[0, h / 2, 0]} castShadow>
          <cylinderGeometry args={[c.grosor * 0.8, c.grosor, h, 7]} />
          <meshStandardMaterial color={c.tronco} roughness={1} />
        </mesh>
        {Array.from({length: 9}).map((_, i) => (
          <mesh key={i} geometry={geoPenca()} castShadow
                position={[Math.cos(i * 0.7) * 1.5, h + 0.5 - (i % 3) * 0.3, Math.sin(i * 0.7) * 1.5]}
                rotation={[Math.cos(i * 0.7) * 1.15, i * 0.7, Math.sin(i * 0.7) * 1.15 + 2.5]}
                scale={[1, 1, 0.22]}>
            <meshStandardMaterial color={elige(c.col, k + i)} roughness={0.95} side={THREE.DoubleSide} />
          </mesh>
        ))}
      </group>
    );
  }
  return (
    <group position={[p[0], y, p[1]]}>
      <mesh position={[0, h * 0.5, 0]} castShadow>
        <cylinderGeometry args={[c.grosor * 0.45, c.grosor, h, 8]} />
        <meshStandardMaterial color={c.tronco} roughness={1} />
      </mesh>
      <mesh geometry={geoCopa(Math.floor(rnd(k + 17) * 5))} castShadow
            position={[0, h + rad * c.ry * 0.55, 0]}
            rotation={[0, v * 6.28, 0]}
            scale={[rad, rad * c.ry, rad * (0.88 + v2 * 0.24)]}>
        <meshStandardMaterial color={col} roughness={1} flatShading />
      </mesh>
      {/* segunda lobula, descentrada: sin ella la copa se lee como pelota */}
      <mesh geometry={geoCopa(Math.floor(rnd(k + 91) * 5))} castShadow
            position={[rad * (v - 0.5) * 0.7, h + rad * c.ry * (0.3 + v2 * 0.4), rad * (v2 - 0.5) * 0.7]}
            rotation={[0, v2 * 6.28, 0]}
            scale={[rad * 0.66, rad * c.ry * 0.78, rad * 0.62]}>
        <meshStandardMaterial color={elige(c.col, k + 57)} roughness={1} flatShading />
      </mesh>
    </group>
  );
};

// ============================================================ postes y cables
// "Cables cruzando la calle" esta en la biblia. Sin ellos el barrio parece maqueta.
export const Poste: React.FC<{p: [number, number]; alto?: number; farol?: boolean; trafo?: boolean; noche?: boolean}> =
({p, alto = 8.6, farol, trafo, noche}) => (
  <group position={[p[0], 0, p[1]]}>
    <mesh position={[0, alto / 2, 0]} castShadow>
      <cylinderGeometry args={[0.13, 0.19, alto, 8]} />
      <meshStandardMaterial color="#9a958a" roughness={0.95} />
    </mesh>
    <Caja x={[-0.95, 0.95]} y={[alto - 0.6, alto - 0.42]} z={[-0.07, 0.07]} c="#8c8579" rug={0.95} />
    {trafo && (
      <mesh position={[0.5, alto - 1.9, 0]} castShadow>
        <cylinderGeometry args={[0.36, 0.36, 0.95, 10]} />
        <meshStandardMaterial color="#77716a" roughness={0.7} metalness={0.4} />
      </mesh>
    )}
    {farol && (
      <group>
        <Caja x={[0, 1.5]} y={[alto - 0.25, alto - 0.1]} z={[-0.07, 0.07]} c="#8c8579" rug={0.9} />
        <mesh position={[1.55, alto - 0.34, 0]} castShadow>
          <boxGeometry args={[0.62, 0.2, 0.34]} />
          <meshStandardMaterial color="#c9c4b8" roughness={0.5}
            emissive={noche ? '#ffcf8a' : '#000000'} emissiveIntensity={noche ? 3.2 : 0} />
        </mesh>
      </group>
    )}
  </group>
);

/** un vano de cable con su comba. Dos hilos, que es lo que se ve de lejos. */
export const Cable: React.FC<{a: [number, number, number]; b: [number, number, number]; comba?: number}> =
({a, b, comba = 1.1}) => {
  const geo = useMemo(() => {
    const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b);
    const M = A.clone().add(B).multiplyScalar(0.5);
    M.y -= comba * 2;
    const c = new THREE.QuadraticBezierCurve3(A, M, B);
    return new THREE.TubeGeometry(c, 10, 0.024, 3, false);
  }, [a, b, comba]);
  return (
    <mesh geometry={geo}>
      <meshStandardMaterial color="#2b2b2b" roughness={0.9} />
    </mesh>
  );
};

// ============================================================ vehiculos
// Los carros dan escala y dicen el pais. No hay personas a proposito: una figura
// humana mal hecha en la referencia se le contagia al video generado.
const COLOR_AUTO = ['#b7bec4', '#2f3a44', '#8c1f1a', '#d8d4cc', '#1f3f6b', '#5c6b57', '#c9a227', '#7a7e82'];

export const Carro: React.FC<{p: [number, number]; rot?: number; k: number; tipo?: 'auto' | 'camioneta' | 'buseta'}> =
({p, rot = 0, k, tipo = 'auto'}) => {
  const col = elige(COLOR_AUTO, k);
  const L = tipo === 'buseta' ? 6.4 : tipo === 'camioneta' ? 5.2 : 4.2;
  const A = tipo === 'buseta' ? 2.2 : 1.8;
  const hC = tipo === 'buseta' ? 2.5 : 1.42;
  return (
    <group position={[p[0], 0, p[1]]} rotation={[0, rot, 0]}>
      <Caja x={[-L / 2, L / 2]} y={[0.38, 0.95]} z={[-A / 2, A / 2]} c={col} rug={0.35} met={0.25} />
      {tipo === 'buseta' ? (
        <Caja x={[-L / 2 + 0.2, L / 2 - 0.2]} y={[0.95, hC]} z={[-A / 2, A / 2]} c="#20272e" rug={0.2} met={0.3} />
      ) : (
        <>
          <Caja x={[-L * 0.22, L * 0.28]} y={[0.95, hC]} z={[-A / 2 + 0.1, A / 2 - 0.1]} c="#20272e" rug={0.15} met={0.4} />
          {tipo === 'camioneta' && <Caja x={[-L / 2, -L * 0.24]} y={[0.95, 1.18]} z={[-A / 2, A / 2]} c={col} rug={0.4} />}
        </>
      )}
      {[[-L * 0.32, -A / 2], [-L * 0.32, A / 2], [L * 0.32, -A / 2], [L * 0.32, A / 2]].map(([a, b], i) => (
        <mesh key={i} position={[a, 0.34, b]} rotation={[Math.PI / 2, 0, 0]} castShadow>
          <cylinderGeometry args={[0.34, 0.34, 0.22, 12]} />
          <meshStandardMaterial color="#1a1a1a" roughness={0.95} />
        </mesh>
      ))}
    </group>
  );
};

/** moto y tricimoto: el vehiculo real de la costa, y la mitad del trabajo del taller */
export const Moto: React.FC<{p: [number, number]; rot?: number; k: number; tri?: boolean}> = ({p, rot = 0, k, tri}) => (
  <group position={[p[0], 0, p[1]]} rotation={[0, rot, 0]}>
    <Caja x={[-0.75, 0.55]} y={[0.5, 0.82]} z={[-0.14, 0.14]} c={elige(['#8c1f1a', '#1f3f6b', '#20242a', '#2f6b4a'], k)} rug={0.4} met={0.3} />
    <Caja x={[-0.2, 0.2]} y={[0.82, 1.18]} z={[-0.1, 0.1]} c="#2a2a2a" rug={0.6} />
    {[-0.78, 0.62].map((a, i) => (
      <mesh key={i} position={[a, 0.32, 0]} rotation={[Math.PI / 2, 0, 0]} castShadow>
        <cylinderGeometry args={[0.32, 0.32, 0.1, 12]} />
        <meshStandardMaterial color="#1a1a1a" roughness={0.95} />
      </mesh>
    ))}
    {tri && (
      <group>
        <Caja x={[-2.2, -0.7]} y={[0.4, 1.9]} z={[-0.62, 0.62]} c={elige(['#c9a227', '#b33', '#2f6b4a'], k + 5)} rug={0.5} />
        <Caja x={[-2.24, -0.66]} y={[1.9, 2.02]} z={[-0.7, 0.7]} c="#d8d4cc" rug={0.6} />
        {[-0.62, 0.62].map((b, i) => (
          <mesh key={i} position={[-1.9, 0.32, b]} rotation={[Math.PI / 2, 0, 0]} castShadow>
            <cylinderGeometry args={[0.32, 0.32, 0.1, 12]} />
            <meshStandardMaterial color="#1a1a1a" roughness={0.95} />
          </mesh>
        ))}
      </group>
    )}
  </group>
);

// ============================================================ remates de azotea
/** tanque, antena y tendedero. Vistos desde el aire son la mitad del realismo. */
export const Azotea: React.FC<{x: [number, number]; z: [number, number]; y: number; k: number}> = ({x, z, y, k}) => {
  const a = rnd(k + 401), b = rnd(k + 907), c = rnd(k + 1301);
  const cx = x[0] + (x[1] - x[0]) * (0.25 + a * 0.5);
  const cz = z[0] + (z[1] - z[0]) * (0.25 + b * 0.5);
  return (
    <group>
      {a > 0.48 && (
        <mesh position={[cx, y + 0.55, cz]} castShadow>
          <cylinderGeometry args={[0.55, 0.55, 1.1, 12]} />
          <meshStandardMaterial color={c > 0.5 ? '#2b2b2f' : '#2f6fa8'} roughness={0.55} />
        </mesh>
      )}
      {b > 0.72 && (
        <mesh position={[cx + 1.4, y + 1.1, cz]} castShadow>
          <cylinderGeometry args={[0.03, 0.03, 2.2, 4]} />
          <meshStandardMaterial color="#8a8a8a" roughness={0.8} />
        </mesh>
      )}
    </group>
  );
};

// ============================================================ la casa del barrio
// Bloque enlucido y pintado, medianeras ciegas (los lotes se pegan), cubierta de
// zinc a dos aguas con alero, rejas en la planta baja y, en una de cada cinco, la
// loza de arriba sin terminar con las varillas al aire esperando el otro piso.
export const CASAS = ['#e8ded0', '#d9c9a8', '#cdd9cf', '#e3cdb4', '#cfd8dd', '#e6d7a8',
                      '#d6c2be', '#c9d6c2', '#e0cfc0', '#bfd0cd', '#e5c9a6', '#d2cfc4'];
export const FUERTES = ['#7fb3a8', '#d9a441', '#c96f52', '#8fa9c4', '#b5c47a', '#cf8fa0',
                        '#e0b64c', '#9ec0b4', '#c98b6a'];
const TONOS_ZINC: ('nuevo' | 'viejo' | 'oxido')[] = ['viejo', 'viejo', 'oxido', 'nuevo', 'oxido'];

export type Frente = 'n' | 's' | 'e' | 'o';

export const Casa: React.FC<{
  x: [number, number]; z: [number, number]; k: number;
  frente: Frente; pisos?: number; col?: string; noche?: boolean; local?: boolean;
}> = ({x, z, k, frente, pisos, col, noche, local}) => {
  const a = rnd(k), b = rnd(k + 7919), c = rnd(k + 104729), d = rnd(k + 31337);
  const np = pisos ?? (a < 0.63 ? 1 : 2);
  const h = np * 2.95 + 0.4;
  const color = col ?? (c < 0.26 ? elige(FUERTES, k + 31) : elige(CASAS, k + 53));
  const sinTerminar = np === 2 && d > 0.82;          // la loza esperando el tercer piso
  const ejeTecho: 'x' | 'z' = (frente === 'n' || frente === 's') ? 'x' : 'z';

  const fach = local ? texLocal(color, k, noche) : texFachada(color, np, k, b > 0.35, noche);
  const lateral = texMuro(color, k + 11, np);
  const trasera = b > 0.6 ? texBloque(k) : texMuro(color, k + 23, np);
  const enc = noche && !local ? texEncendidas(np, k, b > 0.35) : undefined;
  const mats = useMemo(() => {
    const f = mat(fach, 0.93, enc);
    const l = mat(lateral), tr = mat(trasera);
    // orden de BoxGeometry: +x, -x, +y, -y, +z, -z
    const o = [l, l, l, l, l, l];
    if (frente === 'e') o[0] = f; else if (frente === 'o') o[1] = f;
    else if (frente === 's') o[4] = f; else o[5] = f;
    if (frente === 'e') o[1] = tr; else if (frente === 'o') o[0] = tr;
    else if (frente === 's') o[5] = tr; else o[4] = tr;
    return o;
  }, [fach, lateral, trasera, frente, enc]);

  return (
    <group>
      <Caja x={x} y={[0, h]} z={z} mats={mats} />
      {sinTerminar ? (
        <group>
          <Caja x={[x[0] - 0.12, x[1] + 0.12]} y={[h, h + 0.22]} z={[z[0] - 0.12, z[1] + 0.12]}
                mapa={texBloque(k + 7)} rug={0.95} />
          {Array.from({length: 6}).map((_, i) => (
            <mesh key={i} castShadow
                  position={[x[0] + 0.5 + ((x[1] - x[0] - 1) * i) / 5, h + 0.62, z[0] + 0.5 + rnd(k + i) * (z[1] - z[0] - 1)]}>
              <cylinderGeometry args={[0.035, 0.035, 0.8, 4]} />
              <meshStandardMaterial color="#8a7a63" roughness={1} />
            </mesh>
          ))}
          <Azotea x={x} z={z} y={h + 0.22} k={k} />
        </group>
      ) : (
        <>
          <TechoDosAguas x={x} z={z} y={h} eje={ejeTecho} k={k}
            tono={elige(TONOS_ZINC, k + 211)} pend={0.2 + b * 0.1} alero={0.45 + a * 0.35}
            mapaHastial={lateral} />
          <Azotea x={x} z={z} y={h + 0.2} k={k + 3} />
        </>
      )}
    </group>
  );
};

/** local con portal sobre la vereda: la sombra que se hace en la costa */
export const LocalConPortal: React.FC<{
  x: [number, number]; z: [number, number]; k: number; frente: Frente; noche?: boolean;
}> = ({x, z, k, frente, noche}) => {
  const a = rnd(k), col = a < 0.4 ? elige(FUERTES, k + 41) : elige(CASAS, k + 59);
  const np = a > 0.66 ? 2 : 1;
  const h = np * 3.1 + 0.4;
  const P = 2.6;                                     // vuelo del portal
  const fz: [number, number] = frente === 'n' ? [z[0] + P, z[1]] : frente === 's' ? [z[0], z[1] - P] : z;
  const fx: [number, number] = frente === 'o' ? [x[0] + P, x[1]] : frente === 'e' ? [x[0], x[1] - P] : x;
  const px: [number, number] = frente === 'o' ? [x[0], x[0] + P] : frente === 'e' ? [x[1] - P, x[1]] : x;
  const pz: [number, number] = frente === 'n' ? [z[0], z[0] + P] : frente === 's' ? [z[1] - P, z[1]] : z;
  const ejeTecho: 'x' | 'z' = (frente === 'n' || frente === 's') ? 'x' : 'z';
  return (
    <group>
      <Casa x={fx} z={fz} k={k} frente={frente} pisos={np} col={col} noche={noche} local />
      {/* losa del portal y sus columnas */}
      <Caja x={px} y={[3.0, 3.24]} z={pz} c="#cdc6b6" rug={0.92} />
      {[0, 1].map((i) => {
        const cx = frente === 'n' || frente === 's'
          ? x[0] + 0.5 + i * (x[1] - x[0] - 1) : (px[0] + px[1]) / 2;
        const cz = frente === 'n' || frente === 's'
          ? (pz[0] + pz[1]) / 2 : z[0] + 0.5 + i * (z[1] - z[0] - 1);
        return <Caja key={i} x={[cx - 0.16, cx + 0.16]} y={[0, 3.0]} z={[cz - 0.16, cz + 0.16]} c="#cdc6b6" rug={0.92} />;
      })}
      <TechoDosAguas x={fx} z={fz} y={h} eje={ejeTecho} k={k + 5}
        tono={elige(TONOS_ZINC, k + 77)} pend={0.18} alero={0.5} mapaHastial={texMuro(col, k + 11, np)} />
    </group>
  );
};

/** nave: mercado, bodega, camaronera. Cubierta larga a dos aguas sobre muro bajo. */
export const Nave: React.FC<{
  x: [number, number]; z: [number, number]; alto?: number; col?: string; k: number;
  eje?: 'x' | 'z'; tono?: 'nuevo' | 'viejo' | 'oxido'; sinAberturas?: boolean; noche?: boolean;
}> = ({x, z, alto = 5.6, col = '#d8d2c4', k, eje = 'x', tono = 'nuevo', sinAberturas, noche}) => {
  // Puertas y ventanas altas en las dos caras largas. Sin ellas, de cerca el mercado
  // y la escuela son cajas, y se nota en cuanto la camara baja a la calle.
  const largo = eje === 'x' ? x[1] - x[0] : z[1] - z[0];
  const n = Math.max(2, Math.round(largo / 9));
  const paso = largo / n;
  const vidrio = noche ? '#ffc97a' : '#28313a';
  return (
    <group>
      <Caja x={x} y={[0, alto]} z={z} mapa={texMuro(col, k, 2)} rug={0.94} />
      {!sinAberturas && Array.from({length: n}).map((_, i) => {
        const a = (eje === 'x' ? x[0] : z[0]) + i * paso + paso * 0.28;
        const b = a + paso * 0.44;
        const puerta = i % 3 === 1;
        const y0 = puerta ? 0.1 : alto * 0.48;
        const y1 = puerta ? alto * 0.62 : alto * 0.82;
        return eje === 'x' ? (
          <group key={i}>
            <Caja x={[a, b]} y={[y0, y1]} z={[z[0] - 0.06, z[0] + 0.04]} c={vidrio} rug={0.4}
                  e={noche ? vidrio : undefined} ei={noche ? 1.4 : 0} />
            <Caja x={[a, b]} y={[y0, y1]} z={[z[1] - 0.04, z[1] + 0.06]} c={vidrio} rug={0.4}
                  e={noche ? vidrio : undefined} ei={noche ? 1.4 : 0} />
          </group>
        ) : (
          <group key={i}>
            <Caja x={[x[0] - 0.06, x[0] + 0.04]} y={[y0, y1]} z={[a, b]} c={vidrio} rug={0.4}
                  e={noche ? vidrio : undefined} ei={noche ? 1.4 : 0} />
            <Caja x={[x[1] - 0.04, x[1] + 0.06]} y={[y0, y1]} z={[a, b]} c={vidrio} rug={0.4}
                  e={noche ? vidrio : undefined} ei={noche ? 1.4 : 0} />
          </group>
        );
      })}
      <TechoDosAguas x={x} z={z} y={alto} eje={eje} k={k} tono={tono} pend={0.16} alero={0.8}
        mapaHastial={texMuro(col, k, 2)} />
    </group>
  );
};
