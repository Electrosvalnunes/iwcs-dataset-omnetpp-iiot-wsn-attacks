import inet.common.scenario.ScenarioManager;
import inet.physicallayer.contract.packetlevel.IRadioMedium;
import inet.visualizer.contract.IIntegratedVisualizer;
import inet.networklayer.configurator.ipv6.Ipv6FlatNetworkConfigurator;
import rpl.RplRouter;

network RplNetworkmaio
{
    parameters:
        // Número de sensores legítimos. O valor é sobrescrito no omnetpp.ini
        // pelas configurações Grid_36, Grid_49, Grid_64 e Grid_100.
        int numNodes = default(64);

        // Número de nós atacantes externos. No dataset, o ataque pode ser
        // representado por um atacante dedicado ou por um host comprometido.
        int numAttack = default(1);

        // Número de sinks/raízes RPL.
        int numSinks = default(1);

        @display("bgb=700,700");

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

        // Sink / raiz do RPL. Recebe o tráfego UDP dos sensores.
        sink[numSinks]: RplRouter {
            @display("i=misc/sensor;p=350,350;is=s");
        }

        // Sensores legítimos em grade. A posição real é definida no .ini
        // por StationaryMobility, de acordo com cada topologia.
        host[numNodes]: RplRouter {
            @display("i=misc/sensor2;p=100,100");
        }

        // Nó atacante dedicado, agora ATIVO. No seu .ned antigo esse bloco
        // estava comentado, o que impedia o cenário Flooding de funcionar.
        Attack[numAttack]: RplRouter {
            @display("i=block/process_s;p=80,620");
        }

    connections allowunconnected:
        // Rede sem fio: não há conexões cabeadas.
        // A comunicação ocorre pelo rádio IEEE 802.15.4 e pelo RPL/IPv6.
}