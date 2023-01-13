import cadquery as cq
from cq_server.ui import ui, show_object

from common import NOZZLE_DIAMETER, MIN_WALL_THICKNESS, export_stl


BASEPLATE_HOLE = (
    8.5,
    6.5,
)
BASEPLATE_OFFSET = BASEPLATE_HOLE[0] * 1.5
BASEPLATE_MOUNT = (
    81.5,
    58,
    MIN_WALL_THICKNESS * 3.5,
)
BASEPLATE_CUTOFF_DIAMETER = 45

BOARD_STANDOFF = 5
BOARD_HOLE = (
    3 / 2,
    3 + BOARD_STANDOFF
)
BOARD_OFFSET = BOARD_HOLE[0] * 4
BOARD_MOUNT = (
    63,
    53,
    MIN_WALL_THICKNESS,
)
BOARD_Y_OFFSET = -2

baseplate = (
    cq.Workplane("XY")
    .box(BASEPLATE_MOUNT[0] + BASEPLATE_OFFSET, BASEPLATE_MOUNT[1] + BASEPLATE_OFFSET, BASEPLATE_MOUNT[2])
    .faces("<Z")
    .workplane()
    .rect(BASEPLATE_MOUNT[0], BASEPLATE_MOUNT[1], forConstruction=True)
    .vertices()
    .hole(BASEPLATE_HOLE[0], BASEPLATE_HOLE[1])
    # .cylinder(BASEPLATE_HOLE[1], BASEPLATE_HOLE[0], centered=(True, True, False))
    # .center(0, 0)
    # .cylinder(BASEPLATE_HOLE[1], BASEPLATE_HOLE[0], centered=(True, True, False))
)

board = (
    cq.Workplane("XY")
    .box(BOARD_MOUNT[0] + BOARD_OFFSET, BOARD_MOUNT[1] + BOARD_OFFSET + BOARD_Y_OFFSET * 2, BOARD_MOUNT[2])
    .faces(">Z")
    .workplane()
    .rect(BOARD_MOUNT[0], BOARD_MOUNT[1], forConstruction=True)
    .vertices()
    .cylinder(BOARD_HOLE[1], BOARD_HOLE[0], centered=(True, True, False))
    .rect(BOARD_MOUNT[0], BOARD_MOUNT[1], forConstruction=True)
    .vertices()
    .cylinder(BOARD_STANDOFF, BOARD_HOLE[0] * 1.5, centered=(True, True, False))
)

adapter = (
    baseplate
    .union(
        board.translate(
            (0, BOARD_Y_OFFSET, 0)
        ),
    )
    .center(-BASEPLATE_MOUNT[0] / 2, 0)
    .lineTo(BASEPLATE_MOUNT[0], 0, forConstruction=True)
    .vertices()
    .hole(BASEPLATE_CUTOFF_DIAMETER)
    .center(BASEPLATE_MOUNT[0] / 2, -BASEPLATE_MOUNT[1] / 2)
    .lineTo(0, BASEPLATE_MOUNT[1], forConstruction=True)
    .vertices()
    .hole(BASEPLATE_CUTOFF_DIAMETER)
)

def main():
    export_stl(adapter, __file__)

if __name__ == "__main__":
    main()
else:
    show_object(adapter)

