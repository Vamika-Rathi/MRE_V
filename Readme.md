# Data Re-packer

## Description

Open files, especially the dat format DaVis files exported from DaVinci.
Whatever file you open, be it matlab, numpy, h5 or those dat files, you can use this
script to convert them into what you can use best.

The content will be saved as is. Except for the dat files.

From those data coordinate, index and zone data will be saved into poi, idi and zon as
float3, integer and integer respectively.


## Requirements

Besides Python, you also need Numpy, Scipy and h5py package.
Numpy for most of the performance computation and scipy and h5py for Matlab
import and export.

## Usage

First, default will be compact data and export as Numpy file:

```
$ python main.py <file>
```

Default is a Matlab file, since the majority of us. But you can do the following:

```
$ python main.py <file> -t ".npz" -s "_my_test"
```

The "-t" (type) flag allows you to save the file as npz (Numpy native data file).
You can choose between ".mat", ".npy" and ".h5" as extension.
H5 is a Hierarchical Data Format, which seems to be quite popular in scientific work.

The "-s" (suffix) flag allows you to add some name at the end. I.e. time or parameter.

Default is that the file will be saved where you run the script from.
Of course, you can also change the destination with:

```
$ python main.py <file> -o "~/my_experiments"
```

In this case, in your home folder a "my_experiments" folder will be created if it does
not exist yet. Furthermore, the file will be saved there.


## Credits

Thanks to Team HAW Hamburg and TUHH for providing the data which
I used to write this converter. ^^

## License

[MIT](https://choosealicense.com/licenses/mit/)
