// PUERTO CANDELA ENTERA, en 3D y con material.
//
// Sustituye a la maqueta de bloques. La geometria del barrio El Cruce sale tal cual
// del plano urbano (01-plano-urbano-el-cruce.png); lo que se agrega aqui es todo lo
// que el plano no dice y las camaras si necesitan: el territorio alrededor, los
// otros barrios, el paisajismo y el color de la ciudad.
//
// POR QUE: varios episodios abren con la ciudad y desde angulos distintos. Sin un
// modelo unico, cada toma la inventa y a los tres videos el espectador nota que el
// pueblo cambio. Y una maqueta de cajas grises no sirve de referencia para generar
// video: el generador necesita ver material, luz y escala.
//
// SEMILLA FIJA (realismo.tsx). El mismo lote saca siempre la misma casa, del mismo
// color, con el mismo techo. Cambiar la semilla cambia el pueblo entero.
//
// EJES: x crece al este (0 a 600 en el barrio), z crece al sur (0 a 299), y es la
// altura. Es el mismo norte-arriba del plano.
import React, {useLayoutEffect, useMemo} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {
  Ambiente, Hora, Estacion, Caja, Suelo, Casa, LocalConPortal, Nave, TechoDosAguas,
  Arbol, Especie, Poste, Cable, Carro, Moto, rnd, elige, texMuro, texZinc, texPisoRep,
  texBloque, CASAS, FUERTES, Frente,
} from './realismo';

type V3 = [number, number, number];

// ================================================================ el plano
const COLS: [number, number][] = [[12, 112], [124, 224], [244, 344], [356, 456], [468, 588]];
const FILAS: Record<string, [number, number]> = {
  '1': [12, 56], '2': [68, 112], '3': [152, 187], '4': [187, 231], '5': [243, 287],
};
const CALLES_V: [number, number][] = [[0, 12], [112, 124], [224, 244], [344, 356], [456, 468], [588, 600]];
const CALLES_H: [number, number][] = [[0, 12], [56, 68], [231, 243], [287, 299]];
const AV = {z0: 112, z1: 152, p0: 130, p1: 134};        // Av. El Cruce, 40 m con parterre
const OLMEDO: [number, number] = [224, 244];             // la colectora: la calle de los mecanicos
const PASAJE = {x0: 244, x1: 344, z0: 182, z1: 187};     // Pasaje La Esperanza

// ================================================================ manzanas
/** manzana residencial: dos hileras de lotes pegados que miran a calles opuestas */
const ManzanaCasas: React.FC<{x: [number, number]; z: [number, number]; k: number; noche?: boolean}> =
({x, z, k, noche}) => {
  const hijos = useMemo(() => {
    const n = Math.max(2, Math.round((x[1] - x[0]) / 8.5));
    const paso = (x[1] - x[0]) / n;
    const medio = (z[0] + z[1]) / 2;
    const out: JSX.Element[] = [];
    for (let i = 0; i < n; i++) {
      const a = x[0] + i * paso, b = x[0] + (i + 1) * paso;
      // el fondo del lote queda de patio: la casa no ocupa toda la profundidad
      const fN = medio - (1.5 + rnd(k + i * 7) * 3.5);
      const fS = medio + (1.5 + rnd(k + i * 11) * 3.5);
      if (rnd(k + i * 3) > 0.06) out.push(<Casa key={`n${i}`} x={[a, b]} z={[z[0], fN]} k={k + i * 13} frente="n" noche={noche} />);
      if (rnd(k + i * 5) > 0.06) out.push(<Casa key={`s${i}`} x={[a, b]} z={[fS, z[1]]} k={k + 500 + i * 13} frente="s" noche={noche} />);
    }
    return out;
  }, [x, z, k, noche]);
  return <group>{hijos}</group>;
};

/** franja comercial con portal: es lo que hay a los dos lados de la avenida */
const Franja: React.FC<{x: [number, number]; z: [number, number]; frente: Frente; k: number; noche?: boolean}> =
({x, z, frente, k, noche}) => {
  const hijos = useMemo(() => {
    const n = Math.max(2, Math.round((x[1] - x[0]) / 11));
    const paso = (x[1] - x[0]) / n;
    return Array.from({length: n}).map((_, i) => (
      <LocalConPortal key={i} x={[x[0] + i * paso, x[0] + (i + 1) * paso]} z={z}
        k={k + i * 17} frente={frente} noche={noche} />
    ));
  }, [x, z, frente, k, noche]);
  return <group>{hijos}</group>;
};

// ================================================================ los dos anclas
// REGLA DE COLOR DE LA CIUDAD: en todo el pueblo no hay otro edificio negro onix ni
// otro verde botella. El taller y el bar son los unicos. Por eso se reconocen desde
// cualquier angulo y a cualquier hora, y por eso los dos neones se leen de lejos.
const ONIX = '#1d1b19', CREMA = '#efe6d2', VERDE_BAR = '#1f4d3a';

const Taller: React.FC<{noche?: boolean}> = ({noche}) => {
  const zin = texZinc('nuevo', 5);
  return (
    <group>
      {/* nave 24 x 30, piso interior +0,40, altura libre 5,50 */}
      <Caja x={[244, 268]} y={[0, 7.25]} z={[152, 182]} c={ONIX} rug={0.7} />
      <Caja x={[244, 268]} y={[0, 0.42]} z={[151.9, 182.1]} c="#2f2c29" rug={0.9} />
      {/* casa de Gallin encima, 7,50 x 21, en crema */}
      <Caja x={[244, 251.5]} y={[5.75, 9.75]} z={[152, 173]} mapa={texMuro(CREMA, 61, 2)} rug={0.9} />
      <TechoDosAguas x={[243.8, 268.2]} z={[151.8, 182.2]} y={7.25} eje="x" pend={0.14} alero={0.6} tono="nuevo" k={9} sinHastial />
      <TechoDosAguas x={[243.6, 251.7]} z={[151.6, 173.2]} y={9.75} eje="z" pend={0.18} alero={0.5} tono="nuevo" k={13} mapaHastial={texMuro(CREMA, 61, 2)} />
      {/* letrero y gallo sobre la avenida */}
      <Caja x={[252, 266]} y={[4.9, 6.2]} z={[151.85, 152]} c="#121110" rug={0.5} />
      <Caja x={[252.4, 265.6]} y={[5.25, 5.75]} z={[151.78, 151.86]} c="#d4ad52"
            e={noche ? '#ff7a1e' : '#c49a3a'} ei={noche ? 4.2 : 0.5} rug={0.4} met={0.3} />
      <Caja x={[258, 260]} y={[6.2, 8.4]} z={[151.78, 151.95]} c="#c62828"
            e={noche ? '#ff2a1a' : '#8a1d1d'} ei={noche ? 5.0 : 0.3} rug={0.5} />
      {/* portones: el de entrada a la avenida, el de salida a Olmedo */}
      <Caja x={[254, 262]} y={[0.42, 5.2]} z={[151.94, 152.02]} c="#3a3c40" rug={0.55} met={0.5} />
      <Caja x={[243.94, 244.02]} y={[0.42, 5.2]} z={[158, 166]} c="#3a3c40" rug={0.55} met={0.5} />
      {/* cuatro turbinas eolicas en la cubierta */}
      {[[250, 158], [250, 176], [262, 158], [262, 176]].map(([tx, tz], i) => (
        <mesh key={i} position={[tx, 8.55, tz]} castShadow>
          <cylinderGeometry args={[0.46, 0.5, 0.62, 12]} />
          <meshStandardMaterial map={zin.mapa} roughness={0.35} metalness={0.75} />
        </mesh>
      ))}
      {/* el toldo de espera sobre el retiro de la Calle Olmedo */}
      <Caja x={[238.6, 244]} y={[3.1, 3.26]} z={[155, 167]} c="#c9c0ae" rug={0.85} />
      {[156, 166].map((tz) => (
        <Caja key={tz} x={[238.7, 239.0]} y={[0, 3.1]} z={[tz - 0.15, tz + 0.15]} c="#a9a293" rug={0.9} />
      ))}
      {/* puerta gris del Cuarto, al pasaje */}
      <Caja x={[262, 264.4]} y={[0.42, 2.6]} z={[181.94, 182.02]} c="#6f7479" rug={0.7} met={0.25} />
    </group>
  );
};

