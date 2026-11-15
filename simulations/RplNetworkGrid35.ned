import inet.common.scenario.ScenarioManager;
import inet.physicallayer.contract.packetlevel.IRadioMedium;
import inet.visualizer.contract.IIntegratedVisualizer;
import inet.networklayer.configurator.ipv6.Ipv6FlatNetworkConfigurator;
import ned.DatarateChannel;
import rpl.RplRouter;

//
// Canal cabeado privado usado pelo ataque Wormhole (Config
// Grid35_Wormhole_Host20_Host0): conecta dois nós distantes na malha sem
// fio via um link ponto-a-ponto "fora de banda", simulando o túnel físico
// que os dois nós comprometidos usam para se passar por vizinhos próximos
// um do outro. Só é usado quando host[20].pppg[0]/host[0].pppg[0] estão
// conectados (ver "connections" abaixo) — em qualquer outro cenário
// (Normal/Blackhole/Flooding) essas portas ficam livres/não conectadas e
// esse canal simplesmente não existe na topologia.
//
// Taxa deliberadamente BAIXA (100kbps, abaixo dos 250kbps do rádio
// 802.15.4): mesmo sendo um "atalho", o túnel vira um gargalo real quando
// várias vítimas distantes começam a rotear por ele ao mesmo tempo —
// congestionamento de fila no link cabeado, não só no rádio.
//
// Delay ALTO E DELIBERADO (300ms, ~60x mais que um salto normal de rádio
// ~5ms): representa o atacante interceptando/inspecionando o tráfego
// (MITM) antes de repassar pelo túnel — o comportamento clássico de um
// wormhole malicioso, não um atalho benigno. Isso faz o "atalho" de rank
// (poucos saltos aparentes) contradizer o delay real (alto), o que por si
// só é um sinal de detecção clássico de wormhole na literatura.
channel wormholeTunnel extends DatarateChannel
{
    delay = 300ms;
    datarate = 20kbps;
    // Taxa de erro de pacote: o link privado do atacante não é perfeito
    // (interferência, hardware improvisado) — parte do tráfego desviado
    // simplesmente se perde no túnel. Isso, combinado com a banda baixa,
    // é a causa real da queda de PDR nos nós afetados (não é canal de
    // rádio saturado feito no flooding, é o próprio túnel privado sendo
    // não confiável e estreito).
    per = 0.15;
}

network RplNetworkGrid35
{
    parameters:
        // 35 sensores em grade 6x6 (36 posições, uma reservada para o sink central)
        int numNodes = default(35);

        // Um único sink, posicionado no centro da grade
        int numSinks = default(1);

        // Liga o túnel cabeado privado do ataque Wormhole entre
        // host[20] e host[0] (ver canal wormholeTunnel acima). Fica
        // desligado por padrão — só o Config Grid35_Wormhole_Host20_Host0
        // liga isso via **.wormholeEnabled = true no .ini, junto com
        // **.host[20].numPppInterfaces = 1 e **.host[0].numPppInterfaces = 1
        // (sem isso as portas pppg[0] nem existem nesses nós).
        bool wormholeEnabled = default(false);

        @display("bgb=320,320");

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

        // Sensores legítimos dispostos em grade 6x6 (posições reais no .ini)
        host[numNodes]: RplRouter {
            @display("i=misc/sensor2;p=100,100");
        }

    connections allowunconnected:
        // Rede sem fio: não há conexões cabeadas, exceto o túnel privado
        // do ataque Wormhole (condicional, ver wormholeEnabled acima).
        // A comunicação normal ocorre pelo rádio IEEE 802.15.4 e pelo RPL/IPv6.
        host[20].pppg[0] <--> wormholeTunnel <--> host[3].pppg[0] if wormholeEnabled;
}
