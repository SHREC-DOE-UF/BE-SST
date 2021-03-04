
./BE_RUN.sh -c comp_test1.py > test_output.txt
string=$(grep "simulated time:" test_output.txt)
extractedSimTime=$(echo $string | sed -e 's/Simulation is complete, simulated time: \(.*\) s/\1/')

if [[ $extractedSimTime = "22.4" ]]
then
	echo "Computation test case 1   ----  PASS _/"
else
	echo "Computation test case 1   ----  FAIL X"
fi


./BE_RUN.sh -c comp_test2.py > test_output.txt
string=$(grep "simulated time:" test_output.txt)
extractedSimTime=$(echo $string | sed -e 's/Simulation is complete, simulated time: \(.*\) s/\1/')

if [[ $extractedSimTime = "22.4" ]]
then
	echo "Computation test case 2   ----  PASS _/"
else
	echo "Computation test case 2   ----  FAIL X"
fi

./BE_RUN.sh -c comm_test1.py > test_output.txt
string=$(grep "simulated time:" test_output.txt)	#echo "${string#*:}"
extractedSimTime=$(echo $string | sed -e 's/Simulation is complete, simulated time: \(.*\) s/\1/')

if [[ $extractedSimTime = "204.8" ]]
then
	echo "Communication test case 1 ----  PASS _/"
else
	echo "Communication test case 1 ----  FAIL X"
fi

./BE_RUN.sh -c comm_test2.py > test_output.txt
string=$(grep "simulated time:" test_output.txt)	#echo "${string#*:}"
extractedSimTime=$(echo $string | sed -e 's/Simulation is complete, simulated time: \(.*\) s/\1/')

if [[ $extractedSimTime = "1.2" ]]
then
	echo "Communication test case 2 ----  PASS _/"
else
	echo "Communication test case 2 ----  FAIL X"
fi

./BE_RUN.sh -c comm_test3.py > test_output.txt
string=$(grep "simulated time:" test_output.txt)	#echo "${string#*:}"
extractedSimTime=$(echo $string | sed -e 's/Simulation is complete, simulated time: \(.*\) s/\1/')

if [[ $extractedSimTime = "6.4" ]]
then
	echo "Communication test case 3 ----  PASS _/"
else
	echo "Communication test case 3 ----  FAIL X"
fi

./BE_RUN.sh -c comm_testx.py > test_output.txt
string=$(grep "simulated time:" test_output.txt)	#echo "${string#*:}"
extractedSimTime=$(echo $string | sed -e 's/Simulation is complete, simulated time: \(.*\) s/\1/')

if [[ $extractedSimTime = "28.8" ]]
then
	echo "Comm & Comp test case 1   ----  PASS _/"
else
	echo "Comm & Comp test case 1   ----  FAIL X"
fi

./BE_RUN.sh -c comm_testx2.py > test_output.txt
string=$(grep "simulated time:" test_output.txt)	#echo "${string#*:}"
extractedSimTime=$(echo $string | sed -e 's/Simulation is complete, simulated time: \(.*\) s/\1/')

if [[ $extractedSimTime = "25.6" ]]
then
	echo "Comm & Comp test case 2   ----  PASS _/"
else
	echo "Comm & Comp test case 2   ----  FAIL X"
fi

