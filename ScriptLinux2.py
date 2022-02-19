from os import system as s

apti = "apt install -y "
Ans = "null"
User = []
Users = ""

s("cd /")
s("cd LinuxServices/")

while (Ans != "s"):
    s("clear")
    ComProxy = "null"
    IpMaquina = input("Introduzir ip da maquina: ")
    while (ComProxy != "s" and ComProxy != "n"):
        s("clear")
        ComProxy = input("Está a usar proxy?       s/n: ")
    if ComProxy == "s":
        Proxy = input("Introduzir proxy (Exemplo: 172.16.10.251:8080): ")
    s("clear")
    DefGateway = input("Introduzir ip Default Gateway: ")
    s("clear")
    Dns = input("Introduzir ip DNS: ")
    s("clear")
    Dominio = input("Introduzir nome Dominio: ")
    s("clear")
    Password = input("Introduzir a palavra pass geral (para tudo): ")
    s("clear")
    Range = input("Introduzir Range de ip's  \n  Exemplo: <192.168.50.5 192.168.50.35>: ")
    s("clear")
    NomeMaquina = input("Introduzir Nome da maquina (root@<nome_aqui>): ")
    s("clear")
    Nusers = int(input("Introduza o numero de utilizadores: "))
    s("clear")
    for i in range(Nusers):
        User.append(input("Coloque o nome do " + str(i+1) + " User: "))
        s("clear")

    print("IP da maquina: " + IpMaquina)
    if ComProxy == "s":
        print("Proxy: " + Proxy)
    else:
        print("Sem Proxy")
    print("Default Gateway: " + DefGateway)
    print("DNS: " + Dns)
    print("Dominio: " + Dominio)
    print("Password: " + Password)
    print("Range: " + Range)
    print("Nome da maquina: " + NomeMaquina)
    for i in range(Nusers):
        if i != Nusers-1:
            Users = Users + User[i] + ", "
        else:
            Users += User[i]
    print("Users: " + Users)
    print()
    print("Esta informacao está correta?      s/n")
    Ans = input()

s("ip link set enp0s3 up")
s("ip link set enp0s8 down")
s("apt update && apt upgrade -y")
for i in ["asterisk"]: #services to install
    s(apti + i)

for i in range(Nusers):
    s('echo " " >> /etc/asterisk/sip.conf')
    s('echo "[' + User[i] + ']" >> /etc/asterisk/sip.conf')
    s('echo "type=friend" >> /etc/asterisk/sip.conf')
    s('echo "port=5060" >> /etc/asterisk/sip.conf')
    s('echo "nat=yes" >> /etc/asterisk/sip.conf')
    s('echo "qualify=yes" >> /etc/asterisk/sip.conf')
    RegContext = str(i+1)
    RegContext = RegContext.zfill(3)
    s('echo "regcontext=' + RegContext + '" >> /etc/asterisk/sip.conf')
    s('echo "context=from-internal" >> /etc/asterisk/sip.conf')

for i in range(Nusers):
    s('echo " " >> /etc/asterisk/users.conf')
    s('echo "[' + User[i] + ']" >> /etc/asterisk/users.conf')
    s('echo "full name = ' + User[i] + '" >> /etc/asterisk/users.conf')
    s('echo "hassip = yes" >> /etc/asterisk/users.conf')
    s('echo "secret = ' + Password + '" >> /etc/asterisk/users.conf')
    s('echo "context = from-internal" >> /etc/asterisk/users.conf')
    s('echo "host = dynamic" >> /etc/asterisk/users.conf')

s('echo " " >> /etc/asterisk/extensions.conf')
s('echo "[from-internal]" >> /etc/asterisk/extensions.conf')
for i in range(Nusers):
    RegContext = str(i+1)
    RegContext = RegContext.zfill(3)
    s('echo "exten=>' + RegContext + ',1,Dial(SIP,' + User[i] + ',10)" >> /etc/asterisk/extensions.conf')
s('echo " " >> /etc/asterisk/extensions.conf')
All = "exten=>all,1,Dial("
for i in range(Nusers):
    if i == Nusers-1:
        All = All + "SIP/" + User[i] + ",10)"
    else:
        All = All + "SIP/" + User[i] + "&"
s('echo "' + All + '" >> /etc/asterisk/extensions.conf')
s("service asterisk restart")


s("ip link set enp0s3 down")
s("ip link set enp0s8 up")



