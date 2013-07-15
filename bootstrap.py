import naoutil.naoenv as naoenv
import naoutil.memory as memory
import fluentnao.nao as nao
from datetime import datetime
from naoutil import broker

# broker (must come first)
broker.Broker('bootstrapBroker', naoIp="nao.local", naoPort=9559)

# nao env
env = naoenv.make_environment(None) #using broker don't need ->, ipaddr="nao.local", port=9559)

# fluent nao
nao = nao.Nao(env, None)