# Avogadro Plugin: Visualize Valence Bond Orbitals of Molecules

## Overall Goals and Initial Planning
 - develop a plugin for Avogadro 2 according to the requirements on https://avogadro.cc/develop/plugins/index.html
 - it will be a `Pixi project` style plugin
    - therefore I will use `pixi` to handle the Python development environment
 - the plugin will create a new menu command in the PLUGINS menu. Therefore it is a "Menu Commands" Feature Type plugin. 
 - plugin should be easily installable in Avogadro 2 through the plugins widget
 - I have local plugins after which I can pattern my project locally on my hard drive at `C:\Users\mccan\AppData\Local\OpenChemistry\Avogadro\plugins\`

## Capabilities: What the Plugin Should Do

 - the plugin will enable the user to use a MENU COMMAND within Avogadro to display the valence atomic orbitals of the molecule that is 
   currently drawn on the Avogadro screen. 
 - When the user clicks "Display Valence Orbitals", new surfaces will appear over the molecule. These surfaces will be the atomic orbitals of each atom.
 - Because this plugin is geared as an educational tool, the orbitals that are displayed will be those that are taught at the undergraduate
   general chemistry and undergraduate organic chemistry level. They will not be rigorously calculated by quantum mechanics. Rather, they will be based upon 
   the geometry of the molecule and will be produced entirely algorithmically according to VSEPR rules.

## How Will the Plugin Do this, Generally

Here is a conceptual roadmap of how your algorithm can translate a 3D molecular structure into textbook-style Valence Bond visualizations in real-time.

To generate the orbitals programmatically, the Python script will need to pass the molecule through a four-step pipeline every time the structure is loaded or updated.

```
[Molecule Geometry] ➔ [Step 1: Steric Number] ➔ [Step 2: Hybridization] ➔ [Step 3: Vector Orientation] ➔ [Step 4: Grid Generation]
```

### Step 1: Calculate the Steric Number

For any given atom, look at its local environment to find its **Steric Number (SN)**:

$$\text{Steric Number} = (\text{Number of attached atoms}) + (\text{Number of lone pairs})$$

- *Implementation Tip:* Avogadro handles the attached atoms easily via the molecular graph. For lone pairs, you can subtract the atom's current shared valence electrons from its standard periodic table valence count.

### Step 2: Assign Hybridization and Ideal Geometry

Map the steric number directly to the standard VSEPR geometries and orbital sets:

| **Steric Number** | **Hybridization** | **Ideal Geometry**            | **Orbital Set Components**                          |
| ----------------- | ----------------- | ----------------------------- | --------------------------------------------------- |
| **2**             | $sp$              | Linear ($180^\circ$)          | Two $sp$ hybrids, two unhybridized $p$ orbitals     |
| **3**             | $sp^2$            | Trigonal Planar ($120^\circ$) | Three $sp^2$  hybrids, one unhybridized $p$ orbital |
| **4**             | $sp^3$            | Tetrahedral ($109.5^\circ$)   | Four $sp^3$ hybrids, zero unhybridized $p$ orbitals |

### Step 3: Orient the Orbital Vectors (The Core Math)

This is the most critical step. You must determine exactly *where* the lobes of these hybrid orbitals are pointing in 3D space so they align with the actual bonds.

1. **For Hybrid Orbitals ($\sigma$-bonding/Lone Pairs):** Create a unit vector pointing from the central atom toward each of its bonded neighbors. If the actual geometry is slightly distorted from the ideal VSEPR angles, using the actual atom-to-atom vectors ensures the hybrid lobes point directly at each other to show the $\sigma$ "overlap zone."
2. **For Unhybridized $$p$$-Orbitals ($\pi$-bonding):** These must be mathematically orthogonal (at $90^\circ$) to the hybrid vectors.
   - *Example ($$sp^2$$ Carbon in Ethylene):* Find the plane defined by the carbon and its three neighbors. The unhybridized $$p_z$$ orbital vector will simply be the **normal vector** to that plane (calculated using a cross product of the bonding vectors). This perfectly aligns the $$p$$ orbitals parallel to each other, visually demonstrating how they overlap side-by-side to form a $\pi$ bond.

### Step 4: Generate the 3D Voxel Grid

Once you have the directional vectors for every orbital on an atom, you generate a local 3D scalar grid (a voxel map) around that atom.

For every point $(x, y, z)$ in the grid, evaluate the mathematical shape of the orbital relative to its target vector. Because you are going for a textbook look, you don't need complex radial wavefunctions. You can use simple, clean functions:

- **$p$-orbital lobe amplitude:** Directly proportional to the cosine of the angle $$\theta$$ between the grid point vector and the orbital's primary vector: $A = \cos(\theta)$.
- **Hybrid orbital ($sp^n$) lobe amplitude:** You can simulate the classic asymmetric "large front lobe, tiny back lobe" look by mixing an $$s$$ component (always positive) with a $$p$$ component: $A = C_1 + C_2\cos(\theta)$.
- To handle the VSEPR assignment logic for edge cases—like detecting aromatic/conjugated rings vs. standard localized double bonds—to ensure the $$p$$-orbitals line up correctly, the logic for the $$\pi$$-system plane determination is simple. Calculating the plane of the $$\sigma$$-framework and projecting the unhybridized $p$-orbitals along the normal vector is precisely how you guarantee that the visualization updates accurately, even when a bond is twisted or distorted away from ideal textbook angles.

## How the Plugin Will Work from a Bird's Eye View

## 1. Reading the Geometry (The Entry Point)

When a user clicks your extension, Avogadro pipes the active molecule data directly into your Python script via standard input as a JSON string (CJSON format).

You can extract the atomic positions and bond connectivity instantly using Python's built-in `json` module:

Python

```python
import sys
import json

