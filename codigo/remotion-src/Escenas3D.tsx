// Maquetas 3D del Bar La Gata y del Pasaje La Esperanza, sacadas de 04-planta-bar y 06-plano-pasaje.
// Bar: x = oeste(0)->este(12), z = fondo(0)->fachada(20); la avenida sigue hacia z>20 y el taller esta en z=60.
// Pasaje: x = Jr. Los Mecanicos(0)->Calle San Martin(100), z = espalda del taller(0)->casas(5).
import React, {useLayoutEffect, useMemo} from 'react';
import * as THREE from 'three';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';

type V3 = [number, number, number];
const Caja: React.FC<{x: [number, number]; y: [number, number]; z: [number, number]; c: string; e?: string; ei?: number; o?: number}> = ({x, y, z, c, e, ei, o}) => (
  <mesh position={[(x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2]} castShadow receiveShadow>
    <boxGeometry args={[Math.abs(x[1] - x[0]), Math.abs(y[1] - y[0]), Math.abs(z[1] - z[0])]} />
    <meshStandardMaterial color={c} emissive={e ?? '#000'} emissiveIntensity={e ? (ei ?? 1.5) : 0} transparent={o !== undefined} opacity={o ?? 1} roughness={0.8} />
  </mesh>
);
const Cil: React.FC<{p: V3; r: number; h: number; c: string; e?: string}> = ({p, r, h, c, e}) => (
  <mesh position={p} castShadow>
    <cylinderGeometry args={[r, r, h, 24]} />
    <meshStandardMaterial color={c} emissive={e ?? '#000'} emissiveIntensity={e ? 1.5 : 0} />
  </mesh>
);

// silueta del gallo del letrero (misma que la fachada del taller), 2,0 x 2,2 m
const SIL = [[0.40, 0.00], [0.44, 0.00], [0.45, 0.18], [0.52, 0.18], [0.53, 0.00], [0.57, 0.00], [0.58, 0.22], [0.70, 0.30],
  [0.85, 0.35], [0.95, 0.50], [1.00, 0.75], [0.92, 0.95], [0.85, 0.80], [0.80, 0.98], [0.72, 0.78], [0.66, 0.70], [0.55, 0.62],
  [0.45, 0.72], [0.40, 0.86], [0.42, 0.92], [0.38, 0.97], [0.34, 0.93], [0.30, 0.99], [0.27, 0.93], [0.23, 0.96], [0.22, 0.89],
  [0.18, 0.86], [0.10, 0.83], [0.18, 0.80], [0.20, 0.76], [0.23, 0.70], [0.27, 0.74], [0.28, 0.62], [0.25, 0.48], [0.30, 0.34], [0.40, 0.24]];
const GalloNeon: React.FC<{p: V3; rotY?: number}> = ({p, rotY = 0}) => {
  const geo = useMemo(() => {
    const s = new THREE.Shape();
    SIL.forEach(([a, b], i) => (i ? s.lineTo(a * 2 - 1, b * 2.2) : s.moveTo(a * 2 - 1, b * 2.2)));
    return new THREE.ShapeGeometry(s);
  }, []);
  return (
    <group position={p} rotation={[0, rotY, 0]}>
      <mesh geometry={geo}><meshStandardMaterial color="#ff2a2a" emissive="#ff1a1a" emissiveIntensity={2.5} side={2} /></mesh>
      <pointLight position={[0, 1, 0.8]} color="#ff3030" intensity={10} distance={14} decay={1.5} />
    </group>
  );
};

// ---------------------------------------------------------------- BAR LA GATA
const Bar: React.FC = () => {
  const VERDE = '#1f4d3a', CREMA = '#efe6d2', ROJO = '#7a2a22', MADERA = '#4a2e1f';
  const H = 3.6;
  const losetas: JSX.Element[] = [];
  for (let i = 0; i < 24; i++) for (let j = 0; j < 24; j++)
    losetas.push(<Caja key={`${i}-${j}`} x={[i * 0.5, i * 0.5 + 0.5]} y={[-0.02, 0]} z={[8 + j * 0.5, 8.5 + j * 0.5]} c={(i + j) % 2 ? '#e8e2d4' : '#2a2a2a'} />);
  return (
    <group>
      {losetas}
      {/* muros interiores: zocalo de madera y estuco rojo */}
      {[[[-0.2, 0], [8, 18]], [[12, 12.2], [8, 20]], [[0, 12], [7.8, 8]]].map(([xx, zz], k) => (
        <group key={k}>
          <Caja x={xx as [number, number]} y={[0, H]} z={zz as [number, number]} c={ROJO} />
          <Caja x={[(xx as number[])[0] - 0.02, (xx as number[])[1] + 0.02]} y={[0, 1.1]} z={[(zz as number[])[0] - 0.02, (zz as number[])[1] + 0.02]} c={MADERA} />
        </group>
      ))}
      <Caja x={[0, 12]} y={[H, H + 0.15]} z={[7.8, 20.2]} c="#2a1a14" />
      {/* fachada con puerta, vitrina y ochavo */}
      {[[2, 3.5], [4.7, 6.5], [11, 12]].map(([a, b]) => <Caja key={a} x={[a, b]} y={[0, H]} z={[20, 20.25]} c={VERDE} />)}
      <Caja x={[3.5, 4.7]} y={[2.6, H]} z={[20, 20.25]} c={VERDE} />
      <Caja x={[6.5, 11]} y={[0, 0.9]} z={[20, 20.25]} c={VERDE} />
      <Caja x={[6.5, 11]} y={[2.8, H]} z={[20, 20.25]} c={VERDE} />
      <Caja x={[6.5, 11]} y={[0.9, 2.8]} z={[20.1, 20.14]} c="#bcd3dc" o={0.18} />
      <mesh position={[1, H / 2, 19]} rotation={[0, -Math.PI / 4, 0]}><boxGeometry args={[2.83, H, 0.25]} /><meshStandardMaterial color={VERDE} /></mesh>
      {/* segundo piso, cornisas, balcon */}
      <Caja x={[-0.2, 12.2]} y={[H, 7.5]} z={[19.9, 20.25]} c={VERDE} />
      {[3.6, 3.9, 6.9, 7.45].map((yy) => <Caja key={yy} x={[-0.25, 12.25]} y={[yy, yy + 0.08]} z={[20.25, 20.4]} c={CREMA} />)}
      <Caja x={[3, 9]} y={[3.95, 4.05]} z={[20.25, 21.1]} c={MADERA} />
      <Caja x={[3, 9]} y={[5.0, 5.1]} z={[21.0, 21.1]} c={MADERA} />
      {Array.from({length: 17}).map((_, i) => <Caja key={i} x={[3 + i * 0.37, 3 + i * 0.37 + 0.05]} y={[4.05, 5.0]} z={[21.02, 21.08]} c={MADERA} />)}
      {[3.8, 6.4].map((x0) => <Caja key={x0} x={[x0, x0 + 1.8]} y={[3.95, 6.4]} z={[20.26, 20.3]} c="#3a2a1e" e="#ffb070" ei={0.25} />)}
      {/* neon de la gata sobre la vitrina */}
      <Caja x={[5.6, 10.4]} y={[3.0, 3.55]} z={[20.3, 20.36]} c="#ff6ab5" e="#ff2f9c" ei={2.2} />
      <pointLight position={[8, 3.3, 21.2]} color="#ff4fae" intensity={8} distance={10} decay={1.5} />
      {/* barra, contrabarra con botellas y taburetes */}
      <Caja x={[1.3, 2.0]} y={[0, 1.1]} z={[9, 17]} c={MADERA} />
      <Caja x={[1.25, 2.1]} y={[1.1, 1.15]} z={[9, 17]} c="#2b1a10" />
      <Caja x={[0.05, 0.55]} y={[0, 2.4]} z={[9, 17]} c="#3a2618" />
      <Caja x={[0.5, 0.56]} y={[0.9, 2.3]} z={[9.1, 16.9]} c="#ffcf7a" e="#ffae42" ei={1.2} />
      {Array.from({length: 30}).map((_, i) => <Cil key={i} p={[0.35, 1.2 + (i % 3) * 0.5, 9.3 + Math.floor(i / 3) * 0.75]} r={0.05} h={0.3} c={['#2f5a2f', '#6b2020', '#8a6a2a'][i % 3]} />)}
      {Array.from({length: 8}).map((_, i) => <Cil key={i} p={[2.575, 0.75, 9.5 + i]} r={0.22} h={0.08} c="#9b2f2f" />)}
      {Array.from({length: 8}).map((_, i) => <Cil key={i} p={[2.575, 0.37, 9.5 + i]} r={0.04} h={0.74} c="#222" />)}
      {/* mesas y sillas */}
      {[[5, 11], [8, 11], [5, 14.2], [8, 14.2], [8.7, 18.2]].map(([x, z]) => (
        <group key={`${x}${z}`}>
          <Cil p={[x, 0.75, z]} r={0.45} h={0.05} c="#c9a877" />
          <Cil p={[x, 0.37, z]} r={0.06} h={0.74} c="#222" />
          <Caja x={[x - 1.0, x - 0.6]} y={[0, 0.9]} z={[z - 0.2, z + 0.2]} c="#5a3a22" />
          <Caja x={[x + 0.6, x + 1.0]} y={[0, 0.9]} z={[z - 0.2, z + 0.2]} c="#5a3a22" />
        </group>
      ))}
      {/* pared de fotos y rocola */}
      {Array.from({length: 12}).map((_, i) => <Caja key={i} x={[11.9, 11.95]} y={[1.4 + (i % 2) * 0.7, 1.9 + (i % 2) * 0.7]} z={[9.6 + Math.floor(i / 2) * 1.05, 10.2 + Math.floor(i / 2) * 1.05]} c="#e8dcc0" />)}
      <Caja x={[10.8, 11.8]} y={[0, 1.5]} z={[8.3, 9.1]} c="#b3261e" e="#ff7a3a" ei={0.6} />
      {/* lamparas colgantes rojas */}
      {[[5, 12.5], [8, 12.5], [4.5, 16.5]].map(([x, z]) => (
        <group key={`${x}${z}`}>
          <Cil p={[x, 2.6, z]} r={0.18} h={0.25} c="#8a1c1c" e="#ff5a3a" />
          <pointLight position={[x, 2.4, z]} color="#ff9a6a" intensity={5} distance={6} decay={1.6} />
        </group>
      ))}
      {/* --- lo ecuatoriano del bar: no cambian las medidas, cambia como se vive --- */}
      {/* reja corrediza, RECOGIDA contra el borde: el bar esta abierto. Cerrada taparia
          la vista del taller desde la mesa de la ventana, que es el plano de Micaela. */}
      {Array.from({length: 20}).map((_, i) => (
        <Caja key={i} x={[6.55 + i * 0.045, 6.58 + i * 0.045]} y={[0.9, 2.8]} z={[20.04, 20.08]} c="#9fb0a6" />
      ))}
      {/* porton metalico enrollable, recogido: por el calor se abre de par en par */}
      <Caja x={[6.4, 11.1]} y={[2.82, 3.0]} z={[20.0, 20.2]} c="#7b8288" />
      {/* ventilador de pie apuntando a la barra */}
      <Cil p={[3.7, 0.5, 12.8]} r={0.05} h={1.0} c="#4a4a4a" />
      <Cil p={[3.7, 1.02, 12.8]} r={0.34} h={0.12} c="#c9c4b6" />
      {/* hielera: la cerveza grande y helada, en el extremo de la barra */}
      <Caja x={[2.4, 3.6]} y={[0, 0.85]} z={[17.3, 18.3]} c="#5d8fb3" />
      <Caja x={[2.45, 3.55]} y={[0.85, 0.92]} z={[17.35, 18.25]} c="#cfe2ee" />
      {/* tele colgada en la esquina: cuando hay partido, la rocola se calla */}
      <Caja x={[11.2, 11.3]} y={[2.2, 2.85]} z={[18.4, 19.4]} c="#2b2b2b" />
      <Caja x={[11.3, 11.34]} y={[2.26, 2.79]} z={[18.46, 19.34]} c="#6f8ea0" e="#8fb3c8" ei={0.5} />
      {/* dos mesas de plastico que salen a la vereda al atardecer */}
      {[[3.6, 21.3], [5.3, 21.3]].map(([x, z]) => (
        <group key={`${x}${z}`}>
          <Cil p={[x, 0.68, z]} r={0.38} h={0.05} c="#e8e3d6" />
          <Cil p={[x, 0.34, z]} r={0.05} h={0.68} c="#dcd7c9" />
        </group>
      ))}
      {/* vereda, avenida y el taller enfrente (a 40 m) */}
      <Caja x={[-30, 42]} y={[-0.08, -0.03]} z={[20.25, 23]} c="#6b6b6b" />
      <Caja x={[-30, 42]} y={[-0.12, -0.08]} z={[23, 59]} c="#1c1d20" />
      <Caja x={[-30, 42]} y={[-0.07, -0.05]} z={[40.6, 41.4]} c="#3d5a2e" />
      <Caja x={[0, 24]} y={[0, 7.25]} z={[60, 61]} c="#141312" />
      <Caja x={[0, 7.5]} y={[5.75, 9.75]} z={[60, 61]} c="#d9d0bb" />
      <Caja x={[8, 22]} y={[4.9, 6.2]} z={[59.9, 60]} c="#0d0d0d" />
      <Caja x={[8.5, 21.5]} y={[5.3, 5.8]} z={[59.88, 59.9]} c="#d4ad52" e="#c49a3a" ei={0.8} />
      <GalloNeon p={[15, 6.2, 59.85]} rotY={Math.PI} />
      <Caja x={[0, 24]} y={[0, 0.4]} z={[59.88, 60]} c="#2f2c29" />
      {[9, 12, 18.5, 21.5].map((xx) => <Cil key={xx} p={[xx, 7.6, 60.5]} r={0.45} h={0.5} c="#b9c0c6" />)}
      <Caja x={[9, 14]} y={[0.4, 1.6]} z={[59.9, 60]} c="#ffb35c" e="#ff9a2a" ei={1.5} />
      <pointLight position={[11.5, 1, 58]} color="#ffae5c" intensity={6} distance={10} />
    </group>
  );
};

// ---------------------------------------------------------------- PASAJE LA ESPERANZA
const Pasaje: React.FC = () => {
  const casas = ['#8a6f55', '#9a8a70', '#7a6a5a', '#a08b6e', '#6f5e4e', '#8e7d68'];
  return (
    <group>
      <Caja x={[-5, 105]} y={[-0.05, 0]} z={[0, 5]} c="#55524e" />
      <Caja x={[-5, 105]} y={[-0.06, 0.005]} z={[2.35, 2.65]} c="#2e2d2b" />
      {[[8, 1.2, 3.5], [30, 3.8, 1.6], [48, 1.0, 2.8], [70, 3.5, 2.2]].map(([x, z, w]) => <Caja key={x} x={[x, x + w]} y={[0, 0.012]} z={[z, z + 1.1]} c="#1a1c20" />)}
      {/* norte: espalda del taller y de las tiendas */}
      <Caja x={[0, 24]} y={[0, 7.25]} z={[-0.3, 0]} c="#6d6a64" />
      <Caja x={[21.8, 22.8]} y={[0, 2.1]} z={[0, 0.05]} c="#8c8c8c" />
      <Caja x={[12.5, 13.5]} y={[2.2, 2.8]} z={[0, 0.06]} c="#2d2d2d" />
      <Caja x={[0.3, 2.8]} y={[2.6, 3.1]} z={[0, 0.05]} c="#2f5aa0" e="#1e3f80" ei={0.3} />
      {[24, 36, 49, 62, 75, 88].map((x, i) => <Caja key={x} x={[x, x + 12.5]} y={[0, 4.2 + (i % 3) * 0.5]} z={[-0.3, 0]} c={casas[i]} />)}
      {/* sur: espaldas de las casas de la Mz. R */}
      {Array.from({length: 13}).map((_, i) => (
        <group key={i}>
          <Caja x={[i * 8, i * 8 + 8]} y={[0, 5.6 - (i % 4) * 0.4]} z={[5, 5.3]} c={casas[(i + 2) % 6]} />
          <Caja x={[i * 8 + 2.5, i * 8 + 3.5]} y={[3.2, 4.0]} z={[4.97, 5]} c={i % 3 ? '#1b1b1b' : '#caa860'} e={i % 3 ? undefined : '#b08030'} ei={0.4} />
          {i % 4 === 1 && <Caja x={[i * 8 + 5, i * 8 + 7.6]} y={[0, 2.4]} z={[4.97, 5]} c="#5e6166" />}
        </group>
      ))}
      {/* faroles: solo el primero funciona */}
      {[[20, true], [55, false], [88, false]].map(([x, on]) => (
        <group key={x as number}>
          <Cil p={[x as number, 2.1, 4.6]} r={0.06} h={4.2} c="#333" />
          <Cil p={[x as number, 4.25, 4.35]} r={0.16} h={0.12} c="#ddd" e={on ? '#ffd23f' : undefined} />
          {on && <pointLight position={[x as number, 4.1, 4.2]} color="#ffcf4a" intensity={16} distance={16} decay={1.5} castShadow />}
        </group>
      ))}
      {/* tachos, cables y el gato */}
      {[31, 47, 72].map((x) => <Cil key={x} p={[x + 0.45, 0.45, 4.1]} r={0.3} h={0.9} c="#2f4a2f" />)}
      {[10, 26, 41, 58].map((x) => <Caja key={x} x={[x, x + 0.03]} y={[5.9, 5.93]} z={[-0.3, 5.3]} c="#111" />)}
      <Caja x={[65, 65.5]} y={[5.2, 5.55]} z={[5.05, 5.25]} c="#0d0d0d" />
    </group>
  );
};

const VISTAS: Record<string, {esc: 'bar' | 'pasaje'; p: V3; t: V3; fov: number}> = {
  bar_fachada: {esc: "bar", p: [6.5, 1.7, 33], t: [6.0, 3.5, 20], fov: 58},
  bar_barra: {esc: 'bar', p: [4.3, 1.6, 19.2], t: [1.5, 1.2, 10.5], fov: 62},
  bar_ventana: {esc: 'bar', p: [8.4, 1.25, 17.2], t: [13.0, 3.6, 60], fov: 58},
  bar_fotos: {esc: 'bar', p: [5.5, 1.6, 12.8], t: [12, 1.9, 12.8], fov: 62},
  pasaje_entrada: {esc: 'pasaje', p: [-3, 1.7, 2.5], t: [40, 1.8, 2.5], fov: 55},
  pasaje_puerta: {esc: 'pasaje', p: [27, 1.6, 3.9], t: [22.3, 1.3, 0], fov: 60},
};
export const ORDEN_ESC = Object.keys(VISTAS);

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

export const Escenas3D: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const v = VISTAS[ORDEN_ESC[Math.min(frame, ORDEN_ESC.length - 1)]];
  return (
    <ThreeCanvas width={width} height={height} shadows style={{background: '#0c0f16'}} camera={{position: v.p, fov: v.fov, near: 0.05, far: 300}}>
      <Camara v={v} />
      <ambientLight intensity={v.esc === 'bar' ? 0.35 : 0.18} />
      <hemisphereLight args={['#6d7fa8', '#1c1c1c', v.esc === 'bar' ? 0.35 : 0.25]} />
      <directionalLight position={[-20, 30, -10]} color="#8ea0c8" intensity={0.35} />
      {v.esc === 'bar' ? <Bar /> : <Pasaje />}
    </ThreeCanvas>
  );
};
