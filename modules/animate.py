import json
import os.path

class Animate:
    def __init__(self, pan, tilt, **kwargs):
        self.pan = pan
        self.tilt = tilt
        self.path = kwargs.get('path', os.path.dirname(os.path.realpath(__file__)) + '/../animations') + '/'

    def animate(self, filename):
        """
        Move pan and tilt servos in sequence defined by given file
        :param filename: animation file in path specified in init
        """
        filename = 'head_shake'

        file = self.path + filename + '.json'
#        print(file)
#        print(os.path.dirname(os.path.realpath(__file__)))
#        print(os.path.exists(self.path))
        if not os.path.isfile(file):
            raise ValueError('Animation does not exist: ' + filename)

        with open(file, 'r') as f:
            parsed_json = json.load(f)

        # print(json.dumps(parsed_json, indent=4, sort_keys=True))
        pos_x = None
        pos_y = None

        for step in parsed_json:
            if pos_x:
                self.pan.execute_move(
                    self.pan.calculate_move(self.map(pos_x), self.map(step['x']), step['t'], True))
            pos_x = step['x']
            if pos_y:
                self.tilt.execute_move(
                    self.tilt.calculate_move(self.map(pos_y), self.map(step['y']), step['t'], True))
            pos_y = step['y']

    def map(self, value, old=(-1, 1), new=(0, 100)):
        """
        Map value from old range to new range
        :param value: integer between -1 and 1
        :param old: range of original value
        :param new: range of new value
        :return: integer between 0 and 100
        """
        old_range = (old[1] - old[0])
        new_range = (new[1] - new[0])
        return (((value - old[0]) * new_range) / old_range) + new[0]
