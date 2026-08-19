import matplotlib.pyplot as plt
import numpy as np

# Configuración de la figura y proporciones
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.set_aspect('equal')

# Límites de la vista
ax.set_xlim(-8.5, 1.5)
ax.set_ylim(-3.5, 3.5)

# Configuración de la cuadrícula
ax.set_xticks(np.arange(-8, 2, 1))
ax.set_yticks(np.arange(-3, 4, 1))
ax.grid(True, which='both', color='#d0d0d0', linestyle='-', linewidth=0.8)

# Desactivar marcas y etiquetas externas
ax.tick_params(top=False, bottom=False, left=False, right=False,
               labeltop=False, labelbottom=False, labelleft=False, labelright=False)

# Ejes principales (Horizontal y Vertical en el vértice)
ax.axhline(0, color='black', linewidth=1.5)
ax.axvline(0, color='black', linewidth=1.5)

# Arco del espejo cóncavo (Centro en x=-4, R=4)
theta = np.linspace(-np.radians(45), np.radians(45), 200)
x_mirror = -4 + 4 * np.cos(theta)
y_mirror = 4 * np.sin(theta)
ax.plot(x_mirror, y_mirror, color='black', linewidth=2.8)

# Escala numérica sobre el eje horizontal (-6u, -4u, -2u, 0)
ax.text(-6, -0.35, '-6u', fontsize=11, ha='center', va='top')
ax.text(-4, -0.35, '-4u', fontsize=11, ha='center', va='top')
ax.text(-2, -0.35, '-2u', fontsize=11, ha='center', va='top')
ax.text(0.15, -0.35, '0  (u)', fontsize=11, ha='left', va='top')

# Textos de referencia del diagrama original
ax.text(-8.3, -0.35, 'EJE PRINCIPAL', fontsize=10, fontweight='bold', ha='left', va='top')
ax.text(0.25, 2.3, 'ESPEJO\nCÓNCAVO', fontsize=10, fontweight='bold', ha='left', va='center')
ax.text(-1.3, 2.7, 'R=4u', fontsize=10, fontweight='bold', ha='right', va='bottom')
ax.text(0.15, 0.2, 'V', fontsize=12, fontweight='bold', ha='left', va='bottom')

# Ocultar marco exterior
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig('espejo_concavo_base.png', bbox_inches='tight', dpi=300)
plt.show()