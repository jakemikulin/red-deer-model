# Agent Based Model For Red Deer Management

This repository contains an agent based model implemented for MoSS (Modelling of Systems for Sustainability) Coursework 2 at the University of Edinburgh.

The model is based on this [master's thesis](https://bora.uib.no/bora-xmlui/handle/1956/20034).

## How To Use

`src/main.py` aims to implement exactly the model found in the source paper. `reproduce_results.ipynb` runs the model and visualises the results.

`src/main_v2.py` extends the model to enable real-world culling data to be used in the model. `blackmount.ipynb` contains code for running the model and visualising it against data from the Black Mount deer management group (linked below).

`blackmount_desired_density.ipynb` includes experiments to determine an appropriate culling strategy to get the population below the desired density of 4 per square kilometre required for natural regeneration of trees and other plant life to occur.

## Blackmount Deer Management Group (updated 2019)

[Blackmount DMG](https://blackmountdmg.deer-management.co.uk/deer-management-plan/)

--- Theses are estimated based off of two terrible 3D graphs ---

### Deer Count Figures (2005-2018) from Figure 2

| Year | Stags | Hinds | Calves | Total |
| ---- | ----- | ----- | ------ | ----- |
| 2005 | 2000  | 4100  | 4100   | 10200 |
| 2008 | 1900  | 3850  | 3500   | 9250  |
| 2011 | 1800  | 3950  | 3500   | 9350  |
| 2014 | 1600  | 3500  | 3000   | 8100  |
| 2015 | 1700  | 4000  | 4000   | 9700  |
| 2018 | 1400  | 3600  | 3500   | 8500  |

### Deer Cull Figures (2005-2018) from Figure 3

| Year | Stags | Hinds | Calves | Total |
| ---- | ----- | ----- | ------ | ----- |
| 2005 | 420   | 570   | 160    | 1150  |
| 2006 | 520   | 500   | 200    | 1220  |
| 2007 | 450   | 580   | 260    | 1290  |
| 2008 | 450   | 550   | 210    | 1210  |
| 2009 | 430   | 490   | 260    | 1180  |
| 2010 | 520   | 510   | 270    | 1300  |
| 2011 | 550   | 490   | 160    | 1200  |
| 2012 | 590   | 600   | 290    | 1480  |
| 2013 | 610   | 650   | 290    | 1550  |
| 2014 | 500   | 620   | 290    | 1410  |
| 2015 | 510   | 590   | 220    | 1320  |
| 2016 | 490   | 610   | 290    | 1390  |
| 2017 | 600   | 830   | 400    | 1830  |
| 2018 | 580   | 520   | 200    | 1300  |