const Bar: React.FC<{noche?: boolean}> = ({noche}) => (
  <group>
    <Caja x={[244, 256]} y={[0, 7.5]} z={[92, 112]} mapa={texMuro(VERDE_BAR, 71, 2)} rug={0.82} />
    <TechoDosAguas x={[243.8, 256.2]} z={[91.8, 112.2]} y={7.5} eje="x" pend={0.16} alero={0.55}
      tono="viejo" k={17} mapaHastial={texMuro(VERDE_BAR, 71, 2)} />
    {[3.6, 6.9].map((yy) => (
      <Caja key={yy} x={[243.7, 256.3]} y={[yy, yy + 0.12]} z={[91.7, 112.3]} c={CREMA} rug={0.8} />
    ))}
    {/* el neon de la gata, 4,80 x 0,55 a 3,00 m */}
    <Caja x={[247.6, 252.4]} y={[3.0, 3.55]} z={[111.88, 112.02]} c="#ff6ab5"
          e={noche ? '#ff2f9c' : '#8a2f5e'} ei={noche ? 5.2 : 0.2} rug={0.4} />
    {/* balcon de Micaela, vuela 1,20 m (VALIDAR con el cabildo) */}
    <Caja x={[247, 253]} y={[4.75, 4.95]} z={[112, 113.2]} c="#6b4a2e" rug={0.9} />
    <Caja x={[247, 253]} y={[4.95, 5.9]} z={[113.1, 113.2]} c="#6b4a2e" rug={0.9} />
    {/* tanque elevado y tendedero en la azotea */}
    <mesh position={[245.6, 9.1, 94.2]} castShadow>
      <cylinderGeometry args={[0.85, 0.85, 1.5, 12]} />
      <meshStandardMaterial color="#2f6fa8" roughness={0.6} />
    </mesh>
  </group>
);

