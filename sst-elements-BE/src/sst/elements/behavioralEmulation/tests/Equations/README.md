## Sample txt file to write analytical equations

#### Rules:
1. Lines starting with '#' are used for commenting and will not be intepreted by the simulator. It is for user to add notes/documentation. (Optional)
2. Line starting with 'parameters' will contain all the application parameters that are present in the equation. (Required)
3. Line starting with 'equation' will contain the analytical equation. (Required)

#### Example sample file looks like:
```txt
# Comments describing the file (optional)
parameters=epp,es,pc
equation=("add(mul(mul(add(es,1),epp),0.01),pc)")
```

> **_Note:_** This sample shows the updated method for txt files with analytical equation