def main():
    # Avogadro 2.0.0 sends the molecule via stdin
    input_data = json.loads(sys.stdin.read())
    
    # Grab the molecule object from CJSON
    molecule = input_data.get("molecule", {})
    atoms = molecule.get("atoms", {})
    bonds = molecule.get("bonds", {})
    
    atomic_numbers = atoms.get("elements", [])
    coords = atoms.get("coords", {}).get("3d", []) # Flattened array [x1, y1, z1, x2, y2, z2...]
    
    # Reshape coordinates into an Nx3 NumPy array for clean vector math
    import numpy as np
    positions = np.array(coords).reshape(-1, 3)
    
    # Run your VSEPR + Orbital logic here...
```

## 3. Feeding Volumetric Data Back to Avogadro 2

One of the best design improvements in Avogadro 2 is how cleanly it handles meshes and scalar fields. To show the visual "overlap" of your geometric hybrid orbitals, your script can generate a **3D Scalar Grid (Cube File style)** entirely in memory and attach it to the CJSON output.

When your script finishes its calculations, it prints a JSON string back to `stdout`. Avogadro reads this and renders the surfaces immediately.

Your returned JSON will look something like this:

JSON

```json
{
  "molecule": {
    "cube": {
      "origin": [-5.0, -5.0, -5.0],
      "spacing": [0.1, 0.1, 0.1],
      "dimensions": [100, 100, 100],
      "scalars": [0.001, 0.005, 0.01, "..."] 
    }
  }
}
```

- **Origin:** The starting 3D coordinate of your bounding grid box.
- **Spacing:** The step size between grid points (0.1 Ångströms gives a beautifully smooth resolution).
- **Dimensions:** How many voxels along the X, Y, and Z axes.
- **Scalars:** A single, flattened array containing the evaluated wavefunction amplitudes ($\psi_{VB}$) at every grid point.

Once Avogadro receives this `cube` object, the user can use the native rendering options to set the isosurface values (isovalues) and transparency, letting them see the hybrid lobes intersecting beautifully.