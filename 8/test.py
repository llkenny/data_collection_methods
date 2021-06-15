from open_data import GosUslugi

gs = GosUslugi()
gs.fetch()
gs.unzip()
gs.convert()

gs.read()
