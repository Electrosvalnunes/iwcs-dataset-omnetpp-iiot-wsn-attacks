import inet.common.scenario.ScenarioManager;
import inet.physicallayer.contract.packetlevel.IRadioMedium;
import inet.visualizer.contract.IIntegratedVisualizer;
import inet.networklayer.configurator.ipv6.Ipv6FlatNetworkConfigurator;
import ned.DatarateChannel;
import rpl.RplRouter;

//
// Topologia irmã da RplNetworkGrid35 (mesma abordagem: grade quadrada,
// sink no centro, RplRouter em todos os nós), só que numa grade 7x7 (49
// posições) em vez de 6x6 (36 posições) — 48 sensores + 1 sink central.
//

//
// Canal cabeado privado usado pelo ataque Wormhole (Config
// Grid48_Wormhole_Host24_Host44), mesmos parâmetros já validados e
// calibrados na RplNetworkGrid35 (canal wormholeTunnel de lá): túnel
// físico ponto-a-ponto ligando dois nós distantes na malha sem fio,
// simulando os dois nós comprometidos se passando por vizinhos próximos
// um do outro. Só existe na topologia quando wormholeEnabled=true.
channel wormholeTunnel48 extends DatarateChannel
{
    delay = 300ms;
    datarate = 20kbps;
    per = 0.15;
}

network RplNetworkGrid48
{
    parameters:
        // 48 sensores em grade 7x7 (49 posições, uma reservada para o sink central)
        int numNodes = default(48);

        // Um único sink, posicionado no centro da grade
        int numSinks = default(1);

        // Liga o túnel cabeado privado do ataque Wormhole entre
        // host[24] e host[44] (ver canal wormholeTunnel acima). Fica
        // desligado por padrão — só o Config Grid48_Wormhole_Host24_Host44
        // liga isso via **.wormholeEnabled = true no .ini, junto com
        // **.host[24].numPppInterfaces = 1 e **.host[44].numPppInterfaces = 1.
        bool wormholeEnabled = default(false);

        @display("bgb=360,360");

    submodules:
        visualizer: <default("IntegratedCanvasVisualizer")> like IIntegratedVisualizer if hasVisualizer() {
            @display("p=610,70");
            networkRouteVisualizer.displayRoutes = true;
        }

        radioMedium: <> like IRadioMedium {
            @display("p=610,150;is=s");
        }

        configurator: Ipv6FlatNetworkConfigurator {
            @display("p=610,230;is=s");
        }

        scenarioManager: ScenarioManager {
            @display("p=610,310;is=s");
        }

        // Sink / raiz do RPL, posicionado no centro da grade (ver .ini)
        sink[numSinks]: RplRouter {
            @display("i=misc/sensor;p=350,350;is=s");
        }

        // Sensores legítimos dispostos em grade 7x7 (posições reais no .ini)
        host[numNodes]: RplRouter {
            @display("i=misc/sensor2;p=100,100");
        }

    connections allowunconnected:
        // Rede sem fio: não há conexões cabeadas, exceto o túnel privado
        // do ataque Wormhole (condicional, ver wormholeEnabled acima).
        // A comunicação normal ocorre pelo rádio IEEE 802.15.4 e pelo RPL/IPv6.
        host[24].pppg[0] <--> wormholeTunnel48 <--> host[44].pppg[0] if wormholeEnabled;
}
