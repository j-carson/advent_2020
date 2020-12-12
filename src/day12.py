from collections import namedtuple
from dataclasses import dataclass, field
import numpy as np

NavIns = namedtuple("NavIns", "code,value")


@dataclass
class MovingThing:
    offset_n: int = 0
    offset_e: int = 0

    def go(self, code, value):
        if code == "N":
            self.offset_n += value
        elif code == "S":
            self.offset_n -= value
        elif code == "E":
            self.offset_e += value
        elif code == "W":
            self.offset_e -= value
        else:
            raise ValueError("unknown compass direction")
            
    def manhattan_distance(self):
        return abs(self.offset_n) + abs(self.offset_e)

    @staticmethod
    def change_heading(heading, direction, turn_degrees):
        """heading is in compass degrees,
        direction R=clockwise, L=counter-clockwise"""

        if direction == "R":
            # right == clockwise
            heading += turn_degrees
        elif direction == "L":
            heading -= turn_degrees

        while heading < 0:
            heading += 360
        while heading > 360:
            heading -= 360

        return heading

    @staticmethod
    def heading_to_dir(heading):
        if heading == 90:
            return "E"
        elif heading == 180:
            return "S"
        elif heading == 270:
            return "W"
        elif heading in (0, 360):
            return "N"
        raise ValueError("heading not on 90 degree axis")



class Waypoint(MovingThing):
    def turn(self, direction, turn_degrees):
        az = np.degrees(np.arctan2(self.offset_n, self.offset_e))

        # convert azimuth (in trig unit circle coords) to compass heading
        heading = 90 - az
        new_heading = self.change_heading(heading, direction, turn_degrees)
        new_az = 90 - new_heading

        r = np.sqrt(self.offset_n ** 2 + self.offset_e ** 2)
        self.offset_n = int(np.round(np.sin(np.radians(new_az)) * r, 0))
        self.offset_e = int(np.round(np.cos(np.radians(new_az)) * r, 0))


@dataclass
class Ship(MovingThing):
    navigation: list = None
    waypoint: Waypoint = None
    heading: int = 90
    debug: bool = False

    def turn(self, code, value):
        self.heading = self.change_heading(self.heading, code, value)

    def execute_q1(self):
        """
        Action N means to move north by the given value.
        Action S means to move south by the given value.
        Action E means to move east by the given value.
        Action W means to move west by the given value.
        Action L means to turn left the given number of degrees.
        Action R means to turn right the given number of degrees.
        Action F means to move forward by the given value in the direction 
                 the ship is currently facing.
                 
        Ship starts facing E
        """
        for ins in self.navigation:
            if ins.code in ("N", "S", "E", "W"):
                self.go(ins.code, ins.value)
            elif ins.code in ("L", "R"):
                self.turn(ins.code, ins.value)
            elif ins.code == "F":
                self.go(self.heading_to_dir(self.heading), ins.value)

    def execute_q2(self):
        """
        Action N means to move the waypoint north by the given value.
        Action S means to move the waypoint south by the given value.
        Action E means to move the waypoint east by the given value.
        Action W means to move the waypoint west by the given value.
        Action L means to rotate the waypoint around the ship left (counter-clockwise) 
                 the given number of degrees.
        Action R means to rotate the waypoint around the ship right (clockwise) 
                 the given number of degrees.
        Action F means to move forward to the waypoint a number of times 
                 equal to the given value.

        The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is 
        relative to the ship; that is, if the ship moves, the waypoint moves with it.
        """
        for ins in self.navigation:
            if ins.code in ("N", "S", "E", "W"):
                self.waypoint.go(ins.code, ins.value)
            elif ins.code in ("L", "R"):
                self.waypoint.turn(ins.code, ins.value)
            elif ins.code == "F":
                self.go("N", self.waypoint.offset_n * ins.value)
                self.go("E", self.waypoint.offset_e * ins.value)
            if self.debug:
                print(
                    f"{ins.code}{ins.value}:"
                    f"\tship E/N: {self.offset_e}/{self.offset_n}"
                    f"\twaypt E/N: {self.waypoint.offset_e}/{self.waypoint.offset_n}"
                )


if __name__ == "__main__":
    test_data = """F10
N3
F7
R90
F11""".splitlines()
    test_nav = [NavIns(d[0], int(d[1:])) for d in test_data]

    with open("navigate.txt") as fp:
        data = fp.read().splitlines()
    nav_ins = [NavIns(d[0], int(d[1:])) for d in data]

    test_ship = Ship(navigation=test_nav)
    test_ship.execute_q1()
    print(f"Q1 Test {test_ship.manhattan_distance()}")

    test_ship = Ship(
        navigation=test_nav, waypoint=Waypoint(offset_e=10, offset_n=1), debug=True
    )
    test_ship.execute_q2()
    print(f"Q2 Test {test_ship.manhattan_distance()}")

    ship = Ship(navigation=nav_ins)
    ship.execute_q1()
    print(f"Q1 Problem {ship.manhattan_distance()}")

    ship = Ship(navigation=nav_ins, waypoint=Waypoint(offset_e=10, offset_n=1))
    ship.execute_q2()
    print(f"Q2 Problem {ship.manhattan_distance()}")
