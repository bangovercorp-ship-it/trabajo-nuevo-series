"""Plan v4 (tiempos ORIGINALES). Todo cuelga de palabras reales via guion2.ons()."""
from guion2 import ons, fin, WORDS
O=ons
BLA=(255,255,255); AMB=(255,193,64); ROJ=(255,92,80); CIA=(96,226,232); VER=(150,225,90); LIM=(196,238,70)

P_END = O(15)-0.02          # la persona solo vive en el gancho: hasta "…no huele mal."
T_POTO = O(9)               # "poto"
T_BACT1 = O(24)             # "bacterias" (primera vez)
T_PUNTO = 10.66             # dentro de la pausa dramatica tras "bacterias"
T_BACT2 = O(56)             # "las bacterias de tu piel"
T_COMEN = O(61); T_APESTA = O(67); T_GEN = O(86)

# ---------------- subtitulos: (palabra_ini, palabra_fin|None, texto, color, tamano, hasta_t_opcional)
def cap(i,j,txt,col=BLA,sz='n',fin_t=None): return dict(a=O(i),b=(fin_t if fin_t is not None else fin(j)+0.10),txt=txt,col=col,sz=sz)
CAPS=[
 cap(0,0,'¿SABES?',BLA,'n',O(1)-0.04), cap(1,2,'¿POR QUÉ?',BLA,'n',O(7)-0.04), cap(7,8,'HUELES A…',BLA,'n',O(9)-0.02),
 cap(9,9,'POTO',AMB,'big',O(10)-0.10),
 cap(11,11,'SUDOR'), cap(12,13,'NO HUELE'),
 cap(17,18,'HUELE MAL',ROJ,'n'),
 cap(24,24,'BACTERIAS',CIA,'big',T_PUNTO-0.06), dict(a=O(24)+0.62,b=T_PUNTO-0.06,txt='CORYNEBACTERIUM',col=CIA,sz='small'),
 dict(a=T_PUNTO,b=11.62,txt='PUNTO.',col=BLA,sz='big'),
 cap(26,26,'SUDAS'), cap(28,28,'CALOR',AMB), cap(30,30,'AGUA'), cap(32,32,'SAL'),
 cap(34,35,'SIN OLOR'),
 cap(37,38,'OLOR FUERTE'), cap(42,42,'AXILAS',AMB), cap(45,45,'INGLE',AMB),
 cap(48,48,'GLÁNDULAS'), cap(50,50,'SUSTANCIAS'), cap(53,54,'NO HUELEN'),
 cap(56,56,'BACTERIAS',CIA,'big',O(58)-0.05), dict(a=O(56)+0.62,b=O(58)-0.02,txt='STAPHYLOCOCCUS',col=VER,sz='small'),
 cap(59,60,'SE LAS',BLA,'n',O(61)-0.03), cap(61,61,'COMEN',BLA,'n',O(62)-0.05),
 cap(65,65,'DESECHAN'), cap(67,67,'APESTA',LIM,'big'),
 cap(70,71,'SUDAR MUCHO'), cap(72,73,'NO ES'), cap(74,75,'OLER MAL',ROJ),
 cap(80,80,'GENTE'), cap(83,84,'NO HUELE'),
 cap(86,86,'GENÉTICO'),
 cap(94,94,'EL TRUCO'), cap(95,96,'NO TAPAR',ROJ),
 cap(102,104,'SIN COMIDA'), cap(107,107,'BACTERIAS',CIA),
 cap(108,108,'LAVA'), cap(110,110,'AXILAS',AMB), cap(111,111,'INGLE',AMB), cap(113,113,'PIES',AMB), cap(115,115,'SÉCATE'), cap(117,117,'COMPLETO',BLA,'n',fin(117)+0.35),
]
# ABCC11: letras al ritmo de la voz (picos de silaba medidos)
ABC=[(45.48-0.05,'A'),(45.70-0.05,'B'),(46.27-0.05,'C'),(46.57-0.05,'C'),(46.90-0.05,'1'),(47.12-0.05,'1')]
ABC_END=47.95

# ---------------- insignias animadas (arriba): (t, nombre)
CARDS=[(O(30),'gota'),(O(32),'sal'),(O(34),'sinolor'),
       (O(42),'cuerpo_axilas'),(O(45),'cuerpo_ingle'),(O(48),'glandula'),(O(53),'sinolor'),
       (O(72),'igual'),(O(80),'gente'),(O(86),'adn'),
       (O(95),'spray'),(O(107),'micro'),(O(108),'jabon'),(O(110),'cuerpo_axilas'),(O(111),'cuerpo_ingle'),(O(113),'cuerpo_pies'),(O(115),'toalla')]
# ventanas en que vive la fila de insignias (conveyor de 3 huecos)
GRUPOS=[(O(29)-0.1,O(36)+0.15),(O(41)+0.0,O(56)-0.1),(O(71)-0.1,O(87)+0.2),(O(94)-0.1,None)]

