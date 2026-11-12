2026-09-06 <br>

Phase 001 <br>

Interests: <br>
- 5 Computational Imaging and Optics + Software <br>
- 8 Hardware, Architecture and Embedded Systems <br>
- 9 Photonics & Quantum (Software/Simulation angle) <br>

Who is the end user for the final deliverable prototype? <br>
- Hobbyist (low risk, recreational use) <br>
- Scientific community (moderate risk, they understand what goes on in the background and concepts) <br>
- Government (high risk, safeguarding important information) <br>

Key points for proposal: <br>
- Identification of the problem <br>
- Why it matters <br>
- What exists today (competition) <br>
- What is the final deliverable for 12 weeks from now <br>
- What decisons do the end users make with the deliverable
- What does a wrong answer cost
- What are the constraints of the end user's setting
- Who else touches the result
- What exists for them today and why is it not enough

References to Research Funding Agenda
- Horizon Europe ; Quantum Computing https://research-and-innovation.ec.europa.eu/funding/funding-opportunities/funding-programmes-and-open-calls/horizon-europe_en <br>
What: Make Europe the first continent with fully integrated quantum computing in daily life <br>
How: Develop applications from medicine to climate, solving previously impossible problems for 450 million citizens <br>
- NSF ; Gravitational Physics PD 26-1243 <br>
https://www.nsf.gov/funding/opportunities/gp-gravitational-physics <br>
What: Gravitational Physics program supports research and infrastructure on gravitation across large and small scales, including
Data analysis for gravitational-wave detectors, Instrumentation development and detector characterization at the NSF Laser Interferometer Gravitational-Wave Observatory (NSF LIGO), Technologies for next-generation detectors, Research in classical and quantum gravity theory <br>
- NSF ; Transport Phenomena PD 26-366Y <br>
https://www.nsf.gov/funding/opportunities/transport-phenomena <br>
What: Transport Phenomena (TP) program supports fundamental research to understand, model, and control the transport of mass, momentum, energy, and species across multiple scales <br>
- NSF ; Electronic, Photonic, Magnetic, and Quantum Devices (EPMQD) PD 26-1517 <br>
https://www.nsf.gov/funding/opportunities/epmqd-electronic-photonic-magnetic-quantum-devices
What: The Electronic, Photonic, Magnetic, and Quantum Devices (EPMQD) program supports fundamental research on devices with new and/or enhanced capabilities based on their structure and material properties. EPMQD’s goal is to expand the frontiers of micro-, nano- and quantum- devices. Innovations will advance artificial intelligence, computing, communications, healthcare, energy, manufacturing, and other domains. The program encourages research based on emerging ideas for miniaturization, integration, and energy efficiency. <br>
- NSF ; Circuits and Systems for Communications and Sensing (CSCS) PD 26-7564
https://www.nsf.gov/funding/opportunities/cscs-circuits-systems-communications-sensing
What: The Circuits and Systems for Communications and Sensing (CSCS) program supports the key role of electrical engineering in future communications, sensing, circuits, and signal processing. The program's main goal is to advance next-generation systems that integrate communication, sensing, and computation with physical domains, from the nano- to the macro-scale. CSCS covers a wide range of fields and topics, with a focus on both classical and quantum aspects. The program addresses the need for spectrum sharing and resilient connectivity. It also advances national priorities such as quantum engineering, biotechnology and artificial intelligence (AI). Ultimately, CSCS aims to create innovative solutions to spur economic growth, improve lives, and address national challenges.​
- Moonshot ; Goal 6 Realization of a fault-tolerant universal quantum computer that will revolutionize economy, industry, and security by 2050.
https://www8.cao.go.jp/cstp/english/moonshot/sub6_en.html
What: Development of a certain scale of NISQ computer and demonstration of the effectiveness of quantum error correction by 2030 & Achievement of the large-scale integration required for fault-tolerant universal quantum computers by around 2050

References to Startup & Industry Signals
- YCombinator ; The Future of American Defense
https://www.ycombinator.com/rfs#the-future-of-american-defense <br>
Need: <br>
A. So here is our request for startups. We are actively funding low-cost interceptors or any component that helps us lower the cost per kill. <br>
B. We need next-gen sensors, software, payloads, and other hardware that plugs directly into our open system architecture. We need cutting-edge drones, resilient logistics, and advanced manufacturing, and we need it all to survive the most extreme climates on Earth. Bring us your ideas, and we will give you the capital and the proving ground to scale.
- YCombinator ; Counter-Swarm Defense
https://www.ycombinator.com/rfs#counter-swarm-defense <br>
Need: I want to fund founders building the counter-swarm stack. That could mean high-capacity interceptors — a single platform that neutralizes fifty drones, not one. Software that fuses every sensor and every defender on a site into a single real-time picture. We need non-kinetic defenses that don't exist yet: aerosols that foul rotors, streamers that entangle swarms. We need new attacks on the autonomy stack itself now that radio jamming is becoming obsolete.<br>
- techNode ; DeepSeek begins in-house AI chip development to cut reliance on NVIDIA, sources say
https://technode.com/2026/07/08/deepseek-begins-in-house-ai-chip-development-to-cut-reliance-on-nvidia-sources-say/ <br>
Need: Chinese AI startup DeepSeek has launched an in-house AI chip project focused on inference workloads, according to Reuters. The company aims to reduce inference costs through custom-designed processors while lowering its reliance on overseas suppliers such as NVIDI <br>


