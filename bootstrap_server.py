import os
import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from naoutil import broker

naoIp = os.environ["NAO_IP"]
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)
env = naoenv.make_environment(None)
nao = nao.Nao(env, None)

import server
server.start(nao, block=True)
