import unittest
from unittest.mock import patch, mock_open

from shadow.polyedr import Polyedr


class TestPolyedr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """200.0	45.0	45.0	30.0
8	4	16
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5"""
        fake_file_path = 'data/holey_box.geom'
        new_fake_file_content = """200.0	45.0	45.0	30.0
8	6	24
-1.0	-1.0	1.1
-1.0	1.0	1.1
1.0	1.0	1.1
1.0	-1.0	1.1
-1.0	-1.0	-1.1
-1.0	1.0	-1.1
1.0	1.0	-1.1
1.0	-1.0	-1.1
4	1    2    3    4
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5
4	8    7    6    5"""
        new_fake_file_path = 'data/holey_cube.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr1 = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=new_fake_file_content)) as _file:
            self.polyedr2 = Polyedr(new_fake_file_path)
            _file.assert_called_once_with(new_fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr1.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr1.facets), 4)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr1.edges), 16)

    # Сумма площадей «хороших» граней
    def test_sum_area01(self):
        self.assertEqual(self.polyedr1.sum_area(), 0.0)

    def test_sum_area02(self):
        self.assertAlmostEqual(self.polyedr2.sum_area(), 8.0)
