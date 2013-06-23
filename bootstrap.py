import naoutil.naoenv as naoenv
import fluentnao.nao as nao
env = naoenv.make_environment(None, ipaddr="nao.local", port=9559)
nao = nao.Nao(env, None)
