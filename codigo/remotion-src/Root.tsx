import {Composition} from 'remotion';
import {Prueba} from './Prueba';
import {Taller3D, ORDEN} from './Taller3D';
import {Escenas3D, ORDEN_ESC} from './Escenas3D';
import {Ciudad3D, CiudadVertical, ORDEN_CIUDAD, ORDEN_VERTICAL} from './Ciudad3D';
export const Root = () => (
  <>
    <Composition id="Prueba" component={Prueba} durationInFrames={45} fps={30} width={1080} height={1920} />
    <Composition id="Taller3D" component={Taller3D} durationInFrames={ORDEN.length} fps={1} width={1920} height={1080} />
    <Composition id="Escenas3D" component={Escenas3D} durationInFrames={ORDEN_ESC.length} fps={1} width={1920} height={1080} />
    {/* la ciudad se renderiza al doble y se baja a 1920 con PIL: asi los bordes
        quedan limpios sin depender del antialias del GL por software */}
    <Composition id="Ciudad3D" component={Ciudad3D} durationInFrames={ORDEN_CIUDAD.length} fps={1} width={2560} height={1440} />
    <Composition id="CiudadVertical" component={CiudadVertical} durationInFrames={ORDEN_VERTICAL.length} fps={1} width={1440} height={2560} />
  </>
);
