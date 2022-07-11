#### _Notes about the web app_

- Web app developed using __*flask*__
- All the files requiered are inside the folder sent, __*nba.zip*__. Decompress, and read the following instructions.
- To run the app, as specified, run __*docker-compose up*__ inside the folder __*nba/*__, once decompressed.
- When you run the *docker compose* command, you can access the app using this link:
    - http://localhost:5000/nbastats
- Added an additional feature: __*Drop zeros*__ option, if you want to ignore players with values equal to 0 in the graph shown. This happens sometimes with some of the available stats, only when we consider __*sort=ascending*__.
- You can get the graph in the same page in which the options are available, clicking __*Get Graph!*__. The choosen options are stored in the page when you get the graph.
 
