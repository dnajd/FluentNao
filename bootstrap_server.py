import atexit
import os
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from naoutil import broker

os.environ['FLUENTNAO_BRIDGE'] = '1'

naoIp = os.environ["NAO_IP"]
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)
env = naoenv.make_environment(None)
nao = nao.Nao(env, None)

atexit.register(nao.shutdown)

import server
server.start(nao, block=True)
