import queue
from cherrypy.process import plugins

class PooledDatabaseConnections(plugins.SimplePlugin):

    def __init__(self, bus, connection_factory=None):
        super().__init__(bus)
        self.queue = queue.Queue(maxsize=10)
        if connection_factory is not None:
            self.connection_factory = connection_factory

    def start(self):
        self.bus.log('Starting up pooled database plugin')
        self.bus.subscribe('get-database', self.get_database)
        self.bus.subscribe('put-database', self.put_database)

    def stop(self):
        self.bus.log('Shutting down pooled database plugin')
        self.bus.unsubscribe('get-database', self.get_database)
        self.bus.unsubscribe('put-database', self.put_database)

    def get_database(self):
        try:
            return self.queue.get(block=False)
        except queue.Empty:
            conn = self.connection_factory()
            return conn

    def put_database(self, conn):
        try:
            self.queue.put(conn, block=False)
        except queue.Full:
            conn.close()
