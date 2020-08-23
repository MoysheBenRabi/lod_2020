import storm
from web.network import Network


class Tagger(storm.BasicBolt):
    # There's nothing to initialize here,
    # since this is just a split and emit
    # Initialize this instance
    def initialize(self, conf, context):
        self._conf = conf
        self._context = context
        self.nw = Network()
        self.nw.init()
        storm.logInfo("Tager bolt instance starting...")

    def process(self, tup):
        pred = self.nw.predict(tup.values[0])
        storm.emit([pred[1]])

# Start the bolt when it's invoked


Tagger().run()

