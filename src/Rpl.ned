// 
//   Simulation model for RPL (Routing Protocol for Low-Power and Lossy Networks)
//  
//   Copyright (C) 2021  Institute of Communication Networks (ComNets),
//                       Hamburg University of Technology (TUHH)
//             (C) 2021  Yevhenii Shudrenko
//  
//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//  
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//  
//   You should have received a copy of the GNU General Public License
//   along with this program.  If not, see <https://www.gnu.org/licenses/>.
//  

package rpl;

import inet.routing.contract.IManetRouting;

module Rpl like IManetRouting
{   
    parameters:
        // Control signals
        @signal[parentUnreachable](type=long);
        
        // Statistics collections
        @signal[dioReceived](type=inet::Dio);
        @signal[daoReceived](type=inet::Dao);
        @signal[disReceived](type=long);
        @signal[rssi](type=double);
     	@signal[isSink](type=bool);
     	@signal[parentChanged](type=long);
     	@signal[rankUpdated](type=long);
     	@signal[parentUnreachable](type=inet::Dio);
     	//@statistic[isSink](title="Node is a sink"; source="isSink"; record=count; interplationmode=none);
        @statistic[dioReceived](title = "DIO packets received"; source="dioReceived"; record=count; interpolationmode=none);
        @statistic[daoReceived](title = "DAO packets received"; source="daoReceived"; record=count; interpolationmode=none);
        @statistic[disReceived](title = "DIS packets received"; source="disReceived"; record=count; interpolationmode=none);
        @statistic[rssi](title = "RSSI of received DIO (dBm)"; source="rssi"; record=vector,mean,min,max; interpolationmode=none);
        @statistic[parentChanged](title = "Preferred parent has changed"; source="parentChanged"; record=count; interpolationmode=none);
        @statistic[rankUpdated](title = "Rank is updated"; source="rankUpdated"; record=vector, count; interpolationmode=none);
        @statistic[parentUnreachable](title = "Preferred parent unreachability detected"; source="parentUnreachable"; record=count; interpolationmode=none);
        
        // properties
        @class("inet::Rpl");
        @display("i=block/routing");

        // context parameters
        string interfaceTableModule = default(absPath("^.interfaceTable"));  // The path to the InterfaceTable module
        string routingTableModule = default(absPath("^.ipv6.routingTable"));
        string networkProtocolModule = default(absPath("^.ipv6.ipv6"));
    	
    	// General parameters
        bool isRoot = default(false);
        bool disabled = default(false);
        bool daoEnabled = default(true);
        bool daoAckEnabled = default(true);
        int numDaoRetransmitAttempts = default(3);
        bool storing = default(true);
        bool poisoning = default(false);
        bool useBackupAsPreferred = default(false);
        bool unreachabilityDetectionEnabled = default(false);
        int minHopRankIncrease = default(1); // required difference in rank to consider switching preffered parent  
        double startDelay = default(0);
        string objectiveFunctionType = default("hopCount");	 // hopCount, ETX, energy, ...
        bool allowDodagSwitching = default(false);
        bool allowDaoForwarding = default(true);
        
        // Utility params (mostly required for specific simulation scenarios, not for general use)
        
        // Manual topology generation
        bool layoutConfigurator = default(false);
        bool branchesLayout = default(false);
        
        // required for ReSA demo use case with seatbelts 
        bool allowJoinAtSink = default(true);
        double joinAtSinkProbability = default(0.5);    
        double joinAtSinkPowerThresh = default(-1);
          
        int numBranches = default(3);
        int numHops = default(1);
        double yAnchor = default(200); // first sink location
        double xAnchor = default(200); // 
        double padY = default(5);
        double padX = default(10);
        double gridColumnsGapMultiplier = default(4); // Determines width of the central 'hallway' in aircraft
        
        bool useWarmup = default(true);
        int numSkipTrickleIntervalUpdates = default(0);
		int connectorColorId = default(0); // index of the connector line color from the color palette vector
		bool drawConnectors = default(true);
		bool showBackupParents = default(false);

		// Optional low-latency mode settings (6TiSCH) 
		bool lowLatencyMode = default(false);
		
		// Optional up-/downlink redundancy (6TiSCH-TRED / 6TiSCH-CLX (down))
		bool downlinkRequired = default(false);
		bool uplinkRequired = default(false);

		// Blackhole/sinkhole attack simulation: forces this node's own rank
		// (and what it advertises in DIOs) to a fixed value instead of the
		// objective-function-computed one, making it artificially attractive
		// as a preferred parent regardless of real link quality/hop count.
		// Combined with dropping of transit (forwarded) data traffic while
		// active. -1 = disabled (normal RPL behaviour).
		int maliciousRank = default(-1);

		// Attack time window (shared by maliciousRank and the wormhole
		// tunnel below). attackStartTime < 0: attack is active from the
		// start of the simulation (t=0). attackEndTime < 0: attack never
		// stops once started.
		double attackStartTime @unit(s) = default(-1s);
		double attackEndTime @unit(s) = default(-1s);

		// Wormhole attack: while the attack window is active, redirect
		// this node's own default (upward) route to go out a private
		// wired PPP tunnel (see wormholeTunnel channel / wormholeEnabled
		// in the network NED) to wormholePeerPath instead of the normal
		// wireless interface. Meant to be combined with maliciousRank so
		// this node's real wireless neighbours are lured into picking it
		// as their preferred parent, then have their upward traffic
		// silently relayed through the tunnel to a node far away in the
		// mesh (which then forwards it on normally from there) - a false
		// "shortcut" that looks attractive (low advertised rank) but
		// concentrates traffic through one low-bandwidth private link.
		bool wormholeTunnelEndpoint = default(false);
		// Absolute module path (e.g. "RplNetworkGrid35.host[20]") of the
		// node on the other end of the wormhole tunnel.
		string wormholePeerPath = default("");

    gates:
        input ipIn;
        output ipOut;
        inout ttModule; // trickle timer interface
}

