# $\color{#00ff00}\textsf{Plan as required - Lecture 2026-09-28}$ 

## $\color{#00ff00}\textsf{Mission Statement}$
For $\color{#ffe135}\textsf{students}$ who $\color{#ffe135}\textsf{need a GUI-based quantum circuit simulator}$, the $\color{#ffe135}\textsf{Quantum Circuit Design and Simulation Tool}$ is a $\color{#ffe135}\textsf{design and simulation tool}$ that $\color{#ffe135}\textsf{accelerates learning}$. Unlike $\color{#ffe135}\textsf{Qiskit}$, it $\color{#ffe135}\textsf{provides an additional layer of abstraction to make simulation intuitive and rapid.}$
## $\color{#00ff00}\textsf{User}$
Main User: Students ranging from juniors in high school to sophomores in college<br>
Other User: Researchers looking for a second opinion<br>
## $\color{#00ff00}\textsf{User stories}$
i.e. As a [specific user], I want [capability], so that [outcome I care about].<br>
- As a $\color{#ffe135}\textsf{student}$, I want $\color{#ffe135}\textsf{a GUI-based design and simulation tool}$, so that $\color{#ffe135}\textsf{I can learn about quantum circuits}$<br>
- As a $\color{#ffe135}\textsf{student}$, I want $\color{#ffe135}\textsf{a GUI-based design and simulation tool with support of many languages}$, so that $\color{#ffe135}\textsf{I can learn about quantum circuits and concepts across many languages}$<br>
- As a $\color{#ffe135}\textsf{student}$, I want $\color{#ffe135}\textsf{a GUI-based design and simulation tool with wiki of information}$, so that $\color{#ffe135}\textsf{I can learn about quantum circuits and concepts across a range of students with different prerequisite knowledge}$<br>
- As a $\color{#ffe135}\textsf{student}$, I want $\color{#ffe135}\textsf{a GUI-based design and simulation tool that is easy to install and navigate}$, so that $\color{#ffe135}\textsf{accessing the tool is quick, efficient and easy}$<br>
- As a $\color{#ffe135}\textsf{sudent}$, I want $\color{#ffe135}\textsf{a GUI-based design and simulation tool with ability to incorporate algorithms for error reduction (zero-fault tolerant) and view code under hood}$, so that $\color{#ffe135}\textsf{I can simulate a circuit in question and verify whether certain algorithms are better than others on certain applications of circuits}$
## $\color{#00ff00}\textsf{Feasability}$
- I will have a functional example of Qiskit to compile and run on the PC, which will demonstrate how these tests are built, compiled, transpiled for execution on real hardware and what the results are.
- I will re-gain access to a 10-day trial for API token needed to run the code on remote QPU server
- The above two are for demo
- The following will be moving forward
- Wrap the code with an intuitive GUI (help from LLM)
- Add capability to add Language selection (help from LLM)
- Add capability to add a couple algorithm choices or none (help from LLM)
- Add capability to access wiki (help from LLM and explain in many ways with analogies and different levels of complexity)
- Add capability for this to be deployed as an executable (help from LLM)
## $\color{#00ff00}\textsf{Tooling}$
- IBM's Qiskit will be used for the project, which is supported by C/C++ and Python.
- Python will be what the GUI is made through as well as referenced to Qiskit API
- Any models required will be pulled from Python via API or coded in with references from sources
## $\color{#00ff00}\textsf{Demo Statement}$
- At the end of the next two weeks we will demonstrate an example quantum circuit that can execute on a real server, with a GUI that has drop downs for language (supports english and spanish for now) and a initial pass for wiki on quantum information and references.

## $\color{#00ff00}\textsf{Kill criteria and 5 potentially proposal-ending assumptions}$
We terminate the project if there exists a tool that already provides this service and targets the same audience<br>
| Assumptions if proven wrong can cause failure |
| -------- |
| Students Have Sufficient Prior Knowledge  | 
| The GUI is Intuitive Enough for Students  |
| Access to Required Hardware/Software  | 
| Students Are Motivated to Use the Tool Independently  |
| The Simulation Accurately Represents Real Quantum Circuits  |

https://terriergpt.bu.edu/share/tQPIuZe7L7_pgDNBznsWL 
## $\color{#ff0000}\textsf{IBM Composer}$
https://quantum.cloud.ibm.com/composer<br>
https://construct.psiquantum.com/qdk
