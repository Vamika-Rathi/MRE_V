#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename    :  pack_core.py
Date        :  2024/11/29 15:15:38
Author      :  Tung Thai
"""

import time
from pathlib import Path

import h5py
import numpy as np
import scipy.io


class PackCore:
    """Load file and try to merge tracks while at it."""

    def __init__(self):
        self._path: Path = Path()
        self._data = {}

    ## ============================================================= # MARK: Properties

    @property
    def name(self) -> str:
        """Get name"""
        return self._path.name

    def stat(self):
        """Get Stats"""
        return self._path.stat()

    def data(self):
        """Get data read only. Prevents unintended overwrite of data"""
        return self._data

    ## =================================================================== # MARK: Load
    def load(self, file_path: str) -> int:
        """Open file as is. If successful, attr 'data' will contain data"""
        t_now = time.perf_counter()

        self._path = Path(file_path)
        if not self._path.is_file():
            print(f"-- Error, '{self._path}' does not exist.")
            return -1

        if self._path.suffix == ".mat":
            self._load_matlab()
        elif self._path.suffix == ".dat":
            self._load_dat()
        elif self._path.suffix in [".npz", ".npy"]:
            self._load_numpy()
        elif self._path.suffix in [".h5", ".hdf5"]:
            self._load_h5()
        else:
            print("-- Error, unknown file.")
            return -1

        ## ==============================

        print(f"opened in {(time.perf_counter() - t_now):2.3f}s")
        return 0

    ## ======================================== # MARK: Load matlab
    def _load_matlab(self):
        print("matlab", end=".")
        data = self._path.read_bytes()
        if data[:6] == b"MATLAB":
            if float(data[7:10]) > 7.2:
                self._load_h5()
            else:
                self._data = scipy.io.loadmat(self._path, mat_dtype=True)
        else:
            print("-- Error, unknown content of mat file.")

    ## ======================================== # MARK: Load numpy
    def _load_numpy(self):
        print("numpy", end=".")
        self._data = np.load(self._path, allow_pickle=False)

    ## ======================================== # MARK: Load h5
    def _load_h5(self):
        print("h5", end=".")
        paren = h5py.File(self._path, "r")
        my_list = []
        paren.visit(my_list.append)

        self._data = {}
        for key in my_list:
            if ":" in str(paren[key]):
                self._data[key] = np.array(paren[key])

    ## ======================================== # MARK: Load dat
    def _load_dat(self):
        print("dat", end=".")
        self._data = {}

        # I decided to ignore the velocity and acceleration data,
        # because they are computed from the point data anyway.
        # If you need them, uncomment needed lines.

        with open(self._path, "r", encoding="utf-8") as l_file:

            vals = {}
            z_total = 0
            scan_count = 0
            for line in l_file:
                if line.startswith("VARIABLES", 0, 9):
                    vari = line.split("=")[1].strip().replace('"', "").split(" ")
                    tva = {name: idx for idx, name in enumerate(vari)}
                    vals["s"] = [tva["x[mm]"], tva["y[mm]"], tva["z[mm]"]]
                    # vals["v"] = [tva["Vx[m/s]"], tva["Vy[m/s]"], tva["Vz[m/s]"]]
                    # vals["a"] = [tva["Ax[m/s²]"], tva["Ay[m/s²]"], tva["Az[m/s²]"]]
                    vals["index"] = [tva["trackID"]]

                elif line.startswith("I=", 0, 2):
                    scan_count += int(line.split(", ")[0].split("=")[1])

                elif line.startswith("ZONE T", 0, 6):
                    z_total += 1

            print(f"counted_zones {z_total}")

            self._data["idi"] = np.empty(scan_count, dtype="i4")
            self._data["zon"] = np.empty(scan_count, dtype="i4")
            self._data["poi"] = np.empty((scan_count, 3), dtype="f4")
            # self._data["vel"] = np.empty((scan_count, 3), dtype="f4")
            # self._data["acc"] = np.empty((scan_count, 3), dtype="f4")

            l_file.seek(0)  # Return to beginning of time and space. Literally.

            z_now = 0
            z_total -= 1
            idx_count = 0
            for line in l_file:
                if line.startswith("I=", 0, 2):
                    scan_count = int(line.split(", ")[0].split("=")[1])

                elif line.startswith("ZONE T", 0, 6):
                    z_now = int(line.split("=")[1].split(" ")[1].rstrip().strip('"'))
                    print(f"\rZone scanned {z_now/z_total:5.1%}", end="")

                elif line.startswith("DATAPACKING", 0, 11):
                    for _ in range(scan_count):
                        pl = l_file.readline().replace(",", ".").split(" ")
                        self._data["idi"][idx_count] = int(pl[8])
                        self._data["zon"][idx_count] = z_now
                        self._data["poi"][idx_count, 0] = pl[vals["s"][0]]
                        self._data["poi"][idx_count, 1] = pl[vals["s"][1]]
                        self._data["poi"][idx_count, 2] = pl[vals["s"][2]]

                        # self._data["vel"][idx_count, 0] = pl[vals["v"][0]]
                        # self._data["vel"][idx_count, 1] = pl[vals["v"][1]]
                        # self._data["vel"][idx_count, 2] = pl[vals["v"][2]]

                        # self._data["acc"][idx_count, 0] = pl[vals["a"][0]]
                        # self._data["acc"][idx_count, 1] = pl[vals["a"][1]]
                        # self._data["acc"][idx_count, 2] = pl[vals["a"][2]]

                        idx_count += 1

            print()

    ## =================================================================== # MARK: Save
    def save_lst(self, append="", suff=".mat", compress=False, dest: str = None):
        """Save the results. Append additional info. Suffix defines data type."""

        f_path = (
            Path("" if dest is None else dest).expanduser()
            / f"{self._path.stem}{append}{suff}"
        )
        f_path.parent.mkdir(exist_ok=True, parents=True)

        if suff == ".mat":
            scipy.io.savemat(f_path, self._data, do_compression=compress)
        elif suff in ".npz":
            if compress:
                np.savez_compressed(f_path, **self._data)
            else:
                np.savez(f_path, **self._data)
        elif suff in [".h5", ".hdf5"]:
            with h5py.File(f_path, "w") as f_out:
                for key, val in self._data.items():
                    f_out.create_dataset(key, data=val)
        else:
            print("-- Oi, dunno suffix. So me did nothin'")
            return

        print(f"File saved as '{f_path.name}' in dir '{f_path.parent}'")


if __name__ == "__main__":
    my_pack = PackCore()

    my_pack.load("")

