from pathlib import Path

from cadquery import exporters


NOZZLE_DIAMETER = 0.4
MIN_WALL_THICKNESS = NOZZLE_DIAMETER * 4.5



def export_stl(model, filepath):
    filepath = Path(Path(filepath).parent / Path(filepath).stem).with_suffix(".stl")
    exporters.export(
        model, 
        str(filepath),
    )
