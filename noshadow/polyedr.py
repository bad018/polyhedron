from math import pi
from common.r3 import R3
from common.tk_drawer import TkDrawer


class Edge:
    """ Ребро полиэдра """
    # Параметры конструктора: начало и конец ребра (точки в R3)

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin


class Facet:
    """ Грань полиэдра """
    # Параметры конструктора: список вершин

    def __init__(self, vertexes):
        self.vertexes = vertexes
        self._area = 0.0

    # Центр грани
    def center(self):
        return sum(self.vertexes, R3(0.0, 0.0, 0.0)) * \
            (1.0 / len(self.vertexes))

    # «Хорошая» ли грань?
    # У «хорошей» грани центр и все вершины — «хорошие» точки
    def is_good_facet(self):
        center = self.center()
        if center.is_good():
            for vertex in self.vertexes:
                if not vertex.is_good():
                    return False
            return True
        else:
            return False

    # Площадь «хорошей» грани
    def area(self):
        if not self.is_good_facet():
            return 0.0
        else:
            for i in range(len(self.vertexes) - 1):
                self._area += abs(R3.area(self.vertexes[i],
                                          self.vertexes[i + 1],
                                          self.center()))
            self._area += abs(R3.area(self.vertexes[0],
                                      self.vertexes[len(self.vertexes) - 1],
                                      self.center()))
        return self._area

    # Сумма площадей «хороших» граней равна площади текущей грани
    def sum_area(self):
        return self.area()


class Polyedr:
    """ Полиэдр """
    # Параметры конструктора: файл, задающий полиэдр

    def __init__(self, file):

        # списки вершин, рёбер и граней полиэдра
        self.vertexes, self.edges, self.facets = [], [], []
        # изначально сумма площадей «хороших» граней равна нулю
        self._sum_area = 0.0

        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    c = float(buf.pop(0))
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    self.vertexes.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                else:
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани
                    vertexes = [self.vertexes[int(n) - 1] for n in buf]
                    facet = Facet(vertexes)
                    # добавляем к сумме площадей «хороших» граней
                    # площадь этой грани
                    self._sum_area += facet.area()
                    # задание рёбер грани
                    for n in range(size):
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes))

    # Сумма площадей граней,
    # центр и все вершины которой - «хорошие» точки
    def sum_area(self):
        return self._sum_area

    # Метод изображения полиэдра
    def draw(self, tk):
        tk.clean()
        for e in self.edges:
            tk.draw_line(e.beg, e.fin)

