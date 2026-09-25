// Maqueta 3D del Barrio El Cruce, Puerto Candela. Medidas en metros.
// La geometria sale TAL CUAL del plano urbano (01-plano-urbano-el-cruce.png): las
// mismas columnas, las mismas filas, la misma avenida de 40 m con parterre y el
// mismo pasaje de 5 m. Si el plano cambia, esto cambia con el.
//
// POR QUE EXISTE: algunos episodios abren con la ciudad y desde angulos distintos.
// Sin una maqueta, cada toma inventa el barrio y a los tres videos el espectador
// nota que el lugar no es el mismo.
//
// SEMILLA FIJA. Las casas, sus alturas y sus colores salen de un generador
// pseudoaleatorio con semilla constante: el mismo lote saca siempre la misma casa,
// del mismo color y del mismo alto. La ciudad es reproducible. Cambiar SEMILLA
// cambia el barrio entero, asi que no se toca.
//
// Ejes: x = 0 al oeste y 600 al este; z = 0 al norte (el cerro) y 299 al sur (la
// zona industrial); y = altura. Es el mismo norte-arriba del plano.
import React, {useLayoutEffect, useMemo} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';

type V3 = [number, number, number];

// ---------------------------------------------------------------- utilidades
const SEMILLA = 20260925;
function rnd(n: number) {
  // generador determinista: misma n, mismo numero, siempre
  let t = (n * 1103515245 + SEMILLA) >>> 0;
  t ^= t >>> 15;
  t = Math.imul(t, 2246822507) >>> 0;
  t ^= t >>> 13;
  return (t >>> 0) / 4294967296;
}

