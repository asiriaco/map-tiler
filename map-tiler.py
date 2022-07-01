import os
from itertools import product
import rasterio as rio
from rasterio import windows

#inserir aqui o diretorio fonte e do arquivo que se deseja dividir
in_path = 'arquivos_matriciais'
in_filename = 'uso_terra_sfx_fbds_726_974.tif'
#inserir aqui o diretorio alvo e como deverão chamar os arquivos divididos
out_path = 'arquivos_matriciais_tile/uso_terra_sfx_fbds_726_974'
out_filename = 'tile_{}-{}.tif'

def get_tiles(ds, width , height):
    nols, nrows = ds.meta['width'], ds.meta['height']
    offsets = product(range(0, nols, width), range(0, nrows, height))
    big_window = windows.Window(col_off=0, row_off=0, width=nols, height=nrows)
    for col_off, row_off in offsets:
        window = windows.Window(col_off=col_off, row_off=row_off, width=width, height=height).intersection(big_window)
        transform = windows.transform(window, ds.transform)
        yield window, transform

def process(in_path, in_filename, out_path, out_filename, tile_width, tile_height):
    with rio.open(os.path.join(in_path, in_filename)) as inds:
         
        meta = inds.meta.copy()
        for window, transform in get_tiles(inds, tile_width, tile_height):
            print(window)
            meta['transform'] = transform
            meta['width'], meta['height'] = window.width, window.height
            outpath = os.path.join(out_path,out_filename.format(int(window.col_off), int(window.row_off)))
            with rio.open(outpath, 'w', **meta) as outds:
                outds.write(inds.read(window=window))

process(in_path, in_filename, out_path, out_filename, 512, 512)
