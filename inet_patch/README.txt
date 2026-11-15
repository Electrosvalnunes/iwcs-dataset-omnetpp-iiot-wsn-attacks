Patch applied to INET 4.2.10 (inet-4.2.10-src.tgz) for this campaign.
Generated with: git diff a3bcad9 ambiente-revisao-v1   (in the INET repository)
  a3bcad9 = unmodified INET 4.2.10 tree before the patch
  ambiente-revisao-v1 = 62282fdcc99868db3ba723c4597559eb2c5fb7f2
Apply from the INET root:  patch -p1 < inet-4.2.10_rpl_patch_ambiente-revisao-v1.diff
The same files are also provided, already patched, under ../inet/ (RPL project layout).
Build: OMNeT++ 5.7.1, INET 4.2.10 in release mode with the Visualization feature ON
(every .ned uses IntegratedCanvasVisualizer); the RPL project needs MSGC:=$(MSGC) --msg6.
Exact binaries, hashes and command line: ../campaign_v2/manifest.txt.
