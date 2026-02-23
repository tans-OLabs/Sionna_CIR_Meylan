Read me  17/02/2026
File name”Sionna_CIR_Meylab.py »

Analyse Réponse Impulsionnelle 
Simulation d’un transmetteur OFDM 3.7 GHz depuis le bâtiment New Meylan Module C 3ème étage vers un récepteur niveau du sol au 22 chemin du Vieux Chêne.
Scène
Scène Openstreetmap + blender (export xml  Mitsuba)
scene = load_scene("test_scene/test_scene.xml")     # Batiment New Meylan et environs ~500m
Matériau
Matériau ITU_glass (parois verticales et ITU_Concrete sol et toits
Coordonnées transmetteur/récepteur 
tx = Transmitter("tx", [-19,-29,10],[0.0, 0.0, 0.0]) # Coordonnées Meylan BatA   A3B38 Balcon 
rx = Receiver("rx", [-30,-34,1.5],[0.0, 0.0, 0.0]) # Rue du Vieux Chêne local Vélo 
Fréquence 3.7 GHz
Import
import numpy  
import tensorflow 
from sionna.rt  import load_scene, Transmitter, Receiver, PlanarArray, Paths2CIR
import matplotlib.pyplot 
