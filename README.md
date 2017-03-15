# AqulaMap

Plot map of Aquila City

*forked from dev3map.github.io*

Uses [CivMap](https://github.com/Gjum/CivMap).

## Extra files

*voxeltojson.py* is the script that accepts voxelmap waypoints file named *way.points* and plot owners file *all-latest-plots.csv*
> This is now obsolete, You shouldn't use it. Instead use aquilamap edit and **updateplots.py -i**

*way.points* has to be a voxelmap file with waypoints for each plot named with three digit number.
Waypoints for one plot should have the same name and be arranged in proper order.

*all-latest-plots.csv* is a csv file in format
player name,x,z

*plots-info.csv* - csv file in a format of
```

number,name,type,address,zone,owner,premium,open

```
> These attributes are not in any way hardcoded, you can add or delete any of these and it will go into the json file. Just update the header and stay away from *positions*. Also *number* is obvously required, as it identifies the plot.

*updateplots.py* is now the to-go script. Use it to update the plots.json file either with changed CSVs or edits from dev3map.

```

Options:
-if <filename> - input plots file; defaults to *plots.json*
-of <filename> - output plots file; defaults to *plots.json*
-prop <filename> - additional properties file; defaults to *plots-info.csv*
-own <filename> - csv file with owners and coords of their house (this is here just for the time being, hopefully we'll move to plot numbers in the census)
-i - interactive mode; ignores all options except -if and -of

```