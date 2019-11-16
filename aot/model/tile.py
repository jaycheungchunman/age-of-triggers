from aot.model.enums import *


class Tile:
    """Tile class provide basic information about one tile from
        map tiles. You are able to manipulate with basic paramaters
        as Type, Elevation or Unknown. It has also X and Y paramters,
        but these are for internal purpose only.

    Attributes:
        row (int, readonly): row position
        col (int, readonly): column position
        x (int, readonly): x position
        y (int, readonly): y position
        type (int): type of terrain
        elevation (int): terrain elevation

    Note:
        for all terrain types, check terrain enums
    """

    @property
    def row(self):
        return self.__r

    @property
    def col(self):
        return self.__c

    @property
    def x(self):
        return self.__c

    @property
    def y(self):
        return self.__r

    def __init__(self, row, col, type=0, elevation=0, unknown=0,unknown1 = 255,unknown2=255, layer_type=255, is_layering=255):
        """create Tile

        Args:
            row (int): X position
            col (int): Y position
            type (int, optional): terrain type, 0
            elevation (int, optional): elevation, 0
            unknown (int, optional): 0
        """
        self.type = type
        self.elevation = elevation
        self.unknown = unknown
        self.unknown1 = unknown1
        self.unknown2 = unknown2
        self.__r = row
        self.__c = col
        self.layer_type = layer_type
        self.is_layering = is_layering

    def __repr__(self):
        name = "Tile:\n"
        info = "\tX:{} Y:{}\n".format(self.__c, self.__r)
        info2 = "\televation: {}\tunknown: {}\n".format(
            self.elevation, self.unknown)
        info3 = "\ttype: {}\n".format(self.type)
        is_layering = "\tis_layering: {} \n".format("True" if self.is_layering==0 else "False")
        str = name + info + info2 + info3 + is_layering

        if self.is_layering == 0:
            layer_type = "\tlayer_type: {}\n".format(self.layer_type)
            str+=layer_type
        return str
    def toJSON(self):
        """return JSON"""
        data = dict()
        data['type'] = self.type
        data['elevation'] = self.elevation
        return data

    def position(self):
        """position of tile in map

        Return:
            (tuple): X and Y
        """
        return (self.__c, self.__r)

    def clear(self):
        """set terrain type to default 0"""
        self.type = 1

    def flat(self):
        """set tile elevation to 1"""
        self.elevation = 1

    def up(self, increase=1):
        """increase elevation

            Args:
                increase (int, optional): how much
        """
        self.elevation += increase

    def down(self, decrease=1):
        """decrease elevation

            Args:
                decrease (int, optional): how much
        """
        self.elevation -= decrease
