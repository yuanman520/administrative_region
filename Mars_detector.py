#!/usr/bin/env python3


class Detector:
    def __init__(self, x_axis, y_axis, direction):
        """

        :param x_axis: int
        :param y_axis: int
        :param direction: in ('N', 'E', 'S', 'W')
        """
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.direction = direction

    def move(self, max_x, max_y):
        if self.direction == 'N':
            self.y_axis += 1
        elif self.direction == 'E':
            self.x_axis += 1
        elif self.direction == 'S':
            self.y_axis -= 1
        else:
            self.x_axis -= 1

        status = False if self.x_axis > max_x or self.y_axis > max_y else True
        return status

    def rotate(self, rotate_direction):
        if self.direction == 'N':
            self.direction = 'W' if rotate_direction == 'L' else 'E'
        elif self.direction == 'E':
            self.direction = 'N' if rotate_direction == 'L' else 'S'
        elif self.direction == 'S':
            self.direction = 'E' if rotate_direction == 'L' else 'W'
        else:
            self.direction = 'S' if rotate_direction == 'L' else 'N'

    @property
    def location(self):
        return '{} {} {}'.format(self.x_axis, self.y_axis, self.direction)


def input_instructs():
    lines = []
    data = input('请输入指令，最后以"end"结束\n').strip()
    while data != 'end':
        if data:
            lines.append(data)
        data = input().strip()

    if lines:
        records = []
        max_axis = lines[0]
        try:
            x, y = max_axis.split(' ')
            x = int(x)
            y = int(y)
        except (TypeError, ValueError):
            print('输入的右上角坐标有误')
            return

        detector_data = lines[1:]
        if not detector_data:
            print('未输入探测器数据信息')
            return
        for k, v in enumerate(detector_data):
            if k % 2 == 0:
                location_list = v.split(' ')
                try:
                    rotation_list = list(detector_data[k + 1])
                except IndexError:
                    print('每个探测器需要输入两行信息')
                    return

                if len(location_list) == 3:
                    x_axis, y_axis, direction = location_list
                    if x_axis.isdigit() and y_axis.isdigit() and 0 <= int(x_axis) <= x and 0 <= int(y_axis) <= y and \
                            direction in ['N', 'E', 'S', 'W']:
                        detector = Detector(int(x_axis), int(y_axis), direction)
                    else:
                        print('输入的探测器位置信息不合理，应该由两个正整数和一个区分方向的字母组成')
                        return
                else:
                    print('输入的探测器位置信息有误，示例：0 0 N')
                    return

                for item in rotation_list:
                    if item == 'M':
                        status = detector.move(x, y)
                        if not status:
                            print('移动超出网状最大范围，指令错误')
                            return
                    elif item in ['L', 'R']:
                        detector.rotate(item)
                    else:
                        print('输入的移动位置信息有误')
                        return

                records.append(detector.location)
        print('\n'.join(records))
    else:
        print('输入指令有误')


if __name__ == '__main__':
    input_instructs()
