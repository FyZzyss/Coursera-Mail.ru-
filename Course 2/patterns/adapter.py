class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def _get_objects_in_grid(self, grid, object):
        result = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == object:
                    result.append((j, i))
        return result

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)
        lights = self._get_objects_in_grid(grid, 1)
        obstacles = self._get_objects_in_grid(grid, -1)
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.generate_lights()