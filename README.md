# iwcs-dataset-omnetpp-iiot-wsn-attacks
Curated OMNeT++/INET simulation dataset for cyberattack analysis in IIoT wireless sensor networks.

# IWCS-Dataset: OMNeT++/INET Dataset for Cyberattack Analysis in IIoT Wireless Sensor Networks

This repository contains the IWCS-Dataset, a curated simulation dataset generated with OMNeT++/INET for cyberattack analysis in Industrial Internet of Things wireless sensor networks.

## Overview

The dataset was generated using OMNeT++ 5.7.1 and INET 4.2.1, with IEEE 802.15.4, IPv6/6LoWPAN, and RPL in storing mode.

The dataset includes five scenarios:

- Normal
- Flooding
- Blackhole
- Wormhole
- Manipulated Backoff

The final curated dataset contains:

- 20,331 records
- 16 attributes
- 4 grid topologies: Grid_36, Grid_49, Grid_64, and Grid_100
- Performance, routing, link-quality, and energy metrics

## Repository Structure

```text
dataset/        Final curated CSV dataset
simulation/     OMNeT++/INET .ini and .ned files
scripts/        Extraction, cleaning, validation, and figure-generation scripts
metadata/       Data dictionary, quality report, metadata, and raw-file manifest
raw-samples/    Representative .sca, .vec, and .vci raw samples
figures/        Figures used in the article
paper/          LaTeX manuscript files
