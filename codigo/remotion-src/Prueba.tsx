import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
// prueba: una palabra que entra con rebote, estilo subtitulo de agencia
export const Prueba = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 11, stiffness: 160}});
  return (
    <AbsoluteFill style={{background: '#0b0b0b', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{fontFamily: 'Arial Black', fontSize: 120, color: '#DDAA3F',
                   transform: `scale(${0.6 + 0.4 * s})`, opacity: s}}>LÁZARO</div>
    </AbsoluteFill>
  );
};
