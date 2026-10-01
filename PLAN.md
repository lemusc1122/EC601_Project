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
- As a $\color{#ffe135}\textsf{sudent}$, I want $\color{#ffe135}\textsf{a GUI-based design and simulation tool with ability to incorporate algorithms for error reduction (zero-fault tolerant) and view code under the hood}$, so that $\color{#ffe135}\textsf{I can simulate a circuit in question and verify whether certain algorithms are better than others on certain applications of circuits}$
## $\color{#00ff00}\textsf{Assumption Table with Test Results}$
| Assumption | Test Results |
| -------- | -------- | 
| Students with various knowledge need a tool to design and simulate | Create a GUI where design is possible |
| Researchers want a tool quickly test new ideas | GUI, plus options to implement algorithms and debug Qiskit code |
| Any methods that can reduce error in simulated quantum circuit can be used in larger Quantum system | Apply methods to different scale processors to confirm behavior |
## $\color{#00ff00}\textsf{Proposal re-written as assumptions}$
- Students with different exposure levels wants to learn about quantum circuits (#3 - Someone will want a tool like this)
- Quantum circuits can be easily simulated on computers (#1 - Most fatal if wrong)
- The results will assist in reinforcing understanding or expected results (i.e. testing a new algorithm) (#2 - results might be wrong but can always fix on next iteration. Non-fatal)
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
