#linear interpolation of the coordinates between GS (POSCAR_I) and STE(POSCAR_F)

from ase.io import read, write
import numpy as np

def interpolate_and_extrapolate(poscar1, poscar2, nsteps, outprefix="POSCAR", xdatcar="XDATCAR"):
    """
    Interpolate and extrapolate between two POSCAR structures under PBC.
    Output POSCAR files and a combined XDATCAR trajectory.

    Parameters
    ----------
    poscar1 : str
        Path to initial POSCAR
    poscar2 : str
        Path to final POSCAR
    nsteps : int
        Number of intermediate steps (between and beyond)
    outprefix : str
        Prefix for output POSCAR files (e.g. 'POSCAR')
    xdatcar : str
        Name of output XDATCAR trajectory file
    """
    # Read structures
    atoms1 = read(poscar1, format="vasp")
    atoms2 = read(poscar2, format="vasp")

    if len(atoms1) != len(atoms2):
        raise ValueError("POSCARs must have the same number of atoms!")

    # Cell and fractional coordinates
    cell = atoms1.get_cell()
    f1 = atoms1.get_scaled_positions()
    f2 = atoms2.get_scaled_positions()

    # Minimum image convention
    df = f2 - f1
    df -= np.round(df)

    # Total number of frames
    total_structs = 2 + 2 * nsteps
    frames = []

    # Generate interpolations + extrapolations
    for i in range(total_structs):
        alpha = i / (nsteps + 1)  # interpolation parameter

        f_interp = f1 + alpha * df

        atoms_interp = atoms1.copy()
        atoms_interp.set_cell(cell, scale_atoms=True)
        atoms_interp.set_scaled_positions(f_interp)

        # Save POSCAR
        fname = f"{outprefix}{i+1}"  # POSCAR1, POSCAR2, ...
        write(fname, atoms_interp, format="vasp")
        print(f"Written {fname} (alpha={alpha:.3f})")

        # Collect for XDATCAR
        frames.append(atoms_interp)

    # Write XDATCAR trajectory
    write(xdatcar, frames, format="vasp-xdatcar")
    print(f"Written trajectory {xdatcar} with {len(frames)} frames")


# Example usage:
# interpolate_and_extrapolate("POSCAR1", "POSCAR2", nsteps=5, outprefix="POSCAR", xdatcar="XDATCAR")
