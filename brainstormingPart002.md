# 2026-09-14  Notes for part 2:

## Proposal before executing part II:<br>
Can algorithms be applied to quantum circuits (qc) to reduce noise? can any pi-pulsing patterns used in optical clock systems (NIST) 
be utilized in a qc environment? If algorithms can be applied (Qiskit), which are the best? Does efficiency depend on qc?

## $\color{#00ff00}\textsf{Next Steps - Validate Before Build}$
1. Rewrite your proposal as 3–5 assumptions.  Someone has this problem · we can build it with data we can access · it beats what the user does today.

2. Rank them: most fatal × most uncertain first.  Not the one you already know how to test — the one that kills the project if wrong.

3. Run the cheapest test that could prove you wrong.  Talk to 3 real users → mock it on paper → baseline on real data → only then build. If your first test is writing code, you skipped a cheaper one.

4. Write your kill criterion before testing.  “We pivot if…” — decided now, while you’re still honest.

5. Bring to next class:  mission sentence · named user · top-5 stories with acceptance criteria · assumption table with test results — in your GitHub repo.

## $\color{#00ff00}\textsf{5 W's and How}$ 
### What?  What are you building — one sentence, no jargon. 
Software package using *Qiskit* as the base that simulates circuits and measurements
### Who?  Who uses it, and who else is affected?  
Main users are students eager to explore quantum concepts. Secondary users are researchers who understand the concepts and want a secondary tool for troubleshooting
### Why?  What breaks if it doesn’t exist?  
This provides a source for learning about qc for new users and allows for opportunities to explore methods to reduce error in qc's
### When?  When is it used — and when is it needed by? 
This is needed by end of November and will be used anytime there is a need to model a qc
### Where?  In what setting or workflow does it live?  
All source code will live in Github, available for public to download and use on the *Qiskit* environment on their laptops
### How?  How, at the architecture-sketch level? 
*Qiskit* API -> Python as main GUI interface -> Successful qc implementation and transpilation to QPU hardware-> Measurements of possible states
## $\color{#00ff00}\textsf{INVEST - 6 Checks, 6 Failure Modes}$
I — Independent:  No waiting on another story, so you can build in risk order.  ✗ “Show feedback trends” before feedback collection exists.

N — Negotiable:  A promise to talk, not a frozen spec — the how is decided when you build it.  ✗ “Rank with cosine similarity over abstracts” — that’s implementation, not need.

V — Valuable:  A vertical slice a user would notice — the check engineers break most.  ✗ “Set up the database” — no user wakes up wanting a database.

E — Estimable:  The team can size it. If not: too vague, or hides an unknown → run a spike (1-day time-boxed experiment; the deliverable is knowledge).  ✗ “Filter by relevance” before anyone tested if relevance is detectable.

S — Small:  Fits in one sprint. Too big = an epic → split it (next slide).  ✗ Demo is “we’re 40% done.”

T — Testable:  Done vs not-done is checkable by someone other than the author.  ✓ “8/10 picks judged relevant by a labmate in ≤10s.”
# 2026-09-16  For class:
## $\color{#00ff00}\textsf{Mission Statement}$
For $\color{#ffe135}\textsf{students}$ who $\color{#ffe135}\textsf{need a GUI-based quantum circuit simulator}$, the $\color{#ffe135}\textsf{Quantum Circuit Design and Simulation Tool}$ is a $\color{#ffe135}\textsf{design and simulation tool}$ that $\color{#ffe135}\textsf{accelerates learning}$. Unlike $\color{#ffe135}\textsf{Qiskit}$, it $\color{#ffe135}\textsf{provides an additional layer of abstraction to make simulation intuitive and rapid.}$
## $\color{#00ff00}\textsf{User and Subproduct}$
Student is user, Raw design tool to lay out circuit and run simulation/measurements<br>
Researcher is user, Raw design tool plus access to implement algorithms, simulate/measure results, and Qiskit code under hood<br>
## $\color{#00ff00}\textsf{User stories}$
i.e. As a [specific user], I want [capability], so that [outcome I care about].<br>
As a $\color{#ffe135}\textsf{student}$, I want $\color{#ffe135}\textsf{a GUI-based design and simulation tool}$, so that $\color{#ffe135}\textsf{I can learn about qunatum circuits}$<br>
As a $\color{#ffe135}\textsf{researcher}$, I want $\color{#ffe135}\textsf{a GUI-based design and simulation tool with ability to incorporate algorithms for error reduction (zero-fault tolerant) and view code under the hood}$, so that $\color{#ffe135}\textsf{I can simulate a circuit in question and verify whether certain algorithms are better than others}$
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

# 2026-09-19  Final Project 1 Deliverables: 
- All deliverables located in the EC601 Google drive under Christopher_Lemus/First Project

#2026-10-26 New additions to document
	•	Node.js v22.23.4 to /usr/local/bin/node
	•	npm v10.9.9 to /usr/local/bin/npm
  The plan with these is to implement AI Agent to do the work for me