const Caja: React.FC<{x: [number, number]; y: [number, number]; z: [number, number]; c: string; e?: string; ei?: number}> =
  ({x, y, z, c, e, ei}) => (
    <mesh position={[(x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2]} castShadow receiveShadow>
      <boxGeometry args={[Math.abs(x[1] - x[0]), Math.abs(y[1] - y[0]), Math.abs(z[1] - z[0])]} />
      <meshStandardMaterial color={c} emissive={e ?? '#000000'} emissiveIntensity={e ? (ei ?? 1) : 0} roughness={0.85} />
    </mesh>
  );

// ---------------------------------------------------------------- paisajismo
// PROPUESTA. Tres especies, una por jerarquia de via, que es como se planta de
// verdad y ademas hace que cada calle se reconozca desde el aire:
//   ceibo     en el parterre de la avenida  — el arbol grande de la costa
//   almendro  en la Calle Olmedo            — copa ancha y baja, sombra al taller
//   mango     en las calles locales         — es el arbol de patio del Guayas
const Arbol: React.FC<{p: [number, number]; tipo: 'ceibo' | 'almendro' | 'mango'; k: number}> = ({p, tipo, k}) => {
  const v = rnd(k);
  const esc = 0.85 + v * 0.3;
  const conf = {
    ceibo: {h: 7.5, r: 4.6, c: '#5d7f4a', tronco: '#b9b0a0', ry: 0.72},
    almendro: {h: 4.2, r: 3.8, c: '#4f7340', tronco: '#6e6152', ry: 0.5},
    mango: {h: 5.0, r: 3.0, c: '#3f6236', tronco: '#6b5b47', ry: 0.95},
  }[tipo];
  return (
    <group position={[p[0], 0, p[1]]}>
      <mesh position={[0, (conf.h * esc) / 2, 0]} castShadow>
        <cylinderGeometry args={[0.22 * esc, 0.34 * esc, conf.h * esc, 7]} />
        <meshStandardMaterial color={conf.tronco} roughness={1} />
      </mesh>
      <mesh position={[0, conf.h * esc, 0]} castShadow scale={[1, conf.ry, 1]}>
        <sphereGeometry args={[conf.r * esc, 9, 7]} />
        <meshStandardMaterial color={conf.c} roughness={1} />
      </mesh>
    </group>
  );
};

// ---------------------------------------------------------------- color del barrio
// PROPUESTA DE COLORES. Bloque enlucido y pintado en colores fuertes pero gastados
// por el sol y el salitre: nada saturado, todo con tiza. La regla que sostiene todo:
// EN EL BARRIO NO HAY OTRO EDIFICIO NEGRO NI OTRO VERDE BOTELLA. El taller y el bar
// son los unicos, y por eso se reconocen desde cualquier angulo y a cualquier hora.
const CASAS = ['#e8ded0', '#d9c9a8', '#cdd9cf', '#e3cdb4', '#cfd8dd', '#e6d7a8',
               '#d6c2be', '#c9d6c2', '#e0cfc0', '#bfd0cd', '#e5c9a6', '#d2cfc4'];
const FUERTES = ['#7fb3a8', '#d9a441', '#c96f52', '#8fa9c4', '#b5c47a', '#cf8fa0'];
const ZINC = '#8f959b';
const ZINC_NUEVO = '#b3bcc2';
const ZINC_VIEJO = '#9a8676';   // oxidado por el salitre
const TECHOS = [ZINC, ZINC_NUEVO, ZINC_VIEJO, ZINC, ZINC_VIEJO];

const COLS: [number, number][] = [[12, 112], [124, 224], [244, 344], [356, 456], [468, 588]];
const FILAS: Record<string, [number, number]> = {
  '1': [12, 56], '2': [68, 112], '3': [152, 187], '4': [187, 231], '5': [243, 287],
};

/** una casa de lote: uno o dos pisos, con su techo de zinc y a veces un portal */
const Casa: React.FC<{x0: number; x1: number; z0: number; z1: number; k: number}> = ({x0, x1, z0, z1, k}) => {
  const a = rnd(k), b = rnd(k + 7919), c = rnd(k + 104729);
  const pisos = a < 0.62 ? 1 : 2;
  const h = pisos === 1 ? 3.1 + b * 0.5 : 5.9 + b * 0.8;
  const col = c < 0.22 ? FUERTES[Math.floor(rnd(k + 31) * FUERTES.length)]
                       : CASAS[Math.floor(rnd(k + 53) * CASAS.length)];
  const fondo = z0 + (z1 - z0) * (0.62 + a * 0.28);       // el patio queda atras
  return (
    <group>
      <Caja x={[x0 + 0.25, x1 - 0.25]} y={[0, h]} z={[z0, fondo]} c={col} />
      <Caja x={[x0 + 0.05, x1 - 0.05]} y={[h, h + 0.35]} z={[z0 - 0.35, fondo + 0.35]}
            c={TECHOS[Math.floor(rnd(k + 211) * TECHOS.length)]} />
      {b > 0.68 && <Caja x={[x0 + 0.4, x1 - 0.4]} y={[h, h + 1.0]} z={[z0 + 0.4, z0 + 1.6]} c={col} />}
    </group>
  );
};

/** una manzana residencial: dos filas de lotes que miran a calles opuestas */
const ManzanaCasas: React.FC<{x0: number; z0: number; x1: number; z1: number; k: number}> = ({x0, z0, x1, z1, k}) => {
  const n = Math.max(1, Math.round((x1 - x0) / 8));
  const paso = (x1 - x0) / n;
  const medio = (z0 + z1) / 2;
  const out: JSX.Element[] = [];
  for (let i = 0; i < n; i++) {
    out.push(<Casa key={`n${i}`} x0={x0 + i * paso} x1={x0 + (i + 1) * paso} z0={z0} z1={medio} k={k + i * 13} />);
    out.push(<Casa key={`s${i}`} x0={x0 + i * paso} x1={x0 + (i + 1) * paso} z0={z1} z1={medio} k={k + 500 + i * 13} />);
  }
  return <group>{out}</group>;
};

/** la franja comercial de la avenida: locales de un piso con portal a la vereda */
const Franja: React.FC<{x0: number; z0: number; x1: number; z1: number; k: number}> = ({x0, z0, x1, z1, k}) => {
  const n = Math.max(1, Math.round((x1 - x0) / 10));
  const paso = (x1 - x0) / n;
  const out: JSX.Element[] = [];
  for (let i = 0; i < n; i++) {
    const a = rnd(k + i * 17);
    const h = 4.2 + a * 2.6;
    const col = a < 0.35 ? FUERTES[Math.floor(rnd(k + i * 41) * FUERTES.length)]
                         : CASAS[Math.floor(rnd(k + i * 59) * CASAS.length)];
    out.push(
      <group key={i}>
        <Caja x={[x0 + i * paso + 0.2, x0 + (i + 1) * paso - 0.2]} y={[0, h]} z={[z0 + 2.6, z1]} c={col} />
        <Caja x={[x0 + i * paso + 0.2, x0 + (i + 1) * paso - 0.2]} y={[h, h + 0.3]} z={[z0 + 2.0, z1 + 0.3]} c={TECHOS[Math.floor(rnd(k + i * 97) * TECHOS.length)]} />
        {/* portal sobre la vereda: sombra, que es lo que se hace en la costa */}
        <Caja x={[x0 + i * paso + 0.2, x0 + (i + 1) * paso - 0.2]} y={[3.2, 3.45]} z={[z0, z0 + 2.6]} c="#cfc7b6" />
        <Caja x={[x0 + i * paso + 0.35, x0 + i * paso + 0.65]} y={[0, 3.2]} z={[z0 + 0.1, z0 + 0.4]} c="#cfc7b6" />
      </group>,
    );
  }
  return <group>{out}</group>;
};

// ---------------------------------------------------------------- los dos anclas
const Taller: React.FC = () => (
  <group>
    <Caja x={[244, 268]} y={[0, 7.25]} z={[152, 182]} c="#1d1b19" />
    <Caja x={[244, 251.5]} y={[5.75, 9.75]} z={[152, 173]} c="#efe6d2" />
    <Caja x={[243.8, 268.2]} y={[7.25, 7.55]} z={[151.8, 182.2]} c={ZINC} />
    <Caja x={[243.8, 251.7]} y={[9.75, 10.05]} z={[151.8, 173.2]} c={ZINC} />
    <Caja x={[244, 268]} y={[0, 0.4]} z={[151.9, 182.1]} c="#2f2c29" />
    {/* letrero y gallo, sobre la avenida */}
    <Caja x={[252, 266]} y={[4.9, 6.2]} z={[151.85, 152]} c="#121110" />
    <Caja x={[252.4, 265.6]} y={[5.25, 5.75]} z={[151.8, 151.86]} c="#d4ad52" e="#c49a3a" ei={0.7} />
    <Caja x={[258, 260]} y={[6.2, 8.4]} z={[151.8, 151.95]} c="#c62828" e="#ff2a1a" ei={2.4} />
    {[253, 256, 262.5, 265.5].map((xx) => (
      <mesh key={xx} position={[xx, 7.9, 160 + (xx % 2) * 8]} castShadow>
        <cylinderGeometry args={[0.45, 0.45, 0.5, 10]} />
        <meshStandardMaterial color="#b9c0c6" />
      </mesh>
    ))}
    {/* el toldo de espera, sobre el retiro de la Calle Olmedo */}
    <Caja x={[239, 244]} y={[3.1, 3.25]} z={[155, 167]} c="#c9c0ae" />
  </group>
);

const Bar: React.FC = () => (
  <group>
    <Caja x={[244, 256]} y={[0, 7.5]} z={[92, 112]} c="#1f4d3a" />
    <Caja x={[243.8, 256.2]} y={[7.5, 7.8]} z={[91.8, 112.2]} c={ZINC} />
    {[3.6, 6.9].map((yy) => <Caja key={yy} x={[243.7, 256.3]} y={[yy, yy + 0.12]} z={[91.7, 112.3]} c="#efe6d2" />)}
    <Caja x={[247.6, 252.4]} y={[3.9, 4.45]} z={[111.9, 112.1]} c="#ff6ab5" e="#ff2f9c" ei={2.0} />
    <Caja x={[247, 253]} y={[4.75, 5.9]} z={[112, 113.2]} c="#6b4a2e" />
    <Caja x={[244.6, 246.6]} y={[7.8, 9.4]} z={[93.2, 95.2]} c="#9fb3bd" />
  </group>
);

// ---------------------------------------------------------------- equipamiento
// Institucional: blanco y azul, que es como se ve un edificio publico ecuatoriano.
// Deliberadamente distinto del color de las casas, para que se lea desde el aire.
const Equipamiento: React.FC = () => (
  <group>
    {/* Mz. B · Escuela Fiscal Vicente Rocafuerte */}
    <Caja x={[128, 220]} y={[0, 6.4]} z={[16, 34]} c="#f0ece2" />
    <Caja x={[127.6, 220.4]} y={[6.4, 6.7]} z={[15.6, 34.4]} c={ZINC} />
    <Caja x={[128, 220]} y={[2.9, 3.4]} z={[15.8, 16.2]} c="#2f5aa0" />
    <Caja x={[150, 200]} y={[0, 0.12]} z={[40, 54]} c="#9db089" />
    {/* Mz. C · Mercado Municipal: una nave de zinc, 84 puestos */}
    <Caja x={[248, 340]} y={[0, 5.6]} z={[16, 52]} c="#e7dcc6" />
    <Caja x={[247, 341]} y={[5.6, 6.9]} z={[15, 53]} c={ZINC_NUEVO} />
    <Caja x={[247, 341]} y={[6.9, 7.1]} z={[33, 35]} c="#6f767c" />
    {/* Mz. F · Iglesia de la Virgen del Carmen */}
    <Caja x={[80, 112]} y={[0, 8.2]} z={[68, 92]} c="#f4f1e8" />
    <Caja x={[79.6, 112.4]} y={[8.2, 8.6]} z={[67.6, 92.4]} c="#9db8c4" />
    <Caja x={[93, 99]} y={[8.6, 17]} z={[70, 76]} c="#f4f1e8" />
    <Caja x={[94.6, 97.4]} y={[17, 19.6]} z={[71.6, 74.4]} c="#9db8c4" />
    <Caja x={[95.6, 96.4]} y={[19.6, 21.4]} z={[72.6, 73.4]} c="#d4ad52" e="#a8801f" ei={0.4} />
    {/* Mz. G · Parque del Reloj, con su torre que atrasa */}
    <Caja x={[124, 224]} y={[-0.02, 0.1]} z={[68, 112]} c="#8fa877" />
    <Caja x={[170, 178]} y={[0, 9.5]} z={[86, 94]} c="#e8e0cc" />
    <Caja x={[170.6, 177.4]} y={[9.5, 12.2]} z={[86.6, 93.4]} c="#b9b0a0" />
    <Caja x={[172, 176]} y={[7.4, 9.2]} z={[85.8, 86.2]} c="#f6f2e4" e="#d8cfa8" ei={0.5} />
    {/* Mz. I · UPC y Centro de Salud */}
    <Caja x={[360, 392]} y={[0, 5.2]} z={[90, 110]} c="#e9eef3" />
    <Caja x={[360, 392]} y={[5.2, 5.5]} z={[89.6, 110.4]} c="#2f5aa0" />
    <Caja x={[398, 428]} y={[0, 5.0]} z={[90, 110]} c="#eef3f2" />
    <Caja x={[398, 428]} y={[5.0, 5.3]} z={[89.6, 110.4]} c="#3f8f86" />
    {/* Mz. J · Hostal El Descanso y Hotel Panamericano */}
    <Caja x={[494, 534]} y={[0, 8.0]} z={[88, 110]} c="#e6d7b8" />
    <Caja x={[540, 588]} y={[0, 10.6]} z={[84, 110]} c="#ddd2c0" />
    {[534, 588].map((xx) => <Caja key={xx} x={[xx - 46, xx]} y={[10.6, 10.9]} z={[84, 110]} c={ZINC} />)}
    {/* Hospital de Emergencias, dos manzanas al sureste */}
    <Caja x={[472, 584]} y={[0, 11.2]} z={[191, 283]} c="#f2f2f0" />
    <Caja x={[471.6, 584.4]} y={[11.2, 11.6]} z={[190.6, 283.4]} c={ZINC_NUEVO} />
    <Caja x={[524, 532]} y={[5.4, 6.2]} z={[190.4, 191]} c="#b3261e" e="#8f1c16" ei={0.5} />
    <Caja x={[527, 529]} y={[4.2, 7.4]} z={[190.4, 191]} c="#b3261e" e="#8f1c16" ei={0.5} />
    {/* Mz. V · losa deportiva */}
    <Caja x={[244, 290]} y={[-0.01, 0.08]} z={[243, 287]} c="#9aa8b4" />
    {/* Gasolinera El Último, donde empieza la carretera */}
    <Caja x={[540, 588]} y={[0, 0.1]} z={[152, 187]} c="#cfcabd" />
    <Caja x={[548, 580]} y={[5.2, 5.9]} z={[158, 176]} c="#f0e08a" e="#d8c07a" ei={0.3} />
    {[550, 578].map((xx) => <Caja key={xx} x={[xx - 0.5, xx + 0.5]} y={[0, 5.2]} z={[166, 168]} c="#cfcabd" />)}
  </group>
);

// ---------------------------------------------------------------- el barrio entero
const BARRIO: React.FC = () => {
  const manzanas = useMemo(() => {
    const out: JSX.Element[] = [];
    const letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let li = 0;
    Object.entries(FILAS).forEach(([fila, [z0, z1]]) => {
      COLS.forEach(([x0, x1], c) => {
        if ((fila === '4' || fila === '5') && c === 4) return;     // ahí va el hospital
        const letra = letras[li++];
        const k = li * 1009;
        if (['B', 'C', 'F', 'G', 'I', 'J', 'V'].includes(letra)) return;   // equipamiento
        if (fila === '3') {
          out.push(<Franja key={letra} x0={x0} z0={z0} x1={x1} z1={c === 2 ? 182 : z1} k={k} />);
        } else if (fila === '4' && c === 2) {
          out.push(<ManzanaCasas key={letra} x0={x0} z0={187} x1={x1} z1={z1} k={k} />);
        } else {
          out.push(<ManzanaCasas key={letra} x0={x0} z0={z0} x1={x1} z1={z1} k={k} />);
        }
      });
    });
    return out;
  }, []);

  const arboles = useMemo(() => {
    const out: JSX.Element[] = [];
    for (let x = 20; x < 590; x += 22) {
      if (x > 218 && x < 252) continue;              // el cruce con la Calle Olmedo va despejado
      out.push(<Arbol key={`c${x}`} p={[x, 132]} tipo="ceibo" k={x} />);
    }
    for (let z = 16; z < 290; z += 17) {
      if (z > 110 && z < 154) continue;
      // delante del toldo del taller no se planta: es la vereda de espera
      if (!(z > 148 && z < 192)) out.push(<Arbol key={`a${z}`} p={[234, z]} tipo="almendro" k={z * 3} />);
      out.push(<Arbol key={`b${z}`} p={[352, z]} tipo="almendro" k={z * 5} />);
    }
    for (let x = 30; x < 590; x += 26) {
      for (const z of [62, 237]) out.push(<Arbol key={`m${x}-${z}`} p={[x, z]} tipo="mango" k={x + z} />);
    }
    for (let i = 0; i < 24; i++) {
      out.push(<Arbol key={`p${i}`} p={[132 + rnd(i) * 84, 72 + rnd(i + 99) * 36]} tipo="mango" k={i * 77} />);
    }
    return out;
  }, []);

  return (
    <group>
      {/* el suelo: tierra de la costa, no asfalto */}
      <Caja x={[-120, 720]} y={[-0.35, -0.06]} z={[-260, 420]} c="#a2977f" />
      {/* calzadas */}
      <Caja x={[-160, 760]} y={[-0.05, 0]} z={[112, 152]} c="#4a4844" />
      <Caja x={[-160, 760]} y={[0, 0.25]} z={[130, 134]} c="#7d8f68" />
      <Caja x={[224, 244]} y={[-0.05, 0]} z={[-20, 320]} c="#55524e" />
      {[[0, 12], [112, 124], [344, 356], [456, 468], [588, 600]].map(([a, b]) => (
        <Caja key={a} x={[a, b]} y={[-0.05, 0]} z={[-20, 320]} c="#5d5a55" />
      ))}
      {[[0, 12], [56, 68], [231, 243], [287, 299]].map(([a, b]) => (
        <Caja key={`h${a}`} x={[-20, 620]} y={[-0.05, 0]} z={[a, b]} c="#5d5a55" />
      ))}
      <Caja x={[244, 344]} y={[-0.04, 0]} z={[182, 187]} c="#6b6862" />
      {/* alumbrado publico: la avenida y la colectora. De noche el barrio se lee,
          pero el foco que manda sigue siendo el del taller. */}
      {Array.from({length: 13}).map((_, i) => {
        const x = 34 + i * 44;
        if (x > 218 && x < 252) return null;
        return (
          <group key={`far${i}`}>
            <Caja x={[x - 0.12, x + 0.12]} y={[0, 8]} z={[131.9, 132.1]} c="#5c5952" />
            <Caja x={[x - 0.5, x + 0.5]} y={[8, 8.3]} z={[131.4, 132.6]} c="#d8d2c4" e="#ffd79a" ei={0.9} />
          </group>
        );
      })}
      {[64, 98, 200, 216, 262].map((z) => (
        <group key={`fo${z}`}>
          <Caja x={[233.9, 234.1]} y={[0, 7]} z={[z - 0.12, z + 0.12]} c="#5c5952" />
          <Caja x={[233.4, 234.6]} y={[7, 7.3]} z={[z - 0.5, z + 0.5]} c="#d8d2c4" e="#ffd79a" ei={0.9} />
        </group>
      ))}
      {manzanas}
      <Equipamiento />
      {arboles}
      <Taller />
      <Bar />
      {/* Cerro El Mirador al norte, con el asentamiento humano en la ladera.
          Las casas se apoyan en la pendiente real del cono, no flotando. */}
      <mesh position={[300, -2, -150]} castShadow receiveShadow>
        <coneGeometry args={[165, 48, 9]} />
        <meshStandardMaterial color="#b0a184" roughness={1} />
      </mesh>
      {Array.from({length: 30}).map((_, i) => {
        const ang = -0.15 + rnd(i * 3) * 3.44;                 // solo la ladera que mira al barrio
        const rad = 58 + rnd(i * 5) * 92;
        const x = 300 + Math.cos(ang) * rad;
        const z = -150 + Math.sin(ang) * rad;
        if (z < -148) return null;
        const suelo = Math.max(0, 46 * (1 - rad / 165) - 2);   // altura del cono a ese radio
        const h = 2.6 + rnd(i) * 2.8;
        return (
          <group key={`as${i}`}>
            <Caja x={[x, x + 6.5]} y={[suelo - 1.5, suelo + h]} z={[z, z + 6.5]}
                  c={CASAS[Math.floor(rnd(i * 11) * CASAS.length)]} />
            <Caja x={[x - 0.3, x + 6.8]} y={[suelo + h, suelo + h + 0.25]} z={[z - 0.3, z + 6.8]} c={ZINC} />
          </group>
        );
      })}
      {/* zona industrial al sur: bodegas y camaroneras, naves sueltas y no una losa */}
      {Array.from({length: 9}).map((_, i) => {
        const x = 30 + i * 62 + rnd(i * 7) * 10;
        const z = 314 + rnd(i * 13) * 16;
        const an = 34 + rnd(i * 17) * 18, fo = 24 + rnd(i * 23) * 12;
        const h = 6.5 + rnd(i * 29) * 3.5;
        return (
          <group key={`zi${i}`}>
            <Caja x={[x, x + an]} y={[0, h]} z={[z, z + fo]} c={i % 3 ? '#cfc8b8' : '#c3cbc6'} />
            <Caja x={[x - 0.6, x + an + 0.6]} y={[h, h + 0.4]} z={[z - 0.6, z + fo + 0.6]} c={ZINC} />
          </group>
        );
      })}
    </group>
  );
};

// ---------------------------------------------------------------- las vistas oficiales
const VISTAS: Record<string, {p: V3; t: V3; fov: number; noche?: boolean}> = {
  barrio_aereo: {p: [-190, 330, -210], t: [300, 0, 150], fov: 42},
  barrio_cenital: {p: [300, 620, 152], t: [300, 0, 150], fov: 40},
  la_cuadra: {p: [180, 78, 240], t: [280, 0, 130], fov: 46},
  la_esquina: {p: [233, 8.5, 226], t: [256, 3.8, 128], fov: 58},
  avenida: {p: [90, 5.2, 142], t: [520, 4.5, 130], fov: 52},
  olmedo: {p: [234, 4.6, 268], t: [234, 3.6, 150], fov: 56},
  parque: {p: [150, 4.4, 130], t: [176, 6, 90], fov: 58},
  esquina_noche: {p: [226, 6.2, 121], t: [268, 5.4, 140], fov: 74, noche: true},
};
export const ORDEN_CIUDAD = Object.keys(VISTAS);

const Camara: React.FC<{v: (typeof VISTAS)[string]}> = ({v}) => {
  const {camera} = useThree();
  useLayoutEffect(() => {
    camera.position.set(...v.p);
    (camera as any).fov = v.fov;
    camera.lookAt(...v.t);
    camera.updateProjectionMatrix();
  }, [camera, v]);
  return null;
};

export const Ciudad3D: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const v = VISTAS[ORDEN_CIUDAD[Math.min(frame, ORDEN_CIUDAD.length - 1)]];
  const noche = !!v.noche;
  return (
    <ThreeCanvas width={width} height={height} shadows
                 style={{background: noche ? '#0d1119' : '#cfe0ea'}}
                 camera={{position: v.p, fov: v.fov, near: 0.3, far: 3000}}>
      <Camara v={v} />
      <ambientLight intensity={noche ? 0.24 : 0.55} />
      <hemisphereLight args={[noche ? '#2e3c56' : '#dfeaf2', '#6b6152', noche ? 0.5 : 0.75]} />
      <directionalLight position={noche ? [-160, 180, -60] : [180, 340, -140]}
                        intensity={noche ? 0.25 : 2.1} castShadow
                        shadow-mapSize-width={2048} shadow-mapSize-height={2048}
                        shadow-camera-left={-420} shadow-camera-right={420}
                        shadow-camera-top={420} shadow-camera-bottom={-420}
                        shadow-camera-far={900} />
      {noche && <pointLight position={[259, 7.5, 150]} color="#ff4a2a" intensity={95} distance={34} decay={1.9} />}
      {noche && <pointLight position={[250, 4.4, 114]} color="#ff4fae" intensity={62} distance={26} decay={2.0} />}
      {noche && <pointLight position={[256, 2.5, 152]} color="#ffb35c" intensity={110} distance={30} decay={1.8} />}
      <BARRIO />
    </ThreeCanvas>
  );
};