# ---------------- planos a pantalla completa tras la persona: (ini, fin, material, z0, z1, extra)
# material: clave de IM (bacterias/ADN) o 'bokeh:<paleta>'. Cuando haya fotos/videos libres, se reemplazan aqui por ruta.
SCENES=[
 (P_END,   T_BACT1,        'bact_amplio',  1.00,1.10,'desenfoque'),   # tension: sale de foco y enfoca en "bacterias"
 (T_BACT1, 11.55,          'bact_bastones',1.04,1.24,None),
 (11.55,   O(33)-0.02,     'bokeh:calor',  1.00,1.06,None),           # sudas por calor, sale agua y sal
 (O(33)-0.02,O(36)-0.02,   'bokeh:agua',   1.00,1.05,None),           # casi sin olor
 (O(36)-0.02,O(46)-0.02,   'bokeh:cuerpo', 1.00,1.06,None),           # olor fuerte: axilas e ingle
 (O(46)-0.02,O(55)-0.02,   'bokeh:violeta',1.00,1.06,None),           # glandulas
 (O(55)-0.02,O(59)-0.02,   'bact_cocos',   1.00,1.18,None),           # las bacterias de tu piel
 (O(59)-0.02,O(64)-0.02,   'bact_comen',   1.00,1.18,'comen'),        # se las comen
 (O(64)-0.02,O(68)-0.02,   'bact_comen',   1.30,1.52,'vapor'),        # lo que desechan... apesta
 (O(68)-0.02,O(85)-0.02,   'bokeh:agua',   1.00,1.06,None),           # sudar mucho no es oler mal / gente que no huele
 (O(85)-0.02,O(93)-0.02,   'adn_vert',     1.00,1.12,'adn'),          # genetico + ABCC11
 (O(93)-0.02,O(107)-0.02,  'bokeh:calor',  1.00,1.06,None),           # el truco
 (O(107)-0.02,O(109)-0.02, 'bact_amplio_f',1.10,1.22,None),           # no darle de comer a las bacterias
 (O(109)-0.02,None,        'bokeh:agua',   1.00,1.08,None),           # lava, seca
]

# ---------------- sonido: (t_orig, tipo, params)
SFX=[
 (T_POTO-0.40,'whoosh',dict(dur=0.40,up=True,vol=0.7)),
 (T_POTO,'boom',dict(vol=1.0)), (T_POTO,'bloop',dict(f=520,vol=0.9)),
 (O(11)-0.02,'tick',dict(vol=0.7)),
 (P_END-0.05,'whoosh',dict(dur=0.22,up=False,vol=0.55)),
 (O(15),'tension',dict(dur=T_BACT1-O(15)-0.10,vol=0.9)),
 (T_BACT1-0.34,'whoosh',dict(dur=0.34,up=True,vol=0.8)),
 (T_BACT1,'boom',dict(vol=1.15)),
 (O(24)+0.62,'pop',dict(n=2,vol=0.7)),
 (T_PUNTO-0.06,'whoosh',dict(dur=0.16,up=False,vol=0.5)),
 (T_PUNTO,'thud',dict(vol=1.0)),
 (O(26),'tick',dict(vol=0.7)),(O(28),'tick',dict(vol=0.7)),
 (O(30),'pop',dict(n=1,vol=0.8)),(O(32),'pop',dict(n=3,vol=0.8)),(O(34),'tick',dict(vol=0.8)),
 (O(36)-0.12,'whoosh',dict(dur=0.18,up=True,vol=0.4)),
 (O(37),'tick',dict(vol=0.7)),
 (O(42),'pop',dict(n=2,vol=0.85)),(O(45),'pop',dict(n=4,vol=0.85)),
 (O(48),'pop',dict(n=1,vol=0.8)),(O(50),'tick',dict(vol=0.7)),(O(53),'pop',dict(n=0,vol=0.7)),
 (T_BACT2-0.34,'whoosh',dict(dur=0.34,up=True,vol=0.8)),
 (T_BACT2,'boom',dict(vol=1.0)),(O(56)+0.62,'pop',dict(n=3,vol=0.8)),
 (O(59)-0.22,'whoosh',dict(dur=0.20,up=True,vol=0.5)),
 (O(59),'tick',dict(vol=0.7)),(T_COMEN,'tick',dict(vol=0.8)),
 (O(65),'tick',dict(vol=0.7)),
 (T_APESTA-0.40,'whoosh',dict(dur=0.40,up=True,vol=0.8)),
 (T_APESTA,'boom',dict(vol=1.1)),(T_APESTA,'stab',dict(vol=0.8)),
 (O(68)-0.12,'whoosh',dict(dur=0.18,up=False,vol=0.5)),
 (O(70),'tick',dict(vol=0.7)),(O(72),'pop',dict(n=2,vol=0.85)),(O(80),'pop',dict(n=0,vol=0.8)),(O(83),'tick',dict(vol=0.7)),
 (T_GEN-0.36,'whoosh',dict(dur=0.32,up=True,vol=0.7)),
 (T_GEN,'boom',dict(vol=1.1)),(O(86),'pop',dict(n=3,vol=0.85)),
 (45.48-0.05,'tick',dict(vol=0.9)),(45.70-0.05,'tick',dict(vol=0.9)),(46.27-0.05,'tick',dict(vol=0.9)),(46.57-0.05,'tick',dict(vol=0.9)),(46.90-0.05,'tick',dict(vol=0.9)),(47.12-0.05,'tick',dict(vol=0.9)),
 (O(93)-0.18,'whoosh',dict(dur=0.16,up=False,vol=0.5)),
 (O(94),'tick',dict(vol=0.7)),(O(95),'pop',dict(n=1,vol=0.85)),(O(102),'tick',dict(vol=0.7)),(O(107),'pop',dict(n=0,vol=0.8)),
 (O(108),'pop',dict(n=0,vol=0.85)),(O(110),'pop',dict(n=1,vol=0.85)),(O(111),'pop',dict(n=2,vol=0.85)),(O(113),'pop',dict(n=3,vol=0.9)),
 (O(115),'pop',dict(n=2,vol=0.85)),(O(117),'chime',dict(vol=0.8)),
]
HITS_T=[T_POTO,T_BACT1,T_PUNTO,T_BACT2,T_APESTA,T_GEN]   # los que llevan golpe de camara
