import dnv.net.runtime
from dnv.sesam.sifapi.core import ISifData
from dnv.sesam.sifapi.io import SesamDataFactory


def main():
    """Reads nodal displacement data (RVNODDIS) of a result case (LC 1) and FE node (node 13) in the R1.SIN file"""
    with SesamDataFactory.CreateReader(".", "R1.SIN") as adapter:
        adapter.CreateModel()

        ires = 1  # result case reference number
        iinod = 13  # internal node number

        data = adapter.ReadExt('RVNODDIS', [ires, iinod])
        print(f'Length of the data: {len(data)}')
        print(f'Data type: {type(data)}')

        # Convert System.Double[] to a Python list
        data_list = [element for element in data]
        print(data_list)  # print all the data in the RVNODDIS

        # Put displacement x, y, z, rx, ry, rz into separate variables and print
        disp_x = data_list[6]
        disp_y = data_list[7]
        disp_z = data_list[8]
        disp_rx = data_list[9]
        disp_ry = data_list[10]
        disp_rz = data_list[11]

        print(f'\nNodal displacement for result case {ires}, node {iinod}:')
        print(f'X  = {disp_x:.2E} m')
        print(f'Y  = {disp_y:.2E} m')
        print(f'Z  = {disp_z:.2E} m')
        print(f'RX = {disp_rx:.2E} rad')
        print(f'RY = {disp_ry:.2E} rad')
        print(f'RZ = {disp_rz:.2E} rad')


if __name__ == "__main__":
    main()
