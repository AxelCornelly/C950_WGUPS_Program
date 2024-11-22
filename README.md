<h1>WGU C950 Performance Assessment Task 2: WGUPS Program Implementation</h1>
<h2>By: Axel Cornelly | Student ID: 002555231</h2>
<p>
	This repository is dedicated to the WGU Computer Science Degree's Data Structures and Algorithms II course and its Performance Assessment, specifically Task 2.
	Please feel free to use my implementation strictly for inspiration, as doing your own work to avoid plagiarism is always advised and adheres to the school's academic
	integrity policy.
</p>
<h3>About the Program</h3>
<p>
	The WGUPS Program aims to be a solution to a scenario that mimics the NP-Hard Traveling Salesman Problem. The program is designed to deliver a
	number of packages given a set of locations while meeting specific delivery requirements and utilizing algorithms to optimize said deliveries. In our case, the locations are surrounding cities/landmarks around 
	WGU's main campus and some delivery requirements involved were:
	<li>Can only use 2 delivery trucks at a time. A third is available for use.</li>
	<li>Individual truck may not exceed 45 miles of travel distance.</li>
	<li>Must comply with package requirements (such as deadline and/or requiring to be on a specific truck).</li>
</p>
<h3>My Solution</h3>
<p>
	For my solution to this task, I utilized the Nearest-Neighbor algorithm to determine how packages are delivered. The algorithm, along with some heuristics, was also used to determine how packages were loaded
	onto the three delivery trucks. As part of the task requirements, my solution includes an interactive GUI that shows real-time updates on the deliveries. In order to achieve this, I utilized Threading to run
	the GUI alongside the delivery algorithm. Specifically, I ran 3 threads:
	<table>
		<tr>
			<th>Thread</th>
			<th>Function</th>
		</tr>
		<tr>
			<td>Main</td>
			<td>Runs main program and builds GUI</td>
		</tr>
		<tr>
			<td>Thread1</td>
			<td>Runs the delivery algorithm starting with Truck 1. Runs for Truck 3 once Truck 1 completes its deliveries.</td>
		</tr>
		<tr>
			<td>Thread2</td>
			<td>Runs the delivery algorithm starting with Truck 2. Runs until Truck 2 finishes its deliveries.</td>
		</tr>
	</table>
 Within the GUI there is also a feature to input a specific time to look up all the packages' statuses at that given time. To implement this feature, I had to create a logging system so that the state of every package was
 stored whenever a package would get delivered or had any updates to it (e.g from being delayed to loaded onto a truck). The logging system utilized nested dictionary structures for quick accessing to logs. 
</p>
<h3>Conclusion</h3>
<p>
	This was a very interesting assessment and I had a very great time developing this program. I had to resubmit it twice for some minor adjustments to the GUI to meet requirements, but besides that, the rest of my program ran
	as expected and without errors. I learned a great deal about data structures and algorithms while doing this project as well as some basic front-end Python development. Overall, I think this project was great and definitely strengthened my knowledge of DSA alongside general Python skills!
</p>
