
class secp256k1:
    def __init__(self):
        # secp256k1
        self.___a = 0
        self.___b = 7
        # p hex = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.___mod = 115792089237316195423570985008687907853269984665640564039457584007908834671663
        # x hex = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        # y hex = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        self.___base = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
                        32670510020758816978083085130507043184471273380659243275938904335757337482424)
        # n hex = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        self.___n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

    @staticmethod
    def ___is_equal_to(pointA: tuple, pointB: tuple) -> bool:
        return pointA[0] == pointB[0] and pointA[1] == pointB[1]

    def ___isOnCurve(self, point: tuple) -> bool:
        # if y ** 2 mod p = x **3 + ax + b mod p
        if (point[1] ** 2) % self.___mod == ((point[0] ** 3) + (self.___a * point[0]) + self.___b) % self.___mod:
            return True
        else:
            print('Point:')
            print(point)
            print('is not on curve')
            return False

    def ___get_inverse(self, n):
        return pow(n, -1, self.___mod)

    def ___getPointsInverse(self, _p: tuple) -> tuple:
        _y = (_p[1] * -1) % self.___mod
        p_1 = (_p[0], _y)
        return p_1

    def ___add(self, pointA: tuple, pointB: tuple) -> tuple:
        if self.___is_equal_to(pointA, pointB):  # is multiple
            # a = 0
            slope = ((3 * pointA[0] ** 2) + self.___a) * self.___get_inverse(n=(2 * pointA[1])) % self.___mod
        else:  # A is base B is poit
            slope = (pointB[1] - pointA[1]) * self.___get_inverse(n=pointB[0] - pointA[0]) % self.___mod

        x = (slope ** 2 - pointA[0] - pointB[0]) % self.___mod
        y = (slope * (pointA[0] - x) - pointA[1]) % self.___mod
        newPoint = (x, y)
        return newPoint  # Point(x, y, self.curve_config)

    def ___multiply(self, pointA: tuple, base: tuple, repeat: int) -> tuple:
        point = self.___add(pointA, base)
        for i in range(repeat - 2):
            point = self.___add(point, base)
        return point

    def ___scalar_multiply(self, point: tuple, repeat: int) -> tuple:
        point_double = point
        offset = 1
        previous_points = []
        while offset < repeat:
            previous_points.append((offset, point_double))
            if 2 * offset <= repeat:
                point_double = self.___add(point_double, point_double)
                offset = 2 * offset
            else:
                next_offset = 1
                next_point = None
                for (previous_offset, previous_point) in previous_points:
                    if previous_offset + offset <= repeat:
                        if previous_point[0] != point_double[0]:
                            next_offset = previous_offset
                            next_point = previous_point
                point_double = self.___add(point_double, next_point)
                offset = offset + next_offset

        return point_double

    def getPublicKeyCoordinate(self, privateKey: int) -> tuple:
        pk = self.___scalar_multiply(point=self.___base, repeat=privateKey)
        if self.___isOnCurve(self.___base) and self.___isOnCurve(pk):
            return pk
        else:
            return ()
