import inet.common.scenario.ScenarioManager;
import inet.physicallayer.contract.packetlevel.IRadioMedium;
import inet.visualizer.contract.IIntegratedVisualizer;
import inet.networklayer.configurator.ipv6.Ipv6FlatNetworkConfigurator;
import ned.DatarateChannel;
import rpl.RplRouter;

//
// Topologia irmã da RplNetworkGrid35/RplNetworkGrid48 (mesma abordagem:
// grade quadrada, sink no centro, RplRouter em todos os nós), agora numa
// grade 8x8 (64 posições) — 63 sensores + 1 sink central. Grade PAR (8x8,
// diferente das 6x6/7x7 anteriores que tinham centro exato): o sink fica
// numa das 4 células mais centrais (160m,160m), não no centro geométrico
// perfeito (180m,180m, que cai entre nós).
//

//
// Canal cabeado privado do ataque Wormhole (Config
// Grid63_Wormhole_Host27_Host58), mesmos parâmetros já validados e
// calibrados na RplNetworkGrid35/RplNetworkGrid48.
channel wormholeTunnel63 extends DatarateChannel
{
    delay = 300ms;
    // Banda reduzida da GRID35/GRID48 (20kbps): aumentar só o "per"
    // (0.15->0.25) não moveu o PDR agregado quase nada (saturado) — a
    // sub-árvore capturada é proporcionalmente menor aqui que na GRID48
    // (~26% vs ~29%, tamanho absoluto parece ter um teto fixo, ~16 nós,
    // quase independente do tamanho da rede), então pra manter o
    // impacto agregado maior que a GRID48 como pedido, reduzida a banda
    // pra criar gargalo real de fila no túnel, não só erro por pacote.
    datarate = 10kbps;
    per = 0.25;
}

network RplNetworkGrid63
{
    parameters:
        // 63 sensores em grade 8x8 (64 posições, uma reservada para o sink)
        int numNodes = default(63);

        // Um único sink
        int numSinks = default(1);

        // Liga o túnel cabeado privado do ataque Wormhole entre
        // host[27] e host[58] (ver canal wormholeTunnel63 acima). Fica
        // desligado por padrão — só o Config Grid63_Wormhole_Host27_Host58
        // liga isso via **.wormholeEnabled = true no .ini.
        bool wormholeEnabled = default(false);

        // Segundo túnel independente (host[26] <-> host[3]) — tentativa
        // de dobrar a área de atração do ataque Wormhole nesta topologia,
        // já que um único túnel capturava uma sub-árvore proporcionalmente
        // menor que a GRID48 (teto físico de ~16 nós). Flag separada da
        // primeira pra poder testar 1 ou 2 túneis independentemente.
        bool wormholeEnabled2 = default(false);

        @display("bgb=400,400");

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

        // Sensores legítimos dispostos em grade 8x8 (posições reais no .ini)
        host[numNodes]: RplRouter {
            @display("i=misc/sensor2;p=100,100");
        }

    connections allowunconnected:
        // Rede sem fio: não há conexões cabeadas, exceto o túnel privado
        // do ataque Wormhole (condicional, ver wormholeEnabled acima).
        host[27].pppg[0] <--> wormholeTunnel63 <--> host[58].pppg[0] if wormholeEnabled;
        host[26].pppg[0] <--> wormholeTunnel63 <--> host[3].pppg[0] if wormholeEnabled2;
}
