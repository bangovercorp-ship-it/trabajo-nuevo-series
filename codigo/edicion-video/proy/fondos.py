import cv2, numpy as np
from bacterias import render
from ilus2 import adn
sv=lambda n,a:cv2.imwrite(f'assets/{n}.png',cv2.cvtColor(a,cv2.COLOR_RGB2BGR))
W,H=1350,2400
sv('bact_amplio', render(W,H,'mixto',seed=11,escala=0.70,pal='ambar',densidad=3.4))
sv('bact_bastones',render(W,H,'bastones',seed=4,escala=1.55,pal='cian',densidad=1.5))
sv('bact_cocos',  render(W,H,'cocos',seed=9,escala=1.85,pal='verde',densidad=2.3))
sv('bact_comen',  render(W,H,'mixto',seed=23,escala=1.05,pal='ambar',densidad=2.0))
sv('adn_vert',    adn(1350,2400,horizontal=False,gen=(0.40,0.60),s=1,vueltas=3.4))
print('ok')
