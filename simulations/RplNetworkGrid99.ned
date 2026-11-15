import inet.common.scenario.ScenarioManager;
import inet.physicallayer.contract.packetlevel.IRadioMedium;
import inet.visualizer.contract.IIntegratedVisualizer;
import inet.networklayer.configurator.ipv6.Ipv6FlatNetworkConfigurator;
import ned.DatarateChannel;
import rpl.RplRouter;

//
// Topologia irmã da RplNetworkGrid35/48/63 (mesma abordagem: grade
// quadrada, sink no centro, RplRouter em todos os nós), agora numa
// grade 10x10 (100 posições) — 99 sensores + 1 sink central. Grade PAR
// (igual à 8x8 da GRID63): o sink fica numa das 4 células mais centrais
// (200m,200m), não no centro geométrico perfeito (220m,220m).
//

//
// Canal cabeado privado do ataque Wormhole, mesmos parâmetros já
// validados na RplNetworkGrid35/48/63.
channel wormholeTunnel99 extends DatarateChannel
{
    delay = 300ms;
    datarate = 20kbps;
    per = 0.15;
}

network RplNetworkGrid99
{
    parameters:
        // 99 sensores em grade 10x10 (100 posições, uma reservada para o sink)
        int numNodes = default(99);

        // Um único sink
        int numSinks = default(1);

        // Liga os 4 túneis independentes do ataque Wormhole (Config
        // Grid99_Wormhole_Quadruplo) — cada um dos 4 vizinhos diretos
        // do sink pareado com um nó distante do lado oposto da grade.
        // Aprendizado da GRID63: um único túnel captura uma sub-árvore
        // de tamanho absoluto praticamente fixo (~14-16 nós,
        // independente do tamanho da rede), então pra ter impacto
        // agregado maior numa rede bem maior como esta, direto com
        // múltiplos túneis desde o início.
        bool wormholeEnabled = default(false);

        @display("bgb=440,440");

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

        // Sink / raiz do RPL (ver .ini para posição)
        sink[numSinks]: RplRouter {
            @display("i=misc/sensor;p=350,350;is=s");
        }

        // Sensores legítimos dispostos em grade 10x10 (posições reais no .ini)
        host[numNodes]: RplRouter {
            @display("i=misc/sensor2;p=100,100");
        }

    connections allowunconnected:
        // Rede sem fio: sem conexões cabeadas exceto os 4 túneis
        // privados do ataque Wormhole (condicional, ver wormholeEnabled
        // acima). Cada vizinho direto do sink (N/S/E/W) pareado com o
        // nó distante do lado oposto da grade.
        host[53].pppg[0] <--> wormholeTunnel99 <--> host[4].pppg[0] if wormholeEnabled;   // S <-> N-far
        host[44].pppg[0] <--> wormholeTunnel99 <--> host[40].pppg[0] if wormholeEnabled;  // E <-> W-far
        host[34].pppg[0] <--> wormholeTunnel99 <--> host[93].pppg[0] if wormholeEnabled;  // N <-> S-far
        host[43].pppg[0] <--> wormholeTunnel99 <--> host[48].pppg[0] if wormholeEnabled;  // W <-> E-far
}
