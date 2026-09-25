// Maqueta 3D del Taller Gallardo, sacada de la planta (02-planta-taller.png). Medidas en metros.
// Version Ecuador: las nueve zonas nuevas, el nivel +0,40 con sus dos rampas y las
// turbinas de extraccion en la cubierta. El piso interior sigue en y=0 y lo que baja
// es la vereda, para no mover ni un objeto de los que ya estaban colocados.
// Ejes: x = oeste(0) -> este(24); z = avenida(0) -> pasaje(30); y = altura.
import React, {useLayoutEffect} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';

type V3 = [number, number, number];

// caja por esquinas: x0..x1, y0..y1, z0..z1
const Caja: React.FC<{x: [number, number]; y: [number, number]; z: [number, number]; c: string; e?: string; o?: number}> = ({x, y, z, c, e, o}) => (
  <mesh position={[(x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2]} castShadow receiveShadow>
    <boxGeometry args={[Math.abs(x[1] - x[0]), Math.abs(y[1] - y[0]), Math.abs(z[1] - z[0])]} />
    <meshStandardMaterial color={c} emissive={e ?? '#000000'} emissiveIntensity={e ? 1.2 : 0} transparent={o !== undefined} opacity={o ?? 1} roughness={0.75} />
  </mesh>
);

const Rueda: React.FC<{p: V3; r?: number; ancho?: number; eje?: 'x' | 'z'}> = ({p, r = 0.32, ancho = 0.22, eje = 'z'}) => (
  <mesh position={p} rotation={eje === 'z' ? [Math.PI / 2, 0, 0] : [0, 0, Math.PI / 2]} castShadow>
    <cylinderGeometry args={[r, r, ancho, 20]} />
    <meshStandardMaterial color="#1a1a1a" roughness={0.9} />
  </mesh>
);

// carro a lo largo de x, apoyado a la altura y0
const Carro: React.FC<{x0: number; z: number; y0?: number; c: string}> = ({x0, z, y0 = 0, c}) => (
  <group>
    <Caja x={[x0, x0 + 4.5]} y={[y0 + 0.3, y0 + 1.05]} z={[z - 0.9, z + 0.9]} c={c} />
    <Caja x={[x0 + 1.1, x0 + 3.5]} y={[y0 + 1.05, y0 + 1.55]} z={[z - 0.8, z + 0.8]} c="#2c3440" o={0.85} />
    {[x0 + 0.85, x0 + 3.65].map((xx) => [z - 0.82, z + 0.82].map((zz) => <Rueda key={`${xx}${zz}`} p={[xx, y0 + 0.32, zz]} />))}
  </group>
);

// carro con el eje largo en z, para la bahia 0 de recepcion
const CarroZ: React.FC<{x: number; z0: number; c: string}> = ({x, z0, c}) => (
  <group>
    <Caja x={[x - 0.9, x + 0.9]} y={[0.3, 1.05]} z={[z0, z0 + 4.5]} c={c} />
    <Caja x={[x - 0.8, x + 0.8]} y={[1.05, 1.55]} z={[z0 + 1.1, z0 + 3.5]} c="#2c3440" o={0.85} />
    {[z0 + 0.85, z0 + 3.65].map((zz) => [x - 0.82, x + 0.82].map((xx) => <Rueda key={`${xx}${zz}`} p={[xx, 0.32, zz]} eje="x" />))}
  </group>
);

// rampa 1:10 que salva los 0,40 m entre la vereda y el piso interior
const Rampa: React.FC<{x: [number, number]; z: [number, number]; eje: 'x' | 'z'}> = ({x, z, eje}) => {
  const lx = x[1] - x[0], lz = z[1] - z[0];
  const largo = eje === 'z' ? lz : lx;
  const ang = Math.atan(0.4 / largo);
  return (
    <mesh position={[(x[0] + x[1]) / 2, -0.2, (z[0] + z[1]) / 2]} rotation={eje === 'z' ? [-ang, 0, 0] : [0, 0, ang]} receiveShadow>
      <boxGeometry args={[eje === 'z' ? lx : Math.hypot(lx, 0.4), 0.08, eje === 'z' ? Math.hypot(lz, 0.4) : lz]} />
      <meshStandardMaterial color="#6b645c" roughness={0.9} />
    </mesh>
  );
};

const Lampara: React.FC<{x: number; z: number}> = ({x, z}) => (
  <group>
    <Caja x={[x - 0.01, x + 0.01]} y={[3.35, 5.5]} z={[z - 0.01, z + 0.01]} c="#222" />
    <mesh position={[x, 3.2, z]}>
      <cylinderGeometry args={[0.14, 0.36, 0.3, 24, 1, true]} />
      <meshStandardMaterial color="#b8923a" metalness={0.7} roughness={0.35} side={2} />
    </mesh>
    <mesh position={[x, 3.08, z]}>
      <sphereGeometry args={[0.07, 16, 16]} />
      <meshStandardMaterial color="#ffd08a" emissive="#ffb35c" emissiveIntensity={3} />
    </mesh>
    <pointLight position={[x, 3.0, z]} color="#ffb35c" intensity={14} distance={9} decay={1.6} castShadow />
  </group>
);

const TALLER = ({puertaAbierta, sinTecho, bahia5Vacia}: {puertaAbierta: boolean; sinTecho: boolean; bahia5Vacia: boolean}) => {
  const CREMA = '#e6ddc6', ONIX = '#1c1b1a', ORO = '#b8923a', ROJO = '#b3261e';
  const H = 7.25;
  const muros: [number, number, number, number][] = [
    // x0, x1, z0, z1 (muro completo)
    [3, 9, -0.25, 0], [14, 24, -0.25, 0], [24, 24.25, -0.25, 30.25], [0, 24, 30, 30.25],
    [-0.25, 0, 3, 16], [-0.25, 0, 20.5, 30.25],
  ];
  const desliz = puertaAbierta ? -4.6 : 0;
  const llantas: JSX.Element[] = [];
  for (let fila = 0; fila < 4; fila++) {
    for (let i = 0; i < 14; i++) {
      llantas.push(<Rueda key={`${fila}-${i}`} p={[17.25 + i * 0.49 + desliz, 0.55 + fila * 1.2, 24.5]} r={0.36} ancho={0.24} eje="z" />);
    }
  }
  return (
    <group>
      {/* piso de resina y lineas amarillas */}
      <Caja x={[0, 24]} y={[-0.05, 0]} z={[0, 30]} c="#8e9195" />
      {/* la vereda y la calle quedan 0,40 m por debajo del piso interior */}
      <Caja x={[-6, 30]} y={[-0.45, -0.4]} z={[-14, 0]} c="#3b3b3d" />
      <Caja x={[-8, 0]} y={[-0.45, -0.4]} z={[0, 32]} c="#3b3b3d" />
      <Caja x={[0, 24]} y={[-0.4, 0]} z={[-0.3, 0]} c="#2f2c29" />
      <Caja x={[-0.3, 0]} y={[-0.4, 0]} z={[0, 30]} c="#2f2c29" />
      {/* zona 4: canaleta perimetral con rejilla, y la trampa de grasas */}
      {[[7.7, 0.6, 7.7, 20.8], [14.8, 0.6, 14.8, 20.8], [0.6, 20.8, 22.6, 20.8]].map(([ax, az, bx, bz], k) => (
        <Caja key={k} x={[ax - 0.09, bx + 0.09]} y={[-0.03, 0.005]} z={[az - 0.09, bz + 0.09]} c="#6d6760" />
      ))}
      <Caja x={[5.5, 7.0]} y={[-0.04, 0.005]} z={[19.3, 20.3]} c="#8d857a" />
      {/* rampas 1:10 de 4,00 m en los dos portones */}
      <Rampa x={[9, 14]} z={[0, 4]} eje="z" />
      <Rampa x={[0, 4]} z={[16, 20.5]} eje="x" />
      {[1, 5, 9, 13.5, 17, 20.5].map((zz) => <Caja key={zz} x={[15, 22.5]} y={[0, 0.01]} z={[zz - 0.05, zz + 0.05]} c="#e0b422" />)}
      <Caja x={[14.95, 15.05]} y={[0, 0.01]} z={[1, 20.5]} c="#e0b422" />
      <Caja x={[7.45, 7.55]} y={[0, 0.01]} z={[0, 15.8]} c="#e0b422" />
      {/* zona 1: bahia 0 de recepcion, pintada contra el borde oeste del pasillo */}
      <Caja x={[7.6, 9.5]} y={[0, 0.012]} z={[5.5, 10]} c="#2aa198" />
      <Caja x={[7.72, 9.38]} y={[0, 0.02]} z={[5.62, 9.88]} c="#e9e3d3" />
      <CarroZ x={8.55} z0={5.75} c="#c9a227" />

      {/* muros: crema arriba, onix hasta 2,40 y filete dorado */}
      {muros.map(([x0, x1, z0, z1], k) => (
        <group key={k}>
          <Caja x={[x0, x1]} y={[0, H]} z={[z0, z1]} c={CREMA} />
          <Caja x={[x0 - 0.02, x1 + 0.02]} y={[0, 2.4]} z={[z0 - 0.02, z1 + 0.02]} c={ONIX} />
          <Caja x={[x0 - 0.03, x1 + 0.03]} y={[2.4, 2.45]} z={[z0 - 0.03, z1 + 0.03]} c={ORO} />
        </group>
      ))}
      {/* dinteles sobre los portones */}
      <Caja x={[9, 14]} y={[4.5, H]} z={[-0.25, 0]} c={CREMA} />
      <Caja x={[-0.25, 0]} y={[4.5, H]} z={[16, 20.5]} c={CREMA} />
      {/* ochavo de la esquina */}
      <mesh position={[1.5, H / 2, 1.5]} rotation={[0, Math.PI / 4, 0]}>
        <boxGeometry args={[4.24, H, 0.25]} />
        <meshStandardMaterial color={CREMA} />
      </mesh>

      {/* losa del segundo piso sobre la franja oeste, y techo */}
      {/* la losa del segundo piso tambien se quita en la vista cenital, si no tapa la franja oeste */}
      {!sinTecho && <Caja x={[0, 7.5]} y={[5.5, 5.75]} z={[0, 21]} c="#cfcac0" />}
      {!sinTecho && <Caja x={[0, 24]} y={[H, H + 0.2]} z={[0, 30]} c="#4a4a4a" />}
      {!sinTecho && [4, 11, 18, 25].map((zz) => <Caja key={zz} x={[9, 22]} y={[H - 0.02, H]} z={[zz, zz + 1.2]} c="#ffffff" e="#f4f6ff" />)}
      {!sinTecho && ([[9, 6], [12, 14], [18.5, 6], [21.5, 14]] as [number, number][]).map(([xx, zz]) => (
        <group key={`${xx}-${zz}`}>
          <Caja x={[xx - 0.12, xx + 0.12]} y={[H + 0.2, H + 0.45]} z={[zz - 0.12, zz + 0.12]} c="#7d858c" />
          <mesh position={[xx, H + 0.7, zz]} castShadow>
            <cylinderGeometry args={[0.45, 0.45, 0.5, 16]} />
            <meshStandardMaterial color="#b9c0c6" metalness={0.5} roughness={0.45} />
          </mesh>
        </group>
      ))}
      {[3, 7, 11, 15, 19].map((zz) => <Caja key={zz} x={[15.5, 22]} y={[5.2, 5.25]} z={[zz - 0.06, zz + 0.06]} c="#ffffff" e="#ffffff" />)}

      {/* recepcion, sala, escritorio de Renzo */}
      <Caja x={[0.9, 3.9]} y={[0, 1.05]} z={[6.0, 6.6]} c="#8a5a34" />
      <Caja x={[1.3, 1.8]} y={[1.05, 1.35]} z={[6.05, 6.5]} c="#6b6b6b" />
      <Caja x={[4.5, 5.9]} y={[0, 0.76]} z={[7.8, 8.5]} c="#5d3b22" />
      {[1.2, 2.0, 2.8, 3.6].map((xx) => <Caja key={xx} x={[xx, xx + 0.5]} y={[0, 0.9]} z={[9.6, 10.1]} c="#3a3a3a" />)}

      {/* banco principal de Gallin con sus dos lamparas y la pared de herramientas */}
      <Caja x={[1.8, 5.8]} y={[0.86, 0.92]} z={[13.5, 14.5]} c="#9aa1a8" />
      {[[1.9, 13.6], [5.6, 13.6], [1.9, 14.3], [5.6, 14.3]].map(([xx, zz]) => <Caja key={`${xx}${zz}`} x={[xx, xx + 0.08]} y={[0, 0.86]} z={[zz, zz + 0.08]} c="#555" />)}
      <Lampara x={2.8} z={14} />
      <Lampara x={4.8} z={14} />
      <Caja x={[0.02, 0.12]} y={[0.8, 3.2]} z={[10.3, 15.8]} c="#111111" />
      {Array.from({length: 18}).map((_, i) => <Caja key={i} x={[0.12, 0.16]} y={[1.3 + (i % 3) * 0.6, 1.7 + (i % 3) * 0.6]} z={[10.6 + Math.floor(i / 3) * 0.85, 10.75 + Math.floor(i / 3) * 0.85]} c={ORO} />)}

      {/* bahias: dos elevadores de 2 columnas, uno de 4 postes, dos en piso */}
      {[[1, 5], [5, 9]].map(([z0, z1], k) => (
        <group key={k}>
          {[(z0 + z1) / 2 - 1.62, (z0 + z1) / 2 + 1.27].map((zz) => <Caja key={zz} x={[18.4, 18.75]} y={[0, 2.9]} z={[zz, zz + 0.35]} c={ROJO} />)}
          <Carro x0={16.4} z={(z0 + z1) / 2} y0={k === 0 ? 1.8 : 0.1} c={k === 0 ? '#1f3a5f' : '#e8e8e6'} />
        </group>
      ))}
      {[[15.5, 9.2], [21.9, 9.2], [15.5, 13.0], [21.9, 13.0]].map(([xx, zz]) => <Caja key={`${xx}${zz}`} x={[xx, xx + 0.3]} y={[0, 2.2]} z={[zz, zz + 0.3]} c={ROJO} />)}
      <Caja x={[15.6, 22.1]} y={[1.1, 1.25]} z={[9.8, 10.4]} c="#6d6d6d" />
      <Caja x={[15.6, 22.1]} y={[1.1, 1.25]} z={[12.1, 12.7]} c="#6d6d6d" />
      <Carro x0={16.5} z={11.25} y0={1.25} c="#8e1c1c" />
      <Carro x0={16.4} z={15.25} c="#6f7378" />
      {!bahia5Vacia && <Carro x0={16.4} z={18.75} c="#141414" />}
      {[3, 11.2, 15.2, 18.7].map((zz) => <Caja key={zz} x={[22.9, 23.6]} y={[0, 1.0]} z={[zz - 0.4, zz + 0.4]} c={ROJO} />)}
      <Caja x={[22.6, 23.7]} y={[0, 1.15]} z={[5.6, 7.6]} c="#2f6f6a" />
      <Caja x={[22.62, 23.0]} y={[1.15, 1.45]} z={[5.9, 6.2]} c="#b3261e" />
      <Caja x={[23.2, 23.6]} y={[1.15, 1.45]} z={[5.9, 6.2]} c="#2e5aa8" />

      {/* franja sur: rincon fino, cafe, motos, almacen, compresor, llantas */}
      <Caja x={[1.5, 4.8]} y={[0, 0.9]} z={[21.3, 22.0]} c="#4a4a4a" />
      <Caja x={[3.5, 3.9]} y={[0.9, 1.5]} z={[21.4, 21.7]} c="#dddddd" e="#fff3d6" />
      <Caja x={[1.5, 4.2]} y={[0, 0.95]} z={[24.3, 24.9]} c="#6b4a2e" />
      <Caja x={[1.7, 2.2]} y={[0.95, 1.4]} z={[24.4, 24.8]} c="#c9c9c9" />
      <Caja x={[0.1, 0.13]} y={[1.4, 1.9]} z={[25.2, 25.6]} c="#f4f1ea" />
      {[[6.2, 25.0], [8.9, 25.0], [6.2, 28.2], [8.9, 28.2]].map(([xx, zz]) => (
        <group key={`${xx}${zz}`}>
          <Caja x={[xx + 0.3, xx + 1.9]} y={[0.35, 0.8]} z={[zz + 0.2, zz + 0.5]} c="#2b2b2b" />
          <Rueda p={[xx + 0.3, 0.3, zz + 0.35]} r={0.3} ancho={0.1} />
          <Rueda p={[xx + 1.9, 0.3, zz + 0.35]} r={0.3} ancho={0.1} />
        </group>
      ))}
      {/* zona 3: residuos peligrosos, y el lavado de piezas separado de las motos */}
      <Caja x={[5.45, 5.55]} y={[0, 3.0]} z={[21, 30]} c={CREMA} />
      <Caja x={[7.95, 8.05]} y={[0, 1.3]} z={[21, 24]} c={CREMA} />
      <Caja x={[5.5, 11.5]} y={[0, 1.3]} z={[23.95, 24.05]} c={CREMA} />
      <Caja x={[5.55, 8.0]} y={[0, 0.06]} z={[21.05, 24]} c="#2aa198" />
      {[5.95, 6.65, 7.35].map((xx) => (
        <mesh key={xx} position={[xx, 0.45, 22.9]} castShadow>
          <cylinderGeometry args={[0.28, 0.28, 0.9, 18]} />
          <meshStandardMaterial color="#c0713a" roughness={0.8} />
        </mesh>
      ))}
      <Caja x={[8.6, 10.9]} y={[0, 0.9]} z={[21.6, 23.4]} c="#7d8a7d" />
      <Caja x={[11.5, 17]} y={[0, 3.0]} z={[20.95, 21.05]} c={CREMA} />
      <Caja x={[11.5, 17]} y={[0, 2.4]} z={[20.9, 21.0]} c={ONIX} />
      <Caja x={[11.5, 11.6]} y={[0, 3.0]} z={[21, 30]} c={CREMA} />
      <Caja x={[11.5, 17]} y={[0, 3.0]} z={[23.95, 24.05]} c={CREMA} />
      <Caja x={[11.5, 17]} y={[0, 3.0]} z={[24.95, 25.05]} c={CREMA} />
      <Caja x={[16.9, 17.0]} y={[0, 3.0]} z={[21, 24]} c={CREMA} />
      <mesh position={[13.0, 1.0, 27.5]} rotation={[0, 0, Math.PI / 2]}><cylinderGeometry args={[0.35, 0.35, 1.6, 20]} /><meshStandardMaterial color={ROJO} /></mesh>
      {/* desmontadora y balanceadora contra las paredes: el centro de la zona de
          llantas queda libre porque por ahi pasa la camara hacia la puerta roja */}
      <Caja x={[17.3, 18.1]} y={[0, 1.0]} z={[22.0, 22.8]} c="#2e5aa8" />
      <Caja x={[22.7, 23.5]} y={[0, 1.1]} z={[22.0, 22.8]} c="#2e5aa8" />
      <Rueda p={[17.7, 1.15, 22.4]} r={0.33} ancho={0.22} eje="x" />

      {/* estanteria de llantas sobre rieles */}
      <Caja x={[11.5, 24]} y={[0, 0.03]} z={[24.1, 24.2]} c="#777" />
      <Caja x={[11.5, 24]} y={[0, 0.03]} z={[24.8, 24.9]} c="#777" />
      <group>
        {[0, 7].map((dx) => [24.02, 24.98].map((zz) => <Caja key={`${dx}${zz}`} x={[17 + dx + desliz - 0.04, 17 + dx + desliz + 0.04]} y={[0, 5]} z={[zz - 0.04, zz + 0.04]} c="#8a8a8a" />))}
        {[0.12, 1.32, 2.52, 3.72, 4.92].map((yy) => <Caja key={yy} x={[17 + desliz, 24 + desliz]} y={[yy, yy + 0.06]} z={[24.0, 25.0]} c="#8a8a8a" />)}
        {llantas}
      </group>

      {/* muro del Cuarto con la puerta roja y la corona */}
      <Caja x={[17, 19.9]} y={[0, 5.5]} z={[25.1, 25.3]} c={CREMA} />
      <Caja x={[21.1, 24]} y={[0, 5.5]} z={[25.1, 25.3]} c={CREMA} />
      <Caja x={[19.9, 21.1]} y={[2.4, 5.5]} z={[25.1, 25.3]} c={CREMA} />
      <Caja x={[17, 19.9]} y={[0, 2.4]} z={[25.07, 25.1]} c={ONIX} />
      <Caja x={[21.1, 24]} y={[0, 2.4]} z={[25.07, 25.1]} c={ONIX} />
      <Caja x={[19.9, 21.1]} y={[0, 2.4]} z={[25.0, 25.12]} c="#9b1f1f" />
      {/* la corona va DELANTE de la cara de la puerta (z=25,0), no dentro: asi se ve */}
      <Caja x={[20.32, 20.68]} y={[1.62, 1.88]} z={[24.94, 25.0]} c={ORO} e="#6b4e12" />
      <Lampara x={20.5} z={23.4} />
      <Caja x={[16.9, 17.0]} y={[0, 5.5]} z={[25.3, 30]} c={CREMA} />

      {/* adentro del Cuarto de Afinamiento */}
      <Caja x={[17, 24]} y={[3.0, 3.1]} z={[25.3, 30]} c="#3b2417" />
      <Caja x={[17.02, 17.06]} y={[0, 3]} z={[25.3, 30]} c="#4a2e1f" />
      <Caja x={[23.94, 23.98]} y={[0, 3]} z={[25.3, 30]} c="#4a2e1f" />
      <Caja x={[17, 24]} y={[0, 3]} z={[29.94, 29.98]} c="#4a2e1f" />
      <Caja x={[18.3, 19.3]} y={[0, 0.9]} z={[27.3, 28.3]} c="#5b1d1d" />
      <Caja x={[21.7, 22.7]} y={[0, 0.9]} z={[27.3, 28.3]} c="#5b1d1d" />
      <Caja x={[19.7, 21.3]} y={[0, 0.5]} z={[27.4, 28.2]} c="#2e1b10" />
      <Caja x={[20.2, 20.6]} y={[0.5, 0.53]} z={[27.6, 27.9]} c="#0d0d0d" />
      <Caja x={[19.5, 21.5]} y={[0.3, 1.9]} z={[29.3, 29.9]} c="#f6e7c4" e="#8a6a2a" o={0.55} />
      <Caja x={[22.4, 23.2]} y={[0, 0.9]} z={[29.2, 29.9]} c="#b8923a" />
      <pointLight position={[20.5, 2.6, 27.8]} color="#ffae5c" intensity={9} distance={6} decay={1.6} />
      <Caja x={[21.8, 22.8]} y={[0, 2.1]} z={[29.98, 30.02]} c="#8c8c8c" />

      {/* escalera a la casa de Gallin */}
      {Array.from({length: 18}).map((_, i) => <Caja key={i} x={[0, 1.3]} y={[0, 0.32 * (i + 1)]} z={[27 - (i + 1) * 0.33, 27 - i * 0.33]} c="#7a746a" />)}
    </group>
  );
};

const VISTAS: Record<string, {p: V3; t: V3; fov: number; abierta?: boolean; sinTecho?: boolean; vacia?: boolean}> = {
  maqueta: {p: [-9, 26, -11], t: [12, 0, 15], fov: 45, sinTecho: true},
  entrada: {p: [11.5, 1.7, 0.6], t: [11.5, 1.8, 30], fov: 62},
  banco: {p: [12.5, 1.65, 13.8], t: [3.2, 1.3, 14.0], fov: 55},
  bahias: {p: [9.0, 2.0, 16.5], t: [18.7, 1.4, 6.5], fov: 60},
  estanteria: {p: [20.5, 1.7, 18.3], t: [20.5, 2.0, 25], fov: 62, vacia: true},
  puerta: {p: [20.5, 1.7, 18.8], t: [20.5, 1.5, 25], fov: 58, abierta: true, vacia: true},
  cuarto: {p: [17.6, 1.55, 25.9], t: [22.2, 0.9, 29.3], fov: 70},
};
export const ORDEN = ['maqueta', 'entrada', 'banco', 'bahias', 'estanteria', 'puerta', 'cuarto'];

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

export const Taller3D: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const v = VISTAS[ORDEN[Math.min(frame, ORDEN.length - 1)]];
  return (
    <ThreeCanvas width={width} height={height} shadows style={{background: '#20242a'}} camera={{position: v.p, fov: v.fov, near: 0.05, far: 200}}>
      <Camara v={v} />
      <ambientLight intensity={0.55} />
      <hemisphereLight args={['#f4f1ea', '#5b5b5b', 0.6]} />
      <directionalLight position={[-12, 28, -10]} intensity={1.4} castShadow shadow-mapSize-width={2048} shadow-mapSize-height={2048}
        shadow-camera-left={-30} shadow-camera-right={30} shadow-camera-top={30} shadow-camera-bottom={-30} />
      <TALLER puertaAbierta={!!v.abierta} sinTecho={!!v.sinTecho} bahia5Vacia={!!v.vacia} />
    </ThreeCanvas>
  );
};
