import numpy as np
import tensorflow as tf
from sionna.rt import load_scene, Transmitter, Receiver, PlanarArray, Paths2CIR, PathSolver
import matplotlib.pyplot as plt

scene = load_scene("test_scene/test_scene.xml")     # Batiment New Meylan et environs ~500m

for i,obj in enumerate(scene.objects.values()):
    print(f"{obj.name} : {obj.radio_material.name}")
    if i>=10:    #    10 block ??? 
        break
scene.tx_array = PlanarArray(numrows=4,
                                num_cols=4,
                                vertical_spacing=0.5,
                                horizontal_spacing=0.5,
                                pattern="tr38901",
                                polarization = "V")

scene.rx_array = PlanarArray(numrows=1,
                                num_cols=1,
                                vertical_spacing=0.5,
                                horizontal_spacing=0.5,
                                pattern="iso",
                                polarization = "V")

tx = Transmitter("tx", [-19,-29,10],[0.0, 0.0, 0.0]) # Coordonnées Meylan BatA   A3B38 Balcon 
scene.add(tx)

rx = Receiver("rx", [-30,-34,1.5],[0.0, 0.0, 0.0]) # Rue du Vieux Chêne local Vélo 
scene.add(rx)

cm= scene.coverage_map()  # package Jupiter pour impression carte couverture

scene.preview(coverage_map=cm)

scene.render("preview", coverage_map=cm);

scene.paths_solver = PathSolver()# to intialize the patrh solver
paths = scene.paths_solver(scene, max_depth=5) # replace  scene.compute_paths()

#p2c = Paths2CIR(sampling_frequency=100e6,scene=scene)
#a, tau = p2c(paths.as_tuple())

#plt.figure()
#plt.stem(tau[0,0,0,:]=1e9, np.abs(a[0,0,0,0,0,:,0)
#plt.xlabel("Delay [ns]")
#plt.ylabel(r"$|a|$");

scene.preview(paths=paths)

scene.render("preview", paths=paths, coverage_map=cm);

# code substitution Paths2CIR

#  'scene' et 'paths' ont été définis  dans  code initial ?
#  'paths' est le résultat de scene.compute_paths()

# Fréquence d'échantillonnage
sampling_freq = 100e6  # 100 MHz

# Récupérer tous les chemins
paths = scene.paths_solver(scene, max_depth=5)

# Extraire délais et amplitudes
delays = []
amplitudes = []

for path in paths.paths:
    delays.append(path.delay.numpy())  # délai en secondes
    amplitudes.append(path.amplitude.numpy())  # amplitude complexe

# Convertir en tenseurs
delays = tf.constant(delays)
amplitudes = tf.constant(amplitudes, dtype=tf.complex64)

# Définir le vecteur temps
t_max = tf.reduce_max(delays)
num_samples = int(tf.ceil(t_max * sampling_freq)) + 1
t = tf.linspace(0.0, t_max, num_samples)

# Initialiser la réponse impulsionnelle
cir = tf.zeros_like(t, dtype=tf.complex64)

# Construire la CIR en ajoutant chaque chemin
indices = tf.cast(delays * sampling_freq, tf.int32)

# Utiliser scatter pour ajouter chaque amplitude à la position correspondante
cir = tf.tensor_scatter_nd_add(cir, tf.reshape(indices, [-1,1]), amplitudes)

# Visualiser la CIR
plt.figure()
plt.plot(t.numpy() * 1e9, tf.abs(cir).numpy())  # en nanosecondes
plt.xlabel("Delay [ns]")
plt.ylabel(r"$|a|$")
plt.title("Réponse impulsionnelle (CIR) construite à partir des chemins")
plt.show()

#code de substitution 