// ================================================================ Parque del Reloj
// PROPUESTA DE DISENO. Mz. G, 100 x 44 m. Es la plaza del pueblo y sale en camara,
// asi que no puede ser una alfombra verde con palitos. Se disena como se disena una
// plaza de pueblo costeno: banda perimetral dura, cuatro cuadrantes de cesped, dos
// diagonales que cruzan en una rotonda, y los usos repartidos para que no se estorben.
//   oeste   cancha de ecuavoley 18 x 9, que es el deporte que de verdad se juega
//   centro  rotonda de 16 m con la torre del reloj que atrasa
//   este    juegos infantiles sobre arena y una concha acustica para las fiestas
// Sombra: mangos grandes en los cuadrantes, almendros en el perimetro, guayacanes
// en las cuatro entradas (florecen amarillo en verano) y dos palmas junto al reloj.
const PQ = {x0: 124, x1: 224, z0: 68, z1: 112};
const ParqueDelReloj: React.FC<{noche?: boolean; est: Estacion}> = ({noche, est}) => {
  const cx = (PQ.x0 + PQ.x1) / 2, cz = (PQ.z0 + PQ.z1) / 2;
  const diag = useMemo(() => {
    // las dos diagonales, como cuatro paralelepipedos girados desde cada esquina
    const out: JSX.Element[] = [];
    const esquinas: [number, number][] = [[PQ.x0, PQ.z0], [PQ.x1, PQ.z0], [PQ.x0, PQ.z1], [PQ.x1, PQ.z1]];
    esquinas.forEach(([ex, ez], i) => {
      const dx = cx - ex, dz = cz - ez;
      const L = Math.hypot(dx, dz);
      out.push(
        <mesh key={i} position={[(ex + cx) / 2, 0.06, (ez + cz) / 2]}
              rotation={[-Math.PI / 2, 0, Math.atan2(dz, dx)]} receiveShadow>
          <planeGeometry args={[L, 3.2]} />
          <meshStandardMaterial map={texPisoRep('adoquin', L / 3.2, 1)} roughness={0.9} />
        </mesh>,
      );
    });
    return out;
  }, [cx, cz]);
  return (
    <group>
      <Suelo x={[PQ.x0, PQ.x1]} z={[PQ.z0, PQ.z1]} y={0.04} tipo="cesped" />
      {/* banda perimetral dura de 3 m */}
      {([[PQ.x0, PQ.x1, PQ.z0, PQ.z0 + 3], [PQ.x0, PQ.x1, PQ.z1 - 3, PQ.z1],
         [PQ.x0, PQ.x0 + 3, PQ.z0, PQ.z1], [PQ.x1 - 3, PQ.x1, PQ.z0, PQ.z1]] as number[][]).map((b, i) => (
        <Suelo key={i} x={[b[0], b[1]]} z={[b[2], b[3]]} y={0.06} tipo="adoquin" />
      ))}
      {diag}
      {/* rotonda y torre del reloj */}
      <mesh position={[cx, 0.07, cz]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <circleGeometry args={[8, 40]} />
        <meshStandardMaterial map={texPisoRep('adoquin', 5, 5)} roughness={0.9} />
      </mesh>
      <Caja x={[cx - 1.7, cx + 1.7]} y={[0.07, 1.0]} z={[cz - 1.7, cz + 1.7]} c="#d9d2c0" rug={0.9} />
      <Caja x={[cx - 1.25, cx + 1.25]} y={[1.0, 9.2]} z={[cz - 1.25, cz + 1.25]} mapa={texMuro('#e8e0cc', 91, 2)} rug={0.9} />
      <Caja x={[cx - 1.5, cx + 1.5]} y={[9.2, 9.5]} z={[cz - 1.5, cz + 1.5]} c="#b9b0a0" rug={0.9} />
      <TechoDosAguas x={[cx - 1.5, cx + 1.5]} z={[cz - 1.5, cz + 1.5]} y={9.5} pend={0.85} alero={0.25} tono="nuevo" k={3} sinHastial />
      {/* las dos esferas del reloj, norte y sur */}
      {[[cz - 1.3, 0], [cz + 1.3, 0]].map(([ez], i) => (
        <mesh key={i} position={[cx, 7.6, ez]} rotation={[Math.PI / 2, 0, 0]}>
          <circleGeometry args={[0.85, 26]} />
          <meshStandardMaterial color="#f6f2e4" roughness={0.5}
            emissive={noche ? '#ffe9b8' : '#000000'} emissiveIntensity={noche ? 2.4 : 0}
            side={THREE.DoubleSide} />
        </mesh>
      ))}
      {/* cancha de ecuavoley al oeste, con su red */}
      <Suelo x={[136, 154]} z={[80, 100]} y={0.05} tipo="losa" />
      {[136, 154].map((px) => (
        <Caja key={px} x={[px - 0.08, px + 0.08]} y={[0, 2.5]} z={[89.9, 90.1]} c="#9a958a" rug={0.9} />
      ))}
      <Caja x={[136, 154]} y={[1.9, 2.4]} z={[89.96, 90.04]} c="#d8d4c8" rug={0.95} />
      {/* juegos infantiles al este, sobre arena */}
      <Suelo x={[192, 212]} z={[74, 88]} y={0.05} tipo="tierra" />
      <Caja x={[196, 202]} y={[0, 0.35]} z={[78, 84]} c="#c9a227" rug={0.9} />
      <Caja x={[201, 207]} y={[0.35, 2.4]} z={[80, 82]} c="#b4332b" rug={0.85} />
      <TechoDosAguas x={[200.4, 207.6]} z={[79.4, 82.6]} y={2.4} pend={0.5} alero={0.3} tono="nuevo" k={7} sinHastial />
      {/* concha acustica: la tarima de las fiestas patronales */}
      <Caja x={[196, 212]} y={[0, 0.9]} z={[96, 106]} c="#cfc8b8" rug={0.92} />
      <Caja x={[196, 212]} y={[0.9, 5.2]} z={[105.4, 106]} mapa={texMuro('#8fa9c4', 97, 2)} rug={0.9} />
      <TechoDosAguas x={[195.4, 212.6]} z={[95.4, 106.6]} y={5.2} pend={0.3} alero={0.6} tono="nuevo" k={11} sinHastial />
      {/* bancas y faroles del parque */}
      {Array.from({length: 14}).map((_, i) => {
        const t = i / 14;
        const bx = PQ.x0 + 6 + t * (PQ.x1 - PQ.x0 - 12);
        const bz = i % 2 ? PQ.z0 + 4.4 : PQ.z1 - 4.4;
        return <Caja key={i} x={[bx, bx + 1.8]} y={[0.06, 0.52]} z={[bz - 0.25, bz + 0.25]} c="#b9b2a2" rug={0.9} />;
      })}
      {[[134, 74], [214, 74], [134, 106], [214, 106], [cx - 12, cz], [cx + 12, cz]].map(([fx, fz], i) => (
        <group key={i} position={[fx, 0, fz]}>
          <Caja x={[-0.09, 0.09]} y={[0, 4.2]} z={[-0.09, 0.09]} c="#3f4247" rug={0.7} />
          <mesh position={[0, 4.4, 0]} castShadow>
            <sphereGeometry args={[0.28, 12, 10]} />
            <meshStandardMaterial color="#e8e4d8" roughness={0.4}
              emissive={noche ? '#ffdca8' : '#000000'} emissiveIntensity={noche ? 3.0 : 0} />
          </mesh>
        </group>
      ))}
      {/* arbolado del parque */}
      {([[132, 76, 'mango'], [132, 104, 'mango'], [162, 74, 'mango'], [162, 106, 'mango'],
         [186, 92, 'mango'], [148, 106, 'almendro'], [176, 72, 'almendro'], [216, 92, 'almendro'],
         [126.5, 90, 'guayacan'], [221.5, 90, 'guayacan'], [174, 69.5, 'guayacan'], [174, 110.5, 'guayacan'],
         [170, 99, 'palma'], [178, 99, 'palma']] as [number, number, Especie][])
        .map(([tx, tz, e], i) => <Arbol key={i} p={[tx, tz]} esp={e} k={i * 131 + 7} est={est} />)}
    </group>
  );
};

// ================================================================ equipamiento
// Institucional en blanco y azul del Estado, deliberadamente distinto del color de
// las casas: desde el aire se lee al instante donde esta la escuela y donde el UPC.
const Equipamiento: React.FC<{noche?: boolean; est: Estacion}> = ({noche, est}) => (
  <group>
    {/* Mz. B - Escuela Fiscal Vicente Rocafuerte: dos bloques y patio civico */}
    <Nave x={[128, 220]} z={[16, 26]} alto={3.4} col="#f0ece2" k={21} eje="x" tono="nuevo" />
    <Nave x={[128, 190]} z={[30, 39]} alto={3.4} col="#f0ece2" k={23} eje="x" tono="nuevo" />
    <Caja x={[128, 220]} y={[1.6, 2.1]} z={[15.8, 16.05]} c="#2f5aa0" rug={0.85} />
    <Suelo x={[130, 218]} z={[42, 54]} y={0.03} tipo="losa" />
    <Caja x={[124, 124.3]} y={[0, 2.4]} z={[12, 56]} c="#cdc6b6" rug={0.9} />
    {/* Mz. C - Mercado Municipal: una nave larga de zinc, 84 puestos */}
    <Nave x={[248, 340]} z={[16, 52]} alto={4.6} col="#e7dcc6" k={27} eje="x" tono="nuevo" noche={noche} />
    {[256, 272, 290, 308, 322].map((mx, i) => (
      <group key={i}>
        <Caja x={[mx, mx + 5]} y={[0, 2.3]} z={[53.4, 55.6]} c={elige(FUERTES, i * 7)} rug={0.9} />
        <Caja x={[mx - 0.4, mx + 5.4]} y={[2.3, 2.45]} z={[52.6, 56.4]} c="#d8d4c8" rug={0.85} />
      </group>
    ))}
    {/* Mz. F - Iglesia de la Virgen del Carmen */}
    <Nave x={[80, 112]} z={[68, 92]} alto={7.0} col="#f4f1e8" k={31} eje="z" tono="nuevo" />
    <Caja x={[93, 99]} y={[0, 14.5]} z={[70, 76]} mapa={texMuro('#f4f1e8', 33, 2)} rug={0.9} />
    <TechoDosAguas x={[92.6, 99.4]} z={[69.6, 76.4]} y={14.5} pend={0.9} alero={0.3} tono="nuevo" k={35} sinHastial />
    <Caja x={[95.6, 96.4]} y={[17.6, 19.4]} z={[72.6, 73.4]} c="#d4ad52"
          e={noche ? '#a8801f' : '#a8801f'} ei={noche ? 1.2 : 0.3} rug={0.4} met={0.5} />
    <Suelo x={[68, 112]} z={[94, 110]} y={0.03} tipo="adoquin" />
    {/* Mz. I - UPC y Centro de Salud del MSP */}
    <Nave x={[360, 392]} z={[90, 104]} alto={3.6} col="#e9eef3" k={41} eje="x" tono="nuevo" />
    <Caja x={[360, 392]} y={[2.6, 3.1]} z={[89.8, 90.05]} c="#2f5aa0" rug={0.85} />
    <Carro p={[376, 86]} rot={0} k={303} />
    <Nave x={[398, 440]} z={[90, 106]} alto={3.8} col="#eef3f2" k={43} eje="x" tono="nuevo" />
    <Caja x={[398, 440]} y={[2.8, 3.3]} z={[89.8, 90.05]} c="#3f8f86" rug={0.85} />
    {/* Mz. J - Hostal El Descanso y Hotel Panamericano */}
    <Casa x={[494, 528]} z={[88, 106]} k={51} frente="n" pisos={2} col="#e6d7b8" noche={noche} />
    <Casa x={[540, 586]} z={[84, 106]} k={53} frente="n" pisos={3} col="#ddd2c0" noche={noche} />
    {/* Hospital basico, dos manzanas al sureste */}
    <Nave x={[476, 580]} z={[196, 240]} alto={7.2} col="#f2f2f0" k={57} eje="x" tono="nuevo" />
    <Nave x={[476, 540]} z={[248, 278]} alto={4.2} col="#f2f2f0" k={59} eje="x" tono="nuevo" />
    <Caja x={[524, 532]} y={[4.2, 5.0]} z={[195.6, 196.1]} c="#b3261e" e="#8f1c16" ei={noche ? 1.8 : 0.4} rug={0.6} />
    <Caja x={[527, 529]} y={[3.0, 6.2]} z={[195.6, 196.1]} c="#b3261e" e="#8f1c16" ei={noche ? 1.8 : 0.4} rug={0.6} />
    <Suelo x={[478, 578]} z={[186, 194]} y={0.03} tipo="losa" />
    {/* Mz. V - losa deportiva del barrio */}
    <Suelo x={[248, 296]} z={[247, 283]} y={0.04} tipo="losa" />
    {[248, 296].map((px) => (
      <group key={px} position={[px === 248 ? 252 : 292, 0, 265]}>
        <Caja x={[-0.08, 0.08]} y={[0, 3.05]} z={[-0.08, 0.08]} c="#8a8f94" rug={0.8} />
        <Caja x={[-0.6, 0.6]} y={[2.6, 3.05]} z={[-0.06, 0.06]} c="#d8d4c8" rug={0.9} />
      </group>
    ))}
    {/* Gasolinera El Ultimo, donde la avenida se vuelve carretera */}
    <Suelo x={[540, 588]} z={[152, 184]} y={0.03} tipo="losa" />
    <Caja x={[548, 580]} y={[4.6, 5.3]} z={[158, 176]} c="#f0e08a"
          e={noche ? '#ffe98a' : '#d8c07a'} ei={noche ? 3.4 : 0.25} rug={0.4} />
    {[[552, 162], [552, 172], [576, 162], [576, 172]].map(([px, pz], i) => (
      <Caja key={i} x={[px - 0.22, px + 0.22]} y={[0, 4.6]} z={[pz - 0.22, pz + 0.22]} c="#cfcabd" rug={0.85} />
    ))}
    {[[560, 166], [568, 166]].map(([px, pz], i) => (
      <Caja key={`s${i}`} x={[px - 0.4, px + 0.4]} y={[0, 1.5]} z={[pz - 0.3, pz + 0.3]} c="#b4332b" rug={0.7} />
    ))}
    <Nave x={[556, 578]} z={[178, 184]} alto={3.2} col="#eae4d6" k={61} eje="x" tono="nuevo" />
    {/* los otros talleres de la Calle Olmedo: vulcanizadora y enderezada */}
    <Nave x={[272, 300]} z={[152, 172]} alto={4.8} col="#d6cbb4" k={63} eje="x" tono="oxido" />
    <Nave x={[304, 340]} z={[152, 176]} alto={5.2} col="#c9d0cb" k={67} eje="x" tono="viejo" />
    <Arbol p={[120, 60]} esp="mango" k={71} est={est} />
  </group>
);

// ================================================================ vialidad
// PROPUESTA DE SECCION POR VIA. En un pueblo de 12.000 habitantes no esta todo
// asfaltado, y eso no es un descuido: es lo que hay, y ademas da dos climas de
// imagen distintos (polvo en verano, barro en invierno).
//   Av. El Cruce      40 m  asfalto          parterre 4 m con ceibos  luminaria doble
//   Calle Olmedo      20 m  adoquin          almendros en vereda      luminaria simple
//   Calles locales    12 m  lastre compacto  mango en las esquinas    farol en poste
//   Pasaje Esperanza   5 m  adoquin          sin arbolado             un solo farol
const X0 = -900, X1 = 1500, Z0 = -700, Z1 = 900;
const Vialidad: React.FC = () => (
  <group>
    {/* Av. El Cruce, que al este se vuelve la carretera */}
    <Suelo x={[X0, X1]} z={[AV.z0 + 4, AV.p0]} y={0.01} tipo="asfalto" />
    <Suelo x={[X0, X1]} z={[AV.p1, AV.z1 - 4]} y={0.01} tipo="asfalto" />
    <Suelo x={[X0, X1]} z={[AV.p0, AV.p1]} y={0.16} tipo="cesped" />
    {([[AV.z0, AV.z0 + 4], [AV.z1 - 4, AV.z1]] as [number, number][]).map((v, i) => (
      <Suelo key={i} x={[X0, X1]} z={v} y={0.15} tipo="vereda" />
    ))}
    {/* Calle Olmedo, la colectora adoquinada */}
    <Suelo x={[OLMEDO[0] + 4, OLMEDO[1] - 4]} z={[-260, 320]} y={0.01} tipo="adoquin" />
    {([[OLMEDO[0], OLMEDO[0] + 4], [OLMEDO[1] - 4, OLMEDO[1]]] as [number, number][]).map((v, i) => (
      <Suelo key={i} x={v} z={[-260, 320]} y={0.15} tipo="vereda" />
    ))}
    {/* calles locales: lastre, con su vereda angosta */}
    {CALLES_V.filter((c) => c[0] !== 224).map((c, i) => (
      <group key={`v${i}`}>
        <Suelo x={[c[0] + 2.5, c[1] - 2.5]} z={[-40, 320]} y={0.01} tipo="lastre" />
        <Suelo x={[c[0], c[0] + 2.5]} z={[-40, 320]} y={0.13} tipo="vereda" />
        <Suelo x={[c[1] - 2.5, c[1]]} z={[-40, 320]} y={0.13} tipo="vereda" />
      </group>
    ))}
    {CALLES_H.map((c, i) => (
      <group key={`h${i}`}>
        <Suelo x={[-40, 640]} z={[c[0] + 2.5, c[1] - 2.5]} y={0.012} tipo="lastre" />
        <Suelo x={[-40, 640]} z={[c[0], c[0] + 2.5]} y={0.13} tipo="vereda" />
        <Suelo x={[-40, 640]} z={[c[1] - 2.5, c[1]]} y={0.13} tipo="vereda" />
      </group>
    ))}
    {/* Pasaje La Esperanza */}
    <Suelo x={[PASAJE.x0, PASAJE.x1]} z={[PASAJE.z0, PASAJE.z1]} y={0.02} tipo="adoquin" />
    {/* veredas del frente de manzana sobre la avenida */}
    {COLS.map((c, i) => (
      <group key={`f${i}`}>
        <Suelo x={c} z={[104, 112]} y={0.14} tipo="vereda" />
        <Suelo x={c} z={[152, 160]} y={0.14} tipo="vereda" />
      </group>
    ))}
  </group>
);

// ================================================================ paisajismo
// PROPUESTA. Tres especies de calle, una por jerarquia de via. Se planta asi porque
// es como se planta de verdad, y ademas hace que cada calle se reconozca desde el
// aire sin leer un rotulo.
//   ceibo     parterre de la Av. El Cruce   el arbol grande del Guayas
//   almendro  Calle Olmedo                  copa baja y ancha, sombra a los mecanicos
//   mango     calles locales y patios       el arbol de patio de la costa
// DOS VACIOS A PROPOSITO: no se planta en el cruce de Olmedo con la avenida ni
// delante del toldo del taller. En los dos sitios el arbol tapaba la toma.
const Paisajismo: React.FC<{est: Estacion}> = ({est}) => {
  const arboles = useMemo(() => {
    const out: JSX.Element[] = [];
    for (let x = -60; x < 900; x += 22) {
      if (x > 216 && x < 252) continue;
      out.push(<Arbol key={`c${x}`} p={[x, 132]} esp="ceibo" k={x * 3 + 1} est={est} regado />);
    }
    for (let z = -40; z < 320; z += 17) {
      if (z > 108 && z < 156) continue;
      if (!(z > 150 && z < 192)) out.push(<Arbol key={`a${z}`} p={[228, z]} esp="almendro" k={z * 5} est={est} regado />);
      out.push(<Arbol key={`b${z}`} p={[240, z + 8]} esp="almendro" k={z * 7 + 3} est={est} regado />);
    }
    for (const c of CALLES_V) {
      if (c[0] === 224) continue;
      for (const z of [58, 234, 290]) {
        out.push(<Arbol key={`m${c[0]}-${z}`} p={[c[0] + 6, z + 6]} esp="mango" k={c[0] * 11 + z} est={est} />);
      }
    }
    // patios: mangos y platanos sueltos dentro de las manzanas
    for (let i = 0; i < 46; i++) {
      const cx = 16 + rnd(i * 17) * 560, cz = 16 + rnd(i * 23) * 268;
      if (cz > 108 && cz < 156) continue;
      if (cx > 240 && cx < 350 && cz > 148 && cz < 190) continue;   // el taller no tiene patio
      out.push(<Arbol key={`p${i}`} p={[cx, cz]} esp={rnd(i) > 0.72 ? 'palma' : 'mango'} k={i * 97 + 5} est={est} />);
    }
    return out;
  }, [est]);
  return <group>{arboles}</group>;
};

/** postes, cables y alumbrado. Los cables cruzando la calle los pide la biblia. */
const Redes: React.FC<{noche?: boolean}> = ({noche}) => {
  const piezas = useMemo(() => {
    const out: JSX.Element[] = [];
    for (let i = 0; i < 18; i++) {                     // avenida: poste alto con farol
      const x = -40 + i * 46;
      if (x > 214 && x < 254) continue;
      out.push(<Poste key={`pa${i}`} p={[x, 153.6]} alto={9.2} farol noche={noche} trafo={i % 4 === 1} />);
      if (i > 0) out.push(<Cable key={`ca${i}`} a={[x - 46, 8.6, 153.6]} b={[x, 8.6, 153.6]} comba={1.3} />);
      if (i % 3 === 0) out.push(<Cable key={`cx${i}`} a={[x, 8.2, 153.6]} b={[x + 6, 7.4, 110.4]} comba={2.2} />);
    }
    for (let i = 0; i < 14; i++) {                     // Olmedo: poste de 7,50
      const z = -30 + i * 34;
      if (z > 106 && z < 158) continue;
      out.push(<Poste key={`po${i}`} p={[222.6, z]} alto={7.6} farol noche={noche} />);
      if (i > 0) out.push(<Cable key={`co${i}`} a={[222.6, 7.1, z - 34]} b={[222.6, 7.1, z]} comba={1.1} />);
      if (i % 2 === 0) out.push(<Cable key={`cz${i}`} a={[222.6, 6.8, z]} b={[245.4, 6.4, z + 5]} comba={1.6} />);
    }
    for (const c of CALLES_V) {                        // calles locales: poste de luz simple
      if (c[0] === 224) continue;
      for (const z of [40, 96, 210, 268]) {
        out.push(<Poste key={`pl${c[0]}${z}`} p={[c[0] + 1.6, z]} alto={7.2} farol={z % 100 === 40} noche={noche} />);
      }
      out.push(<Cable key={`cl${c[0]}`} a={[c[0] + 1.6, 6.8, 40]} b={[c[0] + 1.6, 6.8, 268]} comba={3.2} />);
    }
    return out;
  }, [noche]);
  return <group>{piezas}</group>;
};

// ================================================================ territorio
// PROPUESTA DE PAISAJE. La biblia fija llanura aluvial del Guayas, suelo blando,
// salitre a 15 km del mar, lluvias de enero a abril y seco el resto. De ahi sale
// todo esto, y lo que no estaba escrito va marcado:
//   DATO (biblia)      llanura, sin montana; el pueblo esta a 15 km del mar
//   PROPUESTA          el Estero Candela al sureste. Explica el nombre del pueblo,
//                      explica la Calle El Puerto que ya estaba en el plano, y
//                      explica de que vive: camaroneras y arroz
//   PROPUESTA          camaroneras en damero a los dos lados del estero
//   PROPUESTA          arrozales al norte y al oeste; bosque seco en lo demas
//   HIPOTESIS          la Loma de la Cruz al noroeste, 42 m. En la llanura hay lomas
//                      aisladas, pero la biblia no la nombra: queda por validar.
//                      Sirve para abrir capitulos con el pueblo visto desde arriba.
// NO ES DESIERTO Y NO ES SELVA: es bosque seco tropical. En verano todo ocre y el
// ceibo sin hoja; en invierno todo verde en seis semanas.
const Territorio: React.FC<{est: Estacion; noche?: boolean}> = ({est, noche}) => {
  const seco = est === 'seca';
  const lomaGeo = useMemo(() => {
    const g = new THREE.ConeGeometry(300, 96, 18, 6);
    const p = g.attributes.position as THREE.BufferAttribute;
    for (let i = 0; i < p.count; i++) {
      const x = p.getX(i), y = p.getY(i), z = p.getZ(i);
      const n = 1 + 0.26 * Math.sin(x * 0.013 + 1.7) * Math.cos(z * 0.011 - 0.6)
                  + 0.12 * Math.sin(z * 0.03);
      p.setXYZ(i, x * n, y * (0.92 + 0.2 * Math.sin(x * 0.02)), z * n);
    }
    g.computeVertexNormals();
    return g;
  }, []);
  const LX = -470, LZ = -420;
  return (
    <group>
      {/* la llanura */}
      <Suelo x={[-4200, 5200]} z={[-4200, 4200]} y={-0.12} tipo="seco"
             col={seco ? '#ffffff' : '#b6c9a0'} />
      {/* manchas de monte cerrado: la llanura no es una alfombra pareja */}
      {Array.from({length: 22}).map((_, i) => {
        const mx = -3000 + rnd(i * 13) * 6600, mz = -2600 + rnd(i * 19) * 5200;
        if (mx > -700 && mx < 1300 && mz > -600 && mz < 800) return null;
        const an = 240 + rnd(i * 7) * 700, fo = 200 + rnd(i * 11) * 620;
        return <Suelo key={`mo${i}`} x={[mx, mx + an]} z={[mz, mz + fo]} y={-0.09} tipo="monte" col={seco ? '#ffffff' : '#c2d8ae'} />;
      })}
      {/* arrozales al norte y al oeste: el damero que dice llanura del Guayas */}
      <Suelo x={[-1600, 2600]} z={[-2600, -520]} y={-0.08} tipo="arroz"
             col={seco ? '#e2ddbe' : '#ffffff'} />
      <Suelo x={[-2800, -980]} z={[-420, 760]} y={-0.08} tipo="arroz"
             col={seco ? '#e2ddbe' : '#ffffff'} />
      {/* camaroneras: las piscinas de camaron a los dos lados del estero */}
      <Suelo x={[-900, 420]} z={[440, 640]} y={-0.06} tipo="camaronera" />
      <Suelo x={[760, 2600]} z={[380, 780]} y={-0.06} tipo="camaronera" />
      <Suelo x={[-1400, 700]} z={[860, 1560]} y={-0.06} tipo="camaronera" />
      {/* el Estero Candela */}
      {/* el estero serpentea: cada tramo va girado. Recto parecia un canal de riego. */}
      {([[-1900, 340, 636, 806, 0.055], [180, 1240, 672, 858, -0.085], [1140, 2460, 690, 902, 0.07],
         [2320, 4100, 742, 1010, -0.05]] as number[][]).map((e, i) => (
        <Suelo key={i} x={[e[0], e[1]]} z={[e[2], e[3]]} y={-0.02} tipo="camaronera"
               col="#93a8ab" rug={0.10} met={0.55} rot={e[4]} />
      ))}
      {/* manglar en las dos orillas: franja oscura, mas alta que el agua */}
      {([[-1900, 340, 596, 646, 0.055], [-1900, 340, 798, 852, 0.055],
         [180, 1240, 630, 682, -0.085], [180, 1240, 848, 902, -0.085],
         [1140, 2460, 650, 700, 0.07], [1140, 2460, 892, 946, 0.07]] as number[][]).map((m, i) => (
        <Suelo key={`mg${i}`} x={[m[0], m[1]]} z={[m[2], m[3]]} y={1.6} tipo="monte"
               col="#54734c" rot={m[4]} />
      ))}
      {/* muelle al final de la Calle El Puerto */}
      <Suelo x={[560, 640]} z={[300, 640]} y={0.02} tipo="lastre" />
      <Caja x={[580, 618]} y={[0, 1.4]} z={[640, 690]} c="#8a7b62" rug={0.95} />
      {[588, 600, 612].map((bx, i) => (
        <Caja key={i} x={[bx - 2.2, bx + 2.2]} y={[0.4, 1.5]} z={[694 + i * 5, 706 + i * 5]}
              c={elige(['#d8d4cc', '#2f6fa8', '#c9a227'], i * 7)} rug={0.5} />
      ))}
      <Nave x={[530, 572]} z={[600, 630]} alto={5.2} col="#cfc8b4" k={301} eje="x" tono="oxido" />
      {/* la Loma de la Cruz (HIPOTESIS), con el asentamiento en la ladera que mira al pueblo */}
      <mesh geometry={lomaGeo} position={[LX, 40, LZ]} castShadow receiveShadow>
        <meshStandardMaterial map={texPisoRep('monte', 12, 12)} color={seco ? '#b5ad7e' : '#9fb87c'} roughness={1} />
      </mesh>
      {Array.from({length: 46}).map((_, i) => {
        const ang = 0.15 + rnd(i * 3) * 2.4;                 // solo la ladera sureste
        const rad = 100 + rnd(i * 5) * 178;
        const hx = LX + Math.cos(ang) * rad, hz = LZ + Math.sin(ang) * rad;
        const suelo = Math.max(0, 88 * (1 - rad / 300) - 2);
        const h = 2.5 + rnd(i * 7) * 2.2;
        return (
          <group key={`lm${i}`}>
            <Caja x={[hx, hx + 6.4]} y={[suelo - 2.2, suelo + h]} z={[hz, hz + 6.4]}
                  mapa={texMuro(elige(CASAS, i * 11), i, 1)} rug={0.94} />
            <TechoDosAguas x={[hx, hx + 6.4]} z={[hz, hz + 6.4]} y={suelo + h}
              pend={0.2} alero={0.4} tono={elige(['viejo', 'oxido', 'nuevo'], i * 13)} k={i * 17} sinHastial />
          </group>
        );
      })}
      {/* bosque seco disperso: ceibos sueltos, que en verano estan pelados */}
      {Array.from({length: 120}).map((_, i) => {
        const bx = -2000 + rnd(i * 19) * 4400;
        const bz = -1100 + rnd(i * 29) * 2000;
        if (bx > -120 && bx < 720 && bz > -300 && bz < 340) return null;
        return <Arbol key={`bs${i}`} p={[bx, bz]} esp={rnd(i) > 0.55 ? 'ceibo' : 'muyuyo'} k={i * 37} est={est} />;
      })}
      {/* la carretera, que entra y sale del pueblo por la avenida */}
      <Suelo x={[1500, 4600]} z={[120, 144]} y={0.01} tipo="asfalto" />
      <Suelo x={[-3600, -900]} z={[120, 144]} y={0.01} tipo="asfalto" />
      {noche && <pointLight position={[598, 3, 690]} color="#ffd9a0" intensity={120} distance={60} decay={1.8} />}
    </group>
  );
};

// ================================================================ otros barrios
/** casa simplificada, para lo que la camara ve de lejos: un volumen y su techo.
    Varia alto, fondo, color y direccion del caballete: con todas iguales el barrio
    se lee desde el aire como una fila de contenedores, que es lo que pasaba antes. */
const CasaLejos: React.FC<{x: [number, number]; z: [number, number]; k: number}> = ({x, z, k}) => {
  const a = rnd(k), b = rnd(k + 811), c = rnd(k + 1733);
  const col = a < 0.26 ? elige(FUERTES, k + 3) : elige(CASAS, k + 5);
  const pisos = a < 0.58 ? 1 : a < 0.9 ? 2 : 3;
  const h = pisos * 2.95 + 0.4;
  const fondo = (z[1] - z[0]) * (0.62 + b * 0.38);            // el resto queda de patio
  const zz: [number, number] = c > 0.5 ? [z[0], z[0] + fondo] : [z[1] - fondo, z[1]];
  const crudo = pisos >= 2 && c > 0.80;                        // sin enlucir, esperando plata
  const eje: 'x' | 'z' = (x[1] - x[0]) > (zz[1] - zz[0]) ? 'x' : 'z';
  return (
    <group>
      <Caja x={x} y={[0, h]} z={zz} mapa={crudo ? texBloque(k) : texMuro(col, k, 1)} rug={0.94} />
      {crudo && b > 0.45 ? (
        <Caja x={[x[0] - 0.15, x[1] + 0.15]} y={[h, h + 0.5]} z={[zz[0] - 0.15, zz[1] + 0.15]}
              mapa={texBloque(k + 3)} rug={0.95} />
      ) : (
        <TechoDosAguas x={x} z={zz} y={h} eje={eje} pend={0.18 + b * 0.1} alero={0.4 + a * 0.3}
          tono={elige(['viejo', 'oxido', 'nuevo', 'viejo', 'oxido'], k + 7)} k={k} sinHastial />
      )}
    </group>
  );
};

const BarrioSimple: React.FC<{x: [number, number]; z: [number, number]; k: number; paso?: number}> =
({x, z, k, paso = 9}) => {
  // La misma traza que El Cruce: manzana de 100 x 44 con dos hileras de lotes que
  // miran a calles opuestas, y calle de 12 m entre manzanas. Sin esto el barrio
  // sale como filas de galpones y desde el aire se nota que es inventado.
  const MZ_X = 100, MZ_Z = 44, CALLE = 12;
  const piezas = useMemo(() => {
    const out: JSX.Element[] = [];
    const nx = Math.max(1, Math.floor((x[1] - x[0] + CALLE) / (MZ_X + CALLE)));
    const nz = Math.max(1, Math.floor((z[1] - z[0] + CALLE) / (MZ_Z + CALLE)));
    for (let f = 0; f < nz; f++) {
      const zf = z[0] + f * (MZ_Z + CALLE);
      out.push(<Suelo key={`ch${f}`} x={[x[0] - CALLE, x[1] + CALLE]} z={[zf - CALLE + 2.5, zf - 2.5]}
                      y={0.008} tipo="lastre" />);
      for (let c = 0; c < nx; c++) {
        const xf = x[0] + c * (MZ_X + CALLE);
        if (f === 0) {
          out.push(<Suelo key={`cv${c}`} x={[xf - CALLE + 2.5, xf - 2.5]} z={[z[0] - CALLE, z[1]]}
                          y={0.008} tipo="lastre" />);
        }
        const n = Math.floor(MZ_X / paso);
        for (let i = 0; i < n; i++) {
          const a = xf + i * paso;
          const kk = k + f * 331 + c * 97 + i * 7;
          if (rnd(kk) < 0.10) continue;                          // lotes vacios, siempre hay
          const fN = 18 + rnd(kk + 3) * 5;
          const fS = 26 - rnd(kk + 5) * 5;
          out.push(<CasaLejos key={`a${f}${c}${i}`} x={[a, a + paso - 0.3]} z={[zf, zf + fN]} k={kk} />);
          if (rnd(kk + 11) > 0.14) {
            out.push(<CasaLejos key={`b${f}${c}${i}`} x={[a, a + paso - 0.3]} z={[zf + fS, zf + MZ_Z]} k={kk + 4001} />);
          }
        }
      }
    }
    // un arbol de patio cada pocas manzanas, y mango en las esquinas de calle
    for (let i = 0; i < Math.round((x[1] - x[0]) * (z[1] - z[0]) / 2600); i++) {
      const tx = x[0] + rnd(k + i * 41) * (x[1] - x[0]);
      const tz = z[0] + rnd(k + i * 59) * (z[1] - z[0]);
      out.push(<Arbol key={`t${i}`} p={[tx, tz]} esp={rnd(k + i * 7) > 0.7 ? 'palma' : 'mango'}
                      k={k + i * 173} est="seca" />);
    }
    return out;
  }, [x, z, k, paso]);
  return <group>{piezas}</group>;
};

const OtrosBarrios: React.FC<{est: Estacion}> = ({est}) => (
  <group>
    {/* Nuevo Amanecer, al norte: mas nuevo, mas casas sin terminar, sin asfaltar */}
    <BarrioSimple x={[12, 572]} z={[-244, -32]} k={2001} />
    {/* Los Almendros, al oeste: el barrio viejo, lotes mas grandes */}
    <BarrioSimple x={[-348, -24]} z={[12, 224]} k={3001} paso={11} />
    {/* El Muelle, al sureste: pescadores, bodegas y oficinas de camaronera */}
    <BarrioSimple x={[432, 880]} z={[336, 492]} k={4001} paso={8} />
    {/* zona industrial al sur de la Calle Juan Montalvo */}
    {Array.from({length: 9}).map((_, i) => {
      const x = 20 + i * 64 + rnd(i * 7) * 12;
      const z = 322 + rnd(i * 13) * 20;
      const an = 32 + rnd(i * 17) * 20, fo = 22 + rnd(i * 23) * 14;
      return <Nave key={`zi${i}`} x={[x, x + an]} z={[z, z + fo]} alto={6.4 + rnd(i * 29) * 3}
                   col={i % 3 ? '#cfc8b8' : '#c3cbc6'} k={i * 53 + 9} eje="x"
                   tono={elige(['nuevo', 'viejo', 'oxido'], i * 3)} />;
    })}
    {Array.from({length: 22}).map((_, i) => (
      <Arbol key={`ob${i}`} p={[-360 + rnd(i * 11) * 1200, -240 + rnd(i * 17) * 740]}
             esp={rnd(i * 3) > 0.6 ? 'palma' : 'mango'} k={i * 211 + 3} est={est} />
    ))}
  </group>
);

// ================================================================ el barrio El Cruce
// 25 manzanas, 496 lotes, 2.200 habitantes. Comercio en los dos frentes de la
// avenida y vivienda detras, que es como crece de verdad un pueblo sobre una via.
const ElCruce: React.FC<{noche?: boolean; est: Estacion}> = ({noche, est}) => {
  const manzanas = useMemo(() => {
    const out: JSX.Element[] = [];
    const letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let li = 0;
    Object.entries(FILAS).forEach(([fila, [z0, z1]]) => {
      COLS.forEach(([x0, x1], c) => {
        if ((fila === '4' || fila === '5') && c === 4) return;      // ahi va el hospital
        const letra = letras[li++];
        const k = li * 1009;
        if (['B', 'C', 'F', 'G', 'I', 'J', 'V'].includes(letra)) return;   // equipamiento
        if (fila === '2') {
          // frente sur a la avenida: comercio. Fondo norte: vivienda.
          const cx0 = letra === 'H' ? 258 : x0;
          out.push(<Franja key={`${letra}f`} x={[cx0, x1]} z={[96, 112]} frente="s" k={k} noche={noche} />);
          out.push(<ManzanaCasas key={letra} x={[x0, x1]} z={[z0, 92]} k={k + 77} noche={noche} />);
        } else if (fila === '3') {
          if (letra === 'M') return;                                 // el taller y los otros talleres
          out.push(<Franja key={`${letra}f`} x={[x0, x1]} z={[152, 170]} frente="n" k={k} noche={noche} />);
          out.push(<ManzanaCasas key={letra} x={[x0, x1]} z={[174, z1]} k={k + 91} noche={noche} />);
        } else {
          out.push(<ManzanaCasas key={letra} x={[x0, x1]} z={[z0, z1]} k={k} noche={noche} />);
        }
      });
    });
    return out;
  }, [noche]);

  const trafico = useMemo(() => {
    const out: JSX.Element[] = [];
    // estacionados contra la vereda de la avenida y de Olmedo
    for (let i = 0; i < 16; i++) {
      const x = 20 + rnd(i * 13) * 540;
      if (x > 220 && x < 250) continue;
      out.push(<Carro key={`e${i}`} p={[x, rnd(i) > 0.5 ? 149.4 : 114.6]} rot={0} k={i * 31}
                      tipo={elige(['auto', 'auto', 'camioneta'], i * 7) as any} />);
    }
    for (let i = 0; i < 7; i++) {
      const z = 20 + rnd(i * 17) * 260;
      if (z > 110 && z < 154) continue;
      out.push(<Carro key={`o${i}`} p={[226.6, z]} rot={Math.PI / 2} k={i * 53 + 5}
                      tipo={i % 3 === 0 ? 'camioneta' : 'auto'} />);
    }
    // motos y tricimotos: el vehiculo real de la costa
    for (let i = 0; i < 14; i++) {
      const x = 16 + rnd(i * 19) * 560;
      if (x > 216 && x < 252) continue;
      out.push(<Moto key={`m${i}`} p={[x, rnd(i * 3) > 0.5 ? 150.6 : 113.4]} rot={rnd(i) * 0.5} k={i * 71}
                     tri={rnd(i * 5) > 0.62} />);
    }
    // la fila del mercado y las busetas de ruta
    out.push(<Carro key="b1" p={[294, 116.5]} rot={0} k={9} tipo="buseta" />);
    out.push(<Carro key="b2" p={[150, 147.5]} rot={Math.PI} k={13} tipo="buseta" />);
    // los que estan esperando en el taller, bajo el toldo
    out.push(<Carro key="t1" p={[240.5, 158]} rot={Math.PI / 2} k={101} />);
    out.push(<Carro key="t2" p={[240.5, 165]} rot={Math.PI / 2} k={103} tipo="camioneta" />);
    out.push(<Moto key="t3" p={[241, 170.5]} rot={Math.PI / 2} k={107} tri />);
    return out;
  }, []);

  return (
    <group>
      {manzanas}
      <Equipamiento noche={noche} est={est} />
      <ParqueDelReloj noche={noche} est={est} />
      <Taller noche={noche} />
      <Bar noche={noche} />
      {trafico}
    </group>
  );
};

const Ciudad: React.FC<{noche?: boolean; est: Estacion}> = ({noche, est}) => (
  <group>
    <Territorio est={est} noche={noche} />
    <Vialidad />
    <OtrosBarrios est={est} />
    <ElCruce noche={noche} est={est} />
    <Paisajismo est={est} />
    <Redes noche={noche} />
    {/* los dos neones mandan de noche: el gallo rojo y la gata rosada, enfrentados */}
    {noche && <pointLight position={[259, 7.4, 151]} color="#ff4a2a" intensity={210} distance={46} decay={1.8} />}
    {noche && <pointLight position={[250, 3.3, 113]} color="#ff4fae" intensity={150} distance={34} decay={1.9} />}
    {noche && <pointLight position={[256, 2.6, 153]} color="#ffb35c" intensity={190} distance={38} decay={1.8} />}
    {noche && <pointLight position={[174, 8.0, 90]} color="#ffdca8" intensity={140} distance={60} decay={1.7} />}
    {noche && <pointLight position={[564, 5.0, 167]} color="#ffe9b8" intensity={220} distance={52} decay={1.7} />}
  </group>
);

// ================================================================ las vistas
// Cada vista es una camara fija con su hora. Son las tomas oficiales del pueblo:
// si un capitulo abre con la ciudad, abre desde una de estas y no desde otra.
type Vista = {p: V3; t: V3; fov: number; hora: Hora; foco?: V3; radio?: number; est?: Estacion; niebla?: number};

export const VISTAS: Record<string, Vista> = {
  // 1. el territorio entero: pueblo, estero, camaroneras, arrozales y la loma
  territorio: {p: [-880, 430, 1340], t: [340, 0, 240], fov: 44, hora: 'tarde',
               foco: [300, 0, 260], radio: 1200, niebla: 6500},
  // 2. la ciudad desde el noreste, a 210 m: la que sirve para abrir temporada
  ciudad_aerea: {p: [900, 215, -380], t: [280, 0, 165], fov: 42, hora: 'tarde',
                 foco: [300, 0, 130], radio: 700, niebla: 4200},
  // 3. cenital del casco: se lee la traza, el parque y la avenida
  ciudad_cenital: {p: [300, 780, 155], t: [300, 0, 150], fov: 42, hora: 'mediodia',
                   foco: [300, 0, 150], radio: 560, niebla: 5000},
  // 4. la ciudad desde el suroeste, con el estero detras
  ciudad_sur: {p: [-40, 125, 580], t: [330, 0, 175], fov: 46, hora: 'tarde',
               foco: [300, 0, 190], radio: 520, niebla: 4600},
  // 5. la cuadra del taller
  la_cuadra: {p: [92, 96, 300], t: [286, 4, 132], fov: 40, hora: 'tarde',
              foco: [270, 0, 150], radio: 260},
  // 6. la esquina: el taller y el bar enfrentados por la avenida
  la_esquina: {p: [221, 6.0, 124], t: [266, 5.0, 142], fov: 62, hora: 'tarde',
               foco: [258, 0, 136], radio: 180},
  // 7. la avenida, teleobjetivo: comprime la calle y el taller queda al fondo
  avenida: {p: [26, 4.6, 144], t: [560, 4.4, 128], fov: 26, hora: 'mediodia',
            foco: [280, 0, 136], radio: 340},
  // 8. la Calle Olmedo, la calle de los mecanicos, desde el sur
  olmedo: {p: [234, 4.4, 276], t: [234, 3.6, 120], fov: 48, hora: 'tarde',
           foco: [234, 0, 190], radio: 200},
  // 9. el Parque del Reloj desde la esquina noroeste
  parque: {p: [102, 17, 44], t: [178, 2.5, 94], fov: 50, hora: 'tarde',
           foco: [174, 0, 90], radio: 170},
  // 10. el mercado y la fila de la avenida
  mercado: {p: [330, 4.4, 62], t: [278, 3.4, 42], fov: 58, hora: 'mediodia',
            foco: [296, 0, 44], radio: 170},
  // 11. la esquina de noche: los dos neones, que son la firma visual de la serie
  esquina_noche: {p: [219, 6.4, 122], t: [268, 5.2, 142], fov: 66, hora: 'noche',
                  foco: [258, 0, 134], radio: 190},
  // 12. el pueblo de noche desde el aire
  ciudad_noche: {p: [760, 200, -300], t: [300, 0, 160], fov: 42, hora: 'noche',
                 foco: [300, 0, 140], radio: 620, niebla: 3200},
  // 13. el estero y el muelle al atardecer: de que vive el pueblo
  estero: {p: [508, 32, 508], t: [612, 2, 678], fov: 46, hora: 'tarde',
           foco: [600, 0, 640], radio: 380, niebla: 4000},
  // 14. desde la Loma de la Cruz al amanecer, con la bruma sobre la llanura
  loma: {p: [-142, 46, -226], t: [330, 0, 165], fov: 42, hora: 'amanecer',
         foco: [250, 0, 110], radio: 620, niebla: 4400},
  // 15. entrando al pueblo por la carretera, pasando la gasolinera
  carretera: {p: [842, 4.2, 143], t: [330, 4.6, 139], fov: 32, hora: 'tarde',
              foco: [540, 0, 140], radio: 360},
  // 16. el barrio Nuevo Amanecer: el pueblo que crece sin asfalto
  nuevo_amanecer: {p: [120, 24, 10], t: [360, 3, -180], fov: 46, hora: 'mediodia',
                   foco: [300, 0, -120], radio: 320},
};
export const ORDEN_CIUDAD = Object.keys(VISTAS);

// Las mismas vistas en vertical, que es el formato real de la serie. Se reencuadra:
// una toma pensada en horizontal no sirve recortada, hay que acercar y subir.
export const VERTICALES: Record<string, Vista> = {
  v_ciudad: {p: [860, 260, -380], t: [300, 0, 150], fov: 46, hora: 'tarde', foco: [300, 0, 130], radio: 700, niebla: 4200},
  v_avenida: {p: [103, 4.4, 142], t: [520, 7, 132], fov: 40, hora: 'mediodia', foco: [300, 0, 136], radio: 320},
  v_taller: {p: [257, 2.8, 126], t: [258, 6.0, 152], fov: 62, hora: 'tarde', foco: [258, 0, 148], radio: 130},
  v_esquina: {p: [205, 5.8, 139], t: [262, 4.8, 133], fov: 58, hora: 'tarde', foco: [252, 0, 136], radio: 180},
  v_parque: {p: [187, 3.8, 126], t: [172, 7.0, 88], fov: 60, hora: 'tarde', foco: [174, 0, 96], radio: 150},
  v_esquina_noche: {p: [216, 5.0, 124], t: [266, 5.4, 144], fov: 64, hora: 'noche', foco: [258, 0, 136], radio: 175},
  v_loma: {p: [-300, 52, -180], t: [320, 0, 170], fov: 42, hora: 'amanecer', foco: [180, 0, 60], radio: 680, niebla: 3000},
  v_estero: {p: [504, 44, 496], t: [612, 2, 674], fov: 44, hora: 'tarde', foco: [600, 0, 630], radio: 380, niebla: 4000},
};
export const ORDEN_VERTICAL = Object.keys(VERTICALES);

const Camara: React.FC<{v: Vista}> = ({v}) => {
  const {camera} = useThree();
  useLayoutEffect(() => {
    camera.position.set(...v.p);
    (camera as any).fov = v.fov;
    camera.lookAt(...v.t);
    camera.updateProjectionMatrix();
  }, [camera, v]);
  return null;
};

const Escena: React.FC<{v: Vista; w: number; h: number}> = ({v, w, h}) => (
  <ThreeCanvas width={w} height={h} shadows
    camera={{position: v.p, fov: v.fov, near: 0.5, far: 12000}}>
    <Camara v={v} />
    <Ambiente hora={v.hora} foco={v.foco ?? v.t} radio={v.radio ?? 380} nieblaLejos={v.niebla} />
    <Ciudad noche={v.hora === 'noche'} est={v.est ?? 'seca'} />
  </ThreeCanvas>
);

export const Ciudad3D: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const v = VISTAS[ORDEN_CIUDAD[Math.min(frame, ORDEN_CIUDAD.length - 1)]];
  return <Escena v={v} w={width} h={height} />;
};

export const CiudadVertical: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const v = VERTICALES[ORDEN_VERTICAL[Math.min(frame, ORDEN_VERTICAL.length - 1)]];
  return <Escena v={v} w={width} h={height} />;
};