2026-09-07 <br>

Ideas for goals: <br>
Goal (5): Single-photon / LiDAR data processing for <user> using Qiskit <br>
Goal (7): Measurement studies of 6G, 5G, 4G LTE, WiFi, IOT protocols for <user> using <sw or hw> <br>
Goal (8): FPGA prototype for range detection of various skin tones using VERILOG <br>
Goal (9): Modeling and design tool for <user> using Qiskit <br>


Reasearch papers by area of interest:
- 5 Computational Imaging and Optics + Software <br>
1. 
- 8 Hardware, Architecture and Embedded Systems <br>
1. 
- 9 Photonics & Quantum (Software/Simulation angle) <br>
1. 

SW downloaded:<br>
- Anaconda 2023-09 <br>
- VSCode
- created "qiskit-runtime" custom environment by running "conda create --name qiskit-runtime python=3.11.5" in terminal, then "conda activate qiskit-runtime" to activate it. Once activated, run "pip install 'qiskit[visualization]'" to install the necessary packages. Next, run "pip install qiskit-ibm-runtime".
- For visual confirmation we are running the correct kernel, execute "python -m ipykernel install --user --name qiskit-runtime --display-name 'Qiskit (runtime)'"

2026-09-08 <br>
Problem statement draft 1: Results in Quantum Computing can be improved by choosing algorithms which will prevent the propagation of errors faster than they occur and spread. These algorithms can be applied to quantum circuits in hopes to obtain a fault-tolerant (zero faults) system for reliable computation. Finding which algorithms work best will be a goal here for a few different quantum circuits. Ultimately, this is signifiant to improve computation, security and real world problems like lossy lines and environmental interference. Would we be able to properly simulate a Grover coin interferometer? This simulation could be useful for future student or researchers learning about Qiskit and ultimately even be used as a building block in a larger quantum circuit network?

Error correction articles<br>
- https://www.ibm.com/quantum/blog/nature-qldpc-error-correction
- https://www.ibm.com/quantum/blog/what-is-ftqc
- https://www.nature.com/articles/s41586-024-07107-7

Quantum loss articles<br>
- https://www.nist.gov/news-events/news/2015/09/nist-team-breaks-distance-record-quantum-teleportation
- 

Quantum Cryptography
- https://scholar.google.com/citations?view_op=view_citation&hl=en&user=kSB6hucAAAAJ&cstart=20&pagesize=80&sortby=pubdate&citation_for_view=kSB6hucAAAAJ:bEWYMUwI8FkC
- https://scholar.google.com/citations?view_op=view_citation&hl=en&user=kSB6hucAAAAJ&cstart=20&pagesize=80&sortby=pubdate&citation_for_view=kSB6hucAAAAJ:WC23djZS0W4C
- https://scholar.google.com/citations?view_op=view_citation&hl=en&user=kSB6hucAAAAJ&cstart=20&pagesize=80&sortby=pubdate&citation_for_view=kSB6hucAAAAJ:PYBJJbyH-FwC
- x https://scholar.google.com/citations?view_op=view_citation&hl=en&user=kSB6hucAAAAJ&cstart=80&sortby=pubdate&citation_for_view=kSB6hucAAAAJ:jL-93Qbq4QoC
- x https://scholar.google.com/citations?view_op=view_citation&hl=en&user=kSB6hucAAAAJ&sortby=pubdate&citation_for_view=kSB6hucAAAAJ:L24QuVWYgZ0C

Decisions made by user:
- the user will compare results to their model and ultimately decide whether their predictions are correct / incorrect.

What does a wrong cause - in each direction?
- Any false failures would result in time wasted to investigate. Time is money

What are constraints of user's setting?
- Potentially requiring financial support to purchase API token from IBM Quantum site
- Connectivity in order to reach a real-time quantum processor that IBM provides through their server

Who else touches the result?
- Aside from the direct user, no one can obtain and misinterpret the result - unless each quantum circuit and result gets stored into a repository for public access, at which point the viewers need to do their research to confirm the parameters and configuration.

What exists for the users today, and why is it not enough? 
- There exists methods to simulate continuous wave / classical systems which oblige by friendlier optics theory, but down at the quantum level Qiskit is able to model qudits (d-dimensional)
- This is not enough because there should be a higher level tool for users to more easily implement quantum circuits for their simulation

Prior work
- v

Proposed approach 
- roadmap / milestones here
- what done looks like

Enough ideas on paper to draft proposal

---------------------------------
2026-09-09 <br>
Proposal pass 1 complete <br>
Begin LLM tutorial <br>

Outline:<br>
- Introduction to Quantum Optics. Explain why QO matters and applications (with citations) (quiz also)
- Example of Quantum Optical circuit (HOM?) and explain how it works and why it is important (first principles) (quiz also)
- Explain where fault-tolerance comes into play (quiz also)
- Explain what paper 1 addresses (quiz afterwards)
- Explain what paper 2 addresses (quiz afterwards)
- Exolain what paper 3 addresses (quiz afterwards)
- Exolain what paper 4 addresses (quiz afterwards)
- Brief conclusion 
